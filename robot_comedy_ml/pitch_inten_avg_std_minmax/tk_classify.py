import matplotlib.pyplot as plt
import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt

# How much information to print
verbose = 1															# 0 = false, 1 = true, use for debugging
print_false_predictions = 0											# 0 = false, 1 = exactly as it says

# Data Pre-Processing
features = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'] # 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
two_class = 0 														# 0 = false, 1 = combine 0's and 1's, 2 = combine -1's and 0's
remove_zeros = 0
normalize = 'standard' 												# 'minmax' or 'standard'
column_names_to_normalize = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'] # 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
validation = 'HumanScorePostJokeOnly' 								# 'HumanScore' or 'HumanScorePostJokeOnly'
validation_technique = 'l1po' 										# 'ho20' or 'l1po'
R_State = 1 														# None or Integer, for hold out 20% validation
joke_ids = ['PerformanceId', 'JokeId'] 								# 'PerformanceId', 'JokeId'

# Classifier Types
classifier_type = 'KNN'												# 'SVC' or 'Tree' or 'KNN' or 'NN' or 'SVC_def'

# SVM Classifier Parameters
kernel = 'rbf' 														# 'linear' or 'poly' or 'rbf' or 'sigmoid' or 'precomputed'
SVM_C = 15000														# SVM regularization parameter
#	No Normalization	15000
#	minmax 				100
#	standard 			1000
SVM_Gamma = .00001 													# SVM regularization parameter
#	No Normalization	.00001
#	minmax 				.1
#	standard			.001

# Draw Plot only works if only 2 Features are selected. Selecting more features will result in error.
draw_plt = 0

calibrate = 0														# If calibration else destroy
SVM_C_range = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0] 			# SVM regularization parameters for calibration
SVM_Gamma_range = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0] 		# SVM regularization parameters for calibration

def SVC_def_classify(train, test, y_train, y_test, joke_id):
	clf = svm.SVC(gamma='scale')
	clf.fit(train, y_train)
	if verbose:
		print('SVC_def Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	return clf.score(test, y_test)

def nn_classify(train, test, y_train, y_test, joke_id):
	clf = MLPClassifier()
	clf.fit(train, y_train)
	if verbose:
		print('NN Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	return clf.score(test, y_test)

def knn_classify(train, test, y_train, y_test, joke_id):
	clf = KNeighborsClassifier()
	clf.fit(train, y_train)
	if verbose:
		print('KNN Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	return clf.score(test, y_test)

def tree_classify(train, test, y_train, y_test, joke_id):
	clf = tree.DecisionTreeClassifier()
	clf.fit(train, y_train)
	if verbose:
		print('Tree Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	return clf.score(test, y_test)

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

def draw_plot(clf, test, y_test):
	plot_decision_regions(X=test.values, y=y_test.values,clf=clf, legend=2)
	plt.xlabel(test.columns[0], size=14)
	plt.ylabel(test.columns[1], size=14)
	plt.title('SVM Decision Region Boundary', size=16)
	plt.show()

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
	print("Gamma: ", SVM_Gamma, "\tC: ", SVM_C, "\t-:", nega, "\t0: ", zero, "\t+: ", posi, "  \tRating: ", clf.score(test, y_test))
	if print_false_predictions:
		for q, w, e in zip(prediction, y_test, y_test.index):
			joke = joke_id.iloc[e]
			if q != w:
				print("\tPredicted: ", str(q), "\tActual: ", str(w), "\tPerformance: ", joke['PerformanceId'], "\tJoke: ", joke['JokeId'])

def leave_one_perf_out_split(df, perf):
	train_data = df.loc[df.PerformanceId != perf]
	test_data = df.loc[df.PerformanceId == perf]
	train = train_data[features]
	test = test_data[features]
	y_train = train_data[validation]
	y_test = test_data[validation]
	return train, test, y_train, y_test

##
#
# Driver Code
#
##

# Read in Data
df = pd.read_csv('clean_comedy_data.csv', error_bad_lines=False, encoding='utf-8', delimiter=',')

# If Remove 0's on pitch
if remove_zeros:
	df = df.loc[df.Pitch != 0]

# Keep performane and joke id's
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
	# Min-Max Normalization
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

# Use selected validation technique
	# Hold Out 20%
if validation_technique == 'ho20':
	X = df[features]
	y = df[validation]
	train, test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=R_State, stratify=y)
	if classifier_type == 'SVC':
		svc_classify(train, test, y_train, y_test, joke_id)
	elif classifier_type == 'Tree':
		tree_classify(train, test, y_train, y_test, joke_id)
	elif classifier_type == 'KNN':
		knn_classify(train, test, y_train, y_test, joke_id)
	elif classifier_type == 'NN':
		nn_classify(train, test, y_train, y_test, joke_id)
	elif classifier_type == 'SVC_def':
		SVC_def_classify(train, test, y_train, y_test, joke_id)
	# Leave One Performance Out
elif validation_technique == 'l1po':
	overall = 0.0;
	for perf in range(18):
		train, test, y_train, y_test = leave_one_perf_out_split(df, perf)
		if classifier_type == 'SVC':
			overall += svc_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'Tree':
			overall += tree_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'KNN':
			overall += knn_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'NN':
			overall += nn_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'SVC_def':
			overall += SVC_def_classify(train, test, y_train, y_test, joke_id)
	if calibrate == 0:
		print ("Overall Rating: ", overall/18)