import os
import sys
import pandas as pd

def extract():
    if len(sys.argv) != 2:
        print("[+] NOT ENOUGH ARGS")
        exit()

    print("[+] Begin extraction...")
    
    myCsv = sys.argv[1]
    myCsvAsDF = pd.read_csv(myCsv)
    csvAsDict = myCsvAsDF.to_dict(orient="list")

    # print("[+] Columns")
    # for k in csvAsDict:
    #     print(f"[+] k: {k}")

    # Arrays
    startTimes = csvAsDict.get('Begin Time - ss.msec', None)
    durations = csvAsDict.get('Duration - ss.msec', None)
    filePaths = csvAsDict.get('File Path', None)

    count = 0

    print(len(filePaths))

    with open(myCsv, 'r') as f:
        for line in f:
            count += 1
    
    print(f"[+] Total Lines: {count}")

    # Check if dir exists
    if not os.path.exists('exports'):
        print("[+] Does not exist")
        os.makedirs('exports')

    # Run FFMPEG via PowerShell (I'm a filthy windows user at home)
    for i in range(count - 1):
        inputFilePath = filePaths[i].replace('.eaf', '.mp3')
        inputFileName = inputFilePath.split('/')[-1].replace('.mp3', '')
        dirName = inputFilePath.split('/')[7]
        currStartTime = startTimes[i]
        # currDuration = durations[i] # Not needed anymore

        # os.system(f"powershell.exe ffmpeg -ss {currStartTime} -t {currDuration} -i \'{inputFilePath}\' \'./exports/{inputFileName}_{i}.mp3\'") # Code to run with custon duration
        os.system(f"powershell.exe ffmpeg -ss {currStartTime} -t 1 -i \'{inputFilePath}\' \'./exports/{dirName}/{inputFileName}_{i}.mp3\'")


if __name__ == "__main__":
    extract()
