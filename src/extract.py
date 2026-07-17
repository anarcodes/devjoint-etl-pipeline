import pandas as pd
import requests
import logging

def extract_csv(file_path):
    logging.info(f"CSV faylı oxunur: {file_path}")
    return pd.read_csv(file_path)

def extract_api(url):
    logging.info(f"API-dən data çəkilir: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        logging.error(f"API xətası: Status kodu {response.status_code}")
        raise Exception("API-dən data çəkmək mümkün olmadı.")