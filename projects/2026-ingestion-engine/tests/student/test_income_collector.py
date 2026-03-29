"""
test_income_collector.py — Unit tests for the Census ACS Income Collector
"""

import pytest
import json
from pathlib import Path
from src.student.collect_income import IncomeCollector

@pytest.fixture
def income_collector(tmp_path):
    return IncomeCollector(output_dir=tmp_path)

def test_dev_mode_reads_fixture(income_collector, mocker):
    """Verify that dev mode uses the static JSON fixture."""
    mock_fixture_data = [["NAME", "B19013_001E", "state"], ["Test State", "50000", "99"]]
    
    # Mock the file read
    mocker.patch("pathlib.Path.exists", return_value=True)
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_fixture_data)))
    
    data = income_collector.fetch(env="dev")
    assert data == mock_fixture_data
    assert data[1][1] == "50000"

def test_fetch_prod_returns_empty_when_missing_credentials(income_collector, mocker):
    """Verify that prod mode handles missing API keys gracefully."""
    mocker.patch("os.getenv", return_value=None)
    # Re-init to pickup mocked env
    income_collector.api_key = None
    
    data = income_collector.fetch(env="prod")
    assert data == []

def test_prod_api_call_structure(income_collector, mocker):
    """Verify that the Census API call is constructed correctly."""
    mocker.patch("os.getenv", return_value="fake_key_123")
    income_collector.api_key = "fake_key_123"
    
    mock_resp = mocker.Mock()
    mock_resp.json.return_value = [["header"], ["data"]]
    mock_resp.raise_for_status.return_value = None
    mock_get = mocker.patch("requests.get", return_value=mock_resp)
    
    data = income_collector.fetch(env="prod")
    
    # Check URL and Params
    args, kwargs = mock_get.call_args
    assert "api.census.gov" in args[0]
    assert kwargs["params"]["get"] == "NAME,B19013_001E"
    assert kwargs["params"]["key"] == "fake_key_123"
    assert data == [["header"], ["data"]]

def test_save_income_json(income_collector, tmp_path):
    """Verify that data is saved to the correct landing zone."""
    mock_data = [["NAME"], ["Alabama"]]
    path = income_collector.save(mock_data, "test_income.json")
    
    assert path.exists()
    assert path.name == "test_income.json"
    with open(path, "r") as f:
        saved_data = json.load(f)
    assert saved_data == mock_data
