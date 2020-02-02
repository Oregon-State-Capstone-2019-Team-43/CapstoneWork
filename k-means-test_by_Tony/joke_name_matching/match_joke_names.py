import os
import json
basedir = str(os.getcwd())
pathtoinput = basedir[:-18]+"\\input"
perfpath = basedir[:-39]+"\\V6_robot_recordings"
numfiles = len([f for f in os.scandir(pathtoinput) if f.name.endswith('.txt')])
perfnames = [d.name for d in os.scandir(perfpath) if d.is_dir()]
type = input("Are you matching jokes (enter 'joke') or pauses (enter 'pause') to joke names? ")
if type == "joke":
	for i in range(1, numfiles+1):
		joke_order = []
		praat_path = pathtoinput+"\\"+str(i)+".txt"
		file = open(praat_path, "r", encoding='utf_16_le')
		path = file.read().splitlines()[0][:-16] # get path to the performance directory
		file.close()
		json_name = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'performanceLog' in i] # find name of json file
		json_path = path+json_name[0] # form path to json file
		json_file = open(json_path, "r")
		json_data = json.loads(json_file.read().splitlines()[0]) # read performanceLog json
		json_file.close()
		skips = ["/../sounds/robot_name_joke_1.ogg.wav", "/../sounds/tags/family_joke_negative.ogg.wav"] # skip unused joke names
		for entry in json_data:
			keys = entry.keys()
			if ("audio" in keys) and (entry.get("audio") not in skips):
				joke_name = entry.get("audio")[11:] # find all joke names in the json and save them in order
				joke_order.append(joke_name)
		#print(joke_order) # uncomment to verify the resulting lists
		perfname = perfnames[i-1]
		numindexes = len(joke_order)
		names = []
		for j in range(0, numindexes):
			names.append("joke_"+str(j)+".mp3")
		names = sorted(names) # sort to match the order in the praat files (0, 1, 10, 11, 2)
		output = open(perfname+".txt", "w", encoding='utf_16_le')
		output.write(perfname+"\n")
		for name in names:
			name_indx = int(name[5:-4])
			line = joke_order[name_indx]+":"+name
			output.write(line+"\n")
if type == "pause":
	for i in range(1, numfiles+1):
		joke_order = []
		praat_path = pathtoinput+"\\"+str(i)+".txt"
		file = open(praat_path, "r", encoding='utf_16_le')
		path = file.read().splitlines()[0][:-16] # get path to the performance directory
		file.close()
		json_name = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'performanceLog' in i] # find name of json file
		json_path = path+json_name[0] # form path to json file
		json_file = open(json_path, "r")
		json_data = json.loads(json_file.read().splitlines()[0]) # read performanceLog json
		json_file.close()
		skips = ["/../sounds/robot_name_joke_1.ogg.wav", "/../sounds/tags/family_joke_negative.ogg.wav"] # skip unused joke names
		for entry in json_data:
			keys = entry.keys()
			if ("audio" in keys) and (entry.get("audio") not in skips):
				joke_name = entry.get("audio")[11:] # find all joke names in the json and save them in order
				joke_order.append(joke_name)
		#print(joke_order) # uncomment to verify the resulting lists
		perfname = perfnames[i-1]
		numindexes = len(joke_order)
		names = []
		for j in range(0, numindexes):
			names.append("pause_"+str(j)+".mp3")
		names = sorted(names) # sort to match the order in the praat files (0, 1, 10, 11, 2)
		output = open(perfname+".txt", "w", encoding='utf_16_le')
		output.write(perfname+"\n")
		for name in names:
			name_indx = int(name[6:-4])
			line = joke_order[name_indx]+":"+name
			output.write(line+"\n")
