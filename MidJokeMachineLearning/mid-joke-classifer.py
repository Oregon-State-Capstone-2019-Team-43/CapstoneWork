import os 
import sys
import pandas as pd
import numpy as np 
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import multiprocessing as mp

#This is the class that store a single joke info
class Joke_Info:
    def __init__(self,intensity,stinten,pitch,stpit,max_inten,min_inten,max_pitch,min_pitch,performanceName,jokeindex,performanceID):
        self.intensity = intensity
        self.stinten= stinten
        self.pitch = pitch
        self.stpit= stpit
        self.max_inten=max_inten
        self.min_inten=min_inten
        self.max_pitch=max_pitch
        self.min_pitch=min_pitch
        self.performanceName=performanceName
        self.jokeindex=jokeindex
        self.jokeid=0
        self.jokeName=''
        self.midjokeHappen=0
        self.intensityRange=round(max_inten-min_inten,3)
        self.pitchRange=round(max_pitch-min_pitch,3)
        self.predictY=-1
        self.performanceID=performanceID

#There are some werid space and ecoding issue, so i use this function to remove spaces and newlines
def fixLines(lines):
    infos=[]
    for line in lines:
        element=line.replace('\x00\n','')
        element=element.replace('\x00','')
        element=element.replace('\n','')
        if(element!=''):
            infos.append(element)    
    return infos

#This function will go through all the txt files in the folder and store signle joke information and add them into jokeDict (Dictionary)
#jokeDict is a Dictionary to store all joke information for each performance
#The key of jokeDict is the performance name
#The value of jokeDict is array of Joke_Info
#You can use jokeDict[performanceName] to get a joke array
#In this array, there are all the jokes in this performacne. The data type for jokes is Joke_Info, which contains all info about a single joke.
def readJokeTxT(folder,files):
    jokeDict={}
    for file in files:
        filePath=folder+file
        f=open(filePath,'r',encoding='UTF-8')
        lines=f.readlines()
        infos=fixLines(lines)
        performanceName=infos.pop(0).split('\\')[-2]
        performanceID=performanceIDs[performanceName]
        jokes=[]
        for i in range(0,len(infos)):
            element=infos[i]
            if(i%9==0):
                jokeindex=int(element.split('_')[-1].split('.')[0])
            elif(i%9==1):
                intensity=round(float(element),3)
            elif(i%9==2):
                stinten=round(float(element),3)
            elif(i%9==3):
                min_inten=round(float(element),3)
            elif(i%9==4):
                max_inten=round(float(element),3)
            elif(i%9==5):
                pitch=round(float(element),3)
            elif(i%9==6):
                stpit=round(float(element),3)
            elif(i%9==7):
                max_pitch=round(float(element),3)
            elif(i%9==8):
                min_pitch=round(float(element),3)
                joke=Joke_Info(intensity,stinten,pitch,stpit,max_inten,min_inten,max_pitch,min_pitch,performanceName,jokeindex,performanceID)
                jokes.append(joke)
        jokeDict[performanceName]=jokes
    return jokeDict

#This function will update the real joke id for each joke.
def updateJoke_ID_Name(jokeDict,nameMatchFolder):   
    for performanceName in jokeDict:
        joke_name_id_dict={}
        filePath=nameMatchFolder+performanceName+'.txt'
        f=open(filePath,'r')
        lines=f.readlines()
        lines.pop(0)
        infos=fixLines(lines)    
        for info in infos:
            id=int(info.split(':')[1].split('.')[0].split('_')[1])
            name=info.split(':')[0]
            joke_name_id_dict[id]=name
        jokes=jokeDict[performanceName]
        for joke in jokes:
            joke.jokeName=joke_name_id_dict[joke.jokeindex]
            joke.jokeid=jokeIDs[joke.jokeName]
    return jokeDict

#This function will use human annotation to update if mid joke happen or not into each joke_info
def updateMidjokeHappen(jokeDict,performanceName,jokeindex):
    for perName in jokeDict:
        if (perName==performanceName):
            for joke in jokeDict[perName]:
                if(joke.jokeindex==jokeindex):
                    joke.midjokeHappen=1
                    return

