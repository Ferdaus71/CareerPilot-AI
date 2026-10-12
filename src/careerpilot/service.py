from __future__ import annotations

from careerpilot.matching import compare_resume_job
from careerpilot.recommendations import (
    build_recommendations,
    infer_best_role,
    rank_roles,
    summarize_strengths,
)
from careerpilot.skill_catalog import SKILL_CATEGORIES
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


def _build_category_summary(matched_skills: list[str], missing_skills: list[str]) -> list[dict[str, object]]:
    category_totals: dict[str, dict[str, int]] = {}
    for category, skill_names in SKILL_CATEGORIES.items():
        category_totals[category] = {"matched": 0, "missing": 0}

    for skill in matched_skills:
        for category, skill_names in SKILL_CATEGORIES.items():
            if skill in skill_names:
                category_totals[category]["matched"] += 1

    for skill in missing_skills:
        for category, skill_names in SKILL_CATEGORIES.items():
            if skill in skill_names:
                category_totals[category]["missing"] += 1

    summary: list[dict[str, object]] = []
    for category, totals in category_totals.items():
        if totals["matched"] or totals["missing"]:
            summary.append(
                {
                    "category": category,
                    "matched": totals["matched"],
                    "missing": totals["missing"],
                    "total": totals["matched"] + totals["missing"],
                }
            )

    return summary


def _build_learning_roadmap(missing_skills: list[str]) -> list[str]:
    if not missing_skills:
        return ["Continue refining the strongest matched skills with a small portfolio project and interview practice."]

    roadmap: list[str] = []
    for skill in missing_skills[:4]:
        if skill == "python":
            roadmap.append("Build a Python project that covers automation, APIs, and data processing workflows.")
        elif skill == "sql":
            roadmap.append("Practice SQL joins, window functions, and reporting queries on a realistic dataset.")
        elif skill == "cloud":
            roadmap.append("Deploy a small application on AWS or Azure and document the setup, monitoring, and scaling steps.")
        elif skill == "machine learning":
            roadmap.append("Create a reusable ML workflow with data cleaning, feature engineering, and evaluation metrics.")
        elif skill == "data analysis":
            roadmap.append("Complete a small analysis project with visualizations and a concise business recommendation.")
        elif skill == "docker":
            roadmap.append("Containerize a sample app and document how it runs in local and production environments.")
        else:
            roadmap.append(f"Create a portfolio project that demonstrates {skill} in a real business or technical scenario.")

    return roadmap


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
    best_role = infer_best_role(skill_gap["matched_skills"], skill_gap["missing_skills"])
    recommended_roles = rank_roles(skill_gap["matched_skills"], skill_gap["missing_skills"])
    top_strengths = summarize_strengths(skill_gap["matched_skills"])
    category_summary = _build_category_summary(skill_gap["matched_skills"], skill_gap["missing_skills"])
    learning_roadmap = _build_learning_roadmap(skill_gap["missing_skills"])

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
        "matched_skill_count": len(skill_gap["matched_skills"]),
        "missing_skill_count": len(skill_gap["missing_skills"]),
        "job_skill_count": len(sorted_job_skills),
        "best_role": best_role,
        "recommended_roles": recommended_roles,
        "top_strengths": top_strengths,
        "category_summary": category_summary,
        "learning_roadmap": learning_roadmap,
    }
