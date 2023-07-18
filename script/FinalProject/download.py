from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'psannikov',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
# Define the DAG
dag = DAG(
    dag_id='Execute_download_script',
    description='Execute download.sh script using Airflow',
    schedule_interval='@daily',
    start_date=datetime(2023, 7, 18),
    default_args=default_args
)

# Define the BashOperator to execute the script
execute_script = BashOperator(
    task_id='execute_download_script',
    bash_command='./download.sh',
    dag=dag
)


