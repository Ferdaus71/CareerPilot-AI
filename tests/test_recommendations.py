from __future__ import annotations

from careerpilot.recommendations import (
    build_recommendations,
    infer_best_role,
    summarize_strengths,
)
from careerpilot.skills import detect_skills, get_skill_gap


def test_detect_skills_handles_empty_input() -> None:
    assert detect_skills("") == set()
    assert detect_skills("   ") == set()


def test_get_skill_gap_handles_no_missing_skills() -> None:
    resume = "Python, SQL, and cloud engineering experience."
    job = "Python and SQL."

    gap = get_skill_gap(resume, job)
    assert gap["matched_skills"] == ["python", "sql"]
    assert gap["missing_skills"] == []
    assert gap["recommendations"] == []


def test_build_recommendations_for_empty_and_cloud_roles() -> None:
    assert "already aligns well" in build_recommendations([])[0].lower()

    recommendations = build_recommendations(["cloud", "python"])
    assert recommendations
    assert any("Cloud Engineer" in item for item in recommendations)


def test_infer_best_role_and_strengths() -> None:
    matched = ["python", "sql"]
    missing = ["cloud"]

    assert infer_best_role(matched, missing) == "Data Analyst"
    strengths = summarize_strengths(matched)
    assert "sql" in strengths
    assert "python" in strengths
