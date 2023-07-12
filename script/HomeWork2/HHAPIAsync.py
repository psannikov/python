import requests as req
import bs4  as bs
import pandas as pd
import sqlite3
import asyncio
from aiohttp import ClientSession

ENDPOINT = 'https://api.hh.ru/vacancies'
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
    results = req.get(ENDPOINT, headers = URL_HEADERS, params = api_params).json()
    if (len(results['items']) == 0 or len(vacancy_ids)>=LIMIT_OF_VACANCY_DETAIL):
        break
    getVacancyIDs(results)
    print(len(vacancy_ids))
    api_params['page'] += 1

async def get_vacancy(id, session):
    url = f'/vacancies/{id}'
    
    async with session.get(url=url) as response:
        vacancy_json = await response.json()
        return vacancy_json

async def main(ids):
    async with ClientSession('https://api.hh.ru/') as session:
        tasks = []
        for id in ids:
            tasks.append(asyncio.create_task(get_vacancy(id, session)))
        results = await asyncio.gather(*tasks)
    for result in results:
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

asyncio.run(main(vacancy_ids))

table_columns = ['company_name', 'position', 'job_description', 'key_skills']
df = pd.DataFrame(data=vacancyDetailInfo, columns=table_columns, index=None)

connection = sqlite3.connect(DB_NAME)
df.to_sql(TABLE_NAME,connection, if_exists='replace', index=False)
connection.close()

print(f'Создана таблица {TABLE_NAME} и добавлено {len(vacancyDetailInfo)}')