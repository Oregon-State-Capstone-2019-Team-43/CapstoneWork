#NOTE: got help from this website http://praatscriptingtutorial.com/loopingThroughFiles
#Made by: Ella Bisbee 7/23/2019
#script to extract intensity and pitch from every file starting with "joke" in a directory 
#form: get the full file path of the directory to extract
form Get files
	text Dir hello
endform
writeInfoLine: dir$

#creates list of all files in directory that begin with "joke"
search$ = dir$ + "\joke"
fileList = Create Strings as file list... list 'search$'*
numFiles = Get number of strings

#iterates through all files in directory, extracting pitch and intensity and writing them to info
for i from 1 to numFiles
	selectObject: fileList
	fileName$ = Get string: i
	appendInfoLine: fileName$
	fullPath$ = dir$ + "\" + fileName$
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
	stinten = Get standard deviation... 0 0
	appendInfoLine: stinten
	minIntensity = Get minimum... 0 0 Sinc70
	appendInfoLine: minIntensity
	maxIntensity = Get maximum... 0 0 Sinc70
	appendInfoLine: maxIntensity
	selectObject: "Pitch pitch"
	pitch = Get mean... 0 0 Hertz
	appendInfoLine: pitch
	stpit = Get standard deviation... 0 0 Hertz
	appendInfoLine: stpit	
	max_pitch = Get maximum: 0, 0, "Hertz", "Parabolic"
	appendInfoLine: max_pitch
	min_pitch = Get minimum: 0, 0, "Hertz", "Parabolic"
	appendInfoLine: min_pitch

endfor