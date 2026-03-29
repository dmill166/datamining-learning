import json
from unittest.mock import MagicMock

import pytest
import requests

from src.student.collect import DataCollector


@pytest.fixture
def collector(tmp_path):
    """Initializes collector with a safe, temporary output directory."""
    return DataCollector(output_dir=tmp_path)


def test_api_status_code_handling(collector, mocker):
    """Ensure the collector handles 404/500 errors gracefully without crashing."""
    mock_get = mocker.patch("src.student.collect.requests.get")
    mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")

    data = collector.fetch_api_data("https://fake-url.com")
    assert data is None  # Principle of 'fail-safe' defaults


def test_fetch_api_data_success(collector, mocker):
    """Validates successful JSON parsing from a mocked HTTP response."""
    mock_get = mocker.patch("src.student.collect.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_get.return_value = mock_response

    data = collector.fetch_api_data("https://fake-url.com")
    assert data == {"status": "ok"}
    mock_get.assert_called_once()


def test_fetch_all_pages(collector, mocker):
    """Validates the while-loop pagination logic follows 'next' links correctly."""
    mock_get = mocker.patch("src.student.collect.requests.get")
    
    # Mock three sequential pages. The 3rd page has next=None.
    page_1 = MagicMock()
    page_1.json.return_value = {"results": [{"id": 1}], "next": "url2"}
    
    page_2 = MagicMock()
    page_2.json.return_value = {"results": [{"id": 2}], "next": "url3"}
    
    page_3 = MagicMock()
    page_3.json.return_value = {"results": [{"id": 3}], "next": None}

    mock_get.side_effect = [page_1, page_2, page_3]

    results = collector.fetch_all_pages("url1")
    
    assert len(results) == 3
    assert results[0]["id"] == 1
    assert results[2]["id"] == 3
    assert mock_get.call_count == 3


def test_tag_all_students(collector):
    """Validates domain logic: flagging rows where all subgroups == 99."""
    records = [
        # Match (all 9 fields = 99)
        {f: 99 for f in [
            "race", "sex", "lep", "homeless", "migrant",
            "disability", "foster_care", "military_connected", "econ_disadvantaged"
        ]},
        # Mismatch (one field = 1)
        {f: (1 if f == "race" else 99) for f in [
            "race", "sex", "lep", "homeless", "migrant",
            "disability", "foster_care", "military_connected", "econ_disadvantaged"
        ]},
    ]
    
    result = collector.tag_all_students(records)
    assert result[0]["all_students_flag"] is True
    assert result[1]["all_students_flag"] is False


def test_save_raw_json(collector, tmp_path):
    """Validate data persistence logic to the correct landing zone."""
    test_data = [{"test": "payload"}]
    collector.save_raw_json(test_data, "test_file")
    
    files = list(tmp_path.glob("test_file_*.json"))
    assert len(files) == 1
    
    with open(files[0], "r") as f:
        saved_data = json.load(f)
    assert saved_data == test_data
