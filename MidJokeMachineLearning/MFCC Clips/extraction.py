import os
import sys
import pandas as pd
from shutil import rmtree

def checkDirExist(path):
    """ 
    This method checks to see if the specified path already exists. 
    Creates if it does not exist.

    Returns bool
    """
    
    if not os.path.exists(path):
        print("[+] Directory does not exist")
        os.makedirs(path)
        return False
    else:
        return True


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

    if checkDirExist('exports'):
        print("[+] Deleting existing exports directory...")
        rmtree('exports')
        checkDirExist('exports')

    # Run FFMPEG via PowerShell (I'm a filthy windows user at home)
    for i in range(count - 1):
                                                                                        # Elan appends 'file:///' to the path...
        inputFilePath = filePaths[i].replace('.eaf', '.mp3').replace('file:///', '')    # Messy but should get the job done
        inputFileName = inputFilePath.split('/')[-1].replace('.mp3', '')                # We just want the file name sans extension
        dirName = inputFilePath.split('/')[4]                                           # Grabs the name of the subdirectory to organize files                                     
        currStartTime = startTimes[i]                                                   # Grabs the start time of the annotated laughter
        # currDuration = durations[i]                                                   # Not needed anymore

        checkDirExist(f"./exports/{dirName}")

        # os.system(f"powershell.exe ffmpeg -ss {currStartTime} -t {currDuration} -i \'{inputFilePath}\' \'./exports/{inputFileName}_{i}.mp3\'") # Code to run with custon duration
        os.system(f"powershell.exe ffmpeg -ss {currStartTime} -t 1 -i \'{inputFilePath}\' \'./exports/{dirName}/{inputFileName}-{i}.mp3\'")


if __name__ == "__main__":
    extract()
