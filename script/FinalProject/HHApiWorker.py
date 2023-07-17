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
    vacancy_detail_info = []
    vacancy_key_skills = []
    df_vacancy = pd.DataFrame
    df_skills = pd.DataFrame

    # Настройка логгера
    logging.basicConfig(filename='my_app.log',
                        encoding='utf-8',
                        filemode='w',
                        level=logging.DEBUG,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")

    def __init__(self, endpoint):
        self.ENDPOINT = endpoint

    def get_vacancy_i_ds_in_list(self, data):
        for result in data['items']:
            self.vacancy_ids.append(result['id'])

    def get_all_vacancy_id(self):
        while True:
            results = requests.get(self.ENDPOINT + self.PATH_URL,
                                   headers=self.URL_HEADERS,
                                   params=self.api_params).json()
            if len(results['items']) == 0 or len(self.vacancy_ids) >= self.LIMIT_OF_VACANCY_DETAIL:
                break
            self.get_vacancy_i_ds_in_list(results)
            print(len(self.vacancy_ids))
            self.api_params['page'] += 1

    async def get_vacancy_detail(self, id_vacancy, session):
        url = f'/{self.PATH_URL}/{id_vacancy}'
        logging.debug(f"Начата загрузка вакансии {url}")
        async with session.get(url=url) as response:
            vacancy_json = await response.json()
            logging.debug(f"Завершена загрузка вакансии {url}")
            return vacancy_json

    async def get_all_vacancies(self, ids):
        connector = TCPConnector(limit=3)
        async with ClientSession(self.ENDPOINT, connector=connector) as session:
            tasks = []
            for id in ids:
                tasks.append(asyncio.create_task(self.get_vacancy_detail(id, session)))
            results = await asyncio.gather(*tasks)
        for result in results:
            try:
                vacancy_row = []
                vacancy_id = result['id']
                vacancy_name = result['name']
                company_name = result['employer']['name']
                vacancy_description = result['description']
                for skill in result['key_skills']:
                    self.vacancy_key_skills.append((vacancy_id, skill['name']))
                vacancy_row.append(vacancy_id)
                vacancy_row.append(company_name)
                vacancy_row.append(vacancy_name)
                vacancy_row.append(vacancy_description)
                self.vacancy_detail_info.append(vacancy_row)
            except Exception as e:
                logging.exception(f'Возникло исключение {result}')

    def prepare_all_vacancy_to_df(self):
        table_columns = ['id', 'company_name', 'position', 'job_description']
        return pd.DataFrame(data=self.vacancy_detail_info, columns=table_columns, index=None)

    def prepare_all_key_skill_df(self):
        table_columns = ['id_vacancy', 'skill']
        return pd.DataFrame(data=self.vacancy_key_skills, columns=table_columns, index=None)

    def prepare_vacancy_info(self):
        asyncio.run(self.get_all_vacancies(self.vacancy_ids))
        self.df_vacancy = self.prepare_all_vacancy_to_df()
        self.df_skills = self.prepare_all_key_skill_df()
