# Cloud Monitoring & Automated Alerting System 

A beginner-friendly DevOps/cloud monitoring project that collects system metrics, exposes them to Prometheus, visualizes them in Grafana, and evaluates threshold alerts through Prometheus Alertmanager.

## Features
- CPU, memory, disk and process-count monitoring using `psutil`
- FastAPI REST endpoints: `/`, `/health`, `/status`
- Prometheus-compatible `/metrics` endpoint
- Prometheus alert rules for high CPU, memory and disk usage
- Alertmanager routing with a webhook receiver
- Pre-provisioned Grafana datasource and dashboard
- Docker Compose orchestration for API + Prometheus + Alertmanager + Grafana
- Automated pytest tests

## Architecture

`Host/Container metrics -> FastAPI -> Prometheus -> Alert rules -> Alertmanager -> Webhook`

`Prometheus -> Grafana dashboard`

## Run with Docker

Prerequisite: Docker Desktop with Compose.

```bash
docker compose up --build
```

Open:
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Status JSON: http://localhost:8000/status
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Grafana: http://localhost:3000

Grafana's Prometheus datasource and dashboard are provisioned automatically. Default Grafana credentials are typically `admin/admin` on a fresh local container, subject to the image's current first-login flow.

## Run locally without Docker

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest -q
```

## Important implementation note
The application does not send email/SMS directly. Prometheus evaluates the rules and Alertmanager handles alert routing. The included webhook receiver demonstrates the notification handoff. In a production deployment, replace or extend the receiver with Slack, email, PagerDuty, Teams, etc.

## Interview explanation
**Problem:** Cloud servers can fail or become slow when CPU, memory, or disk resources are exhausted.

**Solution:** This service periodically exposes resource metrics to Prometheus. Prometheus stores the time series and evaluates alert rules. Alertmanager groups/routes alerts, while Grafana provides dashboards for operators.

**Why Docker?** It packages the API and monitoring stack consistently and makes the project easy to run on another machine.

**Cloud extension:** Deploy the containers on AWS ECS/EC2, or replace host metrics with cloud metrics from AWS CloudWatch. Terraform and GitHub Actions can be added for infrastructure and CI/CD.

## Custom Frontend Dashboard

The project includes a clean, responsive white dashboard served by FastAPI at `http://localhost:8000/`. It displays CPU, memory, disk, running processes, active alerts, and the monitoring stack. The dashboard refreshes system status every 10 seconds and is intentionally simple for demonstration and interview use.

### run cases

#to check prometheus is running use 
up
#to see all available metric names use
{__name__=~".+"}
#Scrape meaning : Prometheus collects/reads metrics from a monitoring target at regular intervals.
scrape_samples_scraped
#for cpu metrics
process_cpu_seconds_total
#this gives accurate cpu usage percentage
rate(process_cpu_seconds_total[5m]) * 100
#for memory metrics
process_resident_memory_bytes
#for memory usage
process_resident_memory_bytes / 1024 / 1024



grafana
email:admin
password:admin123
