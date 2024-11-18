from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
import requests

client = TestClient(app)

@patch('requests.post')
def test_read_root(mock_post):
    mock_post.return_value.status_code = 200

    response = client.get("/simulate/daily?date=2023-03-20")

    assert response.status_code == 200
