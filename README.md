# CareerPilot AI

CareerPilot AI is a Python-based resume analysis and career guidance platform. It helps job seekers compare a resume with a role description, detect relevant skills, identify missing capabilities, and receive practical next steps for upskilling.

## Problem statement
Many job seekers struggle to translate their experience into a strong match for a target role. CareerPilot AI provides a transparent, explainable baseline for:
- checking how closely a resume matches a job description
- identifying skills present in both documents
- surfacing skills that may be missing
- suggesting concrete ways to strengthen a resume and career plan

## Features
- Upload a PDF resume
- Paste or type a job description
- Review a similarity score based on TF-IDF and cosine similarity
- Detect matched and missing skills using a configurable skill catalog
- Receive role-oriented recommendations based on the analysis
- Review a clear match status, skill coverage, best-fit role summary, and skill category breakdown
- Run a local Streamlit dashboard with a richer analytics view and learning roadmap
- Use a FastAPI backend for structured JSON analysis
- Export a JSON analysis report from the dashboard

## Technology stack
- Python
- Streamlit
- FastAPI
- Scikit-learn
- PyMuPDF
- Pytest
- Ruff
- GitHub Actions
- Docker

## Architecture overview
The project is organized into modular components:
- `src/careerpilot/app.py` — Streamlit user interface
- `src/careerpilot/api.py` — API entry point and request handling
- `src/careerpilot/service.py` — shared analysis orchestration
- `src/careerpilot/pdf_extractor.py` — PDF text extraction and validation
- `src/careerpilot/matching.py` — TF-IDF similarity logic
- `src/careerpilot/skills.py` — skill detection and skill-gap calculation
- `src/careerpilot/recommendations.py` — transparent career guidance logic
- `src/careerpilot/skill_catalog.py` — skill alias catalog and categories
- `tests/` — automated tests for matching, PDF handling, skill analysis, and API behavior

## Windows setup

1. Clone the repository:
   ```powershell
   git clone https://github.com/Ferdaus71/CareerPilot-AI.git
   cd CareerPilot-AI
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Start the Streamlit app:
   ```powershell
   streamlit run src\careerpilot\app.py
   ```
5. Start the API locally:
   ```powershell
   uvicorn careerpilot.api:app --reload --host 0.0.0.0 --port 8000
   ```

## CLI usage
After installing the package with `pip install -e .`, you can run a resume analysis directly from the terminal:

```powershell
careerpilot --resume .\samples\resume.pdf --job-file .\samples\job-description.txt
```

To save the analysis as JSON instead of printing it to stdout:

```powershell
careerpilot --resume .\samples\resume.pdf --job-description "Python and SQL engineer with cloud experience" --output .\output\analysis.json
```

You can also run the module directly:

```powershell
python -m careerpilot --resume .\samples\resume.pdf --job-file .\samples\job-description.txt
```

## API documentation
When the API server is running, view the docs here:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Testing and linting

```powershell
pytest -q
ruff check .
```

## Docker usage
Build the image:

```powershell
docker build -t careerpilot-ai .
```

Run the app container:

```powershell
docker run -p 8501:8501 careerpilot-ai
```

This runs the Streamlit dashboard by default. If you want to use the API in a container, run the app with a custom command:

```powershell
docker run -p 8000:8000 careerpilot-ai python -m uvicorn careerpilot.api:app --host 0.0.0.0 --port 8000
```

## Known limitations
- The baseline matching model uses TF-IDF and cosine similarity; it measures text similarity rather than hiring probability.
- OCR fallback supports scanned image-only PDFs when the optional OCR dependencies are installed in the environment.
- A skill may not be explicitly detected even if a candidate has practical experience with it.
- Recommendations are explainable and rule-based rather than predictive or guaranteed to produce interviews.
- The similarity score is not a validated candidate-quality score and should not be interpreted as hiring likelihood.

## Privacy and safety
- Uploaded resumes are processed in memory and are not intentionally stored to disk.
- The application does not log or expose full resume text in API responses.
- Avoid uploading sensitive personal data to local or shared environments.

## Project status
This project follows an incremental build workflow: foundation, Streamlit UI, PDF extraction, matching, skill-gap analysis, API integration, testing, CI automation, Docker support, and final documentation review.

## GitHub repository
https://github.com/Ferdaus71/CareerPilot-AI

## Final review notes
The project currently delivers a working, tested baseline for resume/job matching and skill-gap analysis. The implementation is intentionally explainable and transparent rather than predictive or probabilistic. Recent improvements include a clearer match-status summary and OCR fallback support for scanned PDFs when the optional dependencies are available. Future enhancements could include richer NLP models, deeper role taxonomy, and expanded deployment configuration.
