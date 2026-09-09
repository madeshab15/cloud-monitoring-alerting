from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_status_shape():
    response = client.get("/status")
    assert response.status_code == 200
    body = response.json()
    assert "metrics" in body
    assert "alerts" in body
    assert "thresholds" in body
    assert set(body["metrics"]) == {"cpu_percent", "memory_percent", "disk_percent", "process_count"}


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "system_cpu_percent" in response.text
    assert "system_memory_percent" in response.text
    assert "system_disk_percent" in response.text


def test_webhook():
    response = client.post("/alerts/webhook", json={"alerts": [{"labels": {"alertname": "HIGH_CPU"}}]})
    assert response.status_code == 200
    assert response.json()["received"] == 1
