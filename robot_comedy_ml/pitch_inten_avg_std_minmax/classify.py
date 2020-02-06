#made by: Ella Bisbee eloise.bisbee@tufts.edu 8/20/19
#this program will classify the data in clean_comedy_data.csv in ways specified
#by the user in the code below.

#The program expects that clean_comedy_data.csv is in the same directory, and has
#columns: PerformanceId, JokeId, Pitch, PitchStd, Intensity, IntensityStd,
#MinSound, MaxSound, HumanScore, HumanScorePostJokeOnly

#The actual function that does the classification and validation is classifyAndVal,
#which takes options specified in the comment above the function.
#The options for classification are knn, svm, or decision tree.
#The options for validation are random split, nfold, or leave one performance out.

#As written now, the classifyAndVal function takes the data and options and returns
#The percent of test data classified correctly. Hopefully the code is well commented
#enough that you know where to change anything if you wish to adapt the program (email
#me if not!)

#There is also the option to normalize or not normalize the data, either normalizing 
#both the pitch and intensity or just intensity. The method of normalization is to normalize
#every value against the gdpr joke (jokeId 4) for it's performance.

import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.colors import ListedColormap
from mlxtend.plotting import plot_decision_regions
import sklearn
from sklearn import neighbors, datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn import tree

#used to determine if a string is an int
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#takes: com_data (the np.array'ed comedy data from the file),
#X (an np array containing pitch, pitchstd, intensity, intensitystd,
#minsound, maxsound arrays for each joke), 
#y (the ground truth -1, 0, or 1 ratings of each joke in X),
#val_option: either 'rand', 'nfold', or 'leave1out' indicating how
#the classifier should be validated.
#class_option: either 'knn', 'svm', or 'dt' for the classification
#technique to be used. 
#returns the percent of test data correctly classified in decimal form.
def classifyAndVal(com_data, X, y, val_option, class_option):
    if val_option == 'rand':
        train, test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=1, stratify=y)
        if class_option == 'knn':
            #adjust neighbs value if you wish for a different number of neighbors
            neighbs = 5
            #weight can either be 'uniform' or 'distance', as per scikit learn knn
            weight = 'uniform'
            clf = neighbors.KNeighborsClassifier(neighbs, weights=weight)
        elif class_option == 'svm':
            clf = svm.SVC(gamma='scale')
        elif class_option == 'dt':
            clf = tree.DecisionTreeClassifier()
        else: 
            print('invalid classification option. Options are: knn, svm, dt.')
            return
        plot_decision_regions(X=X.values, 
                      y=y.values,
                      clf=clf, 
                      legend=2)
        plt.xlabel(X.columns[0], size=14)
        plt.ylabel(X.columns[1], size=14)
        plt.title('SVM Decision Region Boundary', size=16)
        clf.fit(train, y_train)
        return clf.score(test, y_test)
    elif val_option == 'nfold':
        #adjust if you want a different number of folds for nfolds
        n_folds = 5
        if class_option == 'knn':
            #adjust neighbs value if you wish for a different number of neighbors
            neighbs = 5
            #weight can either be 'uniform' or 'distance', as per scikit learn knn
            weight = 'uniform'
            clf = neighbors.KNeighborsClassifier(neighbs, weights=weight)
        elif class_option == 'svm':
            clf = svm.SVC(gamma='scale')
        elif class_option == 'dt':
            clf = tree.DecisionTreeClassifier()
        else: 
            print('invalid classification option. Options are: knn, svm, dt.')
            return
        #cv_scores contains the scores for all n fold cross validations.
        cv_scores = cross_val_score(clf, X, y, cv=n_folds)
        return np.mean(cv_scores)
    elif val_option == 'leave1out':
        #this block counts the number of performances included in the data,
        #and what indices in X they start and end at
        pers = {}
        curr = -1.0
        for i in range(0, len(com_data)):
            if curr != com_data[i][0]:
                if curr != -1:
                    pers[curr].append(i - 1)
                curr = com_data[i][0]
                pers[curr] = [i]
        pers[curr].append(len(com_data) - 1)
        #this block iterates through each performance and puts that performance in 
        #the test and y_test arrays, and every other performance in the train and y_train
        #The scores for each performance being used as the test is placed in 
        #scores dictionary.
        scores = {}
        for elem in pers:
            if len(X[:pers[elem][0], :]) == 0:
                train = X[pers[elem][1] + 1:, :]
                y_train = y[pers[elem][1] + 1:]
            elif len(X[pers[elem][1] + 1:, :]) == 0:
                train = X[:pers[elem][0], :]
                y_train = y[:pers[elem][0]]
            else:
                train = np.concatenate((X[:int(pers[elem][0]), :], X[int(pers[elem][1]) + 1:, :]), axis=0)
                y_train = np.concatenate((y[:int(pers[elem][0])], y[int(pers[elem][1]) + 1:]), axis=0)
            test = X[pers[elem][0]:pers[elem][1]+1, :]
            y_test = y[pers[elem][0]:pers[elem][1]+1]
            if class_option == 'knn':
                #adjust neighbs value if you wish for a different number of neighbors
                neighbs = 5
                #weight can either be 'uniform' or 'distance', as per scikit learn knn
                weight = 'uniform'
                clf = neighbors.KNeighborsClassifier(neighbs, weights=weight)
            elif class_option == 'svm':
                clf = svm.SVC(gamma='scale')
            elif class_option == 'dt':
                clf = tree.DecisionTreeClassifier()
            else:
                print('invalid classification option. Options are: knn, svm, dt.')
                return
            print(clf.fit(train, y_train))
            scores[elem] = clf.score(test, y_test)
        #calculates the average score and returns it
        sum_score = 0
        for i in scores:
            sum_score += scores[i]
        return sum_score / len(scores)
    else:
        print("invalid validation option. Options are: rand, nfold, leave1out")
        return
    
