from __future__ import annotations

from careerpilot.matching import compare_resume_job
from careerpilot.recommendations import build_recommendations
from careerpilot.skills import detect_skills, get_skill_gap


def _build_match_summary(
    similarity: dict[str, object],
    matched_skills: list[str],
    missing_skills: list[str],
    job_skills: list[str],
) -> dict[str, object]:
    percentage = float(similarity["percentage"])
    if percentage >= 75:
        status = "strong"
        label = "Strong match"
    elif percentage >= 50:
        status = "moderate"
        label = "Moderate match"
    else:
        status = "weak"
        label = "Early-stage match"

    coverage = 0.0
    if job_skills:
        coverage = round((len(matched_skills) / len(job_skills)) * 100, 1)

    focus = ", ".join(missing_skills[:3]) if missing_skills else "no major gaps remain"
    summary = (
        f"{label}: {percentage:.1f}% similarity and {coverage:.1f}% skill coverage. "
        f"Most relevant gaps are {focus}."
    )

    return {
        "status": status,
        "label": label,
        "coverage": coverage,
        "summary": summary,
    }


def build_analysis_result(resume_text: str, job_text: str) -> dict[str, object]:
    similarity = compare_resume_job(resume_text, job_text)
    skill_gap = get_skill_gap(resume_text, job_text)
    career_focus = build_recommendations(skill_gap["missing_skills"])
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_text)
    sorted_resume_skills = sorted(resume_skills)
    sorted_job_skills = sorted(job_skills)
    match_summary = _build_match_summary(
        similarity,
        skill_gap["matched_skills"],
        skill_gap["missing_skills"],
        sorted_job_skills,
    )

    return {
        "similarity": similarity,
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "recommendations": skill_gap["recommendations"],
        "career_focus": career_focus,
        "resume_skills": sorted_resume_skills,
        "job_skills": sorted_job_skills,
        "match_summary": match_summary,
        "match_status": match_summary["status"],
        "skill_coverage": match_summary["coverage"],
    }
