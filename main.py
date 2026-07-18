import logging
import time # Təkrar cəhd üçün lazımdır
from src.extract import extract_csv, extract_api
from src.transform import transform_data
from src.load import load_data_to_postgres, create_table # create_table-ı da import edirik

# Checkpoint 5: Səliqəli Logging quraşdırılması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("etl_process.log"),
        logging.StreamHandler()
    ]
)

DB_CONN = "host=db dbname=etl_database user=devjoint_user password=password port=5432"
API_URL = "https://jsonplaceholder.typicode.com/users"
CSV_PATH = "data/users.csv"

def run_pipeline():
    logging.info("--- ETL PIPELINE BAŞLADI ---")
    
    # Bazanın hazır olmasını gözləmək üçün 10 dəfə cəhd edirik
    for attempt in range(10):
        try:
            # Step 1: Extract
            csv_data = extract_csv(CSV_PATH)
            api_data = extract_api(API_URL)
            
            # Step 2: Transform
            final_df = transform_data(csv_data, api_data)
            
            # Step 3: Cədvəli yoxla/yarat
            create_table(DB_CONN)
            
            # Step 4: Load & Idempotency
            if not final_df.empty:
                load_data_to_postgres(final_df, DB_CONN)
                logging.info("Pipeline uğurla tamamlandı!")
                return # Uğurlu olsa dövrü qır
            else:
                logging.warning("Yükləmək üçün etibarlı data tapılmadı.")
                return
            
        except Exception as main_error:
            logging.warning(f"Cəhd {attempt+1} uğursuz oldu: {main_error}. 5 saniyə gözləyirəm...")
            time.sleep(5)
            
    logging.critical("Baza hazır olmadı, pipeline dayandırıldı.")

if __name__ == "__main__":
    run_pipeline()