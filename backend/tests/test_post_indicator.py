from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_post_air_quality(mock_post_air_quality):

    """
    Test successful post request to /pm25/indicator.
    """

    response = client.post("/pm25/indicator", json={"x_point": 10.0, "y_point": 20.0})
    assert response.status_code == 200
    assert response.json() == {"result": "success"}


def test_post_air_quality_error():

    """
    Test /pm25/indicator error handling.
    """

    with patch("routers.pm25.post_air_quality_indicator", side_effect=Exception("Test Error")):
        response = client.post("/pm25/indicator", json={"x_point": 10.0, "y_point": 20.0})
        assert response.status_code == 500
        assert response.json() == {"detail": "Test Error"}
