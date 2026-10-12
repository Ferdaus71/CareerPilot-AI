from __future__ import annotations

from careerpilot.matching import compare_resume_job
from careerpilot.recommendations import build_recommendations
from careerpilot.skills import detect_skills, get_skill_gap


def build_analysis_result(resume_text: str, job_text: str) -> dict[str, object]:
    similarity = compare_resume_job(resume_text, job_text)
    skill_gap = get_skill_gap(resume_text, job_text)
    career_focus = build_recommendations(skill_gap["missing_skills"])
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_text)

    return {
        "similarity": similarity,
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "recommendations": skill_gap["recommendations"],
        "career_focus": career_focus,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
    }
