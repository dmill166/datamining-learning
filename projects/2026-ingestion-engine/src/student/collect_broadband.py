"""
collect_broadband.py — Bronze Layer: FCC Broadband Data Collection (BDC) Collector

Ingests state-level broadband availability data from the FCC National Broadband Map.

Authentication (prod mode only):
    Per the BDC Public Data API Swagger spec, auth uses TWO request headers:
        username   — FCC User Registration email  (FCC_USERNAME in .env)
        hash_value — Token from Manage API Access  (FCC_HASH_VALUE in .env)
    This is NOT a Bearer token. See docs/bdc-public-data-api-swagger.yaml.

Prod mode executes a three-step FCC BDC flow:
    Step 1: GET /map/listAsOfDates          → select most recent reporting period
    Step 2: GET /map/downloads/listAvailabilityData/{date}?category=State
                                            → get file_id for state summary CSV
    Step 3: GET /map/downloads/downloadFile/availability/{file_id}
                                            → download and parse CSV

Dev mode: reads data/fixtures/broadband_state_summary.json — zero network calls.

Usage:
    python src/collect_broadband.py --env dev
    python src/collect_broadband.py --env prod
"""

import argparse
import csv
import io
import json
import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_DEV_FIXTURE = os.path.join("data", "fixtures", "broadband_state_summary.json")
_FCC_BASE = os.getenv("FCC_BDC_BASE_URL", "https://broadbandmap.fcc.gov/api/public")


class BroadbandCollector:
    """Ingests FCC BDC state-level broadband availability data.

    Dev mode:  reads static fixture, zero network calls.
    Prod mode: executes three-step FCC BDC API flow using header-based auth.
    """

    def __init__(self, output_dir: str | None = None) -> None:
        self.output_dir = output_dir or os.path.join("data", "landing")
        self._username = os.getenv("FCC_USERNAME")
        self._hash_value = os.getenv("FCC_HASH_VALUE")
        os.makedirs(self.output_dir, exist_ok=True)

    def _auth_headers(self) -> dict:
        """Returns FCC BDC authentication headers per Swagger spec."""
        return {"username": self._username, "hash_value": self._hash_value}

    def _get(self, path: str, params: dict | None = None) -> dict | None:
        """Authenticated GET to the FCC BDC API.

        Args:
            path: API path relative to _FCC_BASE.
            params: Optional query parameters.

        Returns:
            Parsed JSON dict, or None on failure.
        """
        url = f"{_FCC_BASE}{path}"
        try:
            resp = requests.get(url, headers=self._auth_headers(), params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error("FCC BDC API error [%s]: %s", path, e)
            return None

    def _most_recent_date(self) -> str | None:
        """Step 1: Returns the most recent available as-of date string."""
        result = self._get("/map/listAsOfDates")
        if not result or not result.get("data"):
            logger.error("Could not retrieve FCC BDC as-of dates.")
            return None
        dates = [d.get("as_of_date") for d in result["data"] if d.get("as_of_date")]
        most_recent = sorted(dates, reverse=True)[0]
        logger.info("FCC BDC most recent date: %s", most_recent)
        return most_recent

    def _state_file_id(self, as_of_date: str) -> str | None:
        """Step 2: Retrieves file_id for the state-level summary CSV."""
        result = self._get(
            f"/map/downloads/listAvailabilityData/{as_of_date}",
            params={"category": "State"},
        )
        if not result or not result.get("data"):
            logger.error("No state-level files found for date: %s", as_of_date)
            return None
        for entry in result["data"]:
            if "Summary by Geography Type" in entry.get("subcategory", ""):
                fid = str(entry.get("file_id") or entry.get("id", ""))
                logger.info("State summary file_id: %s", fid)
                return fid
        logger.error("State summary file not found in FCC listing.")
        return None

    def _download_csv(self, file_id: str) -> list[dict]:
        """Step 3: Downloads state CSV and normalizes to a list of dicts."""
        url = f"{_FCC_BASE}/map/downloads/downloadFile/availability/{file_id}"
        try:
            resp = requests.get(url, headers=self._auth_headers(), timeout=60)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to download FCC file %s: %s", file_id, e)
            return []

        rows = []
        for row in csv.DictReader(io.StringIO(resp.text)):
            rows.append({
                "state_fips": str(row.get("state_fips", "")).zfill(2),
                "state_abbr": row.get("state_abbr", ""),
                "state_name": row.get("state_name", ""),
                "pct_25_3_mbps": float(row.get("pct_25_3_mbps") or 0),
                "pct_100_20_mbps": float(row.get("pct_100_20_mbps") or 0),
                "reporting_period": row.get("as_of_date", ""),
            })
        logger.info("Parsed %d state broadband rows from FCC CSV.", len(rows))
        return rows

    def fetch_dev(self) -> list[dict]:
        """Reads pre-curated fixture. Zero network calls.

        Raises:
            FileNotFoundError: If fixture file is missing.
        """
        logger.info("DEV MODE: Reading broadband fixture → %s", _DEV_FIXTURE)
        with open(_DEV_FIXTURE, "r") as f:
            return json.load(f)

    def fetch_prod(self) -> list[dict]:
        """Executes three-step FCC BDC flow: dates → file listing → CSV download."""
        if not self._username or not self._hash_value:
            logger.error(
                "FCC credentials missing. Set FCC_USERNAME and FCC_HASH_VALUE in .env."
            )
            return []
        date = self._most_recent_date()
        if not date:
            return []
        fid = self._state_file_id(date)
        if not fid:
            return []
        return self._download_csv(fid)

    def fetch(self, env: str = "dev") -> list[dict]:
        """Dispatches to dev or prod fetch strategy."""
        return self.fetch_dev() if env == "dev" else self.fetch_prod()

    def save_raw_json(self, data: list, filename_prefix: str = "broadband_raw") -> None:
        """Persists broadband data to the landing zone."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Broadband data landed at: %s", filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FCC BDC Broadband Collector")
    parser.add_argument(
        "--env", choices=["dev", "prod"], default="dev",
        help="'dev' reads fixture; 'prod' calls the FCC BDC API.",
    )
    args = parser.parse_args()
    collector = BroadbandCollector()
    logger.info("ENVIRONMENT: %s", args.env.upper())
    records = collector.fetch(env=args.env)
    if records:
        collector.save_raw_json(records, f"broadband_{args.env}")
    else:
        logger.error("No broadband data retrieved.")
