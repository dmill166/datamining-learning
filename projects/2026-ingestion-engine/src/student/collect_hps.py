"""
collect_hps.py — Bronze Layer: Census Household Pulse Survey (HPS) Collector

Ingests state-level AI usage and internet adoption data from the U.S. Census
Bureau's Household Pulse Survey REST API.

Why HPS for the AI Adoption Layer?
    HPS Phase 3.9+ (2023) added AIUSE — the only freely available, state-grain,
    API-accessible measure of AI tool adoption across all 50 states + DC.
    Combined with FCC broadband (infrastructure) and NCES (outcome), it
    completes the pipeline narrative:
        Infrastructure (FCC) → Adoption (HPS) → Outcome (NCES)

Temporal Alignment Note:
    AIUSE data is available from 2023. NCES Grade 3 data is from 2020.
    This gap is a documented engineering trade-off and intentional lecture
    teaching point. See LECTURE_NOTES.md for the full rationale.

Census API Response Format:
    The Census API returns a 2D array: [[headers], [row1], [row2], ...]
    This module normalizes that into a list of dicts and aggregates to state grain.

Key Variables:
    INTRNTAVAIL — Internet availability (1 = always/usually available)
    COMP        — Computer access (1 = yes)
    AIUSE       — AI tools used in past 12 months (1 = yes; Phase 3.9+)
    EST_ST      — State FIPS code (join key)

Dev mode: reads data/fixtures/hps_state_summary.json — zero network calls.

Usage:
    python src/collect_hps.py --env dev
    python src/collect_hps.py --env prod
"""

import argparse
import json
import logging
import os
from collections import defaultdict
from datetime import datetime

import requests
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_DEV_FIXTURE = os.path.join("data", "fixtures", "hps_state_summary.json")
_HPS_BASE_URL = "https://api.census.gov/data/timeseries/hps"

# Binary indicator codes
_INTERNET_YES = "1"
_COMPUTER_YES = "1"
_AI_USE_YES = "1"

# State FIPS → abbreviation + name lookup
_STATE_INFO: dict[str, dict] = {
    "01": {"abbr": "AL", "name": "Alabama"},
    "02": {"abbr": "AK", "name": "Alaska"},
    "04": {"abbr": "AZ", "name": "Arizona"},
    "05": {"abbr": "AR", "name": "Arkansas"},
    "06": {"abbr": "CA", "name": "California"},
    "08": {"abbr": "CO", "name": "Colorado"},
    "09": {"abbr": "CT", "name": "Connecticut"},
    "10": {"abbr": "DE", "name": "Delaware"},
    "11": {"abbr": "DC", "name": "District of Columbia"},
    "12": {"abbr": "FL", "name": "Florida"},
    "13": {"abbr": "GA", "name": "Georgia"},
    "15": {"abbr": "HI", "name": "Hawaii"},
    "16": {"abbr": "ID", "name": "Idaho"},
    "17": {"abbr": "IL", "name": "Illinois"},
    "18": {"abbr": "IN", "name": "Indiana"},
    "19": {"abbr": "IA", "name": "Iowa"},
    "20": {"abbr": "KS", "name": "Kansas"},
    "21": {"abbr": "KY", "name": "Kentucky"},
    "22": {"abbr": "LA", "name": "Louisiana"},
    "23": {"abbr": "ME", "name": "Maine"},
    "24": {"abbr": "MD", "name": "Maryland"},
    "25": {"abbr": "MA", "name": "Massachusetts"},
    "26": {"abbr": "MI", "name": "Michigan"},
    "27": {"abbr": "MN", "name": "Minnesota"},
    "28": {"abbr": "MS", "name": "Mississippi"},
    "29": {"abbr": "MO", "name": "Missouri"},
    "30": {"abbr": "MT", "name": "Montana"},
    "31": {"abbr": "NE", "name": "Nebraska"},
    "32": {"abbr": "NV", "name": "Nevada"},
    "33": {"abbr": "NH", "name": "New Hampshire"},
    "34": {"abbr": "NJ", "name": "New Jersey"},
    "35": {"abbr": "NM", "name": "New Mexico"},
    "36": {"abbr": "NY", "name": "New York"},
    "37": {"abbr": "NC", "name": "North Carolina"},
    "38": {"abbr": "ND", "name": "North Dakota"},
    "39": {"abbr": "OH", "name": "Ohio"},
    "40": {"abbr": "OK", "name": "Oklahoma"},
    "41": {"abbr": "OR", "name": "Oregon"},
    "42": {"abbr": "PA", "name": "Pennsylvania"},
    "44": {"abbr": "RI", "name": "Rhode Island"},
    "45": {"abbr": "SC", "name": "South Carolina"},
    "46": {"abbr": "SD", "name": "South Dakota"},
    "47": {"abbr": "TN", "name": "Tennessee"},
    "48": {"abbr": "TX", "name": "Texas"},
    "49": {"abbr": "UT", "name": "Utah"},
    "50": {"abbr": "VT", "name": "Vermont"},
    "51": {"abbr": "VA", "name": "Virginia"},
    "53": {"abbr": "WA", "name": "Washington"},
    "54": {"abbr": "WV", "name": "West Virginia"},
    "55": {"abbr": "WI", "name": "Wisconsin"},
    "56": {"abbr": "WY", "name": "Wyoming"},
}


