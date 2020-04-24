import csv
import os

jokedict={}
newjokedict={}
with open('ground_truth_ratings.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    count=0
    for row in spamreader:
        if(count!=0):    
            key=row[1]
            if(key in jokedict):
                jokedict[key].append(row)
            else:
                jokedict[key]=[row]
        count+=1
        
    
numfiles = len([f for f in os.scandir(os.getcwd()) if f.name.endswith('.txt')]) # check how many txt files the praat script created


for i in range(1,numfiles+1):
    filename=str(i)+".txt"
    
    file = open(filename, "r", encoding='utf_16_le')
    
    title=file.readline().split('\\')[-2]
    
    if(title in jokedict):
        jokelist=(jokedict[title])
        index=0
        
        lines=file.readlines()
        count=0
        arr=[]
        for line in lines:
            if(count%7==0):
                if(arr!=[]):
                    temp=arr[0]
                    arr[0]=arr[2]
                    arr[2]=temp
                    temp=arr[1]
                    arr[1]=arr[3]
                    arr[3]=temp
                       
                    jokelist[index].pop(1)
                    jokelist[index].pop(2)
                    temp=jokelist[index].pop(-1)
                    temp=jokelist[index].pop(-1)
                    for x in arr:
                        jokelist[index].append(x)
                    jokelist[index].append(temp)
                    jokelist[index].append(temp)
                    
                    # print(len(jokelist[index]))
                    if(title=='2019-04-19 Singu-hilarity'):
                        print(len(jokelist[index]))
                        print(jokelist[index])
                    
                    index+=1                  
                arr=[]
            else:
                arr.append(line[:-2])
            count+=1
            
        if(arr!=[]):
            temp=arr[0]
            arr[0]=arr[2]
            arr[2]=temp
            temp=arr[1]
            arr[1]=arr[3]
            arr[3]=temp

            jokelist[index].pop(1)
            jokelist[index].pop(2)
            temp=jokelist[index].pop(-1)
            temp=jokelist[index].pop(-1)
            for x in arr:
                jokelist[index].append(x)
            jokelist[index].append(temp)
            jokelist[index].append(temp)

            # print(len(jokelist[index]))
            index+=1                  
            
        
        newjokedict[title]=jokelist
        
        
with open('clean_comedy_data.csv', 'w', newline='') as f:
    headers=['PerformanceId','JokeId','Pitch','PitchSd','Intensity','IntensitySd','MinSound','MaxSound','HumanScore','HumanScorePostJokeOnly']
    writer = csv.writer(f)
    
    writer.writerow(headers)
    for key in newjokedict:        
        print(key)
        writer.writerows(newjokedict[key])