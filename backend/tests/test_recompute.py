from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


def test_recompute_pm25(mock_precompute):

    """
    Test recompute manual triggers precompute metrics
    """

    response = client.post("/pm25/recompute")
    assert response.status_code == 200
    assert response.json() == {"message": "PM2.5 data recomputed successfully"}
    assert mock_precompute.called
