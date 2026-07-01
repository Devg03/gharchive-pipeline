import glob
from google.cloud import bigquery

client = bigquery.Client(project="gharchive-pipeline")

dataset_id = "gharchive-pipeline.gharchive"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
client.create_dataset(dataset, exists_ok=True)

print(f"Dataset {dataset_id} ready")

def load_parquet(folder, table_name):
    table_id = f"gharchive-pipeline.gharchive.{table_name}"
    files = glob.glob(f"{folder}/part-*.parquet")

    for i, path in enumerate(files):
        job_config = bigquery.LoadJobConfig(
            source_format = bigquery.SourceFormat.PARQUET,
            write_disposition = "WRITE_TRUNCATE" if i == 0 else "WRITE_APPEND",
        )

        with open(path, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)

        job.result() # Waits for the load to finish

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_name}")

load_parquet("data/processed/repo_activity", "repo_activity")
load_parquet("data/processed/events_by_type", "events_by_type")