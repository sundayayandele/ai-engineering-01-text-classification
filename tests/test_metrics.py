from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_prometheus_metrics_endpoint() -> None:
    client.get("/health/live")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text_classifier_http_requests_total" in response.text