class HPSCollector:
    """Ingests Census HPS data and aggregates to state-level adoption metrics."""

    def __init__(self, output_dir: str | None = None) -> None:
        self.output_dir = output_dir or os.path.join("data", "landing")
        self._api_key = os.getenv("CENSUS_API_KEY", "")
        os.makedirs(self.output_dir, exist_ok=True)

    def _parse_response(self, raw: list[list]) -> list[dict]:
        """Converts Census 2D array response to list of dicts.

        Args:
            raw: 2D list where row 0 is headers, rows 1+ are data.

        Returns:
            List of row dicts keyed by column name.
        """
        if not raw or len(raw) < 2:
            return []
        headers = raw[0]
        return [dict(zip(headers, row)) for row in raw[1:]]

    def _aggregate_to_state(self, records: list[dict]) -> list[dict]:
        """Aggregates HPS respondent records to state-level percentage metrics.

        Args:
            records: Individual HPS respondent records with FIPS codes.

        Returns:
            51-row list with pct_internet_access, pct_computer_access, pct_ai_tool_use.
        """
        counts: dict = defaultdict(lambda: {
            "total": 0, "internet": 0, "computer": 0, "ai": 0
        })
        for row in records:
            fips = str(row.get("EST_ST", "")).zfill(2)
            if not fips or fips == "00":
                continue
            counts[fips]["total"] += 1
            if row.get("INTRNTAVAIL") == _INTERNET_YES:
                counts[fips]["internet"] += 1
            if row.get("COMP") == _COMPUTER_YES:
                counts[fips]["computer"] += 1
            if row.get("AIUSE") == _AI_USE_YES:
                counts[fips]["ai"] += 1

        result = []
        for fips, c in sorted(counts.items()):
            total = c["total"] or 1
            info = _STATE_INFO.get(fips, {"abbr": "", "name": ""})
            result.append({
                "state_fips": fips,
                "state_abbr": info["abbr"],
                "state_name": info["name"],
                "pct_internet_access": round(c["internet"] / total * 100, 2),
                "pct_computer_access": round(c["computer"] / total * 100, 2),
                "pct_ai_tool_use": round(c["ai"] / total * 100, 2),
                "survey_year": 2023,
            })
        logger.info("Aggregated HPS data for %d states.", len(result))
        return result

    def fetch_dev(self) -> list[dict]:
        """Reads pre-curated fixture. Zero network calls."""
        logger.info("DEV MODE: Reading HPS fixture → %s", _DEV_FIXTURE)
        with open(_DEV_FIXTURE, "r") as f:
            return json.load(f)

    def fetch_prod(self, survey_year: int = 2023) -> list[dict]:
        """Queries Census HPS API and aggregates to state-level metrics.

        Attempts to fetch AIUSE (AI usage) variable. Falls back to internet/computer
        variables only if AIUSE is not available for the requested year.

        Args:
            survey_year: HPS survey year (2023+ for AIUSE availability).

        Returns:
            List of aggregated state-level dicts, or empty list on failure.
        """
        variables = "INTRNTAVAIL,COMP,AIUSE,EST_ST,WEEK"
        params: dict = {"get": variables, "for": "state:*", "time": survey_year}
        if self._api_key:
            params["key"] = self._api_key

        logger.info("Querying Census HPS API (year=%d) ...", survey_year)
        try:
            resp = requests.get(_HPS_BASE_URL, params=params, timeout=30)
            # Graceful fallback: retry without AIUSE if unavailable for this period
            if resp.status_code == 400 and "AIUSE" in resp.text:
                logger.warning(
                    "AIUSE unavailable for year %d. Retrying without AI variable.",
                    survey_year,
                )
                params["get"] = "INTRNTAVAIL,COMP,EST_ST,WEEK"
                resp = requests.get(_HPS_BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            raw = resp.json()
        except requests.exceptions.RequestException as e:
            logger.error("Census HPS API error: %s", e)
            return []

        records = self._parse_response(raw)
        return self._aggregate_to_state(records)

    def fetch(self, env: str = "dev") -> list[dict]:
        """Dispatches to dev or prod fetch strategy."""
        return self.fetch_dev() if env == "dev" else self.fetch_prod()

    def save_raw_json(self, data: list, filename_prefix: str = "hps_raw") -> None:
        """Persists HPS data to the landing zone."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        logger.info("HPS data landed at: %s", filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Census HPS Technology Adoption Collector")
    parser.add_argument(
        "--env", choices=["dev", "prod"], default="dev",
        help="'dev' reads fixture; 'prod' queries Census HPS API.",
    )
    args = parser.parse_args()
    collector = HPSCollector()
    logger.info("ENVIRONMENT: %s", args.env.upper())
    records = collector.fetch(env=args.env)
    if records:
        collector.save_raw_json(records, f"hps_{args.env}")
    else:
        logger.error("No HPS data retrieved.")
