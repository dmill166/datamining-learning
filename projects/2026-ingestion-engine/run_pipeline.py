import sys
import os
import logging

# Ensure the src directory is accessible for modular imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from collect import DataCollector
from transform import DataTransformer

# Setup basic production-style logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AI & Education Ingestion Pipeline")
    
    # 1. Collection Phase (Bronze/Raw Layer)
    # We will use the placeholder for now; swap for real API logic later
    test_url = "https://jsonplaceholder.typicode.com/posts" 
    collector = DataCollector()
    
    logger.info("Polling API for raw JSON...")
    raw_payload = collector.fetch_api_data(test_url)
    
    if not raw_payload:
        logger.error("Pipeline aborted: Failed to retrieve data from API.")
        return

    collector.save_raw_json(raw_payload, "api_ingest")
    
    # 2. Transformation Phase (Silver/Relational Layer)
    logger.info("Initializing Transformation Engine...")
    transformer = DataTransformer()
    
    try:
        # Standardizing the nested JSON into a relational structure
        flattened_df = transformer.flatten_json(raw_payload)
        
        # Loading into DuckDB to showcase SQL-ready data
        transformer.load_to_relation(flattened_df, "stg_ai_adoption_metrics")
        logger.info("Pipeline Execution Successful: Data is ready for analysis.")
        
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
    finally:
        transformer.close()

if __name__ == "__main__":
    main()
