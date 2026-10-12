from __future__ import annotations

import fitz
from fastapi.testclient import TestClient

from careerpilot.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "careerpilot"


def test_json_analysis_endpoint() -> None:
    response = client.post(
        "/api/analyze-json",
        json={
            "resume_text": "Python developer with SQL and data analytics experience.",
            "job_description": "Need Python, SQL, machine learning, and cloud skills.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] > 0
    assert payload["percentage"] > 0
    assert payload["missing_skills"]
    assert payload["match_status"] in {"strong", "moderate", "weak"}
    assert payload["match_summary"]
    assert 0 <= payload["skill_coverage"] <= 100
    assert payload["matched_skill_count"] >= 0
    assert payload["missing_skill_count"] >= 0
    assert payload["job_skill_count"] >= 0
    assert payload["best_role"]
    assert payload["top_strengths"]
    assert "resume_text" not in payload


def test_uploaded_resume_analysis_endpoint() -> None:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Python developer with SQL and analytics background.")
    pdf_bytes = document.tobytes()
    document.close()

    response = client.post(
        "/api/analyze",
        files={"resume_file": ("resume.pdf", pdf_bytes, "application/pdf")},
        data={"job_description": "Senior Python engineer with SQL and cloud requirements."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] > 0
    assert payload["matched_skills"]
    assert payload["match_status"] in {"strong", "moderate", "weak"}
    assert payload["match_summary"]
    assert 0 <= payload["skill_coverage"] <= 100
    assert payload["matched_skill_count"] >= 0
    assert payload["missing_skill_count"] >= 0
    assert payload["job_skill_count"] >= 0
    assert payload["best_role"]
    assert payload["top_strengths"]
    assert "resume_text" not in payload


def test_invalid_inputs_are_rejected() -> None:
    response = client.post(
        "/api/analyze-json",
        json={"resume_text": "", "job_description": ""},
    )
    assert response.status_code == 400

    response = client.post(
        "/api/analyze",
        files={"resume_file": ("resume.txt", b"not a pdf", "text/plain")},
        data={"job_description": "Python developer"},
    )
    assert response.status_code == 400
