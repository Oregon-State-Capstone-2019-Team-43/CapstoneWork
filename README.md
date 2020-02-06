# Robot Comedy Machine Learning Pipeline

## Written By: Ella Bisbee (eloise.bisbee@tufts.edu) — August 2019

### Folder Layout
There are two subdirectories in this all_robot_comedy directory.robot_comedy contains subdirectories corresponding to robot comedy performances, named exactly what the Performance is called in the ground_truth_ratings file provided by Dr. Fitter. Each performance directory contains the joke andpause after joke audio clips from each joke in that performance. They are numbered (and matched by number, e.g. pause_3.mp3 is the pause after joke_3.mp3) and they are numbered by the order in which they were said in the performance. In addition to the performance directories, robot_comedy also contains a series of bash and praat scripts, which I will explain in the control flow documentation below. robot_comedy_ml contains directories each contain the python scripts for processing and classifying data extracted from the performances. The subdirectories of robot_comedy_ml are named for which features the data they deal with contains. In each subdirectory, there are numbered folders corresponding to the raw data for each performance  extracted using the praatand bash scripts in robot_comedy, named "#.txt".  There is also a csv file named ground_truth_ratings.csv which contain the  human scores of each joke in each performance, in the order the jokes were told at the performance. The to_comedy_data file contains a python program that takes the numbered #.txt files and the ground_truth_ratings.csv files and outputs a file called clean_comedy_data.csv which contains the data from the numbered and ground truth files, cleaned up to be used in classifying. The classify file contains a python program for taking in data from clean_comedy_data and training and testing various classifiers on it.

### Control Flow

1. Run the appropriate bash script in robot_comedy for extracting the features you want. The bash scripts are named by what features they extract (pitch, intensity, standard deviation (std) for both, and min/max sound), and call the corresponding praat script that extracts those features from each file starting with 'pause' from each subdirectory. For each subdirectory, the bash script creates a numbered file (1 indexed) which contains: the full filepath of the directory containing the audio files as the first line, and then lists the pause file names and associated praat features as noted in the Assumptions section. The bash script will then send all those numbered files to a subdir in robot_comedy_ml corresponding to the features extracted.

2. Run to_comedy_data in the subdir of robot_comedy_ml corresponding to the features you are dealing with. This takes the numbered raw praat data files and the ground_truth_ratings.csv and outputs clean_comedy_data.csv which contains all the same information as these files but in a format that can be used by the classify function.

3. Finally, run the classify python script in the subdir of robot_comedy_ml, which has a long comment at the top/comments throughout which tell you how to run it. It takes the clean_comedy_data.csv and will run a classifer and validation technique as specified by the user in a function call in the file.


### Assumptions:

* The to_comedy_data program expects exactly this file structure.

* Directories containing the audio clips for each performance are named exactly what the Performance is named in ground_truth_ratings.csv

* Audio files containing the pause after a joke are named "pause_[order in which they appear in performance, zero indexed].mp3"

* The numbered raw praat data files have the full filepath as the first line and then it will list the full pause file names followed by the extracted praat data from that pause file like so:

```
pause_1.mp3
praat data
praat data
...
pause_2.mp3
praat data
praat data
```

Note that the order that the pauses are listed in does not matter. 

* The clean_comedy_data.csv file has the columns that are noted in the comment at the top of the classify python script corresponding to the specific features dealt with. For example the pitch_inten_avg clean_comedy_data should have columns: PerformanceId, JokeId, Pitch, Intensity, HumanScore HumanScorePostJokeOnly. This depends on how the to_comedy_data outputs.
