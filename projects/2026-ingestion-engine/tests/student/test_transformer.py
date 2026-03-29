import duckdb
import pandas as pd
import pytest

from src.student.transform import DataTransformer


@pytest.fixture
def transformer(tmp_path):
    """Provides a transformer connected to an isolated test DuckDB file."""
    db_file = tmp_path / "test_db.duckdb"
    # Need to override os.getenv dynamically or monkeypatch it.
    # We will instantiate and then overwrite its connection for isolation.
    t = DataTransformer()
    t.conn.close()
    t.conn = duckdb.connect(db_file)
    yield t
    t.close()


def test_flatten_json(transformer):
    """Ensure JSON is flattened properly with lowercase, snake_case cols."""
    raw = [{"First.Name": "Alice", "AGE": 30}]
    df = transformer.flatten_json(raw)
    
    assert list(df.columns) == ["first_name", "age"]
    assert df.iloc[0]["first_name"] == "Alice"


def test_empty_dataframe_guard(transformer):
    """Empty datasets should trip the guard and not write to DB."""
    transformer.load_grade3_to_silver([])
    tables = [row[0] for row in transformer.conn.execute("SHOW TABLES").fetchall()]
    assert "silver_grade3_assessments" not in tables


def test_load_grade3_to_silver(transformer):
    """Ensures NCES data is typed and loaded into the silver table."""
    records = [{
        "leaid": "123", "lea_name": "Test", "fips": "08", "year": 2020,
        "grade_edfacts": 3, "read_test_num_valid": 100,
        "read_test_pct_prof_midpt": "45.5", "math_test_pct_prof_midpt": None,
        "all_students_flag": True
    }]
    
    transformer.load_grade3_to_silver(records)
    
    res = transformer.conn.execute("SELECT * FROM silver_grade3_assessments").fetchall()
    assert len(res) == 1
    # Verify type coercion — fips should be integer in DB
    idx_fips = 2
    assert res[0][idx_fips] == 8


def test_load_broadband_to_silver(transformer):
    """Ensures FCC data is zero-padded and loaded correctly."""
    records = [{
        "state_fips": "8", # Single digit to test zfill
        "state_abbr": "CO", "state_name": "Colorado",
        "pct_25_3_mbps": "90.5", "pct_100_20_mbps": "80.0",
        "reporting_period": "2022-12"
    }]
    
    transformer.load_broadband_to_silver(records)
    
    res = transformer.conn.execute("SELECT * FROM silver_broadband").fetchall()
    assert len(res) == 1
    # Verify zero-padding (VARCHAR)
    assert res[0][0] == "08"


def test_load_hps_to_silver(transformer):
    """Ensures Census HPS data is typed correctly."""
    records = [{
        "state_fips": "08", "state_abbr": "CO", "state_name": "Colorado",
        "pct_internet_access": "85.0", "pct_computer_access": "75.0",
        "pct_ai_tool_use": "40.2", "survey_year": 2023
    }]
    
    transformer.load_hps_to_silver(records)
    
    res = transformer.conn.execute("SELECT * FROM silver_ai_usage").fetchall()
    assert len(res) == 1
    assert res[0][0] == "08"
