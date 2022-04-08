import json

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


INPUT_JSON_FILE = 'output/data.json'


def load_data():
    with open(INPUT_JSON_FILE, 'r') as input_file:
        return json.loads(input_file.read())


def plot_data(therapy_times):

    for esi, lenght_of_visits in therapy_times.items():

        sum_for_avg = 0
        total_occurrencies = 0
        for wait_time, occurrency in lenght_of_visits.items():
            sum_for_avg += int(wait_time) * occurrency
            total_occurrencies += occurrency

        avg = round(sum_for_avg / total_occurrencies)

        variance = 0
        for occurrency in lenght_of_visits.values():
            variance += pow(occurrency - avg, 2)

        variance /= total_occurrencies - 1

        x_values = [int(r) for r in lenght_of_visits.keys()]
        y_values = [r / total_occurrencies for r in lenght_of_visits.values()]

        plt.clf()
        plt.stem(x_values, y_values, linefmt='red', markerfmt=" ")
        plt.xlabel("Time waited")
        plt.ylabel("Occurrences")
        plt.title('Therapy time for patients with an ESI=' + str(esi))

        poisson_x_values = np.arange(1, max(x_values)+1, 1)
        poisson_y_values = norm.pdf(poisson_x_values, avg, variance)
        plt.plot(poisson_x_values, poisson_y_values, 'bs')

        plt.show()
        pass


def main():
    input_data = load_data()

    therapy_times = dict()
    for row in input_data:
        esi = row['esi']
        if esi not in therapy_times:
            therapy_times[esi] = {}

        esi_values = therapy_times[esi]
        length_of_visit = row['visitlength']
        if length_of_visit == '' or length_of_visit == -1:
            continue
        if length_of_visit not in esi_values:
            esi_values[length_of_visit] = 1
        else:
            esi_values[length_of_visit] += 1

    plot_data(therapy_times)


if __name__ == "__main__":
    main()
