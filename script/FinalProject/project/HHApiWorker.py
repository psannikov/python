import requests
import pandas as pd
from time import sleep


class HHApiWorker:

    api_params = {'text': 'python middle',
                  'search_field': 'name',
                  'per_page': 25,
                  'page': 0}
    vacancy_ids = []
    vacancy_detail_info = []
    vacancy_key_skills = []
    company_industries = []
    df_vacancy = pd.DataFrame
    df_skills = pd.DataFrame
    df_company_industries = pd.DataFrame

    def __init__(self, config):
        self.ENDPOINT = config['HHApiWorker']['ENDPOINT']
        self.PATH_URL = config['HHApiWorker']['PATH_URL']
        self.URL_HEADERS = {config['HHApiWorker']['URL_HEADER_KEY'] : config['HHApiWorker']['URL_HEADER_VALUE']}
        self.LIMIT_OF_VACANCY_DETAIL = int(config['HHApiWorker']['LIMIT_OF_VACANCY_DETAIL'])
    
    def get_vacancy_ids_in_list(self, data):
        for result in data['items']:
            self.vacancy_ids.append(result['id'])

    def get_all_vacancy_id(self):
        while True:
            results = requests.get(self.ENDPOINT + self.PATH_URL,
                                   headers=self.URL_HEADERS,
                                   params=self.api_params).json()
            if len(results['items']) == 0 or len(self.vacancy_ids) >= self.LIMIT_OF_VACANCY_DETAIL:
                break
            self.get_vacancy_ids_in_list(results)
            print(f'Список id вакансий содержит {len(self.vacancy_ids)} элементов')
            self.api_params['page'] += 1
    
    def get_vacancy_detail(self, id_vacancy):
        url = f'{self.ENDPOINT}{self.PATH_URL}/{id_vacancy}'
        print(f"Начата загрузка вакансии {url}")
        result = requests.get(url, headers=self.URL_HEADERS).json()
        sleep(1)
        try:
            vacancy_row = []
            vacancy_id = result['id']
            vacancy_name = result['name']
            company_name = result['employer']['name']
            company_id = result['employer']['id']
            company_url = result['employer']['url']
            company_result = requests.get(company_url, headers=self.URL_HEADERS).json()
            company_industries_list = company_result['industries']
            for company_industry in company_industries_list:
                self.company_industries.append((company_id,company_industry['id']))
            vacancy_description = result['description']
            for skill in result['key_skills']:
                self.vacancy_key_skills.append((vacancy_id, skill['name']))
            vacancy_row.append(vacancy_id)
            vacancy_row.append(company_id)
            vacancy_row.append(company_name)
            vacancy_row.append(vacancy_name)
            vacancy_row.append(vacancy_description)
            self.vacancy_detail_info.append(vacancy_row)
        except Exception as e:
            print(f'Возникло исключение {result}')

    def get_all_vacancies_detail(self):
        for vacancy_id in self.vacancy_ids:
            self.get_vacancy_detail(vacancy_id)

    def prepare_all_vacancy_to_df(self):
        table_columns = ['id', 'company_id', 'company_name', 'position', 'job_description']
        return pd.DataFrame(data=self.vacancy_detail_info, columns=table_columns, index=None)

    def prepare_all_key_skill_df(self):
        table_columns = ['id_vacancy', 'skill']
        return pd.DataFrame(data=self.vacancy_key_skills, columns=table_columns, index=None)

    def prepare_all_companies_industries_df(self):
        table_columns = ['company_id', 'industry_id']
        return pd.DataFrame(data=self.company_industries, columns=table_columns, index=None)    

    def prepare_vacancy_info(self):
        self.get_all_vacancy_id()
        self.get_all_vacancies_detail()
        self.df_vacancy = self.prepare_all_vacancy_to_df()
        self.df_skills = self.prepare_all_key_skill_df()
        self.df_company_industries = self.prepare_all_companies_industries_df()
