import matplotlib.pyplot as plt
import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from mlxtend.plotting import plot_decision_regions
import seaborn as sns
import matplotlib.pyplot as plt

from perf_and_joke_dict.py import joke, performance

##################
### Parameters ###
##################

## Print Information

# Print additional line information for the classifiers, useful for debugging
# 0 = false, 1 = true
verbose = 0

# Print the performance and joke ID's of incorrectly classified jokes
# 0 = false, 1 = true
print_false_predictions = 0

# Draw Plot only works if only 2 Features are selected. Selecting more features will result in error.
# 0 = false, 1 = true
draw_plt = 0

## Feature Selection

# Current features are as follows:
# 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'

# What features will be used in the classifier
features = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound']

# What features will be normalized
column_names_to_normalize = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound']

# Which column to look at for data validation
# 'HumanScore' or 'HumanScorePostJokeOnly'
validation = 'HumanScorePostJokeOnly'

# Which columns correspond to the perfomance and joke IDs.
# 'PerformanceId', 'JokeId'
joke_ids = ['PerformanceId', 'JokeId']

## Classifier Information

# 'SVC' or 'Tree' or 'KNN' or 'NN' or 'NB' or 'RF'
classifier_type = 'SVC'

# Whether or not to normalize the data. 0 = no
# 'minmax' or 'standard' or 'per_minmax'
normalize = 0

# 'ho20' or 'l1po'
validation_technique = 'ho20'

# for hold out 20% only
# None for random or Integer
R_State = None
# Number of Trials to run, Integer, only useful for R_State = None
num_trials = 1

## Data Pruning

# 0 = false, 1 = combine 0's and 1's, 2 = combine -1's and 0's
two_class = 0

# Whether or not to remove undefined pitch values. 1 = yes, 0 = no
remove_zeros = 0

# Whether or not to remove silent performacne data. 1 = yes, 0 = no
no_silent = 0

## SVM Classifier Parameters

# 'linear' or 'poly' or 'rbf' or 'sigmoid' or 'precomputed'
kernel = 'rbf'

# SVM regularization parameter
SVM_C = 15000
# Tested Optimal Values (Log10):
#	No Normalization	15000
#	minmax 				100
#	standard 			1000

# SVM regularization parameter
SVM_Gamma = .00001
# Tested Optimal Values (Log10):
#	No Normalization	.00001
#	minmax 				.1
#	standard			.001

# For Log10 Calibration
calibrate = 0
SVM_C_range = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
SVM_Gamma_range = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]

########################
### Helper Functions ###
########################

