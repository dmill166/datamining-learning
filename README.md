# MSU Denver: Data Science & ML Guest Lecture (April 2026)
**Presenter:** Dakota Matthew Hollmann  
**Title:** Senior Data Engineer @ Charter Spectrum  
**Topic:** Real-World Data Lifecycles: From Nested JSON to ML-Ready Features

---

## 🚀 Overview
This repository serves as the technical companion for my guest lecture in **CS 3120 (Machine Learning)**. It demonstrates how we bridge the gap between "Raw Data" and "Model Inputs" using engineering best practices like modularity, automated polling, and unit testing.

### Featured Project: AI & Education Ingestion Engine
A Python-based ETL pipeline that:
1. **Polls** public APIs (Pew Research / NCES) for AI sentiment and educational metrics.
2. **Transforms** complex, nested JSON into a relational schema.
3. **Validates** data integrity through a formal testing suite (inspired by the 141+ tests implemented at Charter).

## 📁 Repository Structure
* `/projects/2026-ingestion-engine/`: The core demonstration code.
    * `src/`: Production-style Python modules for collection and transformation.
    * `data/`: Local landing zone for raw and processed data.
    * `tests/`: Automated validation scripts.
* `/archive-msu-2021/`: Legacy coursework and Data Mining activities from my time as an MSU Denver student.

## 🛠 Tech Stack
* **Language:** Python 3.13+
* **Orchestration:** Modular Scripting (Simulating Airflow/Step Functions)
* **Storage:** JSON (Raw) $\to$ SQLite/DuckDB (Relational)
* **Testing:** PyTest

---
*“Do or do not - there is no try.”*
