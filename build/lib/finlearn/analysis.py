import pandas as pd
import numpy as np
import yfinance as yf
#from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

class TechnicalIndicators:
    def __init__(self, stock_symbol, start_date, end_date):
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date  
        self.data = None
    
    def load_data(self):
        self.data = yf.download(self.stock_symbol, start=self.start_date, end=self.end_date)
        print("Data loaded")
    
    def calculate_bollinger_bands(self, window=20, no_of_std=2):
        self.data['MA20'] = self.data['Close'].rolling(window=window).mean()
        self.data['BB_Upper'] = self.data['MA20'] + (self.data['Close'].rolling(window=window).std() * no_of_std)
        self.data['BB_Lower'] = self.data['MA20'] - (self.data['Close'].rolling(window=window).std() * no_of_std)
    
    def plot_bollinger_bands(self):
        self.calculate_bollinger_bands()
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['MA20'], mode='lines', name='20-Day MA', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['BB_Upper'], mode='lines', name='Upper Bollinger Band', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['BB_Lower'], mode='lines', name='Lower Bollinger Band', line=dict(dash='dash')))

        fig.update_layout(title=f'{self.stock_symbol} Price with Bollinger Bands', xaxis_title='Date', yaxis_title='Price', template='plotly_dark')
        fig.show()

    def calculate_rsi(self, window=14):
        delta = self.data['Close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
    
    def plot_rsi(self):
        self.calculate_rsi()
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['RSI'], mode='lines', name='RSI'))
        fig.add_trace(go.Scatter(x=self.data.index, y=[30]*len(self.data), mode='lines', name='Lower Threshold (30)', line=dict(dash='dash', color='red')))
        fig.add_trace(go.Scatter(x=self.data.index, y=[70]*len(self.data), mode='lines', name='Upper Threshold (70)', line=dict(dash='dash', color='red')))

        fig.update_layout(title='Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI', template='plotly_dark')
        fig.show()

    def calculate_macd(self, slow=26, fast=12, signal=9):
        self.data['EMA12'] = self.data['Close'].ewm(span=fast, adjust=False).mean()
        self.data['EMA26'] = self.data['Close'].ewm(span=slow, adjust=False).mean()
        self.data['MACD'] = self.data['EMA12'] - self.data['EMA26']
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=signal, adjust=False).mean()
    
    def plot_macd(self):
        self.calculate_macd()
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['MACD'], mode='lines', name='MACD'))
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Signal_Line'], mode='lines', name='Signal Line', line=dict(dash='dash')))

        fig.update_layout(title='Moving Average Convergence Divergence (MACD)', xaxis_title='Date', yaxis_title='MACD', template='plotly_dark')
        fig.show()

# Example usage
if __name__ == "__main__":
    tech_indicators = TechnicalIndicators(stock_symbol='AAPL', start_date='2024-01-01', end_date='2024-03-01')
    tech_indicators.load_data()
    tech_indicators.plot_bollinger_bands()
    tech_indicators.plot_rsi()
    tech_indicators.plot_macd()