#This function will read human annotation and update the midjokehappen in joke_info
def readHummanAnnotation(annotattionPath,jokeDict):
    f=open(annotattionPath,'r')
    lines=f.readlines()
    performanceName=None
    jokeindex=None
    midjokeHappen=False
    for line in lines:
        if('#E:'in line):
            if(midjokeHappen==True):
                updateMidjokeHappen(jokeDict,performanceName,jokeindex)
                midjokeHappen=False
                performanceName=None
                jokeindex=None
                midjokeHappen=False
                
            performanceName=line.split('\\')[-2]
            jokeindex=int(line.split('\\')[-1].split('.')[0].split('_')[-1])
            
        elif('Laughter' in line):
            midjokeHappen=True
            
    if(midjokeHappen==True and performanceName!=None and jokeindex!=None):
        updateMidjokeHappen(jokeDict,performanceName,jokeindex)
    return jokeDict

#This will generate ground truth table csv
def generaetGroundTruthCSV(jokeDict):
    CSV_arr=[]
    for perName in jokeDict:
        for joke in jokeDict[perName]:
            jokeArr=[perName,joke.jokeid,joke.jokeName,joke.midjokeHappen]
            CSV_arr.append(jokeArr)
    df = pd.DataFrame(CSV_arr, columns = ['Performance', 'JokeId','Joke','HumanScore'])
    outputpath=os.path.join(currentpath,'MidJokeMachineLearning/mid-joke-GroundTruth.csv')
    df.to_csv(outputpath,index=False)
    print("we output the human rating to mid-joke-GroundTruth.csv\n")
    
#This would split the weird joke and normal joke
def split_Normal_Werid(jokeDict):
    normalJokeDict={}
    weridJokeDict={}
    for perName in jokeDict:
        if('(Weird)' in perName):
            weridJokeDict[perName]=jokeDict[perName]
        else:
            normalJokeDict[perName]=jokeDict[perName]
    return normalJokeDict,weridJokeDict
#This function will split X,Y for you. X will be all the features, you wan to include
def split_XY(joke_arr,backgroundDict=None):
    Xarr=[]
    Yarr=[]
    J_id=[]
    P_id=[]
    if(backgroundDict==None):
        for joke in joke_arr:
            x=[joke.intensity,joke.stinten,joke.pitch,joke.stpit,joke.max_inten,joke.min_inten,joke.max_pitch,joke.min_pitch]
            y=joke.midjokeHappen
            Xarr.append(x)
            Yarr.append(y)
            J_id.append(joke.jokeid)
            P_id.append(joke.performanceID)
    else:
        for joke in joke_arr:
            if(joke.jokeid in backgroundDict):
                background=backgroundDict[joke.jokeid]
                x=[joke.stinten,joke.stpit,joke.min_inten,joke.max_pitch,joke.min_pitch,
                   background.max_pitch,background.min_pitch]
                y=joke.midjokeHappen
                Xarr.append(x)
                Yarr.append(y)
                J_id.append(joke.jokeid)
                P_id.append(joke.performanceID)
    return Xarr,Yarr,J_id,P_id

#This is the SVM training, it will generate 3 models for you. 
def SVM_train(trainX,trainY,gamma_val,c_val):
    rbfclf = SVC(kernel='rbf',C=c_val,gamma=gamma_val)
    rbfclf.fit(trainX, trainY)
    
    linearclf = SVC(kernel='linear')
    linearclf.fit(trainX, trainY)
    
    polyclf = SVC(kernel='poly',degree=3)
    polyclf.fit(trainX, trainY)
    
    return rbfclf,linearclf,polyclf

#This function would predict the Y base on the model you provide and return the accuracy 
def predict_And_calAccuracy(clf,validX,validY):
    predictY = clf.predict(validX)
    error=0
    for y1,y2 in zip(predictY,validY):
        if(y1!=y2):
            error+=1
    return round(1-error/len(validY),3)

