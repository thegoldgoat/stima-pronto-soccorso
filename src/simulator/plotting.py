from threading import Lock
import numpy as np
import matplotlib.pyplot as plt


class Plotting:
    '''Class for plotting the results of the simulations'''
    
    def __init__(self):
        
        self.results = {}
        self.lock = Lock()
        self.flag = 0
        
    def collect_results(self, func, *args):
        '''This function collects the results of each simulation. The 
        results are added to self.results, which is a dictionary with patient
        IDs as keys and arrays of waiting times as values'''
        dict_of_result = func(*args)        
        self.lock.acquire()

        if self.flag == 0:
            for key, value in dict_of_result.items():
                self.results[key] = np.array(value)
            self.flag = 1   
        else:
            for key, value in dict_of_result.items():
                if key in list(self.results.keys()):
                    self.results[key] = np.append(self.results[key], value)
                else:
                    self.results[key] = np.array(value) 
        self.lock.release()
        
    def plot_occurrences(self, N):
        '''This function plots the number of occurrences for each waiting 
        time measured for a patient'''
        
        for key, arr in self.results.items():
            x_values = np.array([])
            y_values = np.array([])
            for value in arr:
                if value not in x_values:
                    x_values = np.append(x_values, value)
                    y_values = np.append(y_values, 1)
                else:
                    index = np.where(x_values == value)[0][0]
                    y_values[index] += 1
        
            mask = np.argsort(x_values)
            x_values = x_values[mask]
            y_values = y_values[mask]
            plt.clf()
            plt.stem(x_values, y_values, linefmt='blue', markerfmt=" ")
            plt.xlabel("Wating time")
            plt.ylabel("Occurrences")
            plt.title(f"Results for {N} simulations", fontsize=10)
            plt.suptitle(f"Patient {key}")
            plt.show()