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
	To MelFilter... 0.015 0.005 100 100 0
    To MFCC... 12
    matrix## = To Matrix
    rows = Get number of rows
	columns = Get number of columns
	for x from 1 to rows
		appendInfoLine: "Row ", x
		for y from 1 to columns
			value = Get value in cell... x y
			appendInfoLine: value
		endfor
	endfor
endfor