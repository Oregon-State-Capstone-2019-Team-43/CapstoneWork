#made by: Ella Bisbee 8/9/19
#loop through all files in a directory and extract pitch and intensity at every 
#1/20th of a second from every file in the directory that begins with "joke"
#writes to a text file
form Get files
	text Dir hello
endform
writeInfoLine: dir$

#create list of all files in directory that begin with "joke"
search$ = dir$ + "\joke"
fileList = Create Strings as file list... list 'search$'*
numFiles = Get number of strings
timestep = 1/4

#iterates through all files in directory
for i from 1 to numFiles
	selectObject: fileList
	fileName$ = Get string: i
	appendInfoLine: fileName$
	fullPath$ = dir$ + "\" + fileName$
	Read from file: fullPath$
	sound = selected ("Sound")
	length = Get total duration
	To Pitch: 0.001, 75, 300
	Rename: "pitch"
	selectObject: sound
	To Intensity: 75, 0.001
	Rename: "intensity"
	time = timestep
	while time < length
		selectObject: "Pitch pitch"
		pitch_val = Get value at time: time, "Hertz", "Linear"
		selectObject: "Intensity intensity"
		inten_val = Get value at time: time, "Cubic"
		appendInfoLine: fixed$ (time, 2), " ", fixed$ (pitch_val, 3), " ", fixed$ (inten_val, 3)
		time = time + timestep
	endwhile	
endfor