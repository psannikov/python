import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
import os
import configparser

home_directory = os.path.expanduser( '~' )
project_path = os.path.join(home_directory, 'project')
setting_path = os.path.join(project_path,'settings.ini')

sys.path.append(project_path)
from DBWorker import DBWorker
from EgrulWorker import EgrulWorker
from HHApiWorker import HHApiWorker
from SQLWorker import SQLWorker
from EmailWorker import EmailWorker

config = configparser.ConfigParser()
config.read(setting_path)

DB_NAME = os.path.join (project_path,config['Main']['DB_NAME'])
TABLE_NAME_COMPANIES = config['Main']['TABLE_NAME_COMPANIES']
TABLE_NAME_VACANCIES = config['Main']['TABLE_NAME_VACANCIES']
TABLE_NAME_SKILLS = config['Main']['TABLE_NAME_SKILLS']
TABLE_NAME_COMPANIES_INDUSTRIES = config['Main']['TABLE_NAME_COMPANIES_INDUSTRIES']

db_worker = DBWorker(DB_NAME)

default_args = {'owner': 'psannikov',
                'retries': 5,
                'retry_delay': timedelta(minutes=2)}

def read_json_save_to_db():
     filename =  os.path.join(project_path,config['Main']['EGRUL_JSON_ZIP_FILENAME'])
     egrul_parse = EgrulWorker(config, filename)
     egrul_parse.prepare_json_data_to_df()
     db_worker.insert_df_to_db(TABLE_NAME_COMPANIES, egrul_parse.df_companies)

def hh_etl_to_db():
     hh_api_worker = HHApiWorker(config)
     hh_api_worker.prepare_vacancy_info()
     db_worker.insert_df_to_db(TABLE_NAME_VACANCIES, hh_api_worker.df_vacancy)
     db_worker.insert_df_to_db(TABLE_NAME_SKILLS, hh_api_worker.df_skills)
     db_worker.insert_df_to_db(TABLE_NAME_COMPANIES_INDUSTRIES, hh_api_worker.df_company_industries)

def prepare_report():
     sql_worker = SQLWorker(config)
     sql_worker.get_data_from_db_to_pd()
     sql_worker.save_df_to_excel()

def send_email():
     email_sender = EmailWorker(config)
     email_sender.prepareMessage()
     email_sender.send_mail()


with DAG(dag_id='Final_project_ETL',
         description='ETL proccess using Airflow to download data, parse data and save it in locacl sqlite DB, prepare and send final report',
         schedule_interval='@daily',
         start_date=datetime(2023, 7, 20),
         default_args=default_args) as dag:
       start = EmptyOperator(task_id="start")
       
       with TaskGroup("section_egrul_etl", tooltip="Tasks for ETL EGRUL") as section_egrul_etl:
            wget_download_egrul = BashOperator(task_id='execute_download_script',bash_command='/home/psannikov/project/download.sh ')
            pars_and_save_egrul = PythonOperator(task_id='parse_and_save',python_callable=read_json_save_to_db)
            wget_download_egrul>>pars_and_save_egrul

       with TaskGroup("section_hhapi_etl", tooltip="Tasks for ETL HeadHunter") as section_hhapi_etl:
            pars_and_save_hh = PythonOperator(task_id='download_parse_and_save',python_callable=hh_etl_to_db)

       with TaskGroup("section_report", tooltip="Tasks for generate and send reports") as section_report:
            prepare_report = PythonOperator(task_id="get_data_and_prepare",python_callable=prepare_report)
            send_report = PythonOperator(task_id="send_report",python_callable=send_email)
            prepare_report>>send_report

    
       end = EmptyOperator(task_id="end")
      
       start>>[section_egrul_etl,section_hhapi_etl]>>section_report>>end
