1. Go to the `Performances` folder. Run `praat_extraction.py` and select 'mid' to generate the raw data of the mid joke audio. It will put them into `MidJokeMachineLearning\jokeinput`

2. Go to `MidJokeMachineLearning\joke_name_matching`\
copy all the txt file from the jokeinput folder and paste here.\
run `match_joke_names.py` and select 'joke'.\
This generates files based on the praat txt files and it will to match joke id and joke index.

3. Have `Mid_Joke_Annotations.txt` in the `MidJokeMachineLearning` folder.

4. Read `mid-joke-classifer.py` and run it. In this code you can decide what kind of normalization you want use and which performance to test.\
This generates `mid-joke-GroundTruth.csv` and shows the classifier results.

5. Check `MidJokeMachineLearning\jokeoutput\SVC_Accuracy_Result.csv` for the final result
