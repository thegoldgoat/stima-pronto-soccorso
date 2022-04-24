import csv

# output.csv is the file that the aggregation Python scripts can read
writer = csv.writer(open('output.csv', 'w'))

writer.writerow([
    'esi',
    'arrivalmonth',
    'arrivalday',
    'arrivalhour_bin'
])

# input.csv is the file from the R script
with open('input.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        writer.writerow([
            row['esi'],
            row['arrivalmonth'],
            row['arrivalday'],
            row['arrivalhour_bin']
        ])
