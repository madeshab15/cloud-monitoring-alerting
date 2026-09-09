from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles

from .monitor import collect_metrics

app = FastAPI(title="Cloud Monitoring & Alerting System", version="2.0.0")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

CPU_LIMIT = 80
MEMORY_LIMIT = 85
DISK_LIMIT = 90


def evaluate_alerts(data):
    alerts = []
    if data["cpu_percent"] > CPU_LIMIT:
        alerts.append("HIGH_CPU")
    if data["memory_percent"] > MEMORY_LIMIT:
        alerts.append("HIGH_MEMORY")
    if data["disk_percent"] > DISK_LIMIT:
        alerts.append("HIGH_DISK")
    return alerts


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/status")
def status():
    data = collect_metrics()
    return {"metrics": data, "alerts": evaluate_alerts(data), "thresholds": {
        "cpu_percent": CPU_LIMIT,
        "memory_percent": MEMORY_LIMIT,
        "disk_percent": DISK_LIMIT,
    }}


@app.get("/metrics")
def metrics():
    # Prometheus scrapes this endpoint. The gauges are updated on every scrape.
    collect_metrics()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/alerts/webhook")
async def alert_webhook(request: Request):
    """Receive Alertmanager webhook payloads for demonstration/logging."""
    payload = await request.json()
    alerts = payload.get("alerts", [])
    return {"received": len(alerts), "status": "accepted"}