#This would take one performance out as a validation dataset
def takeOnePerfomanceOut(X_ALL_ARR,Y_ALL_ARR,TestDict,performanceName,backgroundDict=None):
    validX,validY,trainX,trainY=[],[],[],[]
    Pids,Jids=[],[]
    index=0
    if(backgroundDict==None):
        for name in TestDict:
            arr=TestDict[name]
            if(name==performanceName):
                for joke in arr:
                    validX.append(X_ALL_ARR[index])
                    validY.append(Y_ALL_ARR[index])
                    Jids.append(joke.jokeid)
                    Pids.append(joke.performanceID)
                    index+=1
            else:
                for joke in arr:
                    trainX.append(X_ALL_ARR[index])
                    trainY.append(Y_ALL_ARR[index])
                    index+=1
    else:
        for name in TestDict:
            arr=TestDict[name]
            if(name==performanceName):
                for joke in arr:
                    if(joke.jokeid in backgroundDict):
                        validX.append(X_ALL_ARR[index])
                        validY.append(Y_ALL_ARR[index])
                        Jids.append(joke.jokeid)
                        Pids.append(joke.performanceID)
                        index+=1
            else:
                for joke in arr:
                    if(joke.jokeid in backgroundDict):
                        trainX.append(X_ALL_ARR[index])
                        trainY.append(Y_ALL_ARR[index])
                        index+=1       
                
    return validX,validY,trainX,trainY,Pids,Jids


def generateRandomSample(sample,goalNum):
    extraSample=[]
    X = np.array(sample)
    nbrs = NearestNeighbors(n_neighbors=3, algorithm='auto').fit(X)
    distances, indices = nbrs.kneighbors(X)
    
    for indice in indices:
        p1_index=indice[0]
        p2s=indice[1:]
        for p2_index in p2s:
            p1=np.array([sample[p1_index]])
            p2=np.array([sample[p2_index]])
            newP=(p1+p2)/2
            extraSample.append(newP[0])
            if(len(sample)+len(extraSample)==goalNum):
                return extraSample

def overSample(trainX,trainY):
    posSample=[]
    negSample=[]
    for x,y in zip(trainX,trainY):
        if y==1:
            posSample.append(x)
        else:
            negSample.append(x)
    
    pos=len(posSample)
    neg=len(negSample)
    moreY=[]
    if(neg<pos):
        extraSample=generateRandomSample(negSample,pos)
        moreY=(pos-neg)*[0]
    elif(pos<neg):
        extraSample=generateRandomSample(posSample,neg)
        moreY=(neg-pos)*[1]
    
    trainX+=extraSample
    trainY+=moreY
    return trainX,trainY

