import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.plotting import plot_decision_regions
from sklearn import svm
from sklearn import tree
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# 0 = false, 1 = true, use for debugging
verbose = 1
# 0 = false, 1 = true
normalize = 0
# 'linear' or 'poly' or 'rbf' or 'sigmoid' or 'precomputed'
kernel = 'rbf'
# SVM regularization parameter
C = 1.0
# 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
features = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound']
# 'HumanScore' or 'HumanScorePostJokeOnly'
validation = 'HumanScorePostJokeOnly'
# 'PerformanceId', 'JokeId'
joke_ids = ['PerformanceId', 'JokeId']

df = pd.read_csv('clean_comedy_data.csv', error_bad_lines=False, encoding='utf-8', delimiter=',')

X = df[features]
y = df[validation]
joke_id = df[joke_ids]

if normalize:
	scaler = MinMaxScaler() 
	column_names_to_normalize = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd']
	x = X[column_names_to_normalize].values
	x_scaled = scaler.fit_transform(x)
	df_temp = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = df.index)
	X[column_names_to_normalize] = df_temp

train, test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

clf = svm.SVC(kernel=kernel, degree=10, gamma='scale', C=C)
clf.fit(train, y_train)
if verbose:
	if normalize:
		print("Normalization used")
	else:
		print("Normalization not used")
	prediction = clf.predict(test)
	print("Predictions: ", prediction)
	for q, w, e in zip(prediction, y_test, y_test.index):
		joke = joke_id.iloc[e]
		if q != w:
			print("Incorrectly classified as ", str(q), "\tshould be ", str(w), "\tPerformance: ", joke['PerformanceId'], "\tJoke: ", joke['JokeId'])
	print("Overall Rating: ", clf.score(test, y_test))
else:
	print(clf.score(test, y_test))