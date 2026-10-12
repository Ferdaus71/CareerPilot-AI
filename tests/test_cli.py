from __future__ import annotations

import json
from pathlib import Path

import fitz

from careerpilot.cli import analyze_resume_pdf, main


def test_analyze_resume_pdf_with_cli_data(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Python developer with SQL and cloud experience.")
    resume_path.write_bytes(document.tobytes())
    document.close()

    analysis = analyze_resume_pdf(resume_path, "Python and SQL roles with cloud skills.")
    assert analysis["matched_skills"]
    assert analysis["similarity"]["score"] >= 0


def test_cli_main_prints_json(tmp_path: Path, capsys) -> None:
    resume_path = tmp_path / "resume.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Python developer with SQL and analytics experience.")
    resume_path.write_bytes(document.tobytes())
    document.close()

    exit_code = main(["--resume", str(resume_path), "--job-description", "Python and SQL experience"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["matched_skills"]
    assert payload["best_role"]
