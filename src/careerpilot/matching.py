from __future__ import annotations

import re
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_text(text: str) -> str:
    if text is None:
        return ""
    text = text.strip()
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def calculate_similarity(resume_text: str, job_text: str) -> float:
    if resume_text is None or job_text is None:
        raise ValueError("Both resume text and job description text are required.")

    resume_clean = normalize_text(resume_text)
    job_clean = normalize_text(job_text)

    if not resume_clean or not job_clean:
        raise ValueError("Both resume text and job description text are required.")

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_clean, job_clean])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return float(score)


def compare_resume_job(resume_text: str, job_text: str) -> dict[str, Any]:
    score = calculate_similarity(resume_text, job_text)
    return {
        "score": round(float(score), 4),
        "percentage": round(float(score) * 100, 2),
        "description": "Similarity between resume and job description calculated with TF-IDF and cosine similarity.",
    }
