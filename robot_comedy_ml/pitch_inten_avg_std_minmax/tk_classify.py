import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.plotting import plot_decision_regions
from sklearn import svm
from sklearn import tree
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# 0 = false, 1 = true, use for debugging
verbose = 0
# 0 = false, 1 = true
normalize = 0
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

clf = svm.SVC(gamma='scale')
clf.fit(train, y_train)
if verbose:
	if normalize:
		print("Normalization used")
	else:
		print("Normalization not used")
	prediction = clf.predict(test)
	prediction2 = []
	pmin, pmax = min(prediction), max(prediction)
	for i, val in enumerate(prediction):
		prediction2.append(2*((val-pmin)/(pmax-pmin))-1)
	prediction3 = [round(x) for x in prediction2]
	for x, g, z, t, i in zip(prediction, prediction2, prediction3, y_test, y_test.index):
		joke = joke_id.iloc[i]
		print(round(x, 2), '\t', round(g, 2), '\t', z, '\t', t, '\t', joke['PerformanceId'], '\t', joke['JokeId'])
	# for p, y in zip(prediction, y_test):
	# 	if p != y:
	# 		print("Incorrectly classified as " + str(p) + " should be " + str(y))
	# 	elif p == y:
	# 		print(str(y.index) + " has been classified as " + str(p) + " should be " + str(y))
	# 	else:
	# 		print("Correct")
else:
	print(clf.score(test, y_test))

# pca = PCA(n_components = 2)
# train2 = pca.fit_transform(train)

# # Plot Decision Region using mlxtend's awesome plotting function
# plot_decision_regions(X=train2, y=y_train, clf=clf, legend=2)

# # Update plot object with X/Y axis labels and Figure Title
# plt.xlabel(X.columns[0], size=14)
# plt.ylabel(X.columns[1], size=14)
# plt.title('SVM Decision Region Boundary', size=16)
# plt.show()