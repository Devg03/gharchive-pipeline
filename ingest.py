import os
import boto3
from dotenv import load_dotenv
import requests

load_dotenv()
s3 = boto3.client("s3")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def build_url(year, month, day, hour):
    url = f"https://data.gharchive.org/{year}-{month:02d}-{day:02d}-{hour}.json.gz"

    return url

def download_file(url):
    response = requests.get(url, timeout=60)
    if response.status_code == 404:
        print(f"{url} skipped")
        return None
    response.raise_for_status()

    return response.content

def build_key(year, month, day, hour):
    key = f"raw/year={year}/month={month:02d}/day={day:02d}/hour={hour:02d}/data.json.gz"

    return key

def ingest_hour(year, month, day, hour):
    url = build_url(year=year, month=month,day=day,hour=hour)
    content = download_file(url=url)
    
    if content is None:
        return
    
    key = build_key(year=year, month=month, day=day, hour=hour)
    
    s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=content)
    print(f"Uploaded {key} ({len(content):,} bytes)")

def ingest_day(year, month, day):
    for hour in range(24):
        ingest_hour(year=year, month=month, day=day, hour=hour)

if __name__ == "__main__":
    ingest_day(2024, 1, 1)