Project k-means-for-joke
Purpose: Using k-means method to split Joke into 2 groups in order to detect if mid-laughter happened or not
Author: Tony (Yuhang Chen)
Date: Jan,31th,2020

Instructions:
	1.Get the all txt files by using praat and the Trevor and Brian's python code
	2.Put those txt files into "mid_joke_praat_data" directory
	3.Open "k-means-for-joke.ipynb" file in "k-means-test_by_Tony" folder and run the code
	4.Check the pictures and txt output in "mid_joke_praat_data\pitch_inten_avg_std_minmax\jokeoutput" directory


PS:
	In the "k-means-for-joke.ipynb" file,the important function is clusterData(Info_arr,choice)

	#info_arr represent an array of same jokeID in different performances
	#choice=1 is using intensity and pitch as x-y axis
	#choice=2 is using std intensity and std pitch as x-y axis
	#by default, I am using choice=1,but you can change to 2 later to generate result base on std intensity and std pitch.
	def clusterData(Info_arr,choice):



Test result:

Joke0:(With intensity and pitch)
	Group0
	performance Name: 2019-09-06 RoboCom  Data values: (76, 128)          (Had mid-laughter)
	performance Name: 2019-09-19 Bombs Away Cafe  Data values: (73, 131)  (Had mid-laughter)
	performance Name: 2019-09-21 Laugh Track Town USA  Data values: (73, 133) (do not have mid-laughter)
	performance Name: 2019-04-18 Bombs Away Cafe  Data values: (75, 141)  (Had mid-laughter)
	performance Name: 2019-05-16 Bombs Away Cafe  Data values: (73, 137) (Had mid-laughter)
	performance Name: 2019-06-19 Trek Theater  Data values: (74, 127) (Had mid-laughter)
	performance Name: 2019-06-20 Bombs Away Cafe  Data values: (73, 137) (Had mid-laughter)
	performance Name: 2019-08-15 Bombs Away Cafe  Data values: (72, 133) (Had mid-laughter)
	performance Name: 2019-08-23 Spectrum  Data values: (73, 130) (Had mid-laughter)
	Group1
	performance Name: 2019-04-13 Cienna Nerdy Show at The Drake  Data values: (72, 128) (Had mid-laughter)
	performance Name: 2019-09-05 Stand-up Science  Data values: (72, 129) (do not have mid-laughter)
	performance Name: 2019-10-11 Singu-hilarity  Data values: (70, 128) (Had mid-laughter)
	performance Name: 2019-11-29 Comedy the Musical  Data values: (71, 134) (Had mid-laughter)
	performance Name: 2019-11-29 Crapshoot  Data values: (71, 130) (Had mid-laughter)
	performance Name: 2019-12-06 Silent Background Recording  Data values: (70, 129) (do not have mid-laughter)
	performance Name: 2019-12-09 Singu-Hilarity in San Francisco  Data values: (71, 127) (Had mid-laughter)
	performance Name: 2019-04-19 Singu-hilarity  Data values: (70, 134) (Had mid-laughter)
	performance Name: 2019-04-22 Class Performance  Data values: (70, 131) (do not have mid-laughter)

Base on the human listener result, group0 is the mid-laguhter group and group1 is the no mid-laughter group.
The accurate rate of group0 is 8/9=88%
The accurate rate of group1 is 3/9=30%
I only did a test on joke0 since a lot of other jokes does not match up with ID.


Joke0:(With std-intensity and std-pitch)

	Group0
	performance Name: 2019-04-13 Cienna Nerdy Show at The Drake  Data values: (11, 44) (Had mid-laughter)
	performance Name: 2019-09-05 Stand-up Science  Data values: (12, 48)  (do not have mid-laughter)
	performance Name: 2019-09-19 Bombs Away Cafe  Data values: (12, 46) (Had mid-laughter)
	performance Name: 2019-10-11 Singu-hilarity  Data values: (14, 52) (Had mid-laughter)
	performance Name: 2019-11-29 Comedy the Musical  Data values: (13, 51) (Had mid-laughter)
	performance Name: 2019-11-29 Crapshoot  Data values: (13, 49) (Had mid-laughter)
	performance Name: 2019-12-06 Silent Background Recording  Data values: (14, 46)  (do not have mid-laughter)
	performance Name: 2019-12-09 Singu-Hilarity in San Francisco  Data values: (13, 45) (Had mid-laughter)
	performance Name: 2019-04-19 Singu-hilarity  Data values: (14, 49) (Had mid-laughter)
	performance Name: 2019-04-22 Class Performance  Data values: (13, 48) (do not have mid-laughter)
	performance Name: 2019-06-19 Trek Theater  Data values: (11, 46) (Had mid-laughter)
	Group1
	performance Name: 2019-09-06 RoboCom  Data values: (11, 48) (Had mid-laughter)
	performance Name: 2019-09-21 Laugh Track Town USA  Data values: (11, 50) (do not have mid-laughter)
	performance Name: 2019-04-18 Bombs Away Cafe  Data values: (10, 51) (Had mid-laughter)
	performance Name: 2019-05-16 Bombs Away Cafe  Data values: (11, 57) (Had mid-laughter)
	performance Name: 2019-06-20 Bombs Away Cafe  Data values: (11, 53) (Had mid-laughter)
	performance Name: 2019-08-15 Bombs Away Cafe  Data values: (11, 51) (Had mid-laughter)
	performance Name: 2019-08-23 Spectrum  Data values: (11, 53) (Had mid-laughter)

Hmmm, hard to tell which group is the mid-laughter group....

Conclusion:
 it seems like using intensity and pitch as x-y axis give us a good result. Hight pitch and high intensity seems to be the mid-laughter group. It seems like we can 
detect mid-laughter well but not for no-mid-laughter. We need to do more test once all jokeId match each other and Tim finish the annotation. 
