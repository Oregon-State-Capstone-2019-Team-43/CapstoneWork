# Requires Python 3.5 or later

# Assumptions
#    This script is run in a directory containing 1 or more csv files
#    Only csv files containing information you want are in this directory

# Output
#    three columns, 'Performance', 'Joke', 'HumanScorePostJokeOnly'
#    HumanScorePostJokeOnly is mean average of all ratings

import os
import glob
import pandas as pd

from perf_and_joke_dict import joke, performance

# Look in subdir HumanRatings
path = "./HumanRatings/"
# Get all csv files
extension = 'csv'
all_files = [i for i in glob.glob(path + '*.{}'.format(extension))]
# Combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_files ], sort=False)
# Remove notes
combined_csv = combined_csv.iloc[:, :-1]
# Combine human ratings based on performance and joke
combined_csv = combined_csv.groupby(['Performance', 'Joke']).mean()
# Round number
combined_csv['HumanScorePostJokeOnly'] = combined_csv['HumanScorePostJokeOnly'].round(0)
combined_csv = combined_csv.reset_index()[['Performance', 'Joke', 'HumanScorePostJokeOnly']]
# Add performance, joke ids
combined_csv.insert(0, 'PerformanceID', combined_csv['Performance'].map(performance))
combined_csv.insert(2, 'JokeID', combined_csv['Joke'].map(joke))
combined_csv.insert(4, 'HumanScore', combined_csv['HumanScorePostJokeOnly'])
# print to csv
combined_csv.to_csv("ground_truth_ratings.csv", index=False)