from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_pm25_averages_cached(mock_cache_file):

    """
    Test when cache file (aggregated_pm25.json) exists.
    """

    response = client.get("/pm25/averages")
    assert response.status_code == 200
    assert response.json() == {"data": "mocked_value"}


def test_pm25_averages_precompute(mock_precompute):

    """
    Test when cache file (aggregated_pm25.json) is missing, triggering precompute.
    """

    with patch("os.path.exists", return_value=False):
        response = client.get("/pm25/averages")
    assert response.status_code == 200
    assert response.json() == {"message": "Precomputing PM2.5 averages, try again later."}
    assert mock_precompute.called
