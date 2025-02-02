from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


def test_pm25_map_cached(mock_cache_file):

    """
    Test when cache file (pm25_map.json) exists.
    """

    response = client.get("/pm25/map-data")
    assert response.status_code == 200
    assert response.json() == {"data": "mocked_value"}


def test_pm25_map_precompute(mock_precompute):

    """
    Test when cache file (pm25_map.json) is missing, triggering precompute.
    """

    with patch("os.path.exists", return_value=False):
        response = client.get("/pm25/map-data")
    assert response.status_code == 200
    assert response.json() == {"message": "Precomputing PM2.5 Map, try again later."}
    assert mock_precompute.called
