import os 


class Pause_Info:
    def __init__(self,intensity,stinten,pitch,stpit,max_inten,min_inten,max_pitch,min_pitch,performance,id,jokeName):
        self.intensity = intensity
        self.stinten= stinten
        self.pitch = pitch
        self.stpit= stpit
        self.max_inten=max_inten
        self.min_inten=min_inten
        self.max_pitch=max_pitch
        self.min_pitch=min_pitch
        self.performance=performance
        self.id=id
        self.jokeName=jokeName
        self.midjoke=-100
        self.intensityRange=max_inten-min_inten
        self.pitchRange=max_pitch-min_pitch
        self.predictY=-1
        
def readJokeTxT(folder,files,jokeDict):
    for file in files:
        filePath=folder+file
        f=open(filePath,'r',encoding='UTF-8')
        lines=f.readlines()
        infos=[]
        for line in lines:
            element=line.replace('\x00\n','')
            element=element.replace('\x00','')
            element=element.replace('\n','')
            if(element!=''):
                infos.append(element)
        performanceName=infos.pop(0).split('\\')[-2]
        print(performanceName)
        quit()

currentpath=os.getcwd()
endindex=currentpath.index('CapstoneWork')+len('CapstoneWork')
currentpath=currentpath[:endindex]

inputFolder=currentpath+'\\MidJokeMachineLearning\\jokeinput\\'
files = os.listdir(inputFolder)

jokeDict=[]
readJokeTxT(inputFolder,files,jokeDict)