import psycopg2
from psycopg2.extras import execute_values
import logging

def load_data_to_postgres(df, conn_string):
    logging.info("Verilənlər bazasına yükləmə (Load) başladı...")
    
    # Dataframe-i tuple siyahısına çeviririk (Batch yükləmə üçün)
    data_tuples = [tuple(x) for x in df[['id', 'name', 'email', 'city', 'company']].to_numpy()]
    
    # PostgreSQL üçün UPSERT sorğusu (ON CONFLICT)
    # Əgər ID artıq varsa, məlumatları yeniləyir (Dublikat yaratmır!)
    query = """
        INSERT INTO final_users_report (id, name, email, city, company)
        VALUES %s
        ON CONFLICT (id) 
        DO UPDATE SET 
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            city = EXCLUDED.city,
            company = EXCLUDED.company,
            updated_at = CURRENT_TIMESTAMP;
    """
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Sətir sətir yox, BATCH şəklində hamısını bir dəfəyə göndəririk
        execute_values(cursor, query, data_tuples)
        
        conn.commit()
        logging.info(f"Uğurla {len(data_tuples)} sətir bazaya yükləndi (və ya yeniləndi).")
    except Exception as e:
        conn.rollback()
        logging.error(f"Bazaya yükləmə zamanı xəta baş verdi: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()