#/bin/bash
basedir=$(pwd)
echo extracting praat features from files in subdirs of "$basedir"
count=1
for dir in */ ; do
	fullpath=$basedir/$dir
	filename="$count".txt
	../../praat --run extract_pitch_inten.praat "$fullpath" > $filename
	mv $filename ../robot_comedy_ml/pitch_inten_avg
	count=$((count+1))	
done
