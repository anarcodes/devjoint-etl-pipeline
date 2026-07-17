# Python-un yüngül versiyasını seçirik
FROM python:3.10-slim

# Konteyner daxilində işçi qovluğu təyin edirik
WORKDIR /app

# Kitabxanaların siyahısını konteynerə kopyalayırıq
COPY requirements.txt .

# Kitabxanaları konteyner daxilində yükləyirik
RUN pip install --no-cache-dir -r requirements.txt

# Bütün layihə fayllarını konteynerə köçürürük
COPY . .

# Konteyner işə düşəndə birbaşa main.py işləsin
CMD ["python", "main.py"]