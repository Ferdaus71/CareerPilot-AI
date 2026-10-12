from __future__ import annotations

import re

from careerpilot.matching import normalize_text
from careerpilot.skill_catalog import SKILL_ALIASES


def _alias_pattern(alias: str) -> str:
    alias_normalized = alias.strip().lower()
    if not alias_normalized:
        return ""

    parts = [re.escape(part) for part in alias_normalized.split()]
    if len(parts) == 1:
        return rf"(?<![a-z0-9]){parts[0]}(?![a-z0-9])"

    separator = r"\s+".join(parts)
    return rf"(?<![a-z0-9]){separator}(?![a-z0-9])"


def detect_skills(text: str) -> set[str]:
    if not text:
        return set()

    normalized = normalize_text(text)
    if not normalized:
        return set()

    matches: set[str] = set()
    for skill_name, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = _alias_pattern(alias)
            if pattern and re.search(pattern, normalized):
                matches.add(skill_name)
                break
    return matches


def get_skill_gap(resume_text: str, job_text: str) -> dict[str, list[str]]:
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_text)
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    recommendations: list[str] = []
    for skill in missing:
        if skill == "python":
            recommendations.append("Practice Python projects centered on automation, APIs, and data processing.")
        elif skill == "sql":
            recommendations.append("Build SQL queries for joins, aggregations, and reporting across relational datasets.")
        elif skill == "machine learning":
            recommendations.append("Study scikit-learn pipelines, feature engineering, and model evaluation practices.")
        elif skill == "cloud":
            recommendations.append("Learn a cloud provider such as AWS or Azure with deployment and monitoring basics.")
        elif skill == "deep learning":
            recommendations.append("Review neural network fundamentals and complete a small deep-learning project.")
        elif skill == "natural language processing":
            recommendations.append("Explore tokenization, embeddings, and text-classification exercises in NLP.")
        else:
            recommendations.append(f"Develop hands-on practice around {skill} through project work and tutorials.")

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
    }
