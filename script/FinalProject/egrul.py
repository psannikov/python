from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator

# from DBWorker import DBWorker
# from EgrulWorker import EgrulWorker

default_args = {
    'owner': 'psannikov',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
# def read_json_save_to_db():
#     FILENAME = 'egrul.json.zip'
#     DB_NAME = 'airflow.db'
#     TABLE_NAME_COMPANIES = 'companies'
    
#     egrul_parse = EgrulWorker(FILENAME)
#     egrul_parse.prepare_json_data_to_df()
#     db_worker = DBWorker(DB_NAME)
#     db_worker.insert_df_to_db(TABLE_NAME_COMPANIES, egrul_parse.df_companies)

# Define the DAG
dag = DAG(
    dag_id='EGRUL_ETL',
    description='Execute download.sh script using Airflow to download data, parse data and save it in locacl sqlite DB',
    schedule_interval='@daily',
    start_date=datetime(2023, 7, 18),
    default_args=default_args
)

wget_download = BashOperator(
    task_id='execute_download_script',
    bash_command='./download.sh',
    dag=dag
)
# pars_and_save = PythonOperator(
#         task_id='parse_and_save',
#         python_callable=read_json_save_to_db,
#     )

wget_download