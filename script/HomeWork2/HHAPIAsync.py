import requests as req
import pandas as pd
import sqlite3
import asyncio
from aiohttp import ClientSession, TCPConnector
import logging
import platform

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

ENDPOINT = 'https://api.hh.ru/'
PATH_URL = 'vacancies'
URL_HEADERS = {'User-Agent': 'Mozilla/5.0'}
DB_NAME = 'hh.db'
TABLE_NAME = 'vacancies_api_async'
LIMIT_OF_VACANCY_DETAIL = 1000

api_params = {'text':'python middle developer',
              'search_field':'name',
              'per_page': 25,
              'page':0}
vacancy_ids = []
vacancyDetailInfo =[]

def getVacancyIDs (data):
    for result in data['items']:
        vacancy_ids.append(result['id'])

while (True):
    results = req.get(ENDPOINT + PATH_URL, headers = URL_HEADERS, params = api_params).json()
    if (len(results['items']) == 0 or len(vacancy_ids)>=LIMIT_OF_VACANCY_DETAIL):
        break
    getVacancyIDs(results)
    print(len(vacancy_ids))
    api_params['page'] += 1

async def get_vacancy(id, session):
    url = f'/{PATH_URL}/{id}'
    logging.debug(f"Начата загрузка вакансии {url}")
    async with session.get(url=url) as response:
        vacancy_json = await response.json()
        logging.debug(f"Завершена загрузка вакансии {url}")
        return vacancy_json

async def main(ids):
    connector = TCPConnector(limit=3)
    async with ClientSession(ENDPOINT, connector=connector) as session:
        tasks = []
        for id in ids:
            tasks.append(asyncio.create_task(get_vacancy(id, session)))
        results = await asyncio.gather(*tasks)
    for result in results:
        try:
            vacancyRow = []
            listOfRequirements = []
            vacancyName = result['name']
            companyName = result['employer']['name']
            vacancyDescription = result['description']
            for skill in result['key_skills']:
                listOfRequirements.append(skill['name'])
            stringOfRequirements = ', '.join(listOfRequirements)
            vacancyRow.append(companyName)
            vacancyRow.append(vacancyName)
            vacancyRow.append(vacancyDescription)
            vacancyRow.append(stringOfRequirements)
            vacancyDetailInfo.append(vacancyRow)
        except Exception as e:
            logging.exception(f'Возникло исключение {result}')
# Настройка логгера
logging.basicConfig(filename='my_app.log', 
                    encoding='utf-8', 
                    filemode='w',
                    level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")

asyncio.run(main(vacancy_ids))

table_columns = ['company_name', 'position', 'job_description', 'key_skills']
df = pd.DataFrame(data=vacancyDetailInfo, columns=table_columns, index=None)

connection = sqlite3.connect(DB_NAME)
df.to_sql(TABLE_NAME,connection, if_exists='replace', index=False)
connection.close()

print(f'Создана таблица {TABLE_NAME} и добавлено {len(vacancyDetailInfo)}')