import json


numberModes = 20


metaData = {    
    "name": "MODE",
    "key": "pl"}
metaData['measurements'] = []
for i in range(1,numberModes+1):
    metaData['measurements'].append(

            {
                "name": "Id "+str(i)+" Frequency",
                "key": "id"+str(i)+".Freq",
                "values": [
                    {
                        "key": "value",
                        "name": "Value",
                        "units": "Hz",
                        "format": "integer",
                        "hints": {
                            "range": 1
                        }
                    },
                    {
                        "key": "utc",
                        "source": "timestamp",
                        "name": "Timestamp",
                        "format": "utc",
                        "hints": {
                            "domain": 1
                        }
                    }
                ]
            })
    metaData['measurements'].append(
            {
                "name": "Id "+str(i)+" Damping",
                "key": "id"+str(i)+".Damp",
                "values": [
                    {
                        "key": "value",
                        "name": "Value",
                        "units": "-",
                        "format": "integer",
                        "hints": {
                            "range": 1
                        }
                    },
                    {
                        "key": "utc",
                        "source": "timestamp",
                        "name": "Timestamp",
                        "format": "utc",
                        "hints": {
                            "domain": 1
                        }
                    }
                ]
            })




print(metaData)

with open('MODEdictionary.json', 'w', encoding='utf-8') as outfile:
    json.dump(metaData, outfile, ensure_ascii=False, indent=4)
