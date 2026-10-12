from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from careerpilot.pdf_extractor import extract_pdf_text
from careerpilot.service import build_analysis_result

app = FastAPI(title="CareerPilot AI API", version="0.1.0")


class AnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalysisResponse(BaseModel):
    score: float
    percentage: float
    matched_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]
    career_focus: list[str]
    match_status: str
    match_summary: str
    skill_coverage: float
    matched_skill_count: int
    missing_skill_count: int
    job_skill_count: int


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "careerpilot"}


@app.post("/api/analyze-json", response_model=AnalysisResponse)
def analyze_payload(payload: AnalysisRequest) -> AnalysisResponse:
    if not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    analysis = build_analysis_result(payload.resume_text, payload.job_description)
    similarity = analysis["similarity"]
    return AnalysisResponse(
        score=float(similarity["score"]),
        percentage=float(similarity["percentage"]),
        matched_skills=list(analysis["matched_skills"]),
        missing_skills=list(analysis["missing_skills"]),
        recommendations=list(analysis["recommendations"]),
        career_focus=list(analysis["career_focus"]),
        match_status=str(analysis["match_status"]),
        match_summary=str(analysis["match_summary"]["summary"]),
        skill_coverage=float(analysis["skill_coverage"]),
        matched_skill_count=int(analysis["matched_skill_count"]),
        missing_skill_count=int(analysis["missing_skill_count"]),
        job_skill_count=int(analysis["job_skill_count"]),
    )


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_uploaded_resume(
    resume_file: Annotated[UploadFile, File(...)],
    job_description: Annotated[str, Form(...)],
) -> AnalysisResponse:
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    file_bytes = await resume_file.read()
    if not resume_file.filename or not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        resume_text = extract_pdf_text(file_bytes, resume_file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    analysis = build_analysis_result(resume_text, job_description)
    similarity = analysis["similarity"]
    return AnalysisResponse(
        score=float(similarity["score"]),
        percentage=float(similarity["percentage"]),
        matched_skills=list(analysis["matched_skills"]),
        missing_skills=list(analysis["missing_skills"]),
        recommendations=list(analysis["recommendations"]),
        career_focus=list(analysis["career_focus"]),
        match_status=str(analysis["match_status"]),
        match_summary=str(analysis["match_summary"]["summary"]),
        skill_coverage=float(analysis["skill_coverage"]),
        matched_skill_count=int(analysis["matched_skill_count"]),
        missing_skill_count=int(analysis["missing_skill_count"]),
        job_skill_count=int(analysis["job_skill_count"]),
    )
