import os

from FinalProject.DBWorker import DBWorker
from FinalProject.Downloader import Downloader
from FinalProject.EgrulWorker import EgrulWorker
from FinalProject.HHApiWorker import HHApiWorker

#Константы, перенести в конфиг файл
URL = 'https://sharedby.blomp.com/u3T0GN'
FILENAME = 'egrul.json.zip'
ENDPOINT = 'https://api.hh.ru/'
DB_NAME = 'airflow.db'
TABLE_NAME_COMPANIES = 'companies'
TABLE_NAME_VACANCIES = 'vacancies'
TABLE_NAME_SKILLS = 'skills'

#Реализовать проверку наличия и актуальности файла если он есть и актуален повторная загрузка не нужна
def checkFileAlreadyDownload(filename):
    return os.path.isfile(filename)

if checkFileAlreadyDownload(FILENAME):
    print("Файл уже загружен, загрузка не требуется")
else:
    print("Файл не загружен, будет выполнена загрузка файла")
    #Создаем загрузчик файлов и загружаем данные
    loader = Downloader(URL)
    data = loader.download_data()
    if data:
        loader.save_to_file(data, FILENAME)
        print(f'Данные успешно загружены в файл {FILENAME}')
    else:
        print(f'Не удалось загрузить данные')
#Читаем закачанный файл и ищем в нем нужную информацию
egrulParse = EgrulWorker(FILENAME)
egrulParse.prepareJsonDataToDf()
#Загружаем информацию с HH
hhApiWorker = HHApiWorker(ENDPOINT)
hhApiWorker.getAllVacancyID()
hhApiWorker.prepareVacancyInfo()
dbWorker = DBWorker(DB_NAME)
dbWorker.insertDfToDB(TABLE_NAME_COMPANIES, egrulParse.dfCompanies)
dbWorker.insertDfToDB(TABLE_NAME_VACANCIES, hhApiWorker.dfVacancy)
dbWorker.insertDfToDB(TABLE_NAME_SKILLS, hhApiWorker.dfSkills)



