from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG (
    dag_id = "gharchive-pipeline",
    start_date = datetime(2024, 1, 1),
    schedule = "@daily",
    catchup = False,
    tags = ["gharchive"],
) as dag:
    
    ingest = BashOperator(
        task_id = "ingest",
        bash_command = "echo 'Ingesting GH Archive to S3'",
    )

    process = BashOperator(
        task_id = "process",
        bash_command = "echo 'Processing with PySpark'",
    )

    load = BashOperator(
        task_id = "load",
        bash_command = "echo 'Loading to BigQuery'",
    )

    dbt = BashOperator(
        task_id = "dbt",
        bash_command = "echo 'Running dbt models and tests'",
    )

    ingest >> process >> load >> dbt