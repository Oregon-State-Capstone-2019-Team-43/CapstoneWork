# Robot Comedy Machine Learning Pipeline

## Written By: 2019-2020 Senior Capstone Team — April 2020

TIMOTHY BUI
YUHANG (TONY) CHEN
BRIAN OZAROWICZ
TREVOR WEBSTER

## Original Work: Ella Bisbee (eloise.bisbee@tufts.edu) — August 2019

### Directory Layout

There are two subdirectories, HumanRatings and Performances

HumanRatings should contain the human ratings as CSV files. combine_human_ratings.py will look in this directory for .csv files.

Performances should contain a subdirectories for each performance.

WIP

### Assumptions

Every human rating must contain a rating for all jokes in all performances. There must be at least 1 human rating.

WIP

### Dependencies

WIP

### Control Flow

First, ensure all files are aligned according to the above assumptions.

Second, run praat_extraction.py and choose to extract the post-joke data. As of today (2020-04-24) mid-joke is incomplete.

This should produce a number of .txt files in the main directory equal to the number of performances in the Performances folder.

Third, run combine_human_ratings.py

This will produce a file called ground_truth_ratings.csv in the main directory by combining all of the human ratings in the HumanRatings folder

Fourth, run to_comedy_data.py

This will produce a file called clean_comedy_data.csv which contains the ground truth ratings and the data from the praat extraction.

Fifth, optionally edit the parameters in postjoke_classifier to change which classifier is used, what output is desired, whether or not to print graphs, how much information to print, ect

Sixth, run postjoke_classifier.py

This will produce an output in the console giving you the accuracy of the classifier based on the parameters.

WIP