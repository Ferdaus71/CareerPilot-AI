from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from careerpilot.matching import compare_resume_job
from careerpilot.pdf_extractor import extract_pdf_text
from careerpilot.recommendations import build_recommendations
from careerpilot.skills import detect_skills, get_skill_gap

st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")


def _render_placeholder_results() -> None:
    st.subheader("Analysis results")
    st.info(
        "Upload a resume and enter a job description to generate a similarity score, skill match summary, and recommendations."
    )


def _render_results(resume_text: str, job_text: str) -> None:
    score = compare_resume_job(resume_text, job_text)
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_text)
    skill_gap = get_skill_gap(resume_text, job_text)
    career_focus = build_recommendations(skill_gap["missing_skills"])

    st.subheader("Analysis results")
    st.metric("Resume-to-job similarity", f"{score['score'] * 100:.1f}%")
    st.caption(
        "This score measures text similarity between the resume and job description. It is not a probability of being hired or a validated candidate-quality score."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Matched skills")
        if skill_gap["matched_skills"]:
            for skill in sorted(skill_gap["matched_skills"]):
                st.write(f"- {skill}")
        else:
            st.write("No matching skills detected.")

    with col2:
        st.markdown("### Missing skills")
        if skill_gap["missing_skills"]:
            for skill in sorted(skill_gap["missing_skills"]):
                st.write(f"- {skill}")
        else:
            st.write("No major missing skills detected.")

    st.markdown("### Recommendations")
    if skill_gap["recommendations"]:
        for recommendation in skill_gap["recommendations"]:
            st.write(f"- {recommendation}")
    else:
        st.write("Your resume already reflects many of the job requirements.")

    st.markdown("### Career focus")
    for recommendation in career_focus:
        st.write(f"- {recommendation}")

    if resume_skills or job_skills:
        st.markdown("### Skill overview")
        st.write(f"Resume skills: {', '.join(sorted(resume_skills)) or 'None detected'}")
        st.write(f"Job skills: {', '.join(sorted(job_skills)) or 'None detected'}")
        st.caption("A skill may not be detected in the text even when a candidate has practical experience with it.")


def main() -> None:
    st.title("CareerPilot AI")
    st.write(
        "Analyze resumes against job descriptions, identify skill gaps, and get practical career recommendations."
    )

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder="Paste or type the full job posting here...",
    )

    if st.button("Analyze", type="primary"):
        if uploaded_file is None:
            st.error("Please upload a PDF resume before running analysis.")
            _render_placeholder_results()
            return

        if not job_description.strip():
            st.error("Please provide a job description before analyzing the match.")
            _render_placeholder_results()
            return

        try:
            resume_text = extract_pdf_text(uploaded_file.getvalue(), uploaded_file.name)
            _render_results(resume_text, job_description)
        except ValueError as exc:
            st.error(str(exc))
            _render_placeholder_results()
    else:
        _render_placeholder_results()


if __name__ == "__main__":
    main()
