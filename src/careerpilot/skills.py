from __future__ import annotations

import re

from careerpilot.matching import normalize_text

SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "python": ("python", "py"),
    "sql": ("sql", "postgres", "postgresql", "mysql"),
    "machine learning": ("machine learning", "ml", "ml engineering"),
    "data analysis": ("data analysis", "analytics", "data analytics"),
    "deep learning": ("deep learning", "dl", "neural networks"),
    "natural language processing": ("natural language processing", "nlp", "language processing"),
    "data visualization": ("data visualization", "visualization", "tableau", "power bi"),
    "cloud": ("cloud", "aws", "azure", "gcp"),
    "docker": ("docker", "containers"),
    "software engineering": ("software engineering", "swe", "engineering"),
    "pandas": ("pandas", "python pandas"),
    "scikit-learn": ("scikit-learn", "sklearn"),
    "excel": ("excel", "microsoft excel"),
    "statistics": ("statistics", "statistical analysis"),
    "communication": ("communication", "stakeholder communication"),
    "project management": ("project management", "agile", "scrum"),
}


def detect_skills(text: str) -> set[str]:
    if not text:
        return set()

    normalized = normalize_text(text)
    if not normalized:
        return set()

    matches: set[str] = set()
    for skill_name, aliases in SKILL_ALIASES.items():
        pattern_parts = [re.escape(alias) for alias in aliases]
        combined = "|".join(pattern_parts)
        if re.search(rf"(?<![a-z0-9])(?:{combined})(?![a-z0-9])", normalized):
            matches.add(skill_name)
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
