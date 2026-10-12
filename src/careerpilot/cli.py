from __future__ import annotations

import argparse
import json
from pathlib import Path

from careerpilot.pdf_extractor import extract_pdf_text
from careerpilot.service import build_analysis_result


def analyze_resume_pdf(resume_path: str | Path, job_description: str) -> dict[str, object]:
    resume_file = Path(resume_path)
    if not resume_file.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_file}")

    if resume_file.suffix.lower() != ".pdf":
        raise ValueError("The CLI expects a PDF resume file.")

    resume_text = extract_pdf_text(resume_file.read_bytes(), resume_file.name)
    return build_analysis_result(resume_text, job_description)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="careerpilot",
        description="Analyze a resume against a target job description and print a JSON summary.",
    )
    parser.add_argument("--resume", required=True, help="Path to the resume PDF file.")
    parser.add_argument("--job-description", help="Job description text to compare against.")
    parser.add_argument("--job-file", help="Optional path to a text file containing the job description.")
    parser.add_argument(
        "--output",
        help="Optional path to save the JSON analysis output instead of printing it to stdout.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.job_description and not args.job_file:
        parser.error("Provide --job-description or --job-file.")

    if args.job_file and not args.job_description:
        job_description = Path(args.job_file).read_text(encoding="utf-8")
    else:
        job_description = args.job_description

    analysis = analyze_resume_pdf(args.resume, job_description)
    output_text = json.dumps(analysis, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text + "\n", encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
