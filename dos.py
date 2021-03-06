# -*- coding: utf-8 -*-
"""DoS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ptJCmuB72eLYhmWSidoPsEQ9lE9qx9DE

# Denial of Service Attack Detection

A Denial of Service attack is an attempt to inject data into the network that is false, in order to damage the network. Machine Learning can be used to identify the attacks within the data.
Stages:
- Generate large data set of some kind with standard un-compromised readings
- Overwrite some readings with compromised, false readings
- Throw ML at the data
- Produce a large deep learning architecture to identify DoS

## Data Set

- Data set is a 14 bus smart grid network. 11 consumer lines taking readings (What we are concerned with). 8 lines where energy is being produced (Wind, Solar, Coal and Gas).
- Consumers take readings of 'LoadMinPower' which is the minimum power needed for a power supply to correctly function. Otherwise, the power supply will flicker, and may go off and on rapidly.
- DoS attack will inject completely random readings to attempt to damage the networks ability to interpret and cope with the data
- Injection of false data into the acquired LoadMinPower data set from https://zenodo.org/record/1220935 to mimic FDI attack
"""

#importing library for data
import pandas as pd
import numpy as np
import time

#read csv into dataframe
df = pd.read_csv(r'LoadMinPower.csv', sep=',', header=0)
df.head(5)

#Mean of each column
col_means = [np.array(df.get([f'{i}'])).mean() for i in range(1, 12)]
print(f" Means for all columns in the data set: \n{col_means}")

#Variance of each column
col_vars = [np.array(df.get([f'{i}'])).var() for i in range(1, 12)]
print(f" Variance for all columns in the data set: \n{col_vars}")

"""####Plot the distributions of some features"""

from matplotlib import pyplot as plt

y = df['1'].to_numpy()[:100]
y2 = df['5'].to_numpy()[:100]
y3 = df['11'].to_numpy()[:100]
x = np.arange(0, len(y))
plt.figure(figsize=(8,6))
plt.xlabel('Reading No.',fontsize=14)
plt.ylabel('Sensor Reading',fontsize=14)
plt.title('Sensor Readings Over Time',fontsize=16)
plt.plot(x,y,label='Sensor 1')
plt.plot(y2, label = 'Sensor 5')
plt.plot(y3, label = 'Sensor 11')
plt.legend(loc='upper right')
#plt.savefig('LoadMinSensor1,5,11first100nonDoSorFDIA')
plt.show()

"""## Denial of Service Data Injection
- Injecting False data into the data set to mimic a DoS
- Then convert to appropriate format for ML
- Also need to generate labels. (1 for false reading, 0 for 'true').
- Do not need to append normal noises as the data set is real, not artificially generated
- Append random readings with completely random values between a range and append a 1 label when doing so

## Data Mining
- injecting false readings randomly
- creation of labels
"""

#to avoid tampering of original df
initial_data = df.copy()

#11 false readings to mimic a false reading injection
np.random.randint(-10, 10, 11)

#Performing the false data injection
t0 = time.perf_counter()   #timing

features = []
labels = []
#looping through each row in df
for index, values in initial_data.iterrows():
  #if statement to inject half of the data
  if np.random.random() < 0.5:
    #generating a false reading with 11 random values
    false_reading = np.random.randint(-10, 10, 11)
    #append 1 to label of row as this network reading is a false reading
    labels.append(1)
    #append new injected values to features as list
    features.append(false_reading)
    #setting row equal to new injected row in dataframe
    #initial_data.at[index] = false_reading
  else:
    #append normal values and 0 label as no injection takes place
    features.append(list(values[2:]))
    labels.append(0)

t1 = time.perf_counter()   #timing

#Features and Labels into a numpy array for ML
features = np.array(features)
labels = np.array(labels)

print(f"--------DATA-INJECTED-------- (In {t1-t0} Seconds)")

