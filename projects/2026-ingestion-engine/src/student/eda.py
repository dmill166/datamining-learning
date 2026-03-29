"""
eda.py — Digital Divide Exploratory Data Analysis (EDA) Engine.

Executes the following operations:
1. Validates presence of all three Silver Layer tables.
2. Materializes the Gold table via ANSI-compliant SQL execution.
3. Generates descriptive statistics and prints them to stdout.
4. Generates a Seaborn scatter plot mapping broadband and AI usage against reading.
5. Exports the ML-ready dataset to CSV.
"""

import os
import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from src.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


class EDAEngine:
    """Gold-layer analytics engine for the Digital Divide pipeline."""

    def __init__(self, db_path: str | None = None) -> None:
        """Connects to the DuckDB instance. Defaults to DATABASE_PATH or data/education_metrics.duckdb."""
        self.db_path = db_path or os.getenv("DATABASE_PATH", os.path.join("data", "education_metrics.duckdb"))
        self.conn = duckdb.connect(self.db_path)
        logger.info("EDAEngine connected to: %s", self.db_path)

    def build_gold_feature_table(self) -> None:
        """Materializes gold_digital_divide via sql/gold_digital_divide.sql."""
        tables_df = self.conn.execute("SELECT table_name FROM information_schema.tables").df()
        tables = tables_df["table_name"].tolist()
        required = {"silver_grade3_assessments", "silver_broadband", "silver_ai_usage"}
        
        if not required.issubset(set(tables)):
            raise RuntimeError(f"Missing Silver tables. Found: {tables}")
            
        with open(os.path.join("sql", "student", "gold_digital_divide.sql"), "r") as f:
            query = f.read()
            
        self.conn.execute(query)
        logger.info("Gold table 'gold_digital_divide' materialized successfully.")

    def run_correlation_analysis(self) -> pd.DataFrame:
        """Calculates Pearson correlation between numeric features and reading proficiency."""
        df = self.conn.execute("SELECT * FROM gold_digital_divide").df()
        numeric_cols = df.select_dtypes(include=["number"]).columns
        corr = df[numeric_cols].corr()[["reading_pct_proficient"]].sort_values(by="reading_pct_proficient", ascending=False)
        return corr

    def run_validation_stats(self) -> None:
        """Prints EDA summaries to terminal."""
        df = self.conn.execute("SELECT * FROM gold_digital_divide").df()
        logger.info("Generated Master Dataset with %d continuous/categorical variables.", len(df.columns))
        
        tier_avg = df.groupby("connectivity_tier")["reading_pct_proficient"].mean().reset_index()
        print("\n── Average Reading by Connectivity Tier ──")
        print(tier_avg.to_string(index=False))
        print("=" * 60 + "\n")

        corr = self.run_correlation_analysis()
        print("── Pearson Correlation (each feature vs. reading_pct_proficient) ──")
        print(corr.T.rename(columns={0: "Pearson r"}).to_string())
        print()

    def plot_digital_divide(self, output_path: str | None = None) -> None:
        """Produces a Seaborn scatter plot: broadband % vs. reading proficiency."""
        output_path = output_path or os.path.join("data", "digital_divide.png")
        
        df = self.conn.execute("""
            SELECT state_abbr, reading_pct_proficient, broadband_pct_25_3,
                   hps_pct_ai_use, connectivity_tier
            FROM gold_digital_divide
        """).df()
        
        plt.figure(figsize=(10, 6))
        ax = sns.scatterplot(
            data=df,
            x="broadband_pct_25_3",
            y="reading_pct_proficient",
            hue="connectivity_tier",
            palette="viridis"
        )
        sns.regplot(
            data=df,
            x="broadband_pct_25_3",
            y="reading_pct_proficient",
            scatter=False,
            color="black",
            ax=ax
        )
        
        plt.title("Grade 3 Reading Proficiency vs. Broadband Coverage")
        plt.xlabel("Broadband Coverage (25/3 Mbps %)")
        plt.ylabel("State Average Reading Proficiency (%)")
        
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info("Scatter plot saved -> %s", output_path)

    def export_for_ml(self, output_path: str | None = None) -> None:
        """Exports the finalized Gold feature table to a CSV for downstream ML models."""
        output_path = output_path or os.path.join("data", "gold_export.csv")
        df = self.conn.execute("SELECT * FROM gold_digital_divide").df()
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info("ML export saved -> %s", output_path)

    def close(self) -> None:
        self.conn.close()
        logger.info("DuckDB connection closed.")

if __name__ == "__main__":
    engine = EDAEngine()
    engine.build_gold_feature_table()
    engine.run_validation_stats()
    engine.plot_digital_divide()
    engine.export_for_ml()
    engine.close()