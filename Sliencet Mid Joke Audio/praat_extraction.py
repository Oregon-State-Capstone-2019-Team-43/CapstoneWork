# Program for running the extract_mid_joke.praat or extract_post_joke.praat scripts on multiple performance directories
# Requires Python 3.5 or later

# This script assumes it is run in the directory containing the various performance folders
# and the joke and pause audio files are in a "jokes_and_pauses" subdirectory within each performance folder.
# It is designed to be run on a Windows computer, differences in file path format on another OS may cause errors.
# Praat.exe should be located in the directory this script is run from.

import os

## Calls the appropriate praat extraction script and moves extracted data to correct path

def call_extract(basedir, subdirs, out_path, program):
   if os.path.isdir(out_path) == False:
      os.mkdir(out_path)
   count = 31
   
   fullpath = basedir+"\\"+subdirs[0]
   print(fullpath)
   print("\nWorking on files in %s" % fullpath)
   filename = str(count)+".txt"
   cmd = program+fullpath+'" > '+filename
   print(cmd)
   os.system(cmd)
   mv = 'move '+filename+' '+out_path+' > nul'
   os.system(mv)
   print("Data saved in " + out_path + "/" + filename)

## Driver Program

type = input("Do you want 'mid' or 'mid_mfcc' praat data? ")

basedir = str(os.getcwd())
subdirs = [f.name for f in os.scandir(basedir) if f.is_dir()]
print("Found %s performance directories" % len(subdirs))

if type == "mid":
   print("Extracting praat features from joke files in subdirs of %s" % basedir)
   out_path = '../MidJokeMachineLearning/jokeinput'
   program = 'praat --run extract_mid_joke.praat "'

elif type == "mid_mfcc":
   print("Extracting praat features from joke files in subdirs of %s" % basedir)
   out_path = '../MidJokeMachineLearning/jokeinput'
   program = 'praat --run extract_MFCC_mid_joke.praat "'

else:
   print("Command not recognized")

call_extract(basedir, subdirs, out_path, program)

print("\nAll performance directories have been processed")
