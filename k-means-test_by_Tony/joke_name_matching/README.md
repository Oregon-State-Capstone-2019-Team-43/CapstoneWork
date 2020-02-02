Script for matching the joke_# or pause_# lines in the praat data text files to the joke name they go with.

Instructions:
1) Have the text files you are going to use with the k_means_script in the input folder
2) Run this script from this direcory

The script will generate new text files in this directory for each performance with a file name matching the performance name.
The first line of the file is the performance name. The rest of the lines match the names of the jokes that were told during that performance to the joke or pause numbers they were given in the praat text file for that performance, in the order they are listed in the praat text file.

Output format:
_name of first joke told_**:**joke_0.mp3
_name of second joke told_**:**joke_1.mp3
_name of eleventh joke told_**:**joke_10.mp3
_name of third joke told_**:**joke_2.mp3
