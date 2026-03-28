# Speaker Notes: Real-World Data Engineering (CS 3120)

## Why Grade 3? (The "Business" Logic)
Before writing code, a Senior Engineer must understand *why* the data matters to the stakeholder (in this case, the ML Model).
* **The Literacy Pivot:** Grade 3 is the developmental milestone where students shift from "learning to read" to "reading to learn".
* **The Predictor:** According to the **Annie E. Casey Foundation**, students not proficient in reading by the end of 3rd grade are 4x more likely to drop out of high school.
* **Data Quality:** This dataset was chosen because it provides a high "fill rate" (minimal nulls), which is essential for stable ML training.

## The Pipeline Architecture
1. **Bronze (Raw):** API Polling via `collect.py`.
2. **Silver (Relational):** JSON Flattening via `transform.py`.
3. **Gold (Analytics):** SQL Joins via DuckDB.

## Environment Toggling (The Senior Approach)
* **Dev Mode:** `python src/collect.py --env dev` 
    * Uses `jsonplaceholder.typicode.com` to verify network and file I/O without hitting rate limits.
* **Prod Mode:** `python src/collect.py --env prod`
    * Uses the NCES API to pull real Grade 3 metrics.