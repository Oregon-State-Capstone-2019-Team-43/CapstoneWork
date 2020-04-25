# Robot Comedy Machine Learning Pipeline

## Written By: 2019-2020 Senior Capstone Team — April 2020

* TIMOTHY BUI
* YUHANG (TONY) CHEN
* BRIAN OZAROWICZ
* TREVOR WEBSTER

## Original Work: Ella Bisbee (eloise.bisbee@tufts.edu) — August 2019

### Directory Layout

There are four subdirectories
* HumanRatings
* libs
* MachineLearning
* Performances

HumanRatings contains the human ratings as CSV files as well as combine_human_ratings.py

libs contains the file perf_and_joke_dict.py which contains two dictionaries, one of all of the Performances and a corresponding ID number and one of all of the Jokes and a corresponding ID number.

MachineLearning contains to_comedy_data.py and postjoke_classifier.py, which are used to process the data for the machine learning and actually run the machine learning respectively. ##.txt files will also be generated for each of the performances after the praat extraction is run.

Performances contains a subdirectories for each performance, as well as Praat.exe and the praat extraction files.

WIP

### Assumptions

Every human rating must contain a rating for all jokes in all performances. There must be at least 1 human rating.

WIP

### Dependencies

pandas
sklearn
matplot
seaborn

WIP

### Control Flow

First, ensure all files are aligned according to the above assumptions.

Second, run praat_extraction.py and choose to extract the post-joke data. As of today (2020-04-25) the mid-joke pipeline is incomplete.

This should produce a number of .txt files in the MachineLearning directory equal to the number of performances in the Performances folder.

Third, run combine_human_ratings.py

This will produce a file called ground_truth_ratings.csv in the MachineLearning directory by combining all of the human ratings in the HumanRatings folder

Fourth, run to_comedy_data.py

This will produce a file called clean_comedy_data.csv which contains the ground truth ratings and the data from the praat extraction.

Fifth, optionally edit the parameters in postjoke_classifier to get hte desired output.

Sixth, run postjoke_classifier.py

This will produce an output in the console giving you the accuracy of the classifier based on the parameters.

WIP