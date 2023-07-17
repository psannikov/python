import json
import zipfile
import pandas as pd


class EgrulWorker:
    # Константы, перенести в конфиг файл
    DICT_KEY_SEARCH = 'СвОКВЭД'
    OKVED_SEARCH = 'СвОКВЭДОсн'
    SV_OKVED_KEY_SEARCH = 'КодОКВЭД'
    SV_OKVED_VALUE_SEARCH = '61'

    dfCompanies = pd.DataFrame()
    count = 0

    def __init__(self, filename):
        self.filename = filename

    def prepareJsonDataToDf(self):
        with zipfile.ZipFile(self.filename, 'r') as z:
            for file_name in z.namelist():
                if file_name.endswith('.json'):
                    self.count += 1
                    print(f'Открытие файла {self.count} имя файла {file_name}')
                    with z.open(file_name) as f:
                        data = json.load(f)
                        df = pd.DataFrame(data)
                        df['svokved'] = df['data'].apply(
                            lambda x: x[self.DICT_KEY_SEARCH] if self.DICT_KEY_SEARCH in x else {})
                        df['svokvedosn'] = df['svokved'].apply(
                            lambda x: x[self.OKVED_SEARCH] if self.OKVED_SEARCH in x else {})
                        df['okved'] = df['svokvedosn'].apply(
                            lambda x: x[self.SV_OKVED_KEY_SEARCH] if self.SV_OKVED_KEY_SEARCH in x and x[
                                                                                                           self.SV_OKVED_KEY_SEARCH][
                                                                                                       :2] == self.SV_OKVED_VALUE_SEARCH else None)
                        df = df[~df['okved'].isna()][['ogrn', 'inn', 'kpp', 'name', 'full_name', 'okved']]
                        self.dfCompanies = pd.concat([self.dfCompanies, df])
