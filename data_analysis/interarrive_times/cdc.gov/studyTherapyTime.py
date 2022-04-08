import json
import os
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


INPUT_JSON_FILE = 'output/data.json'


def esi_to_text(esi):
    esi_map = {
        '-9': 'Blank',
        '-8': 'Unknown',
        '0': 'Triage by Emergency Service Areas',
        '1': 'Immediate_1-5',
        '2': 'Emergent_2-5',
        '3': 'Urgent_3-5',
        '4': 'Semi-urgent_4-5',
        '5': 'Nonurgent_5-5',
        '7': 'No triage by Emergency Service Areas'
    }

    if esi not in esi_map:
        raise Exception("Invalid esi: " + str(esi))

    return esi_map[esi]


def load_data():
    with open(INPUT_JSON_FILE, 'r') as input_file:
        return json.loads(input_file.read())


def plot_data(therapy_times):

    for esi, lenght_of_visits in therapy_times.items():
        esi_text = esi_to_text(esi)
        sum_for_avg = 0
        total_occurrencies = 0
        for wait_time, occurrency in lenght_of_visits.items():
            sum_for_avg += int(wait_time) * occurrency
            total_occurrencies += occurrency

        avg = round(sum_for_avg / total_occurrencies)

        variance = 0
        for occurrency in lenght_of_visits.values():
            variance += pow(occurrency - avg, 2)

        variance = sqrt(variance / total_occurrencies)

        x_values = [int(r) for r in lenght_of_visits.keys()]
        y_values = [r / total_occurrencies for r in lenght_of_visits.values()]

        plt.clf()
        plt.stem(x_values, y_values, linefmt='red', markerfmt=" ")
        plt.xlabel("Time waited [Minutes]")
        plt.ylabel("Occurrences [%]")
        plt.title('Visit time with ESI={}\n ($N={}$) $\mu={}$ $\sigma={}$'
                  .format(esi_text, total_occurrencies, avg, variance))

        normal_x_values = np.arange(1, max(x_values)+1, 1)
        normal_y_values = norm.pdf(normal_x_values, avg, variance)
        plt.plot(normal_x_values, normal_y_values, color='blue')

        plt.savefig('output/therapy/esi-{}.png'.format(esi_text))


def main():
    input_data = load_data()

    if not os.path.exists("output"):
        os.mkdir("output")

    if not os.path.exists("output/therapy"):
        os.mkdir("output/therapy")

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