#This is the main function for train model and valid model
def runTest(TestDict,normalize,reference=False):
    backgroundDict=None
    totalX=[]
    totalY=[]
    totalPredictY=[]
    jokeId=[]
    performanceId=[]
    
    c_val=1
    gamma_val=10
    
    CSV_arr=[]
    rbfAccuracy=0
    linearAccuracy=0
    polyAccuracy=0
    total_number_of_jokes=0
    
    X_ALL_ARR=[]
    Y_ALL_ARR=[]
    
    jokeids=[]
    name='2020-01-31 Mt Caz'
    Joke_Arr=TestDict[name]
    for joke in Joke_Arr:
        jokeids.append(joke.jokeid)


    if(reference==False):
        for performanceName in TestDict:
            Joke_Arr=TestDict[performanceName]
            singleX,singelY,_,_=split_XY(Joke_Arr)
            X_ALL_ARR+=singleX
            Y_ALL_ARR+=singelY
    else:
        backgroundName='2019-12-06 Silent Background Recording'
        backgroundArr=TestDict[backgroundName]
        backgroundDict={}
        jokeids2=[]
        for joke in backgroundArr:
            backgroundDict[joke.jokeid]=joke
            jokeids2.append(joke.jokeid)
        for performanceName in TestDict:
            Joke_Arr=TestDict[performanceName]
            singleX,singelY,_,_=split_XY(Joke_Arr,backgroundDict)
            X_ALL_ARR+=singleX
            Y_ALL_ARR+=singelY
    if(normalize=='minmax'):
        scaler = MinMaxScaler()
        X_ALL_ARR = scaler.fit_transform(X_ALL_ARR).tolist()
    if(normalize=='standard'):
        scaler = StandardScaler()
        X_ALL_ARR = scaler.fit_transform(X_ALL_ARR).tolist()    
      
    
    for performanceName in TestDict:
        valid_performanceName=performanceName
        valid_Joke_Arr=TestDict[performanceName]  
        validX,validY,trainX,trainY,Pids,Jids=takeOnePerfomanceOut(X_ALL_ARR,Y_ALL_ARR,TestDict,performanceName,backgroundDict)   
        total_number_of_jokes=len(validX)+len(trainX)
        # trainX,trainY=overSample(trainX,trainY)
            
        print("There are "+str(len(validX))+" jokes.\tIn the valid performance: "+valid_performanceName)
        rbfclf,linearclf,polyclf=SVM_train(trainX,trainY,gamma_val,c_val)
   
        totalX+=validX
        totalY+=validY
        totalPredictY+=rbfclf.predict(validX).tolist()
        jokeId+=Jids
        performanceId+=Pids
        
   
        Accuracy1=predict_And_calAccuracy(rbfclf,validX,validY)
        Accuracy2=predict_And_calAccuracy(linearclf,validX,validY)
        Accuracy3=predict_And_calAccuracy(polyclf,validX,validY)
        rbfAccuracy+=Accuracy1
        linearAccuracy+=Accuracy2
        polyAccuracy+=Accuracy3
        print('RBF Accuracy:',Accuracy1,'\tLinear Accuracy:',Accuracy2,'\tPolynomial Accuracy:',Accuracy3,'\n')
        CSV_arr.append([performanceName,len(valid_Joke_Arr),Accuracy1,Accuracy2,Accuracy3])
    
    
    avgRBF=round(rbfAccuracy/len(TestDict),3)
    avgLinear=round(linearAccuracy/len(TestDict),3)
    avgPoly=round(polyAccuracy/len(TestDict),3)
    print('RBF average Accuracy:',avgRBF,'\tLinear average Accuracy:',avgLinear,'\tPolynomial average Accuracy:',avgPoly,'\n')
    
    CSV_arr.append(['',''+'','','',''])
    CSV_arr.append(['Overall Accuracy','#of Jokes','avgRBF','avgLinear','avgPoly'])
    
    CSV_arr.append(['final',total_number_of_jokes,avgRBF,avgLinear,avgPoly])
    
    df = pd.DataFrame(CSV_arr, columns = ['Performance', '# of jokes','RBF','Linear','Poly'])
    outputpath=os.path.join(currentpath,'MidJokeMachineLearning/jokeoutput/SVC_Accuracy_Result.csv')
    df.to_csv(outputpath,index=False)
    print("we output the human rating to jokeoutput\SVC_Accuracy_Result.csv\n")
    
    outputPrediction(totalX,totalY,totalPredictY,jokeId,performanceId)


