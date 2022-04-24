# Interarrival times analysis

## Data download and preprocess

The dataset used in this analysis is taken from https://github.com/yaleemmlc/admissionprediction.git

See https://doi.org/10.1371/journal.pone.0201016 for more on the topic.

Data can be downloaded and converted to CSV using the following R script:

```r
setwd("workingDirectory")
url <- "https://github.com/yaleemmlc/admissionprediction/raw/master/Results/5v_cleandf.RData"
download.file(url, destfile="filename.rdata", mode='wb')
load("filename.rdata")
write.csv(df, "input.csv", row.names = FALSE, quote = FALSE)
```

It can then be trimmed down to a much smaller file (13MB vs 1.4GB) using `preprocess/preprocess_csv.py` which trims away all the columns unused by our scripts.

## Plotting

Two plotting functions are implemented:

1. `aggregate_by_hour.py`: aggregates the data with the hour intervals. Output can be found in `output/hour`
2. `aggregate_by_hour_in_week.py`: aggregates the data with the hour intervals in the different days in the week. Output can be found in `output/hour_in_week`
