from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


def test_post_pm25_map_data(mock_post_pm25_map):

    """
    Test successful post request to /pm25/map-data.
    """

    response = client.post("/pm25/map-data", json={
        "start_date": '2025-01-01', 
        "end_date": '2025-01-31'
    })
    assert response.status_code == 200
    assert response.json() == {"result": "success"}


def test_post_pm25_map_data_error():

    """
    Test /pm25/map-data error handling.
    """

    with patch("routers.pm25.post_pm25_map", side_effect=Exception("Test Error")):
        response = client.post("/pm25/map-data", json={
            "start_date": '2025-01-01', 
            "end_date": '2025-01-31'
        })
        assert response.status_code == 500
        assert response.json() == {"detail": "Test Error"}