#This function is derived from main function, the goal is testing different c and gamma for SVM RBF
def tuneBoth(TestDict,normalize,c_val,gamma_val,reference=False):
    backgroundDict=None
    rbfAccuracy=0
    total_number_of_jokes=0
    
    X_ALL_ARR=[]
    Y_ALL_ARR=[]
    if(reference==False):
        for performanceName in TestDict:
            Joke_Arr=TestDict[performanceName]
            singleX,singelY,_,_=split_XY(Joke_Arr)
            X_ALL_ARR+=singleX
            Y_ALL_ARR+=singelY
    else:
        backgroundName='2019-12-06 Silent Background Recording'
        backgroundArr=TestDict[backgroundName]
        backgroundDict={}
        jokeids2=[]
        for joke in backgroundArr:
            backgroundDict[joke.jokeid]=joke
            jokeids2.append(joke.jokeid)
        for performanceName in TestDict:
            Joke_Arr=TestDict[performanceName]
            singleX,singelY,_,_=split_XY(Joke_Arr,backgroundDict)
            X_ALL_ARR+=singleX
            Y_ALL_ARR+=singelY
    if(normalize=='minmax'):
        scaler = MinMaxScaler()
        X_ALL_ARR = scaler.fit_transform(X_ALL_ARR).tolist()
    if(normalize=='standard'):
        scaler = StandardScaler()
        X_ALL_ARR = scaler.fit_transform(X_ALL_ARR).tolist()    
    
    
    for performanceName in TestDict:
        valid_performanceName=performanceName
        valid_Joke_Arr=TestDict[performanceName]  
        validX,validY,trainX,trainY,Pids,Jids=takeOnePerfomanceOut(X_ALL_ARR,Y_ALL_ARR,TestDict,performanceName,backgroundDict)  
        total_number_of_jokes=len(validX)+len(trainX)
        # trainX,trainY=overSample(trainX,trainY)
            
        # print("There are "+str(len(valid_Joke_Arr))+" jokes.\tIn the valid performance: "+valid_performanceName)
        rbfclf,linearclf,polyclf=SVM_train(trainX,trainY,gamma_val,c_val)

        Accuracy1=predict_And_calAccuracy(rbfclf,validX,validY)
        rbfAccuracy+=Accuracy1

    avgRBF=round(rbfAccuracy/len(TestDict),3)
    print('RBF average Accuracy:',avgRBF,"(C,Gamma): ",c_val,gamma_val)
    
    return avgRBF

def outputPrediction(totalX,totalY,totalPredictY,jokeId,performanceId):    
    df=pd.DataFrame({'Classifier_Rating':totalPredictY,
                  'Joke':jokeId,
                  'Human_Rating':totalY,
                  'Performance':performanceId})
    
    outputpath=os.path.join(currentpath,'MidJokeMachineLearning/jokeoutput/mid_joke_results.csv')
    df.to_csv(outputpath,index=False)
    print("The mid_joke_results is at: ",outputpath)
    
#Find the current path and import the joke-id, perfomance-id dictionary
currentpath=os.getcwd()
endindex=currentpath.index('CapstoneWork')+len('CapstoneWork')
currentpath=currentpath[:endindex]
libspath=os.path.join(currentpath,'libs')
sys.path.append(libspath)
from perf_and_joke_dict import joke, performance
jokeIDs=joke
performanceIDs=performance
inputFolder=os.path.join(currentpath,'MidJokeMachineLearning/jokeinput/')
print(inputFolder)
#Go through and read all the files in the input folder
files = os.listdir(inputFolder)
jokeDict=readJokeTxT(inputFolder,files)

#Match the joke and joke id
nameMatchFolder=os.path.join(currentpath,'MidJokeMachineLearning/joke_name_matching/')
jokeDict=updateJoke_ID_Name(jokeDict,nameMatchFolder)

#Read the human annotation
annotattionPath=os.path.join(currentpath,'MidJokeMachineLearning/Mid_Joke_Annotations.txt')
jokeDict=readHummanAnnotation(annotattionPath,jokeDict)
generaetGroundTruthCSV(jokeDict)

#Split the normal joke and werid joke
normalJokeDict,weridJokeDict=split_Normal_Werid(jokeDict)

#Train the model and print test

#You can train all the joke(Both normal and werid) or you can train all normal joke
    
# runTest(jokeDict,'minmax',False)
runTest(jokeDict,'minmax',True)

# # This is the code for you to test the best combo of C and gamma for svm
# Cs = [0.1, 1, 10,100,1000]
# gammas = [ 0.1, 1,10,100,1000]
# bothtasks=[(x,y) for x in Cs for y in gammas]
# result=[]

# for task in bothtasks:
#     result.append(tuneBoth(jokeDict,'minmax',task[0],task[1],True))
# print(result)
# bestAccuracy=max(result)
# bestcombo=bothtasks[result.index(bestAccuracy)]

# print("The best combo of (C,gamma) is:")
# print(bestcombo)
# print(bestAccuracy)


