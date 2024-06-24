This is the user guide for using the finlearn library developed by Ankit Dutta, for the analysis of stock markets using high end deep learning and time series algorithms.

The finlearn package consists of several versions:
As of the latest version released on the 24th June, 2024 ...(finlearn 0.0.46) the finlearn package consists of the following functions:
    
i) plotter
ii) time_series
iii) check
iv) analysis

The plotter function enables the user to plot the closing/opening prices of the stock with time. There can be two types of plots which can be made: candlestick plot or normal line plot but interactive plot which enables the user to have a deeper analysis of the equity.

The time_series function uses the LSTM neural network function to predict the prices of the stock. The model predicts almost accurately if the error margin is taken at about 9-10%. Further time-series models will be added to the list with newer versions of finlearn.

The analysis code brings the new features of plotting and calculating the bollinger bands, rsi and macd. This will help the users for further 
financial analysis of the stock.

An example code has been attached below for the ease of implementing the function of the library.

```
from finlearn import time_series
import pandas as pd
import numpy as np 

ts = time_series()
data = ts.download_and_preprocess('AAPL', '2010-01-01', '2020-01-01')
data = data.values

days = 60  # User-defined number of days
X, y = ts.create_sequences(data, days)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

ts.build(input_shape=(days, 1))
ts.train(X, y, epochs=1)

predictions = ts.predict(data, days)
ts.plot_predictions(pd.DataFrame(data[days:], columns=['Close']), predictions)
ts.print_and_save_table(pd.DataFrame(data[days:], columns=['Close']), predictions)
```



The check function does an accuracy check on the predictions made by various models with various levels of error.
An example usage of the code has been attached below for the ease of implementing the function:

```
checker = check_val()
checker.check_accuracy_range('predictions.csv', 5)  # Example: 5% error margin
```
