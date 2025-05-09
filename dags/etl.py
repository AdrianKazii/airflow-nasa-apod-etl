from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from airflow.providers.http.operators.http import HttpOperator
import json

## Define the DAG
with DAG(
    dag_id='nasa_apod_postgres', # any you want
    start_date = datetime.now() - timedelta(days=1), 
    schedule = '@daily',
    catchup=False 
) as dag:
    
    ## step 1: Create the table if it doesnt exists

    @task
    def create_table():
        ## initialize the Postgreshook
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        ## SQL query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        explanation TEXT,
        url TEXT,
        date DATE,
        media_type VARCHAR(50)
        )
"""
        ## Execute the table creation query
        postgres_hook.run(create_table_query)


    ## step 2: Extract the NASA API Data(APOD) - Astronomy Picture of the Day
    # https://api.nasa.gov/planetary/apod?api_key=RaZOhU1GTrXU8MjyoTEgocI4YkVRYlaXax5F2LBF
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={"api_key":"{{ conn.nasa_api.extra_dejson.api_key }}"}, # Use the API Key from
        response_filter=lambda response:response.json()## Convert respons to json
    )

    ## step 3: Transform the data(Pick the information that I need to save)
    @task
    def transform_apod_data(response):
        apod_data={
            'title':response.get('title',''),
            'explanation':response.get('explanation',''),
            'url':response.get('url',''),
            'date':response.get('date',''),
            'media_type':response.get('media_type','')
        }
        return apod_data 

    ## step 4: Load the data into Postgres SQL
    @task
    def load_data_to_postgres(apod_data):
        ## Initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        ## Define the SQL Insert Query
        insert_query = """
INSERT INTO apod_data (title, explanation, url, date, media_type)
VALUES (%s, %s, %s, %s, %s);
"""

        ## Execute the SQL Query
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))

    ## step 5: Verify the data DBViewer
    


    ## step 6: Define the task dependencies
    ## Extract
    create_table() >> extract_apod ## Ensure the table is created before extraction
    api_response=extract_apod.output
    ## Transform
    transformed_data = transform_apod_data(api_response)
    ## Load
    load_data_to_postgres(transformed_data)

