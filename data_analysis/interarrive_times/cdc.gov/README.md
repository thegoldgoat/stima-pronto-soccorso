Data downloaded from https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/sas/

To convert the SAS7BDAT to CSV use: File converted with https://dumbmatter.com/sas7bdat/

Then:

1. place all the CSVs in `input` folder
2. run `python3 csv_to_json.py`
3. run `studyArrivalTime.py`

Output results can be found in `output/group<x>hours` for x in [1, 2, 3, 4, 6, 8, 12, 24]
