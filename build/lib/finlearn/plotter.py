import plotly.graph_objects as go 
import pandas as pd
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import yfinance as yf

class plotter:
    def __init__(self):
        pass

    
    def lineplot(self,name,start,end,volume=False, type='daily', tracker='Close'):
        '''In this function, the following inputs would be needed which are 
        symbol(as per yfinance ticker symbol), start(give the start date in the "YYYY-MM-DD" format, the duration in days), 
        end (give the end date in the YYYY-MM-DD) and type which in this version are of 4 types: "daily", "weekly", "monthly", "yearly"'''
        
        #Find the ticker of the company name given by the user
        data = yf.download(name,start=start,end=end)
        #The data is getting downloaded after this line is getting executed

        if type=="weekly":
            data=data.resample('W').mean()
        elif type=="monthly":
            data=data.resample('M').mean()
        elif type=="yearly":
            data=data.resample('Y').mean()


        #Making subplots with an option to add volume graph as well
        fig = make_subplots(rows=2 if volume else 1, vertical_spacing=0.3, shared_xaxes=True)
        
        '''Now, we want to add the interactive line plot along with the option to add the volume plots! Just need to write True in that case.
        So the following pieces of code exactly do that part.'''
       
        if tracker=="Open":
          if data['Close'].iloc[-1] >= data['Close'].iloc[0]:
            line_color = 'green'
            shadow_color = 'lightgreen'
          else:
            line_color = 'red'
            shadow_color = 'magenta'
          fig.add_trace(go.Scatter(x=data.index, y=data['Open'], mode='lines+markers', name='Open Price Curve', line=dict(color=line_color, width=2)), row=1, col=1)
          #fig.add_trace(go.Scatter(x=data.index, y=data['Open'], mode='lines+markers', name='Open Price Curve', line=dict(color=shadow_color, width=12, dash='solid')), row=1, col=1)        
          fig.update_yaxes(title_text='Open Price', row=1, col=1)

          if volume:
              fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume"), row=2, col=1)
              fig.update_yaxes(title_text='Volume', row=2, col=1)

          fig.update_layout(title=f'{name} Open Price and Volume' if volume else f'{name} Open Price', xaxis_title='Date', height=600)
          fig.update_xaxes(rangeslider_visible=True, row=1, col=1)

          fig.show()

        else:
          if data['Close'].iloc[-1] >= data['Close'].iloc[0]:
            line_color = 'green'
            shadow_color = 'lightgreen'
          else:
            line_color = 'red'
            shadow_color = 'magenta'
          #fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines+markers', name='Close Price Curve', line=dict(color=shadow_color, width=12, dash='solid')), row=1, col=1)
          fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines+markers', name='Close Price Curve', line=dict(color=line_color, width=2)), row=1, col=1)
          fig.update_yaxes(title_text='Close Price', row=1, col=1)

          if volume:
              fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume"), row=2, col=1)
              fig.update_yaxes(title_text='Volume', row=2, col=1)

          fig.update_layout(title=f'{name} Close Price and Volume' if volume else f'{name} Close Price', xaxis_title='Date', height=600)
          fig.update_xaxes(rangeslider_visible=True, row=1, col=1)

          fig.show()
    
    def candlestick(self, name, start, end, volume=False, type='daily'):
      '''In this function, the following inputs would be needed which are 
      symbol(as per yfinance ticker symbol), start(give the start date in the "YYYY-MM-DD" format, the duration in days), 
      end (give the end date in the YYYY-MM-DD) and type which in this version are of 4 types: "daily", "weekly", "monthly", "yearly"'''
    
      # Downloading the yfinance data
      data = yf.download(name, start=start, end=end)
    
      # Resampling the data if necessary
      if type == 'daily':
        linewidth = 4
        pass  
      elif type == 'weekly':
        linewidth = 10
        data = data.resample('W').mean()
      elif type == 'monthly':
        linewidth = 25
        data = data.resample('M').mean()
      elif type == 'yearly':
        linewidth = 70
        data = data.resample('Y').mean()
    
      fig, ax = plt.subplots(figsize=(10, 6))
    
      # Plot vertical lines for high and low
      ax.vlines(data.index, data['Low'], data['High'], color='black', linewidth=1)
    
      # Plot the open and close prices as a line
      for i in range(len(data)):
          if data['Open'][i] > data['Close'][i]:
            ax.plot([data.index[i], data.index[i]], [data['Open'][i], data['Close'][i]], color='red', linewidth=linewidth)
          else:
            ax.plot([data.index[i], data.index[i]], [data['Open'][i], data['Close'][i]], color='green', linewidth=linewidth)
       
      if volume:
        ax2 = ax.twinx()
        ax2.fill_between(data.index, data['Volume'], color='gray', alpha=0.3)
        ax2.set_ylabel('Volume')
    
      # Formatting
      ax.set_xlabel('Date')
      ax.set_ylabel('Price')
      ax.set_title('Candlestick Chart for '+ name)
      ax.xaxis.set_major_locator(mdates.MonthLocator())
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
      plt.xticks(rotation=45)
      plt.tight_layout()
      plt.show()
      
    def heatmap(self, name, start, end):
      '''Downloading the data from yfinance and then using the sns.heatmap feature to generate the correlation between the various
      parameters of the stock price data'''
      
      data = yf.download(name, start=start, end=end)
      sns.heatmap(data.corr(), annot=True, cmap="crest")
      plt.show()
    

       
        

        