# Program for running the extract_pitch_inten_std_minmax_post_joke.praat script or
# the extract_pitch_inten_std_minmax_mid_joke.praat script on multiple performance directories
# Requires Python 3.5 or later

# This script assumes it is run in the directory containing the various performance folders
# and the joke and pause audio files are in a "jokes_and_pauses" subdirectory within each performance folder.
# It is designed to be run on a Windows computer, differences in file path format on another OS may cause errors.
# Praat.exe should be located in the directory this script is run from.

import os
type = input("Do you want mid-joke (enter 'mid') or post-joke (enter 'post') praat data? ")
basedir = str(os.getcwd())
if type == "mid":
   print("Extracting praat features from joke files in subdirs of %s" % basedir)
if type == "post":
   print("Extracting praat features from pause files in subdirs of %s" % basedir)
subdirs = [f.name for f in os.scandir(basedir) if f.is_dir()]
print("Found %s performance directories" % len(subdirs))
if type == "mid":
   count = 1
   for dir in subdirs:
      fullpath = basedir+"\\"+dir+"\\jokes_and_pauses"
      print("\nWorking on files in %s" % fullpath)
      filename = str(count)+".txt"
      cmd = 'praat --run extract_pitch_inten_std_minmax_mid_joke.praat "'+fullpath+'" > '+filename
      os.system(cmd)
      mv = 'move '+filename+' ../mid_joke_praat_data/pitch_inten_avg_std_minmax > nul'
      os.system(mv)
      print("Data saved in %s\\mid_joke_praat_data\\pitch_inten_avg_std_minmax\\%s" % (basedir[:-20], filename))
      count = count+1
if type == "post":
   count = 1
   for dir in subdirs:
      fullpath = basedir+"\\"+dir+"\\jokes_and_pauses"
      print("\nWorking on files in %s" % fullpath)
      filename = str(count)+".txt"
      cmd = 'praat --run extract_pitch_inten_std_minmax_post_joke.praat "'+fullpath+'" > '+filename
      os.system(cmd)
      mv = 'move '+filename+' ../ > nul'
      os.system(mv)
      print("Data saved in %s\\robot_comedy_ml\\pitch_inten_avg_std_minmax\\%s" % (basedir[:-20], filename))
      count = count+1
print("\nAll performance directories have been processed")