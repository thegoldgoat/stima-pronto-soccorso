import os
import csv
from pathlib import Path
import mongoengine
from simulator.src.common.Models.month_arrivals_model import MonthArrivalsModel
from .constants import ESIS, MONTHS
import sys

data_year = -1


def read_args():
    global data_year
    if(len(sys.argv) <= 1):
        print("Please specify input data year by argument")
        exit(1)
    else:
        data_year = int(sys.argv[1])


def aggregate(input_data):
    results = dict()

    for esi in ESIS:
        results[esi] = dict()

        for month, month_value in MONTHS.items():
            results[esi][month] = 0

    for row in input_data:
        esi = row['esi']
        arrivalmonth = row['arrivalmonth']

        results[esi][arrivalmonth] += 1

    for esi, months_dict in results.items():
        month_index = 1
        for month, y_value in months_dict.items():
            if(month_index>=3 and month_index<=6):
                months_dict[month] = y_value/4
            else:
                months_dict[month] = y_value/3
                
            month_index += 1
    
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


def store_results(results):
    for esi, months_dict in results.items():
        if (esi != "NA"):
            for month_name, arrivals_count in months_dict.items():
                MonthArrivalsModel(
                    emergency_code=esi, month=MONTHS[month_name], year=data_year, arrivals=arrivals_count).save()


if __name__ == '__main__':
    read_args()
    print("Plotting data and saving it in db for year {}".format(data_year))
    mongoengine.connect("stima-pronto-soccorso")
    with open(Path(__file__).parent / 'input' / 'input.csv') as csvfile:
        results = aggregate(csv.DictReader(csvfile))
        store_results(results)
        plot_results(results)
