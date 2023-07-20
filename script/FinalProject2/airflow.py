from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'psannikov',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='final_project',
    default_args=default_args,
    description='DAG for final project Python Middle Developer RTK',
    start_date=datetime(2023, 7, 15, 8),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='download_file',
        bash_command="~/airflow/dags/download.sh "
    )



    task1
