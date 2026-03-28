import requests
import json
import os
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, output_dir="data/landing"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_api_data(self, url):
        """Polls the API with error handling."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error polling API: {e}")
            return None

    def save_raw_json(self, data, filename_prefix="raw_data"):
        """Saves raw JSON for auditability."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Data landed at: {filepath}")

if __name__ == "__main__":
    # --- Flag Parsing Logic ---
    parser = argparse.ArgumentParser(description="Ingestion Engine Collector")
    parser.add_argument('--env', choices=['dev', 'prod'], default='dev', 
                        help="Select 'dev' for filler data or 'prod' for live NCES data.")
    args = parser.parse_args()

    collector = DataCollector()

    # Principle of Least Privilege: Default to Dev/Dummy
    if args.env == 'prod':
        target_url = os.getenv("NCES_DATA_ENDPOINT")
        prefix = "nces_grade3_real"
        logger.info("ENVIRONMENT: PROD (Polling live NCES API)")
    else:
        target_url = "https://jsonplaceholder.typicode.com/posts/1"
        prefix = "filler_test_data"
        logger.info("ENVIRONMENT: DEV (Polling dummy filler data)")

    if target_url:
        raw_payload = collector.fetch_api_data(target_url)
        if raw_payload:
            # Handle NCES specific nesting if in prod
            data_to_save = raw_payload['results'] if args.env == 'prod' and 'results' in raw_payload else raw_payload
            collector.save_raw_json(data_to_save, prefix)