from src.student import run_student as run_pipeline
import duckdb
import os
import pytest

def test_full_pipeline_dev_mode(monkeypatch, tmp_path):
    """
    End-to-end integration test enforcing that the entire pipeline 
    works correctly in DEV mode (using static JSON fixtures) without
    any live network calls.
    """
    # 1. Isolate Database
    test_db = str(tmp_path / "test_e2e.duckdb")
    monkeypatch.setenv("DATABASE_PATH", test_db)
    
    # 2. Re-point landing zone to temp dir
    monkeypatch.setattr("src.student.collect.DataCollector.save_raw_json.__defaults__", (test_db,))
    
    # 3. Suppress all plotting so E2E test runs instantly
    monkeypatch.setattr("src.student.eda.EDAEngine.plot_digital_divide", lambda self: None)
    
    # Run the orchestrator
    run_pipeline.run(env="dev")
    
    # Verify Database state
    assert os.path.exists(test_db)
    conn = duckdb.connect(test_db)
    
    # Verify all tables exist and have data
    tables = [row[0] for row in conn.execute("SHOW TABLES").fetchall()]
    assert "silver_grade3_assessments" in tables
    assert "silver_broadband" in tables
    assert "silver_ai_usage" in tables
    assert "gold_digital_divide" in tables
    
    # Verify Silver row counts
    assert conn.execute("SELECT COUNT(*) FROM silver_broadband").fetchone()[0] == 51
    assert conn.execute("SELECT COUNT(*) FROM silver_ai_usage").fetchone()[0] == 51
    
    # Verify Gold table integrity
    gold_df = conn.execute("SELECT * FROM gold_digital_divide").df()
    
    # States that exist in all 3 DEV fixtures should join (at least 40 states)
    assert len(gold_df) >= 40 
    
    # Verify schema contains expected features
    expected_cols = {
        "fips", "state_abbr", "reading_pct_proficient", 
        "broadband_pct_25_3", "hps_pct_ai_use", "connectivity_tier",
        "infra_adoption_gap", "proficiency_gap_vs_national"
    }
    assert expected_cols.issubset(gold_df.columns), "Gold table schema mismatch"
    
    conn.close()
