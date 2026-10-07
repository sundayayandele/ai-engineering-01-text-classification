from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liveness() -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rejects_empty_text() -> None:
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
