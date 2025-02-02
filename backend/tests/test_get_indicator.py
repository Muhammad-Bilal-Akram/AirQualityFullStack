from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_air_quality_indicator_cached(mock_cache_file):

    """
    Test when cache file (pm25_indicator.json) exists.
    """

    response = client.get("/pm25/indicator")
    assert response.status_code == 200
    assert response.json() == {"data": "mocked_value"}


def test_air_quality_indicator_precompute(mock_precompute):

    """
    Test when cache file (pm25_indicator.json) is missing, triggering precompute.
    """

    with patch("os.path.exists", return_value=False):
        response = client.get("/pm25/indicator")
    assert response.status_code == 200
    assert response.json() == {"message": "Precomputing PM2.5 indicator, try again later."}
    assert mock_precompute.called
