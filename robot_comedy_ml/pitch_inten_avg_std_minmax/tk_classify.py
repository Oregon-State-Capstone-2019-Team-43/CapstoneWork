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
import matplotlib.pyplot as plt

joke = {"robot_name_joke_2.ogg.wav":1,"gdpr_joke.ogg.wav":2,"siri_backpropagate.ogg.wav":3,"silicon_valley_joke_pt1.wav":4,"silicon_valley_joke_pt2.wav":5,"rent_prices_oregon.ogg.wav":28,
"job_joke.ogg.wav":7,"inverse_kinematics_equations.ogg.wav":8,"family_joke.ogg.wav":9,"too_robotic_joke.ogg.wav":10,"c3po_joke.ogg.wav":11,"rosie_joke.ogg.wav":12,"wall-e_joke.ogg.wav":13,
"plastic_surgery_joke.ogg.wav":14,"bender_joke.ogg.wav":15,"for_all_my_robots_joke.ogg.wav":16,"white_people_joke.ogg.wav":17,"terminator_joke.ogg.wav":18,"baha_men_joke_oregon.ogg.wav":29,
"light_bulb_joke.ogg.wav":20,"robot_tinder_2.ogg.wav":30,"big_chips_joke.ogg.wav":22,"catfish_joke_2.ogg.wav":31,"ip_address_joke_2.ogg.wav":32,"encryption_joke.ogg.wav":25,
"robot_sexy_times.ogg.wav":26,"closing_take_jobs.ogg.wav":27,"congratulations_youve_won_joke.wav":33,"congratulations_im_feeling_lucky.wav":34,"power_cord_joke.wav":35,
"domain_name_joke.wav":36,"domain_name_dot_com.wav":37,".DS_Store":38,"420_joke.wav":39,"agt":40,"baha_men_india.wav":41,"baha_men_joke.ogg.wav":42,"baha_men_joke_sanfran.wav":43,
"boogie.ogg.wav":44,"catfish_joke.ogg.wav":45,"floppy_1.ogg.wav":46,"floppy_2.ogg.wav":47,"floppy_3.ogg.wav":48,"floppy_4.ogg.wav":49,"ganja_1.ogg.wav":50,"ganja_2.ogg.wav":51,
"ganja_3.ogg.wav":52,"hahahaha.wav":53,"happy_birthday.wav":54,"happy_birthday_taylor.wav":55,"hot_singles.ogg.wav":56,"human_date_1.ogg.wav":57,"human_date_2.ogg.wav":58,
"human_date_3.ogg.wav":59,"human_date_4.ogg.wav":60,"ip_address_joke.ogg.wav":61,"megaman.ogg.wav":62,"plane_0.ogg.wav":63,"plane_1.ogg.wav":64,"plane_2.ogg.wav":65,"plane_3.ogg.wav":66,
"plane_4.ogg.wav":67,"plane_5.ogg.wav":68,"rent_prices.ogg.wav":69,"robot_babies.ogg.wav":70,"robot_drugs.ogg.wav":71,"robot_name_joke.ogg.wav":72,"robot_name_joke_1.ogg.wav":73,
"robot_tinder.ogg.wav":74,"robotic.aiff":75,"robotic.aiff.wav":76,"self_driving_limo.ogg.wav":77,"selfie_drone.ogg.wav":78,"silence.wav":79,"silicon_valley_joke.ogg.wav":80,
"smoking_joke.ogg.wav":81,"software_update.ogg.wav":82,"speech_20180703052826649.ogg.wav":83,"stripper_joke.ogg.wav":84,"stripper_vagina.ogg.wav":85,"stripper_vagina_joke.ogg.wav":86,
"tags":87,"test_negative_tag.wav":88,"thank_you_nick.wav":89,"tinder_joke.ogg.wav":90,"training_data.ogg.wav":91,"transformers_1.ogg.wav":92,"transformers_2.ogg.wav":93,
"vibrator.ogg.wav":94,"vibrator_pt_2.ogg.wav":95,"walken_1.ogg.wav":96,"walken_2.ogg.wav":97,"washing_machine_1.ogg.wav":98,"washing_machine_2.ogg.wav":99,"washing_machine_3.ogg.wav":100,
"tags/catfish_joke_positive.ogg.wav":101, "tags/encryption_joke_positive_2.ogg.wav":102, "tags/family_joke_positive_2.ogg.wav":103, "tags/gdpr_joke_positive.ogg.wav":104,
"tags/inverse_kinematics_equations_positive_2.ogg.wav":105, "tags/plastic_surgery_joke_negative.ogg.wav":106, "tags/rent_prices_oregon_negative.ogg.wav":107, "tags/robot_joke_positive.wav":108,
"tags/robot_tinder_2_negative.ogg.wav":109, "tags/too_robotic_joke_positive_2.ogg.wav":110, "tags/white_people_joke_positive_2.ogg.wav":111, "tags/inverse_kinematics_equations_negative.ogg.wav":112,
"tags/power_cord_joke_negative.wav":113, "tags/killing_tag.wav":114, "tags/power_cord_joke_positive.wav":115, "tags/too_robotic_joke_negative.wav":116, "tags/white_people_joke_negative.ogg.wav":117,
"tags/robot_joke_negative_2.ogg.wav":118, "tags/robot_tinder_2_positive.ogg.wav":119, "tags/megaman_positive.ogg.wav":120, "tags/self_driving_limo_positive.ogg.wav":121,
"tags/robot_babies_positive.ogg.wav":122, "tags/robot_drugs_positive.ogg.wav":123, "tags/robot_tinder_2_positive.ogg.wav":124, "tags/software_update_positive.ogg.wav":125,
"tags/self_driving_limo_negative.ogg.wav":126, "tags/metal_ceiling_positive.ogg.wav":127, "tags/metal_ceiling_positive.ogg.wav":128, "tags/metal_ceiling_positive.ogg.wav":129,
"tags/catfish_joke_negative.ogg.wav":130, "tags/encryption_joke_negative_2.ogg.wav":131, "tags/gdpr_joke_negative.ogg.wav":132, "tags/killing_joke_negative.wav":133,
"tags/megaman_negative.ogg.wav":134, "tags/robot_drugs_negative.ogg.wav":135, "tags/software_update_negative.ogg.wav":136}

