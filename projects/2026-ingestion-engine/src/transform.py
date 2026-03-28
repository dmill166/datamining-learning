import json
import os
import pandas as pd
import duckdb
from dotenv import load_dotenv

# Load environment variables for Principle of Least Privilege
load_dotenv()

class DataTransformer:
    def __init__(self):
        self.db_path = os.getenv("DATABASE_PATH", "data/default.duckdb")
        self.conn = duckdb.connect(self.db_path)

    def flatten_json(self, json_data):
        """
        Logic to flatten complex nested structures.
        Mirroring the logic used for massive-scale telemetry.
        """
        # Using Pandas json_normalize for robust flattening of nested lists/dicts
        df = pd.json_normalize(json_data)
        
        # PEP 8: Clean column names (lowercase, no spaces)
        df.columns = [c.replace(".", "_").lower() for c in df.columns]
        return df

    def load_to_relation(self, df, table_name):
        """Loads flattened dataframe into DuckDB."""
        if df.empty:
            print("Transformation Alert: Dataframe is empty. Skipping load.")
            return

        # Data Quality Control: Ensure the table exists or create it
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df WHERE 1=0")
        self.conn.append(table_name, df)
        
        print(f"Successfully loaded {len(df)} rows into table: {table_name}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    transformer = DataTransformer()
    
    # Example logic: Walking through the 'landing' directory
    landing_zone = "data/landing"
    if os.path.exists(landing_zone):
        for file in os.listdir(landing_zone):
            if file.endswith(".json"):
                with open(os.path.join(landing_zone, file), 'r') as f:
                    raw_data = json.load(f)
                    flattened_df = transformer.flatten_json(raw_data)
                    transformer.load_to_relation(flattened_df, "stg_api_data")
    
    transformer.close()
