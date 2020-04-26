#NOTE: got help from this website http://praatscriptingtutorial.com/loopingThroughFiles
#Made by: Ella Bisbee 7/23/2019
#script to extract intensity and pitch from every file starting with "pause" in a directory 
#form: get the full file path of the directory to extract
form Get files
	text Dir hello
endform
writeInfoLine: dir$

#creates list of all files in directory that begin with "pause"
search$ = dir$ + "\pause"
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
	min = Get minimum... 0 0 Sinc70
	appendInfoLine: min
	max = Get maximum... 0 0 Sinc70
	appendInfoLine: max
	selectObject: "Pitch pitch"
	pitch = Get mean... 0 0 Hertz
	appendInfoLine: pitch
	stpit = Get standard deviation... 0 0 Hertz
	appendInfoLine: stpit
	maxpit = Get maximum: 0, 0, "Hertz", "Parabolic"
	appendInfoLine: maxpit
	selectObject: sound
	To Formant (burg)... 0.01 5 5500 0.025 50
	Rename: "formant"
	selectObject: "Formant formant"
	maxformant = Get maximum... 1 0 0 Bark Parabolic
	appendInfoLine: maxformant
	minformant = Get minimum... 1 0 0 Bark Parabolic
	appendInfoLine: minformant
	meanformant = Get mean... 1 0 0 Bark
	appendInfoLine: meanformant
	sdformant = Get standard deviation... 1 0 0 Bark
	appendInfoLine: sdformant
	selectObject: sound
	To Harmonicity (cc)... 0.01 50 0.1 4.5
	Rename: "harmony"
	selectObject: "Harmonicity harmony"
	maxharmony = Get maximum... 0 0 Parabolic
	appendInfoLine: maxharmony
	minharmony = Get minimum... 0 0 Parabolic
	appendInfoLine: minharmony
	meanharmony = Get mean... 0 0
	appendInfoLine: meanharmony
	harmonysd = Get standard deviation... 0 0
	appendInfoLine: harmonysd
endfor