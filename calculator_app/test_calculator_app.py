from fastapi.testclient import TestClient
from calculator_app import app

client = TestClient(app)


def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