#mean and variance of sensor 1, 5 and 11 after DoS
y = np.array([i[0] for i in features][:100])
y2 = np.array([i[4] for i in features][:100])
y3 = np.array([i[10] for i in features][:100])
print(f" Sensor 1 Mean: {y.mean()}, Variance: {y.var()}")
print(f" Sensor 2 Mean: {y2.mean()}, Variance: {y2.var()}")
print(f" Sensor 3 Mean: {y3.mean()}, Variance: {y3.var()}")

#plotting distributions after DoS
y = [i[0] for i in features][:100]
y2 = [i[4] for i in features][:100]
y3 = [i[10] for i in features][:100]
x = np.arange(0, len(y))
plt.figure(figsize=(8,6))
plt.xlabel('Reading No.',fontsize=14)
plt.ylabel('Sensor Reading',fontsize=14)
plt.title('Sensor Readings After DoS',fontsize=16)
plt.plot(x,y,label='Sensor 1')
plt.plot(y2, label = 'Sensor 5')
plt.plot(y3, label = 'Sensor 11')
plt.legend(loc='upper right')
#plt.savefig('LoadMinSensor1,5,11afterDoS')
plt.show()

# #Storing features and labels as csv
# #"""
# np.savetxt('min_features.csv', features, delimiter=',')
# np.savetxt('min_labels.csv', labels, delimiter=',')
# min_features = np.array(pd.read_csv('min_features.csv'))
# min_labels = np.array(pd.read_csv('min_labels.csv')).astype(int)
# #"""

"""## Train and Test Data"""

#sklearn library for machine learning and data selection
from sklearn.model_selection import train_test_split

#train test split to split data into training and test data
X_train, X_test, y_train, y_test = train_test_split(min_features, min_labels, test_size=0.3, random_state=1)

"""## Decision Tree Classifier"""

#import decision tree classifier
from sklearn.tree import DecisionTreeClassifier
#metric for accuracy score of classifications
from sklearn.metrics import accuracy_score

#decision tree initialized
tree = DecisionTreeClassifier()
#fitting training data
tree.fit(X_train, y_train.ravel())
#getting predictions
tree_preds = tree.predict(X_test)
#accuracy score of Decision Tree Classifier
print(f"Accuracy of Decision Tree: {round(accuracy_score(y_test, tree_preds)*100)}")

"""## KNN Nearest Neighbour Classifier"""

#Import KNN from sklearn
from sklearn.neighbors import KNeighborsClassifier

#KNN classifier
knn_model = KNeighborsClassifier()
#fitting training data
knn_model.fit(X_train, y_train.ravel())
#getting predictions of KNN
knn_predictions = knn_model.predict(X_test)
#Accuracy of KNN
print(f"Accuracy of KNN: {round(accuracy_score(y_test, knn_predictions)*100)}%")

"""## SVM Classifier """

#SVM import
from sklearn.svm import SVC

#Support Vector Machine Implementation
svm = SVC()
#fitting training data
svm.fit(X_train, y_train.ravel())
#predictions of SVM
svm_predictions = svm.predict(X_test)
#accuracy score of SVM
print(f"Accuracy of SVM: {round(accuracy_score(y_test, svm_predictions)*100)}%")

#visualizing the support vectors
support_vectors = svm.support_vectors_
plt.scatter(X_train[:,0], X_train[:,1])
plt.scatter(support_vectors[:,0], support_vectors[:,1], color='red')
plt.figure(figsize=(8,6))
#plt.title('Support Vectors')
plt.show()

"""## Random Forest Classifier using SKLearn"""

#libraries
from sklearn.ensemble import RandomForestClassifier

#Model initialized
rf_model = RandomForestClassifier(200)
#fitting training data, 'ravel()' to get in flat matrix form
rf_model.fit(X_train, y_train.ravel())
#getting rf predictions of test data
rf_predictions = rf_model.predict(X_test)
#getting accuracy score of predictions
print(f"Accuracy of Random Forest: {round(accuracy_score(y_test, rf_predictions)*100)}%")

"""## XGBoost Classifier"""

#xgboost library
from xgboost import XGBClassifier

