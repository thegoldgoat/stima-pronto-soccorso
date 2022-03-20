from threading import Lock
from unittest import result
import numpy as np
import matplotlib.pyplot as plt

results = {}
flag = 0
lock = Lock()

def run_single_simulation_decorator(func):
    
    def wrapper(*args):
    
        result = func(*args)        
        lock.acquire()
        global flag
        global results
        if flag == 0:
            for key, value in result.items():
                results[key] = np.array(value)
            flag = 1   
        else:
            for key, value in result.items():
                if key in list(results.keys()):
                    results[key] = np.append(results[key], value)
                else:
                    results[key] = np.array(value) 
        lock.release()
    
    return wrapper

def plot_occurrences(N):
        
    for key, arr in results.items():
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
    
        plt.stem(x_values, y_values, linefmt='blue', markerfmt=" ")
        plt.xlabel("Wating time")
        plt.ylabel("Occurrences")
        plt.title(f"Results for {N} simulations", fontsize=10)
        plt.suptitle(f"Patient {key}")
        plt.show()