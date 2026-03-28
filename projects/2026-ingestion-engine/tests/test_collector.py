import pytest
from src.collect import DataCollector

@pytest.fixture
def collector():
    """Fixture to initialize collector with a test directory."""
    return DataCollector(output_dir="data/test_landing")

def test_api_status_code_handling(collector):
    """Ensure the collector handles 404/500 errors gracefully."""
    invalid_url = "https://jsonplaceholder.typicode.com/invalid_endpoint"
    data = collector.fetch_api_data(invalid_url)
    assert data is None  # Principle of 'fail-safe' defaults

def test_data_integrity_schema(collector):
    """Data Quality Control: Validate the structure of the incoming JSON."""
    test_url = "https://jsonplaceholder.typicode.com/posts/1"
    data = collector.fetch_api_data(test_url)
    
    # Check for required keys - simulating production schema validation
    expected_keys = {"userId", "id", "title", "body"}
    assert expected_keys.issubset(data.keys()), "API response missing required schema fields"

def test_local_write_privileges(collector, tmp_path):
    """Validate 'Principle of Least Privilege' by testing specific dir writes."""
    collector.output_dir = tmp_path
    test_data = {"test": "payload"}
    collector.save_raw_json(test_data, "test_file")
    
    # Ensure the file exists and is readable
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1
    assert files[0].suffix == ".json"
