1. Go to the `Performances` folder. Run `praat_extraction.py` and select 'mid' or 'mid mfcc' to generate the raw data of the mid joke audio. It will put them into `MidJokeMachineLearning\jokeinput`

2. Go to `MidJokeMachineLearning\joke_name_matching` and run `match_joke_names.py`\
This generates files based on the praat txt files that will match joke id and joke index to the praat data.

3. Have `Mid_Joke_Annotations.txt` in the `MidJokeMachineLearning` folder.\
(This file is already present; this step only needs done if a new performance has been added and annotated.)

4. Go to the folder `CapstoneWork\Sliencet Mid Joke Audio` and `run praat_extraction` to generate all raw pratt data for slienct background.

5. Read `mid-joke-classifer.py` and run it. In this code you can decide what kind of normalization you want to use and which performances to test.\
This program generates `mid-joke-GroundTruth.csv` and calculates the classifier results.

6. Check `MidJokeMachineLearning\jokeoutput\SVC_Accuracy_Result.csv` for the final result
