import os
import csv
from pathlib import Path

from constants import ESIS, DAYS, HOUR_BINS


def aggregate(input_data):
    results = dict()
    arrival_count = dict()

    for esi in ESIS:
        arrival_count[esi] = 0
        results[esi] = dict()

        for day in DAYS:
            results[esi][day] = dict()

            for hour_bin in HOUR_BINS:
                results[esi][day][hour_bin] = 0

    for row in input_data:
        esi = row['esi']
        arrivalday = row['arrivalday']
        arrivalhour_bin = row['arrivalhour_bin']

        arrival_count[esi] += 1
        results[esi][arrivalday][arrivalhour_bin] += 1

    average_arrive_count_in_hour_interval = dict()

    for esi, arr_count in arrival_count.items():
        average_arrive_count_in_hour_interval[esi] = arr_count / \
            (len(DAYS) * len(HOUR_BINS))

    for esi, days_dict in results.items():
        for hours_dict in days_dict.values():
            for hour_interval_keys in hours_dict.keys():
                hours_dict[hour_interval_keys] -= average_arrive_count_in_hour_interval[esi]

    return results


def plot_results(results):
    OUTPUT_BASE_PATH = Path(__file__).parent / 'output'
    if not os.path.exists(OUTPUT_BASE_PATH):
        os.mkdir(OUTPUT_BASE_PATH)

    OUTPUT_DIR_PATH = OUTPUT_BASE_PATH / 'hour_in_week'

    if not os.path.exists(OUTPUT_DIR_PATH):
        os.mkdir(OUTPUT_DIR_PATH)

    import matplotlib.pyplot as plt

    bar_count = len(HOUR_BINS)
    bar_group_width = 0.6
    single_bar_width = bar_group_width / bar_count
    x_values_bar_base = [i for i in range(len(DAYS))]

    for esi, days_dict in results.items():

        plt.clf()

        fig, ax = plt.subplots(figsize=(40, 20))
        rects = []

        for i in range(len(HOUR_BINS)):
            x = [v + i * single_bar_width for v in x_values_bar_base]
            y = [day_dict[HOUR_BINS[i]] for day_dict in days_dict.values()]

            rects.append(
                ax.bar(x, y, single_bar_width, label=HOUR_BINS[i]))

        ax.set_ylabel('Number of arrivals', fontsize=20)
        ax.set_title(
            f'Arrivals divided by day of the week and hours intervals for ESI={esi}/5 in respect to the average', fontsize=30)

        x = [v + single_bar_width * 3 for v in x_values_bar_base]
        ax.set_xticks(x)
        ax.set_xticklabels(DAYS, fontsize=30)
        ax.legend(fontsize=30)

        # for rect in rects:
        #     ax.bar_label(rect)

        fig.tight_layout()
        plt.subplots_adjust()
        plt.savefig(OUTPUT_DIR_PATH / f"ESI-{esi}.png")


if __name__ == '__main__':
    with open(Path(__file__).parent / 'input' / 'input.csv') as csvfile:
        results = aggregate(csv.DictReader(csvfile))
        plot_results(results)
