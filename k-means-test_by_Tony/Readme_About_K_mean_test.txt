Project Name: K-means-cluster
Purpose: Using k-means method to split data into 3 groups
Author: Tony (Yuhang Chen)
Date: Jan,24th,2020

Instructions:
	1.Get the all txt files by using praat and the previous student's bash code
	2.Put those txt files into input directory
	3.Open K-means-test-ipynb and run the code
	4.Check the pictures output in output directory

By default, I used loop to generate result of all files at input directory. If you only want to generate result for a certain file,
please check the commented code.


Right now I got all the result from 18 performances of V6 robot recordings.
Each picture represent one performance.

If you want to test it with some new data files, please remember to change the variable 'numOfFiles'


Special case:
	For some reason, there are a few pauses do not have a pitch, which shows '--undefined--',
my program did not use these data. 
	