import json
import pytest
from src.student.collect_broadband import BroadbandCollector


@pytest.fixture
def collector(tmp_path):
    """Initializes collector with safe outputs and dummy credentials."""
    # Monkeypatch to avoid real .env interference during tests
    return BroadbandCollector(output_dir=tmp_path)


def test_dev_mode_reads_fixture(collector, mocker):
    """Ensures dev mode skips the API and reads the local JSON array."""
    # Mock the built-in open function to avoid depending on actual file presence
    mock_data = [{"state_fips": "08", "pct_25_3_mbps": 99.9}]
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_data)))
    
    result = collector.fetch(env="dev")
    assert len(result) == 1
    assert result[0]["state_fips"] == "08"


def test_fetch_prod_returns_empty_when_missing_credentials(collector, mocker):
    """Validates defensive check against missing headers."""
    # Force credentials to None
    collector._username = None
    collector._hash_value = None
    
    result = collector.fetch(env="prod")
    assert result == []


def test_prod_three_step_flow(collector, mocker):
    """Mocks the 3 distinct Swagger endpoints needed to download the CSV."""
    collector._username = "test_user"
    collector._hash_value = "test_hash"
    
    mock_get = mocker.patch("src.student.collect_broadband.BroadbandCollector._get")
    mock_download = mocker.patch("src.student.collect_broadband.BroadbandCollector._download_csv")
    
    # Step 1: List dates
    mock_get.side_effect = [
        {"data": [{"as_of_date": "2023-06"}, {"as_of_date": "2023-12"}]},  # Call 1
        {"data": [{"subcategory": "Summary by Geography Type", "file_id": "file_123"}]} # Call 2
    ]
    
    # Step 3: Download returns shaped data
    mock_download.return_value = [{"state_fips": "08"}]
    
    result = collector.fetch(env="prod")
    
    assert len(result) == 1
    assert mock_get.call_count == 2
    mock_download.assert_called_once_with("file_123")
