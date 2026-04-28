import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("accelerator-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="DevOps Accelerator Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/pipelines/run")
def run_pipeline(pipeline_id: str, branch: str = "main"):
    logger.info(f"Triggering pipeline {pipeline_id} on branch {branch}")
    return {"status": "Pipeline Triggered", "run_id": "run_882"}

@app.get("/pipelines/history")
def get_pipeline_history():
    return [
        {"id": "run-001", "pipeline": "Auth-Service", "status": "SUCCESS", "duration": "4m 12s", "timestamp": "2026-04-28 14:00:00"},
        {"id": "run-042", "pipeline": "Data-Hub", "status": "FAILED", "duration": "1m 45s", "timestamp": "2026-04-28 12:00:00"},
        {"id": "run-101", "pipeline": "Edge-WAF", "status": "IN_PROGRESS", "duration": "2m 30s", "timestamp": "2026-04-28 15:45:00"}
    ]

@app.post("/platform/provision")
def provision_platform(catalog_item_id: str, params: dict):
    logger.info(f"Provisioning platform item {catalog_item_id} with params {params}")
    return {"status": "Provisioning Job Enqueued", "job_id": "job_992"}

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "global_maturity_index": 0.842,
        "dora_velocity_rating": "Elite",
        "reliability_score": 0.98,
        "compliance_drift": "NONE"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_active_pipelines": 124,
        "avg_deployment_frequency": "14.2 / week",
        "change_failure_rate": "4.2%",
        "platform_adoption": "92%"
    }
