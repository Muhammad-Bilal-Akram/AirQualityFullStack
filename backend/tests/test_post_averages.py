from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_post_pm25_avg(mock_post_pm25_avg):

    """
    Test successful post request to /pm25/averages.
    """

    response = client.post("/pm25/averages", json={
        "x_point": 10.0, 
        "y_point": 20.0,
        "week_number": 1,
        "month_number": 1,
        "year": 2025
    })
    assert response.status_code == 200
    assert response.json() == {"result": "success"}


def test_post_pm25_avg_error():

    """
    Test /pm25/averages error handling.
    """

    with patch("routers.pm25.post_pm25_averages", side_effect=Exception("Test Error")):
        response = client.post("/pm25/averages", json={
            "x_point": 10.0, 
            "y_point": 20.0,
            "week_number": 1,
            "month_number": 1,
            "year": 2025
        })
        assert response.status_code == 500
        assert response.json() == {"detail": "Test Error"}

