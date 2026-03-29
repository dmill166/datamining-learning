"""
collect.py — Bronze Layer: NCES EDFacts Grade 3 Assessment Collector

Polls the Urban Institute Education Data Portal (open REST API, no key required)
for Grade 3 school-district-level reading and math assessment data.

Pagination: The Urban Institute API returns 100 records per page. This module
follows `next` links until exhausted, collecting all district rows.

Subgroup tagging: EDFacts uses numeric code 99 as the "All Students" sentinel.
We tag each record with `all_students_flag` so the Silver layer can filter
cleanly without re-implementing this domain logic downstream.

Usage:
    python src/collect.py --env dev    # dummy data, no API call
    python src/collect.py --env prod   # live NCES EDFacts pagination
"""

import argparse
import json
import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

# EDFacts sentinel: code 99 = "All Students" aggregate (not a demographic subgroup)
_ALL_STUDENTS_CODE = 99
_SUBGROUP_FIELDS = [
    "race", "sex", "lep", "homeless", "migrant",
    "disability", "foster_care", "military_connected", "econ_disadvantaged",
]


class DataCollector:
    """Ingests NCES EDFacts Grade 3 assessment data from the Urban Institute API.

    Dev mode:  fetches a single dummy page from jsonplaceholder.
    Prod mode: paginates through the full EDFacts dataset (~14,586 district rows).
    """

    def __init__(self, output_dir: str | None = None) -> None:
        self.output_dir = output_dir or os.path.join("data", "landing")
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_api_data(self, url: str) -> dict | None:
        """Fetches a single page from a URL with timeout and error handling.

        Args:
            url: Full URL including any query parameters.

        Returns:
            Parsed JSON dict, or None on any failure.
        """
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s", e)
            return None

    def fetch_all_pages(self, base_url: str) -> list[dict]:
        """Paginates through the Urban Institute API following `next` links.

        The API envelope wraps records in a `results` list and sets `next` to
        the URL of the following page (null on the last page).

        Args:
            base_url: Starting endpoint URL.

        Returns:
            Flat list of all result dicts across all pages.
        """
        results: list[dict] = []
        url: str | None = base_url
        page = 1

        while url:
            logger.info("Fetching page %d ...", page)
            payload = self.fetch_api_data(url)
            if not payload:
                logger.warning("Empty response on page %d. Stopping pagination.", page)
                break
            results.extend(payload.get("results", []))
            url = payload.get("next")
            page += 1

        logger.info("Pagination complete. Total records: %d", len(results))
        return results

    @staticmethod
    def _is_all_students(record: dict) -> bool:
        """Returns True when all EDFacts subgroup codes equal 99 (All Students)."""
        return all(record.get(f) == _ALL_STUDENTS_CODE for f in _SUBGROUP_FIELDS)

    def tag_all_students(self, records: list[dict]) -> list[dict]:
        """Appends `all_students_flag` boolean to each record in-place.

        Args:
            records: Raw NCES API result dicts.

        Returns:
            Same records list with `all_students_flag` added to each dict.
        """
        for record in records:
            record["all_students_flag"] = self._is_all_students(record)
        return records

    def save_raw_json(self, data: list | dict, filename_prefix: str = "raw_data") -> None:
        """Persists raw data to the landing zone as a timestamped JSON file.

        Auditability principle: raw data is always saved before transformation.

        Args:
            data: Payload to serialize.
            filename_prefix: Prefix added before the timestamp in the filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Data landed at: %s", filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NCES Grade 3 EDFacts Collector")
    parser.add_argument(
        "--env",
        choices=["dev", "prod"],
        default="dev",
        help="'dev' uses dummy data; 'prod' polls the live NCES API with pagination.",
    )
    args = parser.parse_args()

    collector = DataCollector()

    if args.env == "prod":
        year = os.getenv("NCES_DEFAULT_YEAR", "2020")
        grade = os.getenv("NCES_DEFAULT_GRADE", "3")
        template = os.getenv("NCES_GRADE3_ENDPOINT", "")
        target_url = template.format(year=year, grade=grade)
        logger.info("ENVIRONMENT: PROD — NCES EDFacts (year=%s grade=%s)", year, grade)
        records = collector.fetch_all_pages(target_url)
        records = collector.tag_all_students(records)
        collector.save_raw_json(records, f"nces_grade3_{year}")
    else:
        logger.info("ENVIRONMENT: DEV — Fetching dummy data (no NCES API call)")
        raw = collector.fetch_api_data("https://jsonplaceholder.typicode.com/posts")
        collector.save_raw_json(raw or [], "filler_test_data")