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
	selectObject: sound
	To Intensity: 75, 0
	intensity = Get mean... 0 0 dB
	appendInfoLine: intensity
	stinten = Get standard deviation... 0 0
	appendInfoLine: stinten
	min = Get minimum... 0 0 Sinc70
	appendInfoLine: min
	max = Get maximum... 0 0 Sinc70
	appendInfoLine: max
	selectObject: sound
	To Pitch: 0, 75, 300
	pitch = Get mean... 0 0 Hertz
	appendInfoLine: pitch
	stpit = Get standard deviation... 0 0 Hertz
	appendInfoLine: stpit
	maxpit = Get maximum: 0, 0, "Hertz", "Parabolic"
	appendInfoLine: maxpit
	selectObject: sound
	To MelFilter... 0.015 0.005 100 100 0
	To MFCC... 12
	matrix## = To Matrix
	rows = Get number of rows
	columns = Get number of columns
	for x from 1 to rows
		mean = 0
		max = 0
		min = 1000
		for y from 1 to columns
			value = Get value in cell... x y
			mean += value
			if value > max
				max = value
			endif
			if value < min
				min = value
			endif
		endfor
		mean = mean / columns
		appendInfoLine: mean
		appendInfoLine: max
		appendInfoLine: min
	endfor
endfor