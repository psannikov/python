import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

sys.path.append("/home/psannikov/project")

default_args = {'owner': 'psannikov',
                'retries': 5,
                'retry_delay': timedelta(minutes=2)}

with DAG(dag_id='ETL',
         description='ETL proccess using Airflow to download data, parse data and save it in locacl sqlite DB, prepare and send final report',
         schedule_interval='@daily',
         start_date=datetime(2023, 7, 18),
         default_args=default_args) as dag:
         wget_download_egrul = BashOperator(task_id='execute_download_script',bash_command='/home/psannikov/project/download.sh ')
         