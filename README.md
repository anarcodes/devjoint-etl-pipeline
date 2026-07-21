# Python ETL Pipeline (1-ci Həftə Tapşırığı)

Bu layihə Python, PostgreSQL və Docker istifadə edilərək qurulmuş, istehsal mühitinə hazır (production-ready), xətalara dözümlü və idempotent Extract-Transform-Load (ETL) pipeline-dır. Layihə Data Engineering təcrübə proqramının 1-ci həftəsi üçün nəzərdə tutulmuş bütün əsas tələbləri və checkpoints əhatə edir.

---

## 🏗️ Arxitektura & Məlumat axını

Pipeline iki müxtəlif mənbədən (yerli CSV faylı və xarici Open API) məlumatları ardıcıl şəkildə çıxarır, ciddi təmizləmə və unifikasiya qaydalarını tətbiq edir və nəticəni idempotent `UPSERT` əməliyyatları ilə PostgreSQL instansiyasına yükləyir.

```text
+-------------------+      +-------------------+
|   Local CSV File  |      |   Public Open API |
+---------+---------+      +---------+---------+
          |                          |
          | (Extract)                | (Extract)
          v                          v
+----------------------------------------------+
|          Python ETL Engine (Pandas)          |
|  - Type casting & Null handling              |  <--- Python Logging Module
|  - Common Key Merging / Joining              |       (INFO / WARNING / ERROR)
|  - Row-level Isolation & Error Handling      |
+---------------------+------------------------+
                      |
                      | (Load via Batch Upsert / ON CONFLICT)
                      v
        +----------------------------+
        |   PostgreSQL Database      | <-- Idempotency Verified
        +----------------------------+
```

---

## 🚀 Əsas Xüsusiyyətlər və İcra Olunmuş Mərhələlər

**Mərhələ 1: Ardıcıl Məlumat Çıxarışı (`Extract`)**
    *   Yerli verilənlər bazasından (`.csv`) xammal biznes göstəricilərini çıxarır və onları ictimai REST API vasitəsilə əldə edilən canlı məlumatlarla ardıcıl olaraq zənginləşdirir.

**Mərhələ 2: Məlumatın Təmizlənməsi və Unifikasiyası (`Transform`)**
    *   Ciddi tip çevrilmələrini (type casting) tətbiq edir, çatışmayan/null dəyərləri müəyyən edib doldurur və hər iki məlumat dəstini strukturlaşdırılmış ortaq identifikator açarı vasitəsilə birləşdirir.

**Mərhələ 3: Yüksək Məhsuldarlıqlı Toplu Yükləmə (`Load`)**
    *   Sətir-sətir iterasiyanın ləngliyindən qaçınır. Verilənlər bazası ilə şəbəkə dövriyyəsini minimuma endirmək üçün optimallaşdırılmış toplu icra (`psycopg2 / SQLAlchemy` batch processing) istifadə edir.

**Mərhələ 4: İdempotentlik (`Idempotency Trick`)**
    *   Pipeline-ın eyni məlumat mənbəyinə qarşı təkrar işə salınması zamanı tam olaraq eyni sayda **sətir** verəcəyinə zəmanət verir. Bu, hədəf cədvəl məhdudiyyətləri və `ON CONFLICT (id) DO UPDATE` (Upsert) rutinləri vasitəsilə təmin edilir.

**Mərhələ 5: Production üçün Logging (`Logging`)**
    *   Bütün standart `print()` funksiyaları Python-un daxili logging modulu ilə əvəz edilmişdir. `INFO, WARNING` və `ERROR` səviyyələri üzrə icra mərhələlərini izləyən strukturlaşdırılmış loq formatı konfiqurasiya edilmişdir.

**Mərhələ 6: Xətalara Qarşı Davamlılıq (`Partial Failure Trick`)**
    *   Sətir səviyyəsində xəta izolyasiyası ilə konfiqurasiya edilmişdir. Korlanmış sətirlər, yanlış sxem formaları və ya səhv məlumat tipləri aşkarlanır, sistem izləyicisində loqlaşdırılır və bütün pipeline-ın dayanmasına səbəb olmadan ötürülür.

---

## ▶️ Layihəni işə salma addımları

1. Konteynerləri aktiv edirik:
```bash
docker-compose up -d
```
2. Bazaya daxil olub sətir sayını və məlumatları yoxlamaq üçün:
    
    ```bash
    docker exec -it etl_postgres psql -U devjoint_user -d etl_database
    ```

    2.1. Bazada bu sorğunu icra edin:

    ```sql
    SELECT * FROM final_users_report;
    ```

---

## 🛠️ İstifadə olunan texnologiyalar

*   **Language:** Python 3.10+
*   **Data Processing:** Pandas / NumPy
*   **Database:** PostgreSQL 15+
*   **Containerization:** Docker & Docker Compose
*   **Orchestration Support:** Apache Airflow ready
