"""
transform.py — Silver Layer: Data Transformation Engine

Flattens Bronze-layer JSON into normalized Silver tables in DuckDB.
Each loader applies schema selection, type coercion, an empty-dataset guard,
and an `ingested_at` audit timestamp before persisting to DuckDB.

Silver Tables:
    silver_grade3_assessments  — NCES EDFacts, district grain
    silver_broadband           — FCC BDC, state grain
    silver_ai_usage            — Census HPS, state grain

Principle of Least Privilege:
    DATABASE_PATH is read exclusively from .env. No hardcoded paths.
"""

import json
import logging
import os

import duckdb
import pandas as pd
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class DataTransformer:
    """Transforms Bronze JSON into typed Silver DuckDB tables.

    Follows a consistent pattern for each Silver table:
        1. Convert records to DataFrame
        2. Select and rename to stable Silver schema
        3. Coerce column types (null-safe)
        4. Add `ingested_at` audit timestamp
        5. Guard against empty DataFrames (data quality control)
        6. Upsert into DuckDB
    """

    def __init__(self) -> None:
        self.db_path = os.getenv("DATABASE_PATH", os.path.join("data", "default.duckdb"))
        self.conn = duckdb.connect(self.db_path)
        logger.info("DuckDB connected: %s", self.db_path)

    def flatten_json(self, json_data: list | dict) -> pd.DataFrame:
        """Flattens JSON into a normalized DataFrame with sanitized column names.

        Args:
            json_data: Raw payload — list of records or a single dict.

        Returns:
            DataFrame with lowercase, underscore-separated column names.
        """
        if isinstance(json_data, dict):
            json_data = [json_data]
        df = pd.json_normalize(json_data)
        df.columns = [c.replace(".", "_").lower() for c in df.columns]
        return df

    def _guard_empty(self, df: pd.DataFrame, table_name: str) -> bool:
        """Data quality control: warns and returns True if DataFrame is empty."""
        if df.empty:
            logger.warning(
                "Transformation Alert: Empty DataFrame for '%s'. Skipping load.",
                table_name,
            )
            return True
        return False

    def _upsert_table(self, df: pd.DataFrame, table_name: str) -> None:
        """Creates table schema if absent, then appends rows from DataFrame."""
        self.conn.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} AS "
            f"SELECT * FROM df WHERE 1=0"
        )
        self.conn.append(table_name, df)
        logger.info("Loaded %d rows → %s", len(df), table_name)

    def load_grade3_to_silver(self, records: list[dict]) -> None:
        """Transforms NCES EDFacts records → silver_grade3_assessments.

        Preserves district-level grain. State-level aggregation is deferred
        to the Gold layer (weighted average by student count in SQL).
        The `all_students_flag` field — pre-tagged by DataCollector — is
        retained here to enable clean filtering in the Gold JOIN.

        Args:
            records: Raw NCES result dicts with `all_students_flag` appended.
        """
        table_name = "silver_grade3_assessments"
        if not records:
            logger.warning("No NCES records. Skipping %s.", table_name)
            return

        df = pd.DataFrame(records)
        column_map = {
            "leaid": "leaid",
            "lea_name": "lea_name",
            "fips": "fips",
            "year": "year",
            "grade_edfacts": "grade_edfacts",
            "read_test_num_valid": "read_test_num_valid",
            "read_test_pct_prof_midpt": "read_pct_prof_midpt",
            "math_test_pct_prof_midpt": "math_pct_prof_midpt",
            "all_students_flag": "all_students_flag",
        }
        present = {k: v for k, v in column_map.items() if k in df.columns}
        df = df[list(present.keys())].rename(columns=present)

        df["fips"] = pd.to_numeric(df["fips"], errors="coerce").astype("Int64")
        df["read_pct_prof_midpt"] = pd.to_numeric(df["read_pct_prof_midpt"], errors="coerce")
        df["math_pct_prof_midpt"] = pd.to_numeric(df["math_pct_prof_midpt"], errors="coerce")
        df["ingested_at"] = pd.Timestamp.now()

        if self._guard_empty(df, table_name):
            return
        self._upsert_table(df, table_name)

    def load_broadband_to_silver(self, records: list[dict]) -> None:
        """Transforms FCC BDC records → silver_broadband.

        State-level grain. FIPS codes are zero-padded to ensure consistent
        two-character strings for joining with Census and derived data.

        Args:
            records: List of FCC BDC normalized state row dicts.
        """
        table_name = "silver_broadband"
        if not records:
            logger.warning("No broadband records. Skipping %s.", table_name)
            return

        df = pd.DataFrame(records)
        column_map = {
            "state_fips": "state_fips",
            "state_abbr": "state_abbr",
            "state_name": "state_name",
            "pct_25_3_mbps": "pct_25_3_mbps",
            "pct_100_20_mbps": "pct_100_20_mbps",
            "reporting_period": "reporting_period",
        }
        present = {k: v for k, v in column_map.items() if k in df.columns}
        df = df[list(present.keys())].rename(columns=present)

        df["state_fips"] = df["state_fips"].astype(str).str.zfill(2)
        df["pct_25_3_mbps"] = pd.to_numeric(df["pct_25_3_mbps"], errors="coerce")
        df["pct_100_20_mbps"] = pd.to_numeric(df["pct_100_20_mbps"], errors="coerce")
        df["ingested_at"] = pd.Timestamp.now()

        if self._guard_empty(df, table_name):
            return
        self._upsert_table(df, table_name)

    def load_hps_to_silver(self, records: list[dict]) -> None:
        """Transforms Census HPS records → silver_ai_usage.

        State-level grain. This is the "Adoption" layer bridging the FCC
        infrastructure data and the NCES educational outcome data.

        Args:
            records: List of aggregated HPS state-level dicts.
        """
        table_name = "silver_ai_usage"
        if not records:
            logger.warning("No HPS records. Skipping %s.", table_name)
            return

        df = pd.DataFrame(records)
        column_map = {
            "state_fips": "state_fips",
            "state_abbr": "state_abbr",
            "state_name": "state_name",
            "pct_internet_access": "pct_internet_access",
            "pct_computer_access": "pct_computer_access",
            "pct_ai_tool_use": "pct_ai_tool_use",
            "survey_year": "survey_year",
        }
        present = {k: v for k, v in column_map.items() if k in df.columns}
        df = df[list(present.keys())].rename(columns=present)

        df["state_fips"] = df["state_fips"].astype(str).str.zfill(2)
        for col in ("pct_internet_access", "pct_computer_access", "pct_ai_tool_use"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df["ingested_at"] = pd.Timestamp.now()

        if self._guard_empty(df, table_name):
            return
        self._upsert_table(df, table_name)

    def load_to_relation(self, df: pd.DataFrame, table_name: str) -> None:
        """Generic loader retained for backward compatibility.

        Prefer the typed Silver loaders for new datasets.
        """
        if self._guard_empty(df, table_name):
            return
        self._upsert_table(df, table_name)

    def load_income_to_silver(self, raw_data: list) -> None:
        """Normalizes raw Census ACS income data into DuckDB."""
        if not raw_data:
            logger.warning("Empty income data. Skipping silver load.")
            return

        # Header: ["NAME", "B19013_001E", "state"]
        header = raw_data[0]
        rows = raw_data[1:]
        df = pd.DataFrame(rows, columns=header)
        
        # Rename and cast
        df = df.rename(columns={
            "B19013_001E": "median_income",
            "state": "state_fips"
        })
        df["median_income"] = pd.to_numeric(df["median_income"], errors="coerce")
        
        self.conn.execute("CREATE TABLE IF NOT EXISTS silver_income AS SELECT * FROM df WHERE 1=0")
        self.conn.execute("INSERT INTO silver_income SELECT * FROM df")
        logger.info("Loaded %d rows → silver_income", len(df))

    def close(self) -> None:
        """Closes the DuckDB connection."""
        self.conn.close()
        logger.info("DuckDB connection closed.")


if __name__ == "__main__":
    transformer = DataTransformer()
    landing_zone = os.path.join("data", "landing")
    if os.path.exists(landing_zone):
        for fname in os.listdir(landing_zone):
            if fname.endswith(".json"):
                with open(os.path.join(landing_zone, fname), "r") as f:
                    raw = json.load(f)
                df = transformer.flatten_json(raw if isinstance(raw, list) else [raw])
                transformer.load_to_relation(df, "stg_api_data")
    transformer.close()
