import psycopg2
from psycopg2.extras import execute_values
import logging

def create_table(conn_string):
    """Cədvəli yoxlayır, yoxdursa yaradır."""
    query = """
    CREATE TABLE IF NOT EXISTS final_users_report (
        id INT PRIMARY KEY,
        name TEXT,
        email TEXT,
        city TEXT,
        company TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        logging.error(f"Cədvəl yaradılarkən xəta baş verdi: {e}")
        raise e
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def load_data_to_postgres(df, conn_string):
    logging.info("Verilənlər bazasına yükləmə (Load) başladı...")
    
    # Dataframe-i tuple siyahısına çeviririk (Batch yükləmə üçün)
    data_tuples = [tuple(x) for x in df[['id', 'name', 'email', 'city', 'company']].to_numpy()]
    
    # PostgreSQL üçün UPSERT sorğusu (ON CONFLICT)
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
    
    # Dəyişənləri əvvəlcədən təyin edirik
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Sətir sətir yox, BATCH şəklində hamısını bir dəfəyə göndəririk
        execute_values(cursor, query, data_tuples)
        
        conn.commit()
        logging.info(f"Uğurla {len(data_tuples)} sətir bazaya yükləndi (və ya yeniləndi).")
        
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Bazaya yükləmə zamanı xəta baş verdi: {e}")
        raise e
    finally:
        # Dəyişənlərin mövcud olduğunu yoxlayıb bağlayırıq
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()