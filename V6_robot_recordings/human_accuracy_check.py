# This assumes the csv having its accuracy checked and the csv it is being checked against
# have the same number of rows which contain raings for the same Performance/Joke combinations
# (the order of ratings in the files does not matter)
# If this assumption is incorrect the accuracy value output will not be valid

import csv
import operator
import os
import numpy

if os.path.exists("human_accuracy_results.txt"):
	os.remove("human_accuracy_results.txt")
master_list = []
master_ratings = []
perfnames = []
jokenums = []
# put csv filenames to be checked in this list
tocheck = ['Brian_ground_truths.csv', 'Timothy_ground_truths.csv', 'Trevor_ground_truths.csv']
# specify the csv to check against here
master_file = 'combined_ground_truths.csv'

with open(master_file, 'r') as f:
	reader = csv.reader(f)
	master_list = list(reader) # make a list with all the rating data
	master_list.pop(0) # remove first index (csv headers)
	master_list.sort(key=operator.itemgetter(1, 3)) # order list by Performance then Joke
	# master_list[i][1] = Performance
	# master_list[i][3] = Joke
	# master_list[i][4] = HumanScorePostJokeOnly
	for rating in master_list:
		master_ratings.append(int(float(rating[4]))) # make a list of just the ratings
		if rating[1] not in perfnames:
			perfnames.append(rating[1]) # make a list of the performance names
	for perf in range(len(perfnames)):
		count = 0
		for row in master_list:
			if int(row[0]) == perf:
				count = count+1
		jokenums.append(count) # make a list of how many jokes are in each performance

with open('human_accuracy_results.txt', 'a') as o:
	o.write("Overall results:\n\n")

for rating_file in tocheck:
	matches = 0
	diffs = 0
	result = 0
	print("\nChecking %s against %s" % (rating_file, master_file))
	with open(rating_file, 'r') as f:
		reader = csv.reader(f)
		data_list = list(reader) # make a list with all the rating data
		data_list.pop(0) # remove first index (csv headers)
		data_list.sort(key=operator.itemgetter(0, 1)) # order list by Performance then Joke
		# data_list[i][0] = Performance
		# data_list[i][1] = Joke
		# data_list[i][2] = HumanScorePostJokeOnly
		for rating in data_list:
			beingchecked = data_list.index(rating)
			if int(float(rating[2])) == master_ratings[beingchecked]:
				matches = matches+1
			else:
				diffs = diffs+1
		result = matches/(matches+diffs)
		desc = "("+str(matches)+" matches, "+str(diffs)+" diffs)"
		with open('human_accuracy_results.txt', 'a') as o:
			o.write('{:<35}{:<22}{:<}\n'.format(rating_file, result, desc))

with open('human_accuracy_results.txt', 'a') as o:
	o.write("\nIndividual performance results:\n")

print("\nChecking by individual performance")
masterperfs = []
for i in range(len(jokenums)):
	masterperfs.append(master_ratings[0:jokenums[i]]) # divide the ratings by performance
	master_ratings = master_ratings[jokenums[i]:]

for rating_file in tocheck:
	ratings = []
	perflist = []
	curperf = ""
	matches = 0
	diffs = 0
	result = 0
	with open('human_accuracy_results.txt', 'a') as o:
		o.write("\n%s\n" % rating_file)
	with open(rating_file, 'r') as f:
		reader = csv.reader(f)
		data_list = list(reader) # make a list with all the rating data
		data_list.pop(0) # remove first index (csv headers)
		data_list.sort(key=operator.itemgetter(0, 1)) # order list by Performance then Joke
		for rating in data_list:
			ratings.append(int(float(rating[2]))) # make a list of just the ratings
		for i in range(len(jokenums)):
			perflist.append(ratings[0:jokenums[i]]) # divide the ratings by performance
			ratings = ratings[jokenums[i]:]
		for j in range(len(perfnames)):
			curperf = perfnames[j]
			list1 = numpy.array(perflist[j])
			list2 = numpy.array(masterperfs[j])
			matches = len(numpy.where(list1==list2)[0])
			diffs = jokenums[j]-matches
			result = matches/(matches+diffs)
			desc = "("+str(matches)+" matches, "+str(diffs)+" diffs)"
			with open('human_accuracy_results.txt', 'a') as o:
				o.write('{:<50}{:<22}{:<}\n'.format(curperf, result, desc))

print("\nResults saved in human_accuracy_results.txt")
