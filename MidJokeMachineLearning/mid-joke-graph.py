import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import pearsonr

missingFiles = []
# This is the class that store a single joke info


class Joke_Info:
    def __init__(self, intensity, stinten, pitch, stpit, max_inten, min_inten, max_pitch, min_pitch, performanceName, jokeindex, performanceID):
        self.intensity = intensity
        self.stinten = stinten
        self.pitch = pitch
        self.stpit = stpit
        self.max_inten = max_inten
        self.min_inten = min_inten
        self.max_pitch = max_pitch
        self.min_pitch = min_pitch
        self.performanceName = performanceName
        self.jokeindex = jokeindex
        self.jokeid = 0
        self.jokeName = ''
        self.midjokeHappen = 0
        self.intensityRange = round(max_inten-min_inten, 3)
        self.pitchRange = round(max_pitch-min_pitch, 3)
        self.predictY = -1
        self.performanceID = performanceID

# There are some werid space and ecoding issue, so i use this function to remove spaces and newlines


def fixLines(lines):
    infos = []
    for line in lines:
        element = line.replace('\x00\n', '')
        element = element.replace('\x00', '')
        element = element.replace('\n', '')
        if(element != ''):
            infos.append(element)
    return infos

# This function will go through all the txt files in the folder and store signle joke information and add them into jokeDict (Dictionary)
# jokeDict is a Dictionary to store all joke information for each performance
# The key of jokeDict is the performance name
# The value of jokeDict is array of Joke_Info
# You can use jokeDict[performanceName] to get a joke array
# In this array, there are all the jokes in this performacne. The data type for jokes is Joke_Info, which contains all info about a single joke.


def readJokeTxT(folder, files):
    jokeDict = {}
    for file in files:
        filePath = folder+file
        f = open(filePath, 'r', encoding='UTF-8')
        lines = f.readlines()
        infos = fixLines(lines)
        performanceName = infos.pop(0).split('\\')[-2]
        performanceID = performanceIDs[performanceName]
        jokes = []
        for i in range(0, len(infos)):
            element = infos[i]
            if(i % 9 == 0):
                jokeindex = int(element.split('_')[-1].split('.')[0])
            elif(i % 9 == 1):
                intensity = round(float(element), 3)
            elif(i % 9 == 2):
                stinten = round(float(element), 3)
            elif(i % 9 == 3):
                min_inten = round(float(element), 3)
            elif(i % 9 == 4):
                max_inten = round(float(element), 3)
            elif(i % 9 == 5):
                pitch = round(float(element), 3)
            elif(i % 9 == 6):
                stpit = round(float(element), 3)
            elif(i % 9 == 7):
                max_pitch = round(float(element), 3)
            elif(i % 9 == 8):
                min_pitch = round(float(element), 3)
                joke = Joke_Info(intensity, stinten, pitch, stpit, max_inten, min_inten,
                                 max_pitch, min_pitch, performanceName, jokeindex, performanceID)
                jokes.append(joke)
        jokeDict[performanceName] = jokes
    return jokeDict

# This function will update the real joke id for each joke.


def updateJoke_ID_Name(jokeDict, nameMatchFolder):
    for performanceName in jokeDict:
        joke_name_id_dict = {}
        filePath = nameMatchFolder+performanceName+'.txt'
        f = open(filePath, 'r')
        lines = f.readlines()
        lines.pop(0)
        infos = fixLines(lines)
        for info in infos:
            id = int(info.split(':')[1].split('.')[0].split('_')[1])
            name = info.split(':')[0]
            joke_name_id_dict[id] = name
        jokes = jokeDict[performanceName]
        for joke in jokes:
            joke.jokeName = joke_name_id_dict[joke.jokeindex]
            joke.jokeid = jokeIDs[joke.jokeName]
    return jokeDict

# This function will use human annotation to update if mid joke happen or not into each joke_info


def updateMidjokeHappen(jokeDict, performanceName, jokeindex):
    for perName in jokeDict:
        if (perName == performanceName):
            for joke in jokeDict[perName]:
                if(joke.jokeindex == jokeindex):
                    joke.midjokeHappen = 1
                    return

# This function will read human annotation and update the midjokehappen in joke_info


