from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

def extract_apod():
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    data = response.json()
    print(data)
    return data

with DAG(
    dag_id="nasa_apod_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["nasa"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_apod",
        python_callable=extract_apod
    )
