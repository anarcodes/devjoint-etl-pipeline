import logging
import os
from src.extract import extract_csv, extract_api
from src.transform import transform_data
from src.load import load_data_to_postgres

# Checkpoint 5: Səliqəli Logging quraşdırılması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("etl_process.log"),
        logging.StreamHandler() # Həm fayla yazır, həm terminalda göstərir
    ]
)

DB_CONN = "host=localhost dbname=etl_database user=devjoint_user password=secret_password port=5432"
API_URL = "https://jsonplaceholder.typicode.com/users"
CSV_PATH = "data/users.csv"

def run_pipeline():
    logging.info("--- ETL IPELINE BAŞLADI ---")
    
    # Checkpoint 6: Yarımçıq uğursuzluq trick-i (Try-Except blokları ilə qorunma)
    try:
        # Step 1: Extract
        csv_data = extract_csv(CSV_PATH)
        api_data = extract_api(API_URL)
        
        # Step 2: Transform
        final_df = transform_data(csv_data, api_data)
        
        # Step 3 & 4: Load & Idempotency
        if not final_df.empty:
            load_data_to_postgres(final_df, DB_CONN)
        else:
            logging.warning("Yükləmək üçün etibarlı data tapılmadı.")
            
    except Exception as main_error:
        logging.critical(f"Pipeline kritik xəta səbəbindən dayandı: {main_error}")

if __name__ == "__main__":
    run_pipeline()