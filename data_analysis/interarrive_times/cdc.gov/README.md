Data downloaded from https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/sas/

To convert the SAS7BDAT to CSV use: File converted with https://dumbmatter.com/sas7bdat/
Then in each year folder there are the script to covert the csv in json:
- export.py converts the file in json (only first columns)
- exportEsiTime.py reads the previously generated json and grabs only the important data
- studyArrivalTime.py reads each year file and plots the stats.