#this function takes a value and a gdpr joke value and returns
#a normalized value. If the gdpr value is 0, it defaults to 200
def normalize(val, gdpr):
    default = 200
    if gdpr == 0:
        return val/default
    else:
        return val/gdpr

#this function gets a specific gdpr value from the dict. of 
#gdpr values corresponding to the 'key' performance. It get's
#the j'th value. If the key is not a valid key in the dict., it 
#returns an estimated average based on what j is (corresponding
#to the order of pitch, pitchstd, intensity, intensitystd, min, max in the data)
def getGdpr(gdpr_list, key, j):
    try:
        gdpr_list[key]
        #print(str(key) + " " + str(gdpr_list[key]))
        return gdpr_list[key][j]
    except KeyError:
        if j == 0:
            return 200
        elif j == 1:
            return 30
        elif j == 2:
            return 80
        elif j == 3:
            return 5
        else:
            return 50
        
#This function iterates through the X 2d list (which is expected to
#be the raw_com_data array) and normalizes the pitch, pitchstd, intensity
# and intensitystd values,then returns the normalized array
def normalizeAll(X, gdpr_vals):
    for i in range(0, len(X)):
        for j in range(0,4):
            raw_com_data[i][2 + j] = normalize(raw_com_data[i][2 + j], 
                                               getGdpr(gdpr_vals, raw_com_data[i][0],j))
    return X

#This function iterates through the X 2d list (which is expected to
#be the raw_com_data array) and normalizes the intensity and intensitystd
#values, then returns the normalized array
def normalizeIntensity(X, gdpr_vals):
    for i in range(0, len(X)):
        for j in range(2,4):
            raw_com_data[i][2 + j] = normalize(raw_com_data[i][2 + j], 
                                               getGdpr(gdpr_vals, raw_com_data[i][0],j))
    return X

#_________________________________________________________________________________________________________________________
#______________________________________MAIN FUNCTION BODY BEGINS HERE_____________________________________________________
#_________________________________________________________________________________________________________________________

#read in csv file
raw_com_data = []
com_data_cols = []
gdpr_vals = {}
with open('clean_comedy_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    curr_per = -1
    for row in csv_reader:
        if count == 0:
            com_data_cols = row
        else:
            #this little if statement block is to add the gdpr joke to
            #the list of gdpr values. The key is the performanceId
            if (curr_per != int(row[0]) and int(row[1]) == 4):
                cur_per = int(row[0])
                gdpr_vals[int(row[0])] = [float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7])] 
            for i in range(0, len(row)):
                if isInt(row[i]):
                    row[i] = int(row[i])
                else:
                    row[i] = float(row[i])
            raw_com_data.append(row)
        count += 1

#uncomment if you want to normalize all data:
raw_com_data = normalizeAll(raw_com_data, gdpr_vals)

#uncomment if you want to normalize intensity:
#raw_com_data = normalizeIntensity(raw_com_data, gdpr_vals)

#extracts just the pitch and intensity values into X, and 
#human rating after joke only into y

com_data = np.array(raw_com_data)
X = com_data[:, 2:8]
#for i in X:
#    print(i)
y = com_data[:, 9:]
y = y.ravel()
#print(y)

#this is the call to classifyAndVal, where the actual brute of 
#computation is carried out. Look at comment above function definition
#for information about options
print(classifyAndVal(com_data, X, y, 'rand', 'svm'))
print('sklearn: %s' % sklearn.__version__)