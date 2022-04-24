import os
import csv
from pathlib import Path

from constants import ESIS, DAYS, HOUR_BINS


def aggregate(input_data):
    results = dict()

    for esi in ESIS:
        results[esi] = dict()

        for hour_bin in HOUR_BINS:
            results[esi][hour_bin] = 0

    for row in input_data:
        esi = row['esi']
        arrivalhour_bin = row['arrivalhour_bin']

        results[esi][arrivalhour_bin] += 1

    return results


def plot_results(results):
    OUTPUT_BASE_PATH = Path(__file__).parent / 'output'
    if not os.path.exists(OUTPUT_BASE_PATH):
        os.mkdir(OUTPUT_BASE_PATH)

    OUTPUT_DIR_PATH = OUTPUT_BASE_PATH / 'hour'

    if not os.path.exists(OUTPUT_DIR_PATH):
        os.mkdir(OUTPUT_DIR_PATH)

    import matplotlib.pyplot as plt

    for esi, days_dict in results.items():
        x_values = days_dict.keys()
        y_values = days_dict.values()

        plt.clf()
        plt.stem(x_values, y_values)
        plt.xlabel("Time intervals")
        plt.ylabel("Arrivals count")
        plt.title('Arrival count for ESI={}/5 ($N={}$)'.format(esi, sum(y_values)))

        plt.plot(x_values, y_values, color='blue')

        plt.savefig(OUTPUT_DIR_PATH / 'ESI-{}.png'.format(esi))


if __name__ == '__main__':
    with open(Path(__file__).parent / 'input' / 'input.csv') as csvfile:
        results = aggregate(csv.DictReader(csvfile))
        plot_results(results)
