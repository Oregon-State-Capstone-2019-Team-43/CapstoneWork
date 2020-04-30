### HumanRatings
This folder contains the CSVs of human-recorded post-joke ratings and some scripts to use on them.

### combine_human_ratings.py
This script combines the data from the individual ratings CSVs into one `ground_truth_ratings.csv` file which is used in the `MachineLearning` folder.\
It needs run the first time you clone this repo and any time data in the human rating CSVs is changed.

### accuracy_check.py
This script calculates the inter-rater accuracy (or agreement) between the human post-joke ratings.\
It outputs to `human_accuracy_results.txt` showing the overall accuracy of each rater compared to the consensus ratings, as well as their accuracy per performance. This information can be used to determine a reasonable accuracy level goal for the classifier to perform at.

### ground_truths_template.py
This script generates the file `ground_truths_template.csv` used for recording new individual human ratings.

If creating an entirely new set of human ratings:
* After running, rename the resulting `ground_truths_template.csv` to `<RaterName>_ground_truths.csv`
* To enter your ratings, open the CSV in a spreadsheet editor
* Find the section for the performance you are rating, the jokes told are listed in order
* Open the `jokes_and_pauses` folder for that performance
* Play the "pause" mp3 files in order and enter your ratings in the `HumanScorePostJokeOnly` column

If you have already rated previous performances and a new one is being added:
* After running, open `ground_truths_template.csv` in a spreadsheet editor and find the section for the new performance
* Copy the `Performance` and `Joke` cells for the new performance you need to rate
* Open the CSV containing your previous ratings in a spreadsheet editor
* Scroll to the bottom and paste the copied cells to add the new performance to this file
* Open the `jokes_and_pauses` folder for the new performance
* Play the "pause" mp3 files in order and enter your ratings in the `HumanScorePostJokeOnly` column
