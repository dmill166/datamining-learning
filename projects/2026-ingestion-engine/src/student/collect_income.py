"""
collect_income.py — Census ACS Median Household Income Collector
(The 4th Data Layer: Senior Resolution)

This module fetches 2023 ACS 1-Year Estimates for Median Household Income (B19013).
It serves as the "Ground Truth" confounding variable for the Senior EDA.
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class IncomeCollector:
    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir or "data/landing")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = os.getenv("CENSUS_API_KEY")
        # 2023 ACS 1-Year Estimate: Median Household Income (B19013)
        self.base_url = "https://api.census.gov/data/2023/acs/acs1"

    def fetch(self, env: str = "dev") -> list:
        """Fetches income data from live API or local fixture."""
        if env == "dev":
            return self._fetch_dev()
        return self._fetch_prod()

    def _fetch_dev(self) -> list:
        fixture_path = Path("data/fixtures/census_income.json")
        logger.info("DEV MODE: Reading income fixture → %s", fixture_path)
        if not fixture_path.exists():
            # Fallback to empty if fixture missing
            return []
        with open(fixture_path, "r") as f:
            return json.load(f)

    def _fetch_prod(self) -> list:
        if not self.api_key:
            logger.warning("PROD MODE: Missing CENSUS_API_KEY. Returning empty list.")
            return []

        params = {
            "get": "NAME,B19013_001E",
            "for": "state:*",
            "key": self.api_key
        }

        logger.info("PROD MODE: Fetching ACS 1-Year Median Income (B19013)...")
        resp = requests.get(self.base_url, params=params)
        resp.raise_for_status()
        return resp.json()

    def save_raw_json(self, data: list | dict, filename_prefix: str = "raw_data") -> None:
        """Persists raw data to the landing zone as a timestamped JSON file."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Data landed at: %s", filepath)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Collect Census ACS Income Data")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev")
    args = parser.parse_args()

    collector = IncomeCollector()
    raw_data = collector.fetch(env=args.env)
    if raw_data:
        collector.save(raw_data)
