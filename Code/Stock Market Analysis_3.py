#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 18:33:41 2017

@author: KJ
"""

# Recurrent Neural Network with 3 parameters



# Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the training set
dataset_train = pd.read_csv('train.csv')
dataset_train.drop(dataset_train.index[[0]],inplace = True)
training_set = dataset_train.iloc[:, 1:4].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(60, 1260):
    X_train.append(training_set_scaled[i-60:i, 0:])
    y_train.append(training_set_scaled[i, 0:])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 3))



# Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 3)))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 3))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)



# Making the predictions and visualising the results

# Getting the real stock price of 2017
dataset_test = pd.read_csv('test.csv')
real_stock_price = dataset_test.iloc[:, 3:4].values

# Getting the predicted stock price of 2017
dataset_total = pd.concat((dataset_train['open'], dataset_test['open']), axis = 0)
d1 = pd.concat((dataset_train['close'], dataset_test['close']), axis = 0)
d2 = pd.concat((dataset_train['volume'], dataset_test['volume']), axis = 0)
d3 = pd.concat((d1, d2), axis = 1)
d4 = pd.concat((dataset_train['open'], dataset_test['open']), axis = 0)
d5 = pd.concat((d3,d4), axis = 1)
dataset_total = pd.concat((dataset_train['open'], d3), axis = 1)



inputs = d5[len(d5) - len(dataset_test) - 60:][:].values
inputs = inputs.reshape(-1,1)
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
inputs = sc.fit_transform(inputs)
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0:])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 3))
predicted_stock_price = regressor.predict(X_test)

predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Visualising the results
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price[2], color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()
