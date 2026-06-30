import os
import dotenv
import requests

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
