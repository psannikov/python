from DBWorker import DBWorker
from HHApiWorker import HHApiWorker

DB_NAME = 'airflow.db'
TABLE_NAME_VACANCIES = 'vacancies'
TABLE_NAME_SKILLS = 'skills'
ENDPOINT = 'https://api.hh.ru/'

db_worker = DBWorker(DB_NAME)
hh_api_worker = HHApiWorker(ENDPOINT)
hh_api_worker.prepare_vacancy_info()

print(hh_api_worker.df_vacancy.head())
print(hh_api_worker.df_skills.head())
print(hh_api_worker.df_company_industries.head())