import json
import pytest
from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


@pytest.fixture
def mock_cache_file():

    """
    Mock the cache file check and its contents.
    """

    cache_data = json.dumps({"data": "mocked_value"})
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data=cache_data)):
        yield


@pytest.fixture
def mock_precompute():

    """
    Mock the precompute_metrics function.
    """

    with patch("routers.pm25.precompute_metrics") as mock_func:
        mock_func.return_value = None
        yield mock_func


@pytest.fixture
def mock_post_air_quality():

    """
    Mock post_air_quality_indicator function.
    """

    with patch("routers.pm25.post_air_quality_indicator", return_value={"result": "success"}):
        yield


@pytest.fixture
def mock_post_pm25_avg():

    """
    Mock post_pm25_averages function.
    """

    with patch("routers.pm25.post_pm25_averages", return_value={"result": "success"}):
        yield


@pytest.fixture
def mock_post_pm25_map():

    """
    Mock post_pm25_map function.
    """
    
    with patch("routers.pm25.post_pm25_map", return_value={"result": "success"}):
        yield
