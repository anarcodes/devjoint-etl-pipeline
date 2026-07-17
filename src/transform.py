import pandas as pd
import logging
import re

# Sadə email yoxlama funksiyası (Regex)
def is_valid_email(email):
    if pd.isna(email):
        return False
    # Standart email formatı yoxlanışı
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))

def transform_data(csv_df, api_df):
    logging.info("Data Transformasiyası başladı...")
    
    # API datalarının strukturu düzəldilir
    api_extracted = pd.DataFrame([{
        'id': item['id'],
        'city': item['address']['city'],
        'company': item['company']['name']
    } for item in api_df.to_dict(orient='records')])
    
    csv_df['id'] = pd.to_numeric(csv_df['id'], errors='coerce')
    api_extracted['id'] = pd.to_numeric(api_extracted['id'], errors='coerce')
    
    merged_df = pd.merge(csv_df, api_extracted, on='id', how='inner')
    
    # ─── XƏTA İDARƏETMƏSİ VƏ VALIDASIYA HİSSƏSİ ───
    valid_rows = []
    
    for index, row in merged_df.iterrows():
        # Əgər ID və ya Name yoxdursa, yaxud email səhvdirsə
        if pd.isna(row['id']) or pd.isna(row['name']) or not is_valid_email(row['email']):
            # BÜTÜN PİPELİNE-I ÇÖKDÜRMÜRÜK, sadəcə xətanı loglayıb davam edirik!
            logging.warning(f"⚠️ Sətir {index} xarabdır və keçid almadı! Data: {dict(row)}")
            continue
        
        valid_rows.append(row)
    
    # Əgər etibarlı sətirlər varsa, DataFrame-ə geri çeviririk
    if valid_rows:
        cleaned_df = pd.DataFrame(valid_rows)
    else:
        cleaned_df = pd.DataFrame(columns=merged_df.columns)
        
    logging.info(f"Transformasiya tamamlandı. Keçən sağlam sətir sayısı: {len(cleaned_df)}")
    return cleaned_df