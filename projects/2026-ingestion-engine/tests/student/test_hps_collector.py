import json
import pytest
import requests
from src.student.collect_hps import HPSCollector


@pytest.fixture
def collector(tmp_path):
    return HPSCollector(output_dir=tmp_path)


def test_dev_mode_reads_fixture(collector, mocker):
    """Ensure fast, offline reading in dev mode."""
    mock_data = [{"est_st": "08", "pct_internet_access": 85.0}]
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_data)))
    
    result = collector.fetch(env="dev")
    assert len(result) == 1


def test_parse_response_2d_array(collector):
    """Validates the logic that converts a Census 2D array into list of dicts."""
    raw = [
        ["EST_ST", "COMP", "AIUSE"],
        ["08", "1", "1"],
        ["06", "1", "0"]
    ]
    result = collector._parse_response(raw)
    assert len(result) == 2
    assert result[0] == {"EST_ST": "08", "COMP": "1", "AIUSE": "1"}


def test_aggregate_to_state_logic(collector):
    """Validates the respondent-level to state-level aggregation math."""
    records = [
        {"EST_ST": "08", "INTRNTAVAIL": "1", "COMP": "1", "AIUSE": "1"},
        {"EST_ST": "08", "INTRNTAVAIL": "1", "COMP": "0", "AIUSE": "0"},
        # Invalid FIPS should be ignored
        {"EST_ST": "00", "INTRNTAVAIL": "1", "COMP": "1", "AIUSE": "1"}
    ]
    
    result = collector._aggregate_to_state(records)
    
    assert len(result) == 1
    state = result[0]
    assert state["state_fips"] == "08"
    assert state["pct_internet_access"] == 100.0  # 2/2
    assert state["pct_computer_access"] == 50.0   # 1/2
    assert state["pct_ai_tool_use"] == 50.0       # 1/2


def test_prod_fallback_on_missing_aiuse(collector, mocker):
    """Tests the graceful degradation if AIUSE column is requested for pre-2023 data."""
    mock_get = mocker.patch("src.student.collect_hps.requests.get")
    
    # First call fails because AIUSE doesn't exist
    resp_1 = mocker.MagicMock()
    resp_1.status_code = 400
    resp_1.text = "error: unknown variable 'AIUSE'"
    
    # Second call succeeds without AIUSE
    resp_2 = mocker.MagicMock()
    resp_2.status_code = 200
    resp_2.json.return_value = [["EST_ST"], ["08"]]
    
    mock_get.side_effect = [resp_1, resp_2]
    
    result = collector.fetch_prod(survey_year=2021)
    
    assert mock_get.call_count == 2
    assert len(result) == 1
    # Check that AI usage gracefully falls to 0 when not in payload
    assert result[0]["pct_ai_tool_use"] == 0.0