#XGBoost classifier
x_model = XGBClassifier()
#fitting training data
x_model.fit(X_train, y_train.ravel())
#getting predictions of XGBoost
x_predictions = x_model.predict(X_test)
#Accuracy of XGBoost
print(f"Accuracy of XGBoost: {round(accuracy_score(y_test, x_predictions)*100)}%")

"""## Convolutional Neural Network Model Creation using Keras"""

#keras for network implementation
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Conv1D, Dropout, MaxPool1D, Flatten, Dense, BatchNormalization, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping

#reshape train data to fit into CNN
X_train_cnn = X_train.copy().reshape(len(X_train), 11, 1)

#callbacks to avoid overfitting
callback = EarlyStopping(monitor='accuracy', patience=4)

"""### CNN1 - achieved 100%"""

#Building the model
cnn1 = Sequential()
cnn1.add(Conv1D(filters=100, kernel_size=3, strides=1, activation='relu', input_shape=(11,1)))
cnn1.add(Conv1D(filters=200, kernel_size=3, strides=1, padding = 'same', activation='relu'))
cnn1.add(BatchNormalization())
cnn1.add(LeakyReLU())
cnn1.add(Dropout(0.5))
cnn1.add(Conv1D(filters=100, kernel_size=3, strides=1, activation='relu'))
cnn1.add(Dropout(0.5))
cnn1.add(Conv1D(filters=50, kernel_size=3, strides=1, padding = 'same', activation='relu'))
cnn1.add(Dropout(0.5))
cnn1.add(Conv1D(filters=100, kernel_size=3, strides=1, activation='relu'))
#cnn1.add(BatchNormalization())
#cnn1.add(LeakyReLU())
cnn1.add(Flatten())
cnn1.add(Dense(100, activation='relu'))
cnn1.add(Dense(1, activation='sigmoid'))
print(cnn1.summary())
cnn1.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Training the model
cnn1.fit(X_train_cnn, y_train, epochs=5, batch_size=500, validation_split=0.2, verbose=2)

"""### CNN2 - achieved 100%"""

#Building the model
cnn2 = Sequential()
cnn2.add(Conv1D(filters=100, kernel_size=3, strides=1, activation='relu', input_shape=(11,1)))
cnn2.add(Dropout(0.5))
cnn2.add(BatchNormalization())
cnn2.add(LeakyReLU())
cnn2.add(Conv1D(filters=50, kernel_size=3, strides=1, padding = 'same', activation='relu'))
cnn2.add(Dropout(0.5))
cnn2.add(Flatten())
cnn2.add(Dense(100, activation='relu'))
cnn2.add(Dense(1, activation='sigmoid'))
print(cnn2.summary())
cnn2.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Training the model
cnn2.fit(X_train_cnn, y_train, epochs=5, batch_size=500, validation_split=0.2, verbose=0)

"""### CNN3 - achieved 100%"""

#Building the model
cnn3 = Sequential()
cnn3.add(Conv1D(filters=16, kernel_size=2, strides=1, activation='relu', input_shape=(11,1)))
cnn3.add(Dropout(0.5))
cnn3.add(Conv1D(filters=32, kernel_size=2, strides=1, activation='relu', input_shape=(11,1)))
cnn3.add(Flatten())
cnn3.add(Dense(20, activation='relu'))
cnn3.add(Dense(1, activation='sigmoid'))
print(cnn3.summary())
cnn3.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Training the model
cnn3.fit(X_train_cnn, y_train, epochs=5, batch_size=500, validation_split=0.2, verbose=0)

"""## CNN Model Accuracy Scores"""

#Reshape test data for scores
X1_test = X_test.copy().reshape(len(X_test), 11, 1)

"""###### CNN1"""

#Predictions with CNN
cnn1_preds = cnn1.evaluate(X1_test, y_test, verbose=0)
#accuracy of CNN1
print(f"Accuracy of CNN1: {round(cnn1_preds[1]*100)}%")

