import json

def main():
    datas = []
    with open("export.json","w") as outfile:
        with open("ed2018_sas.csv") as infile:
            line = infile.readline() # Discard first line
            line = infile.readline()
            while(line):
                data = {
                    'VMONTH': None,
                    'VDAYR': None,
                    'ARRTIME': None,
                    'WAITTIME': None,
                    'LOV': None,
                    'AGE': None,
                    'AGER': None,
                    'AGEDAYS': None,
                    'RESIDNCE': None,
                    'SEX': None,
                    'ETHUN': None,
                    'ETHIM': None,
                    'RACEUN': None,
                    'RACER': None,
                    'RACERETH': None,
                    'ARREMS': None,
                    'AMBTRANSFER': None,
                    'NOPAY': None,
                    'PAYPRIV': None,
                    'PAYMCARE': None,
                    'PAYMCAID': None,
                    'PAYWKCMP': None,
                    'PAYSELF': None,
                    'PAYNOCHG': None,
                    'PAYOTH': None,
                    'PAYDK': None,
                    'PAYTYPER': None,
                    'TEMPF': None,
                    'PULSE': None,
                    'RESPR': None,
                    'BPSYS': None,
                    'BPDIAS': None,
                    'POPCT': None,
                    'IMMEDR': None
                }
                lineSplit = line.split(",")
                index = 0
                for key, value in data.items():
                    data[key] =  lineSplit[index]
                    index+=1
                datas.append(data)
                line = infile.readline()
        outfile.write(json.dumps(datas))
            

if __name__ == "__main__":
    main()