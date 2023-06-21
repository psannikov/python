import zipfile
import json
from pathlib import Path
import pandas

ZIP_ARCHIVE = 'egrul.json.zip'
DICT_KEY_SEARCH = 'СвОКВЭД'
OKVED_SEARCH = 'СвОКВЭДОсн'
SV_OKVED_KEY_SEARCH = 'КодОКВЭД'
SV_OKVED_VALUE_SEARCH = '61'

def filter_company_by_okved(source_data):
    res = []
    for items in data:
        company = {}
        if len(items.get('data').get(DICT_KEY_SEARCH,'')) > 0:
            if len(items.get('data').get(DICT_KEY_SEARCH).get(OKVED_SEARCH,'')) >0 :
                if len(items.get('data').get(DICT_KEY_SEARCH).get(OKVED_SEARCH).get(SV_OKVED_KEY_SEARCH,'')) >0 :
                    if items.get('data').get(DICT_KEY_SEARCH).get(OKVED_SEARCH).get(SV_OKVED_KEY_SEARCH) == SV_OKVED_VALUE_SEARCH:
                        company['inn'] = items.get('inn')
                        company['kpp'] = items.get('kpp')
                        company['ogrn'] = items.get('ogrn')
                        company['name'] = items.get('name')
                        company['full_name'] = items.get('full_name')
                        # print(company)
                        res.append(company)
    # print(res)
    return res
def filter_company_by_okved(source_data):
    return [d for d in data if d.get('data',{}).get(DICT_KEY_SEARCH,{}).get(OKVED_SEARCH,{}).get(SV_OKVED_KEY_SEARCH) == SV_OKVED_VALUE_SEARCH]

list_of_company = []
count = 0;
with zipfile.ZipFile(ZIP_ARCHIVE, 'r') as zip_files:
    for file_name in zip_files.namelist():
        if file_name.endswith('.json'):
            count += 1
        # if file_name == '00001.json':
            print(f'Обработка файла №{count} имя файла {file_name}')
            with zip_files.open(file_name) as file:
                data = json.load(file)
                data = filter_company_by_okved(data)
                if len (data) > 0:
                    list_of_company.append(filter_company_by_okved(data))


list_of_company