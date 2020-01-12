import json
import requests
import os
import pandas as pd

URL_CEP_DICTS = "https://api.cepik.gov.pl/slowniki"
DOWNLOAD_DICT = "downloads"

def getjsonfromurl(url):

    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data


def getCEPdicts():

    cep_dicts = getjsonfromurl(URL_CEP_DICTS)["data"]

    if not os.path.exists(DOWNLOAD_DICT):
        os.mkdir(DOWNLOAD_DICT)

    for d in cep_dicts:
        cep_dict = getjsonfromurl(d["links"]["self"])
        cep_dict_name = cep_dict['data']['id']
        cep_dict_values = cep_dict['data']['attributes']['dostepne-rekordy-slownika']
        df = pd.DataFrame(cep_dict_values)
        name = os.path.join(DOWNLOAD_DICT, 'dict_' + cep_dict_name + '.csv')
        df.to_csv(name, encoding='utf-8', index=False)
        print ('saving dictionary: ' + cep_dict_name + ' values: ' + str(len(cep_dict_values)) +' to file: ' + name )

getCEPdicts()


# url = 'https://api.cepik.gov.pl/pojazdy?wojewodztwo=14&data-od=20190901&data-do=20190930'
# response = requests.get(url)
# json_data = json.loads(response.text)
#
#
# url2 = 'https://api.cepik.gov.pl/pojazdy/1368257542571554'
# response2 = requests.get(url2)
# json_data2 = json.loads(response2.text)