performance = {"2019-04-13 Cienna Nerdy Show at The Drake":0,"2019-04-18 Bombs Away Cafe":1,"2019-04-19 Singu-hilarity":2,"2019-04-22 Class Performance":3,
"2019-05-16 Bombs Away Cafe":4,"2019-06-19 Trek Theater":5,"2019-06-20 Bombs Away Cafe":6,"2019-08-15 Bombs Away Cafe":7,
"2019-08-23 Spectrum":8,"2019-09-05 Stand-up Science":9,"2019-09-06 RoboCom":10,"2019-09-19 Bombs Away Cafe":11,"2019-09-21 Laugh Track Town USA":12,
"2019-10-11 Singu-hilarity":13,"2019-11-29 Comedy the Musical":14,"2019-11-29 Crapshoot":15,"2019-12-06 Silent Background Recording":16,"2019-12-09 Singu-Hilarity in San Francisco":17}

# How much information to print
verbose = 1															# 0 = false, 1 = true, use for debugging
print_false_predictions = 0											# 0 = false, 1 = exactly as it says

# Data Pre-Processing
features = ['Intensity', 'IntensitySd'] # 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
two_class = 0 														# 0 = false, 1 = combine 0's and 1's, 2 = combine -1's and 0's
remove_zeros = 0
normalize = 0 														# 'minmax' or 'standard'
column_names_to_normalize = ['Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'] # 'Pitch', 'PitchSd', 'Intensity', 'IntensitySd', 'MinSound', 'MaxSound'
validation = 'HumanScorePostJokeOnly' 								# 'HumanScore' or 'HumanScorePostJokeOnly'
validation_technique = 'l1po' 										# 'ho20' or 'l1po'
R_State = 0 														# None or Integer, for hold out 20% validation
num_trials = 100
joke_ids = ['PerformanceId', 'JokeId'] 								# 'PerformanceId', 'JokeId'

# Classifier Types
classifier_type = 'KNN'												# 'SVC' or 'Tree' or 'KNN' or 'NN' or 'NB' or 'RF'

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

def rf_classify(train, test, y_train, y_test, joke_id):
	clf = RandomForestClassifier(n_estimators=100)
	clf.fit(train, y_train)
	if verbose:
		print('NN Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
	return clf.score(test, y_test)

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

def tree_classify(train, test, y_train, y_test, joke_id):
	clf = tree.DecisionTreeClassifier()
	clf.fit(train, y_train)
	if verbose:
		print('Tree Verbose: ', clf.score(test, y_test))
	else:
		print(clf.score(test, y_test))
	if draw_plt:
			draw_plot(clf, test, y_test)
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
	Title = classifier_type + ' Decision Region Boundary'
	plt.title(Title, size=16)
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
			jokeid = joke_id.iloc[e]
			if q != w:
				print("\tPredicted: ", str(q), "\tActual: ", str(w), "\tPerformance: ", jokeid['PerformanceId'], "\tJoke: ", jokeid['JokeId'], "\t", list(joke.keys())[list(joke.values()).index(jokeid['JokeId'])])

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
		elif classifier_type == 'NB':
			overall += nb_classify(train, test, y_train, y_test, joke_id)
		elif classifier_type == 'RF':
			overall += rf_classify(train, test, y_train, y_test, joke_id)
	if calibrate == 0:
		print ("Overall Rating: ", overall/18)