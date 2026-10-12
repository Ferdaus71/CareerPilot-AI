# CareerPilot AI

CareerPilot AI is a Python-based application for resume analysis, job matching, and career guidance. The platform helps users compare a resume with a job description, identify missing skills, and receive clear recommendations for upskilling.

## Features
- Upload a PDF resume
- Paste or type a job description
- Compare resume text with job text using TF-IDF and cosine similarity
- Detect matching and missing skills
- Recommend next steps based on skill gaps
- Run as a local Streamlit application

## Tech Stack
- Python
- Streamlit
- FastAPI
- Scikit-learn
- PyMuPDF
- Pytest
- Ruff
- GitHub Actions

## Local setup on Windows

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
4. Run the app:
   ```powershell
   streamlit run src\careerpilot\app.py
   ```

## Testing

```powershell
pytest -q
```

## Linting

```powershell
ruff check .
```

## Project status
The project is under active development and follows an incremental build plan from foundation setup through PDF extraction, matching, skill analysis, and recommendation logic.