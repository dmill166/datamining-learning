import duckdb
import pandas as pd

def perform_eda():
    conn = duckdb.connect("data/relational_storage.duckdb")
    # Query to see score distribution by state—simulating "Data Quality Control"
    df = conn.execute("""
        SELECT state_location, AVG(read_test_num_valid) as avg_valid_scores
        FROM stg_ai_adoption_metrics
        GROUP BY state_location
        ORDER BY avg_valid_scores DESC
        LIMIT 10
    """).df()
    print("Top 10 States by Validated Assessment Participation:")
    print(df)
    conn.close()