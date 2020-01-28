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
    file = open(str(i) + ".txt", "r", encoding='utf_16_le')
    path = file.read().splitlines()[0][:-16] # get path to the performance directory
    #print(path)
    file.close()
    json_name = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'performanceLog' in i] # find name of json file
    json_path = path+json_name[0]
    #print(json_path)
    json_file = open(json_path, "r")
    json_data = json.loads(json_file.read().splitlines()[0]) # read performanceLog json
    json_file.close()
    for entry in json_data:
        keys = entry.keys()
        if ("audio" in keys) and (entry.get("audio") != "/../sounds/robot_name_joke_1.ogg.wav") and (entry.get("audio") != "/../sounds/tags/family_joke_negative.ogg.wav"):
            joke_name = entry.get("audio")[11:] # find all joke names in the json and save them in order
            joke_performance.append(joke_name)
    joke_order.append(joke_performance)
    #print(joke_order) # uncomment to verify the resulting list
for elem in joke_order[16]:
    print(elem)

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
    features_per_pause = 6
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
    fieldnames = ['PerformanceId', 'JokeId', 'Pitch', 'PitchSd', 'Intensity', 
                  'IntensitySd', 'MinSound', 'MaxSound', 'HumanScore', 'HumanScorePostJokeOnly']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for elem in all_data:
        idx = all_data[elem]['performance']
        if (len(all_data[elem]['data']) == len(csv_data[str(idx)]["Jokes"])):
            for i in range(0, len(all_data[elem]['data'])):
                cur_joke_name = csv_data[idx]['Jokes'][i][3] # check name of the joke being matched to a praat data txt file
                txt_file_num = joke_order[csv_data[idx]['PerformanceId']].index(cur_joke_name) # find that name in the ordered list, its index is its txt file number
                row = {}
                row["PerformanceId"] = csv_data[idx]['PerformanceId']
                row['JokeId'] = csv_data[idx]['Jokes'][i][0]
                row['Pitch'] = all_data[elem]['data'][txt_file_num][2]
                row['PitchSd'] = all_data[elem]['data'][txt_file_num][3]
                row['Intensity'] = all_data[elem]['data'][txt_file_num][0]
                row['IntensitySd'] = all_data[elem]['data'][txt_file_num][1]
                row['MinSound'] = all_data[elem]['data'][txt_file_num][4]
                row['MaxSound'] = all_data[elem]['data'][txt_file_num][5]
                row['HumanScore'] = csv_data[idx]['Jokes'][i][1]
                row['HumanScorePostJokeOnly'] = csv_data[idx]['Jokes'][i][2]
                writer.writerow(row)
        else:
            #this else case is for if the raw praat data lengths and ground
            #truth lengths which should correspond to the same performance 
            #are not the same length. This means something went wrong
            print("uhhoh")
