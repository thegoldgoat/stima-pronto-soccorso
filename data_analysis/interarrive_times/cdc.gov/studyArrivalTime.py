from functools import total_ordering
import json

import os

import matplotlib.pyplot as plt

from scipy.stats import poisson
import numpy as np

INPUT_JSON_FILE = 'output/data.json'

"""
Lo studio conta quanti arrivi ci sono in una determinata ora (o in un periodo di tempo) per ognuno dei giorni*.

* i giorni sono presi a gruppi di giorno della settimana nel mese poichè non ci sono informazioni relative al singolo giorno.
"""

esi_values = [1, 2, 3, 4, 5]  # 1 urgent, 5 non urgent
total_mse = 0


def meanSquaredError(real_x_values: list, real_y_values: list, theoric_x_values: list, theoric_y_values: list):
    real_values = {}
    theoric_values = {}

    # order the real values using a dict (becuase I have to keep the match between the x and y lists)
    index = 0
    for real_x_value in real_x_values:
        # * total_occurrences  # denormalize with total_occurrences
        real_values[real_x_value] = real_y_values[index]
        index += 1

    # Fill the dict with zeros where I don't have values
    for i in range(1, max(real_x_values)+1):
        if not i in real_values:
            real_values[i] = 0

    # order the theoric values using a dict (should be already ordered tbh)
    index = 0
    for theoric_x_value in theoric_x_values:
        # * total_occurrences  # denormalize with total_occurrences
        theoric_values[theoric_x_value] = theoric_y_values[index]
        index += 1

    if len(real_values) != len(theoric_values):
        raise Exception(
            "Real distribution and Theoric distribution have the same number of x values")

    # MSE = (square of the difference between the y values at the same x value)^2/n
    squaredSum = 0
    for i in range(1, len(real_values)+1):
        squaredSum += pow(real_values[i] - theoric_values[i], 2)

    return round(squaredSum/len(real_values), 6)


def load():
    """ Load 5 years data """
    with open(INPUT_JSON_FILE, 'r') as infile:
        return json.loads(infile.read())


def analyze(datas, esi, hour, hour_interval=0):
    arrivals = {}

    # For each arrival: check the day he's arrived and increment the number of patients that arrived in the emergency room
    # the same day at the same hour
    # Here I don't have all the day information (dd/mm/yyyy) but only the month and the day of the week so
    #  with "a day" I mean the same weekday of that month

    # Here I count on each day, at that hour, how many people arrived
    for data in datas:
        try:
            if int(data['arrivalhour']) >= hour and int(data['arrivalhour']) < hour + hour_interval and int(data['esi']) == esi:
                key = str(data['year']) + "." + data['arrivalmonth'] + "." + \
                    data['arrivalday'] + "." + data['arrivalhour']
                if key in arrivals:
                    arrivals[key] += 1
                else:
                    arrivals[key] = 1
        except Exception as e:
            pass

    # Now I count how much days I have with a specific number of arrivals
    arrival_distribution = {}
    for key, value in arrivals.items():
        if value in arrival_distribution:
            arrival_distribution[value] += 1
        else:
            arrival_distribution[value] = 1

    # Prepare data for plotting
    x_values = []
    y_values = []

    for key, value in arrival_distribution.items():
        x_values.append(key)
        y_values.append(value)

    if len(x_values):
        plot(x_values, y_values, esi, hour, hour_interval)


def plot(x_values, y_values, esi, hour, hour_interval):
    """ Plot the the values with a Poisson whose rate is the values average """
    global total_mse

    avg = 0
    total_occurrences = 0
    sample_number = 0

    # Calculate the average and the sum of all values on y axis to normalize the plot
    for i in range(0, len(x_values)):
        sample_number += x_values[i] * y_values[i]
        total_occurrences += y_values[i]
    avg = round(sample_number/total_occurrences, 3)

    # normalize y_values with 1
    for i in range(0, len(y_values)):
        y_values[i] = y_values[i]/total_occurrences

    # plot my values
    plt.clf()
    plt.stem(x_values, y_values, linefmt='red', markerfmt=" ")
    plt.xlabel("Arrival number")
    plt.ylabel("Occurrences %")

    # I also plot a Poisson with the rate = average previously calculated
    poisson_x_values = np.arange(1, max(x_values)+1, 1)
    poisson_y_values = poisson.pmf(poisson_x_values, mu=avg)
    plt.plot(poisson_x_values, poisson_y_values, 'bs')

    # get the mse (with Poisson as theoric distribution)
    mse = meanSquaredError(
        x_values, y_values, poisson_x_values, poisson_y_values)
    total_mse += mse

    title = "Arrivals between {}:00 and {}:00 with ESI {}\n".format(
        hour, hour+hour_interval, esi)
    title = title + \
        "Sample number: {}    Rate: {}     MSE: {}".format(
            sample_number, avg, mse)
    plt.title(title)

    BASE_BASE_OUTPUT = "output"
    if not os.path.exists(BASE_BASE_OUTPUT):
        os.mkdir(BASE_BASE_OUTPUT)

    BASE_OUTPUT_FOLDER = BASE_BASE_OUTPUT + "/interarrive"

    if not os.path.exists(BASE_OUTPUT_FOLDER):
        os.mkdir(BASE_OUTPUT_FOLDER)

    GROUP_FOLDER = BASE_OUTPUT_FOLDER + \
        "/group_by_{}_hours".format(f'{hour_interval:02}')

    if not os.path.exists(GROUP_FOLDER):
        os.mkdir(GROUP_FOLDER)

    plt.savefig(
        GROUP_FOLDER + '/esi{}_h_{}.png'.format(esi, f'{hour:02}'))


if __name__ == "__main__":
    datas = load()
    hour_intervals = [1, 2, 3, 4, 6, 8, 12, 24]
    for hour_interval in hour_intervals:
        for esi in esi_values:
            for hour in range(0, 24, hour_interval):
                analyze(datas, esi, hour, hour_interval)
    # print("Total MSE:",total_mse)

"""
    Data format in exportEsiTime.json
        data = {
            'year': None,
            'esi': None,
            'arrivalmonth': None,
            'arrivalday': None,
            'arrivalhour': None,
            'arrivalminute': None,
        }
"""
