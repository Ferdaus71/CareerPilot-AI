from __future__ import annotations

import fitz

from careerpilot.matching import calculate_similarity, compare_resume_job
from careerpilot.pdf_extractor import extract_pdf_text
from careerpilot.recommendations import build_recommendations
from careerpilot.skills import detect_skills, get_skill_gap


def test_identical_text_similarity_is_high() -> None:
    text = "Python developer with machine learning and SQL experience."
    score = calculate_similarity(text, text)
    assert score > 0.99


def test_unrelated_text_similarity_is_low() -> None:
    resume = "Experienced chef with food safety and kitchen management skills."
    job = "Senior data scientist with Python, machine learning, and cloud deployment."
    score = calculate_similarity(resume, job)
    assert score < 0.4


def test_empty_input_raises_value_error() -> None:
    try:
        calculate_similarity("   ", "Python developer")
        raise AssertionError("Expected ValueError for empty resume text")
    except ValueError:
        pass


def test_compare_resume_job_returns_summary() -> None:
    result = compare_resume_job("Python SQL analytics", "Python SQL")
    assert result["score"] > 0.5
    assert "similarity" in result["description"].lower()


def test_extract_pdf_text_reads_valid_pdf() -> None:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Python developer with SQL and machine learning skills.")
    pdf_bytes = document.tobytes()
    document.close()

    text = extract_pdf_text(pdf_bytes, "resume.pdf")
    assert "Python developer" in text
    assert "machine learning" in text


def test_extract_pdf_text_rejects_empty_or_invalid_pdf() -> None:
    try:
        extract_pdf_text(b"not a real pdf", "resume.pdf")
        raise AssertionError("Expected ValueError for invalid PDF bytes")
    except ValueError:
        pass

    try:
        extract_pdf_text(b"", "resume.pdf")
        raise AssertionError("Expected ValueError for empty PDF bytes")
    except ValueError:
        pass


def test_skill_detection_supports_aliases_and_avoids_false_matches() -> None:
    text = "Worked with Python, SQL, and NLP in a cloud environment."
    skills = detect_skills(text)
    assert "python" in skills
    assert "sql" in skills
    assert "natural language processing" in skills
    assert "cloud" in skills
    assert "machine learning" not in detect_skills("I sent an email this afternoon and met the team.")


def test_skill_gap_and_recommendation_engine() -> None:
    resume = "I am a Python developer with SQL and data analysis experience."
    job = "Need Python, SQL, machine learning, and cloud experience."

    gap = get_skill_gap(resume, job)
    assert "python" in gap["matched_skills"]
    assert "sql" in gap["matched_skills"]
    assert "machine learning" in gap["missing_skills"]
    assert gap["recommendations"]

    recommendations = build_recommendations(gap["missing_skills"])
    assert recommendations
    assert any("Machine Learning Engineer" in item or "Data Scientist" in item for item in recommendations)