# Random Forest Classifier
def rf_classify(train, test, y_train, y_test, joke_id):
	clf = RandomForestClassifier(n_estimators=100, max_depth=5)
	clf.fit(train, y_train)
	if verbose:
		print('NN Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

# Naive Bayes Classifier
def nb_classify(train, test, y_train, y_test, joke_id):
	clf = GaussianNB()
	clf.fit(train, y_train)
	prediction = clf.predict(test)
	if print_false_predictions:
		for q, w, e in zip(prediction, y_test, y_test.index):
			jokeid = joke_id.iloc[e]
			if q != w:
				print("\tPredicted: ", str(q), "\tActual: ", str(w), "\tPerformance: ", jokeid['PerformanceId'], "\tJoke: ", jokeid['JokeId'], "\t", list(joke.keys())[list(joke.values()).index(jokeid['JokeId'])])
	if verbose:
		print('NB Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

# Naive Bayes Classifier
def nn_classify(train, test, y_train, y_test, joke_id):
	clf = MLPClassifier()
	clf.fit(train, y_train)
	if verbose:
		print('NN Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

# K Nearest Neighbor Classifier
def knn_classify(train, test, y_train, y_test, joke_id):
	clf = KNeighborsClassifier()
	clf.fit(train, y_train)
	if verbose:
		print('KNN Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

# Decision Tree Classifier
def tree_classify(train, test, y_train, y_test, joke_id):
	clf = tree.DecisionTreeClassifier(max_depth=5)
	clf.fit(train, y_train)
	if verbose:
		print('Tree Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

# Support Vector Machine Classifier
def svc_classify(train, test, y_train, y_test, joke_id):
	if calibrate:
		for SVM_C_val in SVM_C_range:
			for SVM_Gamma_val in SVM_Gamma_range:
				clf = svm.SVC(kernel=kernel, degree=3, gamma=SVM_Gamma_val, C=SVM_C_val)
				clf.fit(train, y_train)
				if verbose:
					print_predictions(SVM_Gamma_val, SVM_C_val, clf, test, y_test)
				else:
					print(clf.score(test, y_test))
				if draw_plt:
					draw_plot(clf, test, y_test)
	else:
		clf = svm.SVC(kernel=kernel, degree=3, gamma=SVM_Gamma, C=SVM_C)
		clf.fit(train, y_train)
		if verbose:
			print_predictions(SVM_Gamma, SVM_C, clf, test, y_test)
		else:
			print(clf.score(test, y_test))
		if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

# Draws the plot
def draw_plot(clf, test, y_test):
	plot_decision_regions(X=test.values, y=y_test.values,clf=clf, legend=2)
	plt.xlabel(test.columns[0], size=14)
	plt.ylabel(test.columns[1], size=14)
	Title = classifier_type + ' Decision Region Boundary'
	plt.title(Title, size=16)
	plt.show()

# Prints more detailed information about the classifier
def print_predictions(SVM_Gamma, SVM_C, clf, test, y_test):
	prediction = clf.predict(test)
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
	print("Gamma: ", SVM_Gamma, "\tC: ", SVM_C, "\t-:", nega, "\t0: ", zero, "\t+: ", posi, "\tTotal: ", nega+posi+zero, "\tRating: ", clf.score(test, y_test))
	if print_false_predictions:
		for q, w, e in zip(prediction, y_test, y_test.index):
			jokeid = joke_id.iloc[e]
			if q != w:
				print("\tPredicted: ", str(q), "\tActual: ", str(w), "\tPerformance: ", jokeid['PerformanceId'], "\tJoke: ", jokeid['JokeId'], "\t", list(joke.keys())[list(joke.values()).index(jokeid['JokeId'])])

# Helper function to hold out 1 performance as test data
def leave_one_perf_out_split(df, perf):
	train_data = df.loc[df.PerformanceId != perf]
	test_data = df.loc[df.PerformanceId == perf]
	train = train_data[features]
	test = test_data[features]
	y_train = train_data[validation]
	y_test = test_data[validation]
	return train, test, y_train, y_test

# Helper function for graphing
def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

###############
# Driver Code #
###############

# Read in Data
df = pd.read_csv('clean_comedy_data.csv', error_bad_lines=False, encoding='utf-8', delimiter=',')

Total = len(df)
Removed = 0

# Remove Silent Performance
if no_silent:
	Removed += (Total - len(df.loc[df.PerformanceId != 16]))
	df = df.loc[df.PerformanceId != 16]

# If Remove 0's on pitch
if remove_zeros:
	Removed += (Total - len(df.loc[df.Pitch != 0]))
	df = df.loc[df.Pitch != 0]

# Show how much data was pruned
if verbose:
	print("Removed ", Removed, " out of ", Total, ", ", (Total - Removed)/Total, " remaining.")

# Keep performance and joke id's
joke_id = df[joke_ids]

# If doing a two class validation, replace validation data
	# Combine 0's and 1's
if two_class == 1:
	df[validation] = df[validation].replace(0, 1)
	df[validation] = df[validation].replace(-1, 0)
	# Combine -1's and 0's
elif two_class == 2:
	df[validation] = df[validation].replace(-1, 0)

# Use selected normalization technique
if normalize == 'minmax':
	scaler = MinMaxScaler() 
	x = df[column_names_to_normalize].values
	x_scaled = scaler.fit_transform(x)
	df[column_names_to_normalize] = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = df.index)
if normalize == 'standard':
	scaler = StandardScaler()
	x = df[column_names_to_normalize].values
	x_scaled = scaler.fit_transform(x)
	df[column_names_to_normalize] = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = df.index)
# Per-performance normalization, worth a try but poor results
if normalize == 'per_minmax':
	for perf in range(18):
		scaler = MinMaxScaler()
		x_2 = df.loc[df['PerformanceId'] == perf]
		x = x_2[column_names_to_normalize].values
		x_scaled = scaler.fit_transform(x)
		x_scaled = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = df.loc[df['PerformanceId'] == perf].index)
		for name in column_names_to_normalize:
			df.loc[df['PerformanceId'] == perf, name] = x_scaled.loc[df['PerformanceId'] == perf, name]

# Use selected validation technique
	# Hold Out 20%
if validation_technique == 'ho20':
	overall = 0.0
	X = df[features]
	y = df[validation]
	for trial in range(0, num_trials):
		train, test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=R_State, stratify=y)
		if classifier_type == 'SVC':
			overall += svc_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'Tree':
			overall += tree_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'KNN':
			overall += knn_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'NN':
			overall += nn_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'NB':
			overall += nb_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'RF':
			overall += rf_classify(train, test, y_train, y_test, joke_id)
	print ("Overall Rating: ", overall/num_trials)
	# Leave One Performance Out
elif validation_technique == 'l1po':
	overall = 0.0;
	for perf in df.PerformanceId.unique():
		train, test, y_train, y_test = leave_one_perf_out_split(df, perf)
		if classifier_type == 'SVC':
			overall += svc_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'Tree':
			overall += tree_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'KNN':
			overall += knn_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'NN':
			overall += nn_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'NB':
			overall += nb_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'RF':
			overall += rf_classify(train, test, y_train, y_test, joke_id)
	if calibrate == 0:
		print ("Overall Rating: ", overall/len(df.PerformanceId.unique()))