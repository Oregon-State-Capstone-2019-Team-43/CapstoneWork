# Robot Comedy Machine Learning Pipeline

2019-2020 Senior Capstone Team
* Timothy Bui
* Yuhang (Tony) Chen
* Brian Ozarowicz
* Trevor Webster

Previous Work
* Ella Bisbee (eloise.bisbee@tufts.edu) - August 2019

### Directory Layout

* **HumanRatings** - Contains CSVs of human-recorded post-joke ratings and some scripts to use on them for data processing and analysis.
* **libs** - Contains `perf_and_joke_dict.py` which has two dictionaries, one of all of the Performances with corresponding ID numbers and one of all of the Jokes with corresponding ID numbers.
* **MachineLearning** - Contains `to_comedy_data.py` and `postjoke_classifier.py` which are used to process the data for the machine learning and perform the machine learning respectively. `#.txt` files will also be generated here for each performance when the post-joke praat extraction script is run.
* **Mid-Joke Laughter Annotations** - (work in progress)
* **MidJokeMachineLearning** - Contains the files for processing the data for doing mid-joke machine learning and for running the mid-joke classifier.
* **Performances** - Contains subdirectories for each performance as well as Praat.exe and the praat data extraction files.

### Assumptions

* You are using a Windows computer
* You are using Python 3.5 or later
* There is at least one human rating CSV before running the post-joke classifier
* Each human ratings CSV contains a rating for every joke from every performance

### Dependencies

* matplot
* mlxtend
* pandas
* seaborn
* sklearn

### Control Flow

These are instructions for running the post-joke and mid-joke classifiers. For information on the additional tools in this repo please see the Readmes in each main folder which contain details on the specific files in that section and their functions.

#### Post-Joke Analysis

1. Go to the `HumanRatings` directory and run `combine_human_ratings.py`\
This produces the file `ground_truth_ratings.csv` in the `MachineLearning` directory by combining all of the human ratings CSVs.

2. Go to the `Performances` directory, run `praat_extraction.py` and choose to extract post-joke data\
This should produce a number of .txt files in the `MachineLearning` folder equal to the number of subdirectories in the `Performances` folder.

3. Go to the `MachineLearning` directory and run `to_comedy_data.py`\
This produce a file called `clean_comedy_data.csv` which contains the ground truth ratings for each joke and their corresponding data from the praat extraction.

4. (Optional) Edit the parameters in `postjoke_classifier.py` to get the desired output

5. Run `postjoke_classifier.py`\
This will produce output in the console showing the accuracy of the classifier based on the selected parameters.

#### Mid-Joke Analysis

1. Go to the `Performances` directory, run `praat_extraction.py` and choose to extract mid-joke data\
This should produce a number of .txt files in the `MidJokeMachineLearning\jokeinput` folder equal to the number of subdirectories in the `Performances` folder.

2. Go to `MidJokeMachineLearning\joke_name_matching` and run `match_joke_names.py`\
This generates text files based on the praat extraction files that will match joke ids and indexes to their corresponding praat data.

3. Have `Mid_Joke_Annotations.txt` in the `MidJokeMachineLearning` folder.\
(This file is already present; this step only needs done if a new performance has been added and annotated.)

4. (Optional) Edit `mid-joke-classifer.py` to set what kind of normalization you want to use and which performances to test.

5. Run `mid-joke-classifer.py`\
This program generates `mid-joke-GroundTruth.csv` and calculates the classifier results. Check `MidJokeMachineLearning\jokeoutput\SVC_Accuracy_Result.csv` for the final result.
