import pandas as pd 
import numpy as np 

class check_val:
    def __init__(self):
        pass
    
    def check_accuracy_range(self, filename, x):
        if not (x >= 0 and x <= 100):
            print("Please give a number in the range between 0 and 100")
            return
        
        data = pd.read_csv(filename)
        data['H_accept'] = np.where(abs(data['Predicted'] - data['Close']) / data['Close'] <= x / 100, 1, 0)
        
        correct_predictions = data['H_accept'].sum()
        total_predictions = len(data['Close'])
        
        accuracy = correct_predictions / total_predictions
        
        print("The accuracy for the mentioned range of error level is", accuracy)


