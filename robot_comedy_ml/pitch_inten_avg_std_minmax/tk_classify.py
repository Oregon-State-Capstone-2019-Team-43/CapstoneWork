import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.plotting import plot_decision_regions
from sklearn import svm
from sklearn import tree
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

verbose = 1 # 0 = false, 1 = true, use for debugging
normalize = 1 # 0 = false, 1 = 0-1,
column_names_to_normalize = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'] # 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
kernel = 'rbf' # 'linear' or 'poly' or 'rbf' or 'sigmoid' or 'precomputed'
SVM_C = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0] # SVM regularization parameter
SVM_Gamma = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0] # SVM regularization parameter
R_State = 1 # None or Integer
features = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'] # 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
validation = 'HumanScorePostJokeOnly' # 'HumanScore' or 'HumanScorePostJokeOnly'
validation_technique = 'tts' # 'tts' or 'l1o'
joke_ids = ['PerformanceId', 'JokeId'] # 'PerformanceId', 'JokeId'

df = pd.read_csv('clean_comedy_data.csv', error_bad_lines=False, encoding='utf-8', delimiter=',')

X = df[features]
y = df[validation]
joke_id = df[joke_ids]

if normalize == 1:
	scaler = MinMaxScaler() 
	x = X[column_names_to_normalize].values
	x_scaled = scaler.fit_transform(x)
	df_temp = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = df.index)
	X[column_names_to_normalize] = df_temp

if validation_technique == 'tts':
	train, test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=R_State, stratify=y)
elif validation_technique == 'l1o':


if verbose:
	for SVM_C_val in SVM_C:
		for SVM_Gamma_val in SVM_Gamma:
			clf = svm.SVC(kernel=kernel, degree=3, gamma=SVM_Gamma_val, C=SVM_C_val)
			clf.fit(train, y_train)
			# if normalize:
			# 	print("Normalization Used\n")
			# else:
			# 	print("Normalization Not Used\n")
			prediction = clf.predict(test)
			# print(prediction)
			nega= 0
			zero= 0
			posi= 0
			for val in prediction:
				if val == -1:
					nega += 1
				elif val == 0:
					zero += 1
				else:
					posi += 1
			# print("Gamma: ", SVM_Gamma_val, " C: ", SVM_C_val)
			# for q, w, e in zip(prediction, y_test, y_test.index):
			# 	joke = joke_id.iloc[e]
			# 	if q != w:
			# 		print("\tPredicted: ", str(q), "\tActual: ", str(w), "\tPerformance: ", joke['PerformanceId'], "\tJoke: ", joke['JokeId'])
			print("Gamma: ", SVM_Gamma_val, "\tC: ", SVM_C_val, "\t-:", nega, "\t0: ", zero, "\t+: ", posi, "  \tRating: ", clf.score(test, y_test))
else:
	clf = svm.SVC(kernel=kernel, degree=3, gamma=SVM_Gamma, C=SVM_C)
	clf.fit(train, y_train)
	print(clf.score(test, y_test))