def readHummanAnnotation(annotattionPath, jokeDict):
    f = open(annotattionPath, 'r')
    lines = f.readlines()
    performanceName = None
    jokeindex = None
    midjokeHappen = False
    for line in lines:
        if('#E:'in line):
            if(midjokeHappen == True):
                updateMidjokeHappen(jokeDict, performanceName, jokeindex)
                midjokeHappen = False
                performanceName = None
                jokeindex = None
                midjokeHappen = False

            performanceName = line.split('\\')[-2]
            jokeindex = int(line.split('\\')[-1].split('.')[0].split('_')[-1])

        elif('Laughter' in line):
            midjokeHappen = True

    if(midjokeHappen == True and performanceName != None and jokeindex != None):
        updateMidjokeHappen(jokeDict, performanceName, jokeindex)
    return jokeDict


def split_positive_negative(jokeDict):

    positive_joke_arr, negative_joke_arr = [], []
    for perName in jokeDict:
        joke_arr = jokeDict[perName]
        for joke in joke_arr:
            if(joke.midjokeHappen == 1):
                positive_joke_arr.append(joke)
            else:
                negative_joke_arr.append(joke)
    return positive_joke_arr, negative_joke_arr

def split_jokewise_data(jokeDict):
    joke_wise_dict={}
    for perName in jokeDict:
        joke_arr = jokeDict[perName]
        for joke in joke_arr:
            jokeName=joke.jokeName
            if (jokeName in joke_wise_dict):
                joke_wise_dict[jokeName].append(joke)
            else:
                joke_wise_dict[jokeName]=[joke]
    return joke_wise_dict

def generate_Singel_BoxPlot(positive_joke_arr, negative_joke_arr, feature,title,outputPath):
    pos_val_arr, neg_val_arr = [], []
    for joke in positive_joke_arr:
        pos_val_arr.append(getattr(joke, feature))
    for joke in negative_joke_arr:
        neg_val_arr.append(getattr(joke, feature))
    data = [pos_val_arr, neg_val_arr]
    fig = plt.figure(1, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    red_square = dict(markerfacecolor='r', marker='s')
    bp = ax.boxplot(data, flierprops=red_square,patch_artist=True)

    for box in bp['boxes']:
        # change outline color
        box.set(color='#7570b3', linewidth=2)
        # change fill color
        box.set(facecolor='#1b9e77')

    # change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)

    # change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)

    # change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='#b2df8a', linewidth=2)

    # change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)
    plt.xticks([1, 2], ['Laughter happen(1)', 'Laughter not happen(0)'])

    outputPath=os.path.join(outputPath,title+'.png')
    # print(outputPath)
    plt.savefig(outputPath)
    plt.close()
    
def generate_Singel_Correlation(positive_joke_arr, negative_joke_arr, feature1,feature2,outputPath):
    pos_val_arr, neg_val_arr = [], []
    allX,allY=[],[]
    for joke in positive_joke_arr:
        x=getattr(joke, feature1)
        y=getattr(joke, feature2)
        allX.append(x)
        allY.append(y)
        point=(x,y)
        pos_val_arr.append(point)
    for joke in negative_joke_arr:
        x=getattr(joke, feature1)
        y=getattr(joke, feature2)
        allX.append(x)
        allY.append(y)
        point=(x,y)
        neg_val_arr.append(point)
    corr, _ = pearsonr(allX, allY)
    corr=round(corr,3)
    # print(corr)
        
    fig=plt.figure(figsize=(10,6))
    title=feature1+"-"+feature2
    plt.title(title)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    for point in pos_val_arr:
        plt.scatter(point[0],point[1],marker="^",color='r',label='Blue stars')
    for point in neg_val_arr:
        plt.scatter(point[0],point[1],marker="x",color='b',label='Red stars')
    red_patch = mpatches.Patch(color='red', label='mid joke happened')
    blue_patch = mpatches.Patch(color='blue', label='mid joke did not happen')
    corr_patch=mpatches.Patch(color='black', label='Pearsons correlation: '+str(corr))
    plt.legend(handles=[red_patch,blue_patch,corr_patch],prop={"size":7})
    outputPath=os.path.join(outputPath,title+'.png')
    plt.savefig(outputPath)
    # print(outputPath)
    plt.close()

def generate_ALL_OverALL_Correlations(currentpath,positive_joke_arr, negative_joke_arr):
    
    features=['intensity','pitch','stinten','stpit','max_inten','min_inten','max_pitch','min_pitch']
    outputPath=os.path.join(currentpath,"MidJokeMachineLearning/jokeoutput/overall-correlation-update/")
    for i in range(len(features)):      
        for j in range(i+1,len(features)):
            generate_Singel_Correlation(positive_joke_arr, negative_joke_arr, features[i],features[j],outputPath)
    print("Please check ",outputPath)

def generate_ALL_JokeWise_Correlations(currentpath,joke_wise_dict):
    features=['intensity','pitch','stinten','stpit','max_inten','min_inten','max_pitch','min_pitch']
    
    for jokeName in joke_wise_dict:
        jokeName_path=jokeName.replace('.','_')
        jokeName_path=jokeName_path.replace('/','_')
        outputPath=os.path.join(currentpath,"MidJokeMachineLearning/jokeoutput/jokewise-correlation-update/",jokeName_path)
      
        joke_arr=joke_wise_dict[jokeName]
        if(len(joke_arr)<10):
            print(jokeName,' dataset= ',len(joke_arr),' Skip')
            continue
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        
        positive_joke_arr, negative_joke_arr=[],[]
        for joke in joke_arr:
            if(joke.midjokeHappen == 1):
                positive_joke_arr.append(joke)
            else:
                negative_joke_arr.append(joke)
        for i in range(len(features)):      
            for j in range(i+1,len(features)):
                generate_Singel_Correlation(positive_joke_arr, negative_joke_arr, features[i],features[j],outputPath)
        print("Please check ",outputPath)

def generate_ALL_OverALL_BoxPlots(currentpath,positive_joke_arr, negative_joke_arr):
    
    features=['intensity','pitch','stinten','stpit','max_inten','min_inten','max_pitch','min_pitch']
    titles=['intensity,dB','pitch,Hz','std Intensity,dB','std Pitch,Hz','max_intensity,dB','min_intensity,dB','max_pitch,Hz','min_pitch,Hz']
    
    outputPath=os.path.join(currentpath,"MidJokeMachineLearning/jokeoutput/overall-boxplot-update/")
    for i in range(len(features)):      
        generate_Singel_BoxPlot(positive_joke_arr, negative_joke_arr, features[i],titles[i],outputPath)
    print("Please check ",outputPath)

def generate_ALL_JokeWise_BoxPlots(currentpath,joke_wise_dict):
    features=['intensity','pitch','stinten','stpit','max_inten','min_inten','max_pitch','min_pitch']
    titles=['intensity,dB','pitch,Hz','std Intensity,dB','std Pitch,Hz','max_intensity,dB','min_intensity,dB','max_pitch,Hz','min_pitch,Hz']
    
    for jokeName in joke_wise_dict:
        jokeName_path=jokeName.replace('.','_')
        jokeName_path=jokeName_path.replace('/','_')
        outputPath=os.path.join(currentpath,"MidJokeMachineLearning/jokeoutput/jokewise-boxplot-update/",jokeName_path)
      
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        joke_arr=joke_wise_dict[jokeName]
        positive_joke_arr, negative_joke_arr=[],[]
        for joke in joke_arr:
            if(joke.midjokeHappen == 1):
                positive_joke_arr.append(joke)
            else:
                negative_joke_arr.append(joke)
        for i in range(len(features)):      
            generate_Singel_BoxPlot(positive_joke_arr, negative_joke_arr, features[i],titles[i],outputPath)
        print("Please check ",outputPath)
    
# Find the current path and import the joke-id, perfomance-id dictionary
currentpath = os.getcwd()
endindex = currentpath.index('CapstoneWork')+len('CapstoneWork')
currentpath = currentpath[:endindex]
libspath = os.path.join(currentpath, 'libs')
sys.path.append(libspath)
from perf_and_joke_dict import joke, performance
jokeIDs = joke
performanceIDs = performance
inputFolder = os.path.join(currentpath, 'MidJokeMachineLearning/jokeinput/')
# Go through and read all the files in the input folder
files = os.listdir(inputFolder)
jokeDict = readJokeTxT(inputFolder, files)

# Match the joke and joke id
nameMatchFolder = os.path.join(
    currentpath, 'MidJokeMachineLearning/joke_name_matching/')
jokeDict = updateJoke_ID_Name(jokeDict, nameMatchFolder)

# Read the human annotation
annotattionPath = os.path.join(
    currentpath, 'MidJokeMachineLearning/Mid_Joke_Annotations.txt')
jokeDict = readHummanAnnotation(annotattionPath, jokeDict)

positive_joke_arr, negative_joke_arr = split_positive_negative(jokeDict)
joke_wise_dict=split_jokewise_data(jokeDict)

generate_ALL_OverALL_BoxPlots(currentpath,positive_joke_arr, negative_joke_arr)
generate_ALL_JokeWise_BoxPlots(currentpath,joke_wise_dict)

generate_ALL_OverALL_Correlations(currentpath,positive_joke_arr, negative_joke_arr)
generate_ALL_JokeWise_Correlations(currentpath,joke_wise_dict)