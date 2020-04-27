# This script creates a CSV that can be used for recording human-rated post-joke ground truths
# Requires Python 3.5 or later
# Assumes each performance folder contains a performanceLog json file

# After running, rename the resulting "ground_truths_template.csv" to "<RaterName>_ground_truths.csv"
# To enter your ratings, open the CSV in a spreadsheet editor
# Find the section for the performance you are rating, the jokes told are listed in order
# Open the "jokes_and_pauses" folder for that performance
# Play the pause mp3 files in order and enter your ratings in the "HumanScorePostJokeOnly" column

import os
import json
basedir = str(os.getcwd())
perfspath = basedir[:-12]+"\\Performances"
perfnames = [d.name for d in os.scandir(perfspath) if d.is_dir()]
numfiles = len(perfnames)
output = open("ground_truths_template.csv", "w")
row = "Performance,Joke,HumanScorePostJokeOnly,Notes\n"
output.write(row)
output.close()
for i in range(1, numfiles+1):
	perfpath = perfspath+"\\"+perfnames[i-1]
	joke_order = []
	json_name = [i for i in os.listdir(perfpath) if os.path.isfile(os.path.join(perfpath,i)) and 'performanceLog' in i] # find name of json file
	json_path = perfpath+"\\"+json_name[0] # form path to json file
	json_file = open(json_path, "r")
	json_data = json.loads(json_file.read().splitlines()[0]) # read performanceLog json
	json_file.close()
	skips = ["/../sounds/tags/family_joke_negative.ogg.wav"] # skip unused joke names
	if "audio" in json_data[2].keys():
		skips.append("/../sounds/robot_name_joke_1.ogg.wav")
	for entry in json_data:
		keys = entry.keys()
		if ("audio" in keys) and (entry.get("audio") not in skips):
			joke_name = entry.get("audio")[11:] # find all joke names in the json and save them in the order told
			joke_order.append(joke_name)
	#print(joke_order) # uncomment to verify the resulting lists
	perfname = perfnames[i-1]
	output = open("ground_truths_template.csv", "a")
	for joke in joke_order:
		row = perfname+","+joke+",,"+"\n"
		output.write(row)
	output.close()
