This script is for matching the `joke_#` lines in the mid-joke praat text files to the joke names they go with.

Instructions:
* Have the text files with the mid-joke praat data in `MidJokeMachineLearning/jokeinput`\
(They are put there automatically when running `praat_extraction.py` and selecting the 'mid' option.)
* Run this script from this direcory

The script will generate a text file in this directory for each performance, with the file name being the performance name.\
The first line of the file is the performance name. The rest of the lines match the names of the jokes that were told during that performance to the joke numbers they were given in the praat text file for that performance, in the order they are listed in the praat text file.

Output format:\
*name of first joke told* **:** joke\_0.mp3\
*name of second joke told* **:** joke\_1.mp3\
*name of eleventh joke told* **:** joke\_10.mp3\
*name of third joke told* **:** joke\_2.mp3
