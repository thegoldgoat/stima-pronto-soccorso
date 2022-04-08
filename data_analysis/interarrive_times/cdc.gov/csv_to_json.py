import os
import json
import csv

INPUT_CSV_FILES = [
    ('input/2019.csv', 2019),
    ('input/2018.csv', 2018),
    ('input/2017.csv', 2017),
    ('input/2016.csv', 2016),
    ('input/2015.csv', 2015)
]

OUTPUT_JSON_DIR = 'output'
OUTPUT_JSON_FILE = 'output/data.json'


def main():
    if not os.path.exists(OUTPUT_JSON_DIR):
        os.mkdir(OUTPUT_JSON_DIR)

    outfile = open(OUTPUT_JSON_FILE, 'w')

    output_list = list()
    for (input_path, year) in INPUT_CSV_FILES:
        with open(input_path, 'r') as open_file:
            reader = csv.DictReader(open_file)

            for line in reader:
                output_dict = dict()
                output_dict['year'] = year
                output_dict['esi'] = line['IMMEDR']
                output_dict['arrivalmonth'] = line['VMONTH']
                output_dict['arrivalday'] = line['VDAYR']
                output_dict['arrivalhour'] = line['ARRTIME'][:2]
                output_dict['arrivalminute'] = line['ARRTIME'][2:]
                output_dict['waittime'] = line['WAITTIME']

                # 2015 does not contain
                if year == 2016 or year == 2017:
                    output_dict['visitlength'] = -1
                else:
                    lov = line['LOV']
                    if lov == '-9':
                        lov = -1
                    output_dict['visitlength'] = lov

                output_list.append(output_dict)

    outfile.write(json.dumps(output_list))
    outfile.close()


if __name__ == "__main__":
    main()
