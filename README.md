# Robust Python ETL Pipeline (Week 1 Assignment)

A production-ready, fault-tolerant, and idempotent **Extract-Transform-Load (ETL)** pipeline built with Python, PostgreSQL, and Docker. This project satisfies all the core requirements and edge-case checkpoints for the Week 1 Data Engineering internship milestone.

---

## 🏗️ Architecture & Data Flow

The pipeline sequentially extracts data from two heterogeneous sources (a local CSV file and an external Open API), applies robust cleansing and unification rules, and batches the result into a PostgreSQL instance using idempotent `UPSERT` operations.

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

## 🚀 Key Features & Checkpoints Met

*   **Checkpoint 1: Sequential Extraction (`Extract`)**
    *   Extracts raw business metrics from local data sheets (`.csv`) and enriches them sequentially with live data fetched via HTTP requests from a public REST API.
*   **Checkpoint 2: Data Cleansing & Unification (`Transform`)**
    *   Enforces strict type casting, isolates and fills missing/null values, and merges both datasets seamlessly using a structured common identifier key.
*   **Checkpoint 3: High-Performance Batch Loading (`Load`)**
    *   Avoids sluggish row-by-row iteration. Utilizes optimized bulk execution (`psycopg2` / `SQLAlchemy` batch processing) to minimize network roundtrips to the database.
*   **Checkpoint 4: Strict Idempotency (`Idempotency Trick`)**
    *   Engineered to guarantee that **re-running the pipeline against the same source data yields exactly the same row count**. Handled natively via target table constraints and `ON CONFLICT (id) DO UPDATE` (Upsert) routines.
*   **Checkpoint 5: Production Logging (`Logging`)**
    *   Replaced all native `print()` statements with Python’s built-in `logging` module. Configured structured log layouts tracking timestamped execution phases across `INFO`, `WARNING`, and `ERROR` thresholds.
*   **Checkpoint 6: Graceful Fault Tolerance (`Partial Failure Trick`)**
    *   Configured with row-level error isolation. Corrupted lines, invalid schema shapes, or malformed data types are intercepted, logged into the system tracker, and skipped without halting or crashing the overall ingestion pipeline.

---

## 🛠️ Technology Stack

*   **Language:** Python 3.10+
*   **Data Processing:** Pandas / NumPy
*   **Database:** PostgreSQL 15+
*   **Containerization:** Docker & Docker Compose
*   **Orchestration Support:** Apache Airflow ready
