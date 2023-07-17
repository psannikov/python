import os

from FinalProject.DBWorker import DBWorker
from FinalProject.Downloader import Downloader
from FinalProject.EgrulWorker import EgrulWorker
from FinalProject.HHApiWorker import HHApiWorker

# Константы, перенести в конфиг файл
URL = 'https://sharedby.blomp.com/u3T0GN'
FILENAME = 'egrul.json.zip'
ENDPOINT = 'https://api.hh.ru/'
DB_NAME = 'airflow.db'
TABLE_NAME_COMPANIES = 'companies'
TABLE_NAME_VACANCIES = 'vacancies'
TABLE_NAME_SKILLS = 'skills'


def check_file_already_download(filename):
    return os.path.isfile(filename)


if check_file_already_download(FILENAME):
    print("Файл уже загружен, загрузка не требуется")
else:
    print("Файл не загружен, будет выполнена загрузка файла")
    # Создаем загрузчик файлов и загружаем данные
    loader = Downloader(URL)
    loader.download_file(FILENAME)
    data = loader.download_data()
    if data:
        loader.save_to_file(data, FILENAME)
        print(f'Данные успешно загружены в файл {FILENAME}')
    else:
        print(f'Не удалось загрузить данные')
# Читаем закачанный файл и ищем в нем нужную информацию
egrul_parse = EgrulWorker(FILENAME)
egrul_parse.prepare_json_data_to_df()
# Загружаем информацию с HH
hh_api_worker = HHApiWorker(ENDPOINT)
hh_api_worker.get_all_vacancy_id()
hh_api_worker.prepare_vacancy_info()
db_worker = DBWorker(DB_NAME)
db_worker.insert_df_to_db(TABLE_NAME_COMPANIES, egrul_parse.df_companies)
db_worker.insert_df_to_db(TABLE_NAME_VACANCIES, hh_api_worker.df_vacancy)
db_worker.insert_df_to_db(TABLE_NAME_SKILLS, hh_api_worker.df_skills)