"""###### CNN2"""

#Predictions with CNN
cnn2_preds = cnn2.evaluate(X1_test, y_test, verbose=0)
#accuracy of CNN2
print(f"Accuracy of CNN2: {round(cnn2_preds[1]*100)}%")

X1_test.shape

y_test.shape

"""###### CNN3"""

#Predictions with CNN
cnn3_preds = cnn3.evaluate(X1_test, y_test, verbose=0)
#accuracy of CNN2
print(f"Accuracy of CNN3: {round(cnn3_preds[1]*100)}%")

"""####Testing on Max Supply"""

df = pd.read_csv(r'LoadMaxPower.csv')

df.head(2)

"""######Injecting DoS Into test data"""

#Performing the false data injection
t0 = time.perf_counter()   #timing

features = []
labels = []
#looping through each row in df
for index, values in df.iterrows():
  #if statement to inject half of the data
  if np.random.random() < 0.5:
    #generating a false reading with 11 random values
    false_reading = np.random.randint(999, 1001, 11)
    #append 1 to label of row as this network reading is a false reading
    labels.append(1)
    #append new injected values to features as list
    features.append(false_reading)
    #setting row equal to new injected row in dataframe
    #initial_data.at[index] = false_reading
  else:
    #append normal values and 0 label as no injection takes place
    features.append(list(values[2:]))
    labels.append(0)

t1 = time.perf_counter()   #timing

#Features and Labels into a numpy array for ML
features = np.array(features)
labels = np.array(labels)

print(f"--------DATA-INJECTED-------- (In {t1-t0} Seconds)")

#Storing max features and labels as csv
#"""
np.savetxt('max_features.csv', features, delimiter=',')
np.savetxt('max_labels.csv', labels, delimiter=',')
max_features = np.array(pd.read_csv('max_features.csv'))
max_labels = np.array(pd.read_csv('max_labels.csv')).astype(int)
#"""

"""####Getting the models predictions and plotting confusion matrices"""

#Decision Tree predictions
dt_pred = tree.predict(max_features)
print(f" Decision Tree: {accuracy_score(max_labels, dt_pred)}")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, dt_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#KNN
knn_pred = knn_model.predict(max_features)
print(f" KNN: {accuracy_score(max_labels, knn_pred)}")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, knn_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#SVM
svm_pred = svm.predict(max_features)
print(f" SVM: {accuracy_score(max_labels, svm_pred)}")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, svm_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#Random Forest
rf_pred = rf_model.predict(max_features)
print(f" Random Forest: {accuracy_score(max_labels, rf_pred)}")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, rf_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#XGBoost
xgb_pred = x_model.predict(max_features)
print(f" XGBoost: {accuracy_score(max_labels, xgb_pred)}")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, xgb_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#reshape features for CNN preds
max_features_re = max_features.copy().reshape(len(max_features), 11, 1)

#Predictions with CNN1
cnn1_pred = cnn1.predict(max_features_re)
cnn1_pred = np.array([0 if i[0] < 0.5 else 1 for i in cnn1_pred])
#accuracy of CNN1
print(f"Accuracy of CNN1: {accuracy_score(max_labels, cnn1_pred)}%")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, cnn1_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#Predictions with CNN2
cnn2_pred = cnn2.predict(max_features_re)
cnn2_pred = np.array([0 if i[0] < 0.5 else 1 for i in cnn2_pred])
#accuracy of CNN2
print(f"Accuracy of CNN2: {accuracy_score(max_labels, cnn2_pred)}%")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, cnn2_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

#Predictions with CNN3
cnn3_pred = cnn3.predict(max_features_re)
cnn3_pred = np.array([0 if i[0] < 0.5 else 1 for i in cnn3_pred])
#accuracy of CNN3
print(f"Accuracy of CNN3: {accuracy_score(max_labels, cnn3_pred)}%")
#Confusion Matrix
tn, fp, fn, tp = confusion_matrix(max_labels, cnn3_pred).ravel()
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

