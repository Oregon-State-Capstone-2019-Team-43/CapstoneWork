# made by Eloise Bisbee 8/13/19 eloise.bisbee@tufts.edu
# revised by Brian Ozarowicz - January 2020

# This program takes in files numbered 1-numfiles with a .txt extension
# as well as ground_truth_ratings.csv and outputs clean_comedy_data.csv

# The numbered files should contain praat output data formatted as follows:
# first line: full file path of which folder the data was extracted from
# then a series of couplings:
# pause_#.mp3
# intensity
# intensity std
# pitch
# pitch std
# min
# max

# ground_truth_ratings.csv should contain the ground truth ratings for each comedy
# performance's jokes formatted such that the first columns are:
# PerformanceId, Performance, JokeId, Joke, HumanScore, HumanScorePostJokeOnly

# The output, clean_comedy_data.csv, will contain columns:
# PerformanceId, JokeId, Pitch, PitchStd, Intensity, IntensityStd,
# MinSound, MaxSound, HumanScore, HumanScorePostJokeOnly

# This program is designed to be run on a Windows computer,
# differences in file path format on another OS may cause errors.
# Requires Python 3.5 or later

import re
import csv
import json
import os

# use performanceLog json file to list joke names in order they were told in the performance
joke_order = []
numfiles = len([f for f in os.scandir(os.getcwd()) if f.name.endswith('.txt')]) # check how many txt files the praat script created
for i in range(1, numfiles + 1):
    joke_performance = []
    file = open(str(i)+".txt", "r", encoding='utf_16_le')
    path = file.read().splitlines()[0][:-16] # get path to the performance directory
    file.close()
    json_name = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'performanceLog' in i] # find name of json file
    json_path = path+json_name[0] # form path to json file
    json_file = open(json_path, "r")
    json_data = json.loads(json_file.read().splitlines()[0]) # read performanceLog json
    json_file.close()
    skips = ["/../sounds/tags/family_joke_negative.ogg.wav"] # skip unused joke names
    if "audio" in json_data[2].keys():
        skips.append("/../sounds/robot_name_joke_1.ogg.wav")
    for entry in json_data:
        keys = entry.keys()
        if ("audio" in keys) and (entry.get("audio") not in skips):
            joke_name = entry.get("audio")[11:] # find all joke names in the json and save them in order
            joke_performance.append(joke_name)
    joke_order.append(joke_performance)
    #print(joke_order) # uncomment to verify the resulting list

# reading in data from praat files and storing in dictionary called all_data
all_data = {}
for fi in range(1, numfiles + 1):
    filename = str(fi) + ".txt"
    praat = open(filename, "r", encoding='utf_16_le')
    raw_praat_data = praat.read().splitlines()
    praat_data = {}
    to_add = {}
    to_add["performance"] = raw_praat_data[0].split("\\")[-2] # gets performance name from the directory path
    to_add["data"] = praat_data
    features_per_pause = 43
    for i in range(0, len(raw_praat_data)):
        if raw_praat_data[i][0] == 'p':
            row_data = []
            for j in range(0,features_per_pause):
                neg = re.findall(r'-', raw_praat_data[i + j + 1])
                raw = re.findall(r'\d*\.?\d+', raw_praat_data[i + j + 1])
                if len(raw) != 0:
                    if len(neg) != 0:
                        if float(raw_praat_data[i + j + 1]) > 0:
                            print("uh oh")
                        row_data.append(-1 * float(raw[0]))
                    else:
                        row_data.append(float(raw[0]))
                else:
                    row_data.append(0)
            temp = re.findall(r'\d+', raw_praat_data[i])
            index = int(temp[0])
            praat_data[index] = row_data
    all_data[fi] = to_add
    praat.close()

