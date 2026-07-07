"""
GH Archive ELT Pipeline DAG

Orchestrates the four pipeline stages in dependency order on a daily schedule:
    ingest  -> pull hourly GH Archive files into S3
    process -> aggregate with PySpark, write Parquet back to S3
    load    -> load aggregated Parquet into BigQuery
    dbt     -> build staging + mart models and run data tests

Note: tasks are wired as shell commands to define the pipeline structure and
scheduling. Running the Spark and dbt steps fully inside the Airflow containers
would require packaging their dependencies and cloud credentials into a custom
image, which is the intended next step.
"""

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