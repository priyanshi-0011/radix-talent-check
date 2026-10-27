
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RADIX Talent Check",
    version="1.0.0",
    description="Talent readiness scoring API for RADIX Module 4",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/team/v1/health")
def health_check():
    return {"status": "ok"}

from backend.benchmarks import get_real_benchmark_status


@app.get("/api/team/v1/talent-check/benchmark-status")
def benchmark_status():
    return get_real_benchmark_status()

from fastapi import UploadFile, File, Form, HTTPException
import json

from backend.benchmarks import get_synthetic_benchmark
from backend.models import SKILL_CATEGORIES
from backend.scoring import calculate_readiness


@app.post("/api/team/v1/talent-check/evaluate")
async def evaluate_talent(
    profile_file: UploadFile = File(...),
    company_file: UploadFile = File(...),
    benchmark_mode: str = Form(...),
):
    if benchmark_mode not in ("synthetic", "real"):
        raise HTTPException(
            status_code=422,
            detail="benchmark_mode must be synthetic or real",
        )

    if benchmark_mode == "real":
        raise HTTPException(
            status_code=503,
            detail="Authorized organizer source is not configured",
        )

    try:
        profile = json.loads(await profile_file.read())
        company = json.loads(await company_file.read())
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(
            status_code=422,
            detail="Profile and company files must contain valid JSON",
        )

    if not isinstance(profile, dict) or not isinstance(company, dict):
        raise HTTPException(
            status_code=422,
            detail="Both JSON files must contain JSON objects",
        )

    if profile.get("schema_version") != "TEAM-V1":
        raise HTTPException(
            status_code=422,
            detail="Profile schema_version must be TEAM-V1",
        )

    if company.get("schema_version") != "TEAM-V1":
        raise HTTPException(
            status_code=422,
            detail="Company schema_version must be TEAM-V1",
        )

    if company.get("source_mode") != "synthetic":
        raise HTTPException(
            status_code=422,
            detail="Practice company must be labelled synthetic",
        )

    ratings = profile.get("ratings")
    levels = company.get("levels")

    if not isinstance(ratings, dict) or not isinstance(levels, dict):
        raise HTTPException(
            status_code=422,
            detail="Profile ratings and company levels must be objects",
        )

    try:
        result = calculate_readiness(ratings, levels)
    except (ValueError, TypeError) as error:
        raise HTTPException(status_code=422, detail=str(error))

    result["company"] = company.get("company")
    result["company_id"] = company.get("id")
    result["profile_id"] = profile.get("id")
    result["profile_revision"] = profile.get("revision")
    result["notice"] = company.get("notice")

    return result
