# Requires Python 3.5 or later
# Assumes this script is run in the V6_robot_recordings directory containing the performance folders
# with the pause audio files in a jokes_and_pauses subdirectory within each performance folder
# and praat.exe is located in the directory this script is run from

import os
import sys
basedir = str(os.getcwd())
print("Extracting praat features from files in subdirs of %s" % basedir)
subdirs = [f.name for f in os.scandir(basedir) if f.is_dir()]
print("Found %s performance subdirectories" % len(subdirs))
count = 1
for dir in subdirs:
   fullpath = basedir+"\\"+dir+"\\jokes_and_pauses"
   print("\nWorking on files in %s" % fullpath)
   filename = str(count)+".txt"
   cmd = 'praat --run extract_pitch_inten_std.praat "'+fullpath+'" > '+filename
   os.system(cmd)
   mv = 'move '+filename+' ../robot_comedy_ml/pitch_inten_avg_std'
   os.system(mv)
   print("Data saved in ../robot_comedy_ml/pitch_inten_avg_std/%s" % filename)
   count = count+1
print("All performance directories have been processed")
