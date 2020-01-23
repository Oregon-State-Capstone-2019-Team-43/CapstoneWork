#made by: Eloise Bisbee 8/13/19 eloise.bisbee@tufts.edu
#this program takes in files numbered 1-numfiles with a .txt extension as
#well as ground_truth_ratings.csv and output clean_comedy_data.csv.

#The numbered files should contain praat output data formatted as follows:
#first line: full file path of which folder data was extracted from
#then a series of couplings:
#pause_#.mp3
#intensity
#intensity std
#pitch
#pitch std
#min
#max

#ground_truth_ratings should contain the ground truth ratings for each comedy
#performance formatted such that the first couple columns are:
#PerformanceId, Performance, JokeId, Joke, HumanScore, HumanScorePostJokeOnly

#the output, clean_comedy_data.csv, will contain columns:
#'PerformanceId', 'JokeId', 'Pitch', 'PitchStd', Intensity', 'IntensityStd', 
#'MinSound', 'MaxSound', 'HumanScore', 'HumanScorePostJokeOnly'
import re
import csv
import json
import os

#use performanceLog json file to list joke names in order told in the performance
joke_order = []
file = open("1.txt", "r", encoding='utf-8')
path = file.read().splitlines()[0][:-16]
file.close()
json_name = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'performanceLog' in i]
json_path = path+json_name[0]
json_file = open(json_path, "r")
json_data = json.loads(json_file.read().splitlines()[0])
json_file.close()
for entry in json_data:
    keys = entry.keys()
    if ("audio" in keys) and (entry.get("audio") != "/../sounds/robot_name_joke_1.ogg.wav"):
	    joke_name = entry.get("audio")[11:]
	    joke_order.append(joke_name)
#print(joke_order)


#reading in data from praat files and storing in dictionary called all_data
num_files = 18
all_data = {}
for fi in range(1, num_files + 1):
    filename = str(fi) + ".txt"
    praat = open(filename, "r", encoding='utf-8')
    raw_praat_data = praat.read().splitlines()
    praat_data = {}
    to_add = {}
    to_add["performance"] = raw_praat_data[0].split("\\")[-2]
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

#reading in data from csv file and storing it 
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

#now output csv file with all appropriate data
with open('clean_comedy_data.csv', mode='w', newline='\n', encoding='utf-8') as csv_file:
    fieldnames = ['PerformanceId', 'JokeId', 'Pitch', 'PitchSd', 'Intensity', 
                  'IntensitySd', 'MinSound', 'MaxSound', 'HumanScore', 'HumanScorePostJokeOnly']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for elem in all_data:
        idx = all_data[elem]['performance']
        if (len(all_data[elem]['data']) == len(csv_data[str(idx)]["Jokes"])):
            for i in range(0, len(all_data[elem]['data'])):
                cur_joke_name = csv_data[idx]['Jokes'][i][3]
                txt_file_num = joke_order.index(cur_joke_name)
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
