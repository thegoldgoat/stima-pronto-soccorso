import os
import csv
from pathlib import Path

from constants import ESIS, MONTHS


def aggregate(input_data):
    results = dict()

    for esi in ESIS:
        results[esi] = dict()

        for months in MONTHS:
            results[esi][months] = 0

    for row in input_data:
        esi = row['esi']
        arrivalmonth = row['arrivalmonth']

        results[esi][arrivalmonth] += 1

    return results


def plot_results(results):
    OUTPUT_BASE_PATH = Path(__file__).parent / 'output'
    if not os.path.exists(OUTPUT_BASE_PATH):
        os.mkdir(OUTPUT_BASE_PATH)

    OUTPUT_DIR_PATH = OUTPUT_BASE_PATH / 'months'

    if not os.path.exists(OUTPUT_DIR_PATH):
        os.mkdir(OUTPUT_DIR_PATH)

    import matplotlib.pyplot as plt

    for esi, months_dict in results.items():
        x_values = [month[:3] for month in months_dict.keys()]
        y_values = months_dict.values()

        plt.clf()
        plt.stem(x_values, y_values)
        plt.xlabel("Months")
        plt.ylabel("Arrivals count")
        plt.title('Arrival count for ESI={}/5 ($N={}$)'.format(esi, sum(y_values)))

        plt.plot(x_values, y_values, color='blue')

        plt.savefig(OUTPUT_DIR_PATH / 'ESI-{}.png'.format(esi))


if __name__ == '__main__':
    with open(Path(__file__).parent / 'input' / 'input.csv') as csvfile:
        results = aggregate(csv.DictReader(csvfile))
        plot_results(results)