# reading in data from csv file and storing in dictionary called csv_data
csv_data = {}
with open('ground_truth_ratings.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data_cats = []
    count = 0
    curr = "none"
    temp = {}
    for row in csv_reader:
        if count == 0:
            data_cats = row
        else:
            if curr != row[1]:
                curr = row[1]
                temp = {}
                csv_data[curr] = temp
                temp['PerformanceId'] = int(row[0])
                temp['Performance'] = row[1]
                temp['Jokes'] = []
                temp['Jokes'].append([int(row[2]), row[4], row[5], row[3]])
            else:
                temp['Jokes'].append([int(row[2]), row[4], row[5], row[3]])
        count += 1

# output new csv file with all appropriate data
with open('clean_comedy_data.csv', mode='w', newline='\n', encoding='utf-8') as csv_file:
    fieldnames = ['PerformanceId', 'JokeId', 'Pitch', 'PitchSd', 'PitchMax', 'Intensity', 
                  'IntensitySd', 'MinSound', 'MaxSound', 'HumanScore', 'HumanScorePostJokeOnly',
                  '1_mean', '1_max', '1_min',
                  '2_mean', '2_max', '2_min',
                  '3_mean', '3_max', '3_min',
                  '4_mean', '4_max', '4_min',
                  '5_mean', '5_max', '5_min',
                  '6_mean', '6_max', '6_min',
                  '7_mean', '7_max', '7_min',
                  '8_mean', '8_max', '8_min',
                  '9_mean', '9_max', '9_min',
                  '10_mean', '10_max', '10_min',
                  '11_mean', '11_max', '11_min',
                  '12_mean', '12_max', '12_min',]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for elem in all_data:
        idx = all_data[elem]['performance']
        if (len(all_data[elem]['data']) == len(csv_data[str(idx)]["Jokes"])):
            for i in range(0, len(all_data[elem]['data'])):
                perf_id = csv_data[idx]['PerformanceId']
                cur_joke_name = csv_data[idx]['Jokes'][i][3] # check name of the joke being matched to a praat data txt file
                pause_num = joke_order[perf_id].index(cur_joke_name) # find that name in the ordered list, its index is its pause number
                row = {}
                row["PerformanceId"] = csv_data[idx]['PerformanceId']
                row['JokeId'] = csv_data[idx]['Jokes'][i][0]
                row['Intensity'] = all_data[elem]['data'][pause_num][0]
                row['IntensitySd'] = all_data[elem]['data'][pause_num][1]
                row['MinSound'] = all_data[elem]['data'][pause_num][2]
                row['MaxSound'] = all_data[elem]['data'][pause_num][3]
                row['Pitch'] = all_data[elem]['data'][pause_num][4]
                row['PitchSd'] = all_data[elem]['data'][pause_num][5]
                row['PitchMax'] = all_data[elem]['data'][pause_num][6]
                row['1_mean'] = all_data[elem]['data'][pause_num][7]
                row['1_max'] = all_data[elem]['data'][pause_num][8]
                row['1_min'] = all_data[elem]['data'][pause_num][9]
                row['2_mean'] = all_data[elem]['data'][pause_num][10]
                row['2_max'] = all_data[elem]['data'][pause_num][11]
                row['2_min'] = all_data[elem]['data'][pause_num][12]
                row['3_mean'] = all_data[elem]['data'][pause_num][13]
                row['3_max'] = all_data[elem]['data'][pause_num][14]
                row['3_min'] = all_data[elem]['data'][pause_num][15]
                row['4_mean'] = all_data[elem]['data'][pause_num][16]
                row['4_max'] = all_data[elem]['data'][pause_num][17]
                row['4_min'] = all_data[elem]['data'][pause_num][18]
                row['5_mean'] = all_data[elem]['data'][pause_num][19]
                row['5_max'] = all_data[elem]['data'][pause_num][20]
                row['5_min'] = all_data[elem]['data'][pause_num][21]
                row['6_mean'] = all_data[elem]['data'][pause_num][22]
                row['6_max'] = all_data[elem]['data'][pause_num][23]
                row['6_min'] = all_data[elem]['data'][pause_num][24]
                row['7_mean'] = all_data[elem]['data'][pause_num][25]
                row['7_max'] = all_data[elem]['data'][pause_num][26]
                row['7_min'] = all_data[elem]['data'][pause_num][27]
                row['8_mean'] = all_data[elem]['data'][pause_num][28]
                row['8_max'] = all_data[elem]['data'][pause_num][29]
                row['8_min'] = all_data[elem]['data'][pause_num][30]
                row['9_mean'] = all_data[elem]['data'][pause_num][31]
                row['9_max'] = all_data[elem]['data'][pause_num][32]
                row['9_min'] = all_data[elem]['data'][pause_num][33]
                row['10_mean'] = all_data[elem]['data'][pause_num][34]
                row['10_max'] = all_data[elem]['data'][pause_num][35]
                row['10_min'] = all_data[elem]['data'][pause_num][36]
                row['11_mean'] = all_data[elem]['data'][pause_num][37]
                row['11_max'] = all_data[elem]['data'][pause_num][38]
                row['11_min'] = all_data[elem]['data'][pause_num][39]
                row['12_mean'] = all_data[elem]['data'][pause_num][40]
                row['12_max'] = all_data[elem]['data'][pause_num][41]
                row['12_min'] = all_data[elem]['data'][pause_num][42]
                row['HumanScore'] = int(float(csv_data[idx]['Jokes'][i][1]))
                row['HumanScorePostJokeOnly'] = int(float(csv_data[idx]['Jokes'][i][2]))
                writer.writerow(row)
        else:
            #this else case is for if the raw praat data lengths and ground
            #truth lengths which should correspond to the same performance 
            #are not the same length. This means something went wrong
            print("uhhoh")
