import os
import duckdb
import pytest
from src.student.eda import EDAEngine


@pytest.fixture
def engine(tmp_path):
    """Provides EDAEngine tied to an isolated test DuckDB file with mock source data."""
    db_file = tmp_path / "test_eda.duckdb"
    eng = EDAEngine(db_path=db_file)
    
    # Mock the 3 Silver tables so we can test the Gold build
    eng.conn.execute("CREATE TABLE silver_grade3_assessments AS SELECT 8 AS fips, 2020 AS year, 50.0 AS read_pct_prof_midpt, 40.0 AS math_pct_prof_midpt, 100 AS read_test_num_valid, TRUE AS all_students_flag")
    eng.conn.execute("CREATE TABLE silver_broadband AS SELECT '08' AS state_fips, 'CO' AS state_abbr, 'Colorado' AS state_name, 95.0 AS pct_25_3_mbps, 80.0 AS pct_100_20_mbps")
    eng.conn.execute("CREATE TABLE silver_ai_usage AS SELECT '08' AS state_fips, 90.0 AS pct_internet_access, 85.0 AS pct_computer_access, 40.0 AS pct_ai_tool_use")
    
    yield eng
    eng.close()


def test_build_gold_table_success(engine):
    """Tests that the three-way SQL JOIN completes successfully."""
    engine.build_gold_feature_table()
    
    res = engine.conn.execute("SELECT * FROM gold_digital_divide").df()
    assert len(res) == 1
    
    row = res.iloc[0]
    assert row["fips"] == 8
    assert row["state_abbr"] == "CO"
    assert row["broadband_pct_25_3"] == 95.0
    assert row["connectivity_tier"] == "high"
    assert row["hps_pct_ai_use"] == 40.0
    assert row["infra_adoption_gap"] == 5.0  # 95 - 90


def test_build_gold_table_missing_silver_raises(engine):
    """Validates the pre-flight check that all Silver tables are present."""
    engine.conn.execute("DROP TABLE silver_grade3_assessments")
    
    with pytest.raises(RuntimeError, match="Missing Silver tables"):
        engine.build_gold_feature_table()


def test_export_for_ml(engine, tmp_path):
    """Ensures the ML export creates a valid CSV."""
    engine.build_gold_feature_table()
    export_path = tmp_path / "test_export.csv"
    
    engine.export_for_ml(export_path)
    
    assert os.path.exists(export_path)
    with open(export_path, "r") as f:
        content = f.read()
    assert "connectivity_tier" in content
    assert "CO" in content


def test_plot_digital_divide(engine, tmp_path):
    """Ensures Matplotlib/Seaborn graph generation doesn't crash."""
    engine.build_gold_feature_table()
    plot_path = tmp_path / "test_plot.png"
    
    engine.plot_digital_divide(plot_path)
    
    assert os.path.exists(plot_path)
    assert os.path.getsize(plot_path) > 1024  # Ensure it's not a 0-byte file
