import json

def main():
    datas = []
    with open("export.json") as infile:
        datas = json.loads(infile.read())

    outDatas = []
    with open("exportEsiTime2019.json","w") as outfile:
        for data in datas:
            outData = {}
            outData['year'] = 2019
            outData['esi'] = data['IMMEDR']
            outData['arrivalmonth'] = data['VMONTH']
            outData['arrivalday'] = data['VDAYR']
            outData['arrivalhour'] = data['ARRTIME'][:2]
            outData['arrivalminute'] = data['ARRTIME'][2:]
            outData['waittime'] = data['WAITTIME']
            outData['visitlength'] = data['LOV']
            outDatas.append(outData)
        outfile.write(json.dumps(outDatas))

if __name__ == "__main__":
    main()

    
"""
    Data format in export.json
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
"""