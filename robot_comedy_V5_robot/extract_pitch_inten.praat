#NOTE: got help from this website http://praatscriptingtutorial.com/loopingThroughFiles
#Made by: Ella Bisbee 7/23/2019
#script to extract intensity and pitch from every file starting with "pause" in a directory 
#form: get the full file path of the directory to extract
form Get files
	text Dir hello
endform
writeInfoLine: dir$ 

#creates list of all files in directory that begin with "pause"
search$ = dir$ + "pause"
fileList = Create Strings as file list... list 'search$'*
numFiles = Get number of strings

#iterates through all files in directory, extracting pitch and intensity and writing them to info
for i from 1 to numFiles
	selectObject: fileList
	fileName$ = Get string: i
	appendInfoLine: fileName$
	fullPath$ = dir$ + fileName$
	Read from file: fullPath$
	sound = selected("Sound")
	To Pitch: 0, 75, 300
	Rename: "pitch"
	selectObject: sound
	To Intensity: 75, 0
	Rename: "intensity"
	selectObject: "Intensity intensity"
	intensity = Get mean... 0 0 dB
	appendInfoLine: intensity
	selectObject: "Pitch pitch"
	pitch = Get mean... 0 0 Hertz
	appendInfoLine: pitch
endfor

