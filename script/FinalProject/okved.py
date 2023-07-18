from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'psannikov',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
 
with DAG(
    dag_id='Only_download_OKVED',
    default_args=default_args,
    description='DAG for donwload okved file',
    start_date=datetime(2023, 7, 15, 8),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='download_file',
        bash_command="wget https://ofdata.ru/open-data/download/okved_2.json.zip -O ~/airflow/dags/okved_2.json.zip"
    )

    task1
