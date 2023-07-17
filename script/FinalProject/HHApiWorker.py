import requests
import pandas as pd
import asyncio
from aiohttp import ClientSession, TCPConnector
import logging
import platform


class HHApiWorker:
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    PATH_URL = 'vacancies'
    URL_HEADERS = {'User-Agent': 'Mozilla/5.0'}
    DB_NAME = 'hh.db'
    TABLE_NAME = 'vacancies_api_async'
    LIMIT_OF_VACANCY_DETAIL = 1000

    api_params = {'text': 'python middle developer',
                  'search_field': 'name',
                  'per_page': 25,
                  'page': 0}
    vacancy_ids = []
    vacancyDetailInfo = []
    vacancyKeySkills = []
    dfVacancy = pd.DataFrame
    dfSkills = pd.DataFrame

    # Настройка логгера
    logging.basicConfig(filename='my_app.log',
                        encoding='utf-8',
                        filemode='w',
                        level=logging.DEBUG,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")

    def __init__(self, endpoint):
        self.ENDPOINT = endpoint

    def getVacancyIDsInList(self, data):
        for result in data['items']:
            self.vacancy_ids.append(result['id'])

    def getAllVacancyID(self):
        while True:
            results = requests.get(self.ENDPOINT + self.PATH_URL,
                                   headers=self.URL_HEADERS,
                                   params=self.api_params).json()
            if len(results['items']) == 0 or len(self.vacancy_ids) >= self.LIMIT_OF_VACANCY_DETAIL:
                break
            self.getVacancyIDsInList(results)
            print(len(self.vacancy_ids))
            self.api_params['page'] += 1

    async def getVacancyDetail(self, id, session):
        url = f'/{self.PATH_URL}/{id}'
        logging.debug(f"Начата загрузка вакансии {url}")
        async with session.get(url=url) as response:
            vacancy_json = await response.json()
            logging.debug(f"Завершена загрузка вакансии {url}")
            return vacancy_json

    async def getAllVacances(self, ids):
        connector = TCPConnector(limit=3)
        async with ClientSession(self.ENDPOINT, connector=connector) as session:
            tasks = []
            for id in ids:
                tasks.append(asyncio.create_task(self.getVacancyDetail(id, session)))
            results = await asyncio.gather(*tasks)
        for result in results:
            try:
                vacancyRow = []
                vacancyId = result['id']
                vacancyName = result['name']
                companyName = result['employer']['name']
                vacancyDescription = result['description']
                for skill in result['key_skills']:
                    self.vacancyKeySkills.append((vacancyId, skill['name']))
                vacancyRow.append(vacancyId)
                vacancyRow.append(companyName)
                vacancyRow.append(vacancyName)
                vacancyRow.append(vacancyDescription)
                self.vacancyDetailInfo.append(vacancyRow)
            except Exception as e:
                logging.exception(f'Возникло исключение {result}')

    def prepareAllVacancyToDf(self):
        table_columns = ['id', 'company_name', 'position', 'job_description']
        return pd.DataFrame(data=self.vacancyDetailInfo, columns=table_columns, index=None)

    def prepareAllKeySkillDf(self):
        table_columns = ['id_vacancy', 'skill']
        return pd.DataFrame(data=self.vacancyKeySkills, columns=table_columns, index=None)

    def prepareVacancyInfo(self):
        asyncio.run(self.getAllVacances(self.vacancy_ids))
        self.dfVacancy = self.prepareAllVacancyToDf()
        self.dfSkills = self.prepareAllKeySkillDf()

#
# connection = sqlite3.connect(DB_NAME)
# df.to_sql(TABLE_NAME, connection, if_exists='replace', index=False)
# connection.close()
#
# print(f'Создана таблица {TABLE_NAME} и добавлено {len(vacancyDetailInfo)}')
