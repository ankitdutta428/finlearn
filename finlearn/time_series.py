import yfinance as yf
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import datetime as dt
import matplotlib.pyplot as plt

class time_series:
    def __init__(self):
        self.model = None
    
    def download_and_preprocess(self, name, start, end):
        data = yf.download(name, start=start, end=end)
        data = data[['Close']]
        return data
    
    def create_dataframe(self, data, days):
        X, y = [], []
        for i in range(len(data) - days):
            X.append(data[i:(i + days), 0])
            y.append(data[i + days, 0])
        return np.array(X), np.array(y)
    
    def build(self, input_shape):
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50, return_sequences=False))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=25))
        self.model.add(Dense(units=1))
        
        self.model.compile(optimizer='adam', loss='mean_squared_error')
    
    def train(self, X_train, y_train, epochs=1, batch_size=1):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    
    def predict(self, data, days):
        X_test = []
        for i in range(days, len(data)):
            X_test.append(data[i-days:i, 0])
        
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        
        predictions = self.model.predict(X_test)
        
        return predictions
    
    def plot(self, actual, predictions):
        plt.figure(figsize=(16,8))
        plt.plot(actual.index, actual, label='Actual')
        plt.plot(actual.index[-len(predictions):], predictions.flatten(), label='Predicted')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
    
    def print_and_save_table(self, actual, predictions, filename='predictions.csv'):
        actual = actual[-len(predictions):].reset_index(drop=True)
        predictions = pd.Series(predictions.flatten(), name='Predicted')
        table = pd.concat([actual, predictions], axis=1)
        print(table)
        table.to_csv(filename, index=False)





#A testing example has been put up in the .tests/ts_test.py file, which can be run as an example and used to see how the code is getting executed.
