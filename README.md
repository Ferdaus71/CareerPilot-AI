# CareerPilot AI
### An AI-Powered Resume Analysis, Job Matching, and Career Recommendation System

**CareerPilot AI** is a Python-based career assistance project designed to help job seekers compare their resumes with job descriptions, identify relevant skills, discover potential skill gaps, and receive practical career development recommendations.

The project combines PDF text extraction, natural language processing (NLP), TF-IDF vectorization, cosine similarity, and rule-based skill analysis to provide interpretable insights into resume-job alignment.

> **Important:** The resume-to-job similarity score is a text similarity metric, not a probability of being hired or a validated measure of candidate quality.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [API Usage](#api-usage)
- [Example Analysis](#example-analysis)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Privacy and Security](#privacy-and-security)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

---

## Project Overview

Job seekers often find it difficult to determine how well their resumes align with specific job requirements. Manually reviewing a resume against a job description can be time-consuming, especially when identifying missing technical skills and planning professional development.

CareerPilot AI aims to simplify this process by analyzing resume text alongside a target job description and presenting useful, explainable results.

The system is designed around four main capabilities:

1. **Resume Analysis:** Extract readable text from an uploaded PDF resume.
2. **Job Matching:** Compare resume text and job requirements using TF-IDF and cosine similarity.
3. **Skill-Gap Analysis:** Identify matched skills and potential missing skills.
4. **Career Recommendations:** Suggest relevant career directions and practical learning activities based on identified gaps.

The project is intended as a career-planning aid, not an automated recruitment or hiring decision system.

## Objectives

- Extract text from supported PDF resumes.
- Validate uploaded documents and handle invalid or unreadable files.
- Normalize and preprocess resume and job-description text.
- Calculate resume-to-job textual similarity using TF-IDF and cosine similarity.
- Identify matched and missing skills using a configurable skill dictionary.
- Generate explainable, rule-based career recommendations.
- Provide a user-friendly interface for entering job descriptions and reviewing analysis results.
- Support automated testing, reproducible development, and maintainable code.
- Follow responsible practices for handling resumes and personal information.

## Key Features

### 1. PDF Resume Upload

Users can provide a resume in PDF format for text extraction.

Planned or applicable validation includes:

- Checking the uploaded file type.
- Handling empty or unreadable PDFs.
- Providing understandable validation messages.
- Avoiding unnecessary retention of uploaded documents.

Text-based PDF extraction does not automatically support every scanned document. OCR may be needed for image-only PDFs.

### 2. Resume-to-Job Similarity

The system represents resume text and job-description text using TF-IDF and compares their vectors using cosine similarity.

The similarity result is displayed as a percentage for easier interpretation.

For example, a similarity score of `26.8%` represents the similarity produced by the configured text-processing method. It does not mean there is a 26.8% chance of receiving a job offer.

### 3. Skill-Gap Analysis

A configurable skill dictionary can be used to identify:

- Skills found in both the resume and job description.
- Skills mentioned in the job description but not detected in the resume.
- A skill coverage summary based on the identified skill sets.

Results depend on the configured vocabulary and matching rules. A skill may be present under a synonym or a different expression without being detected.

### 4. Career Recommendations

The application is designed to provide recommendations based on detected skill gaps and configured career rules.

Possible recommendation categories include:

- Relevant career roles.
- Existing strengths.
- Skills to prioritize.
- Suggested projects and hands-on learning activities.
- A practical learning roadmap.

Recommendations should be treated as guidance rather than guaranteed career outcomes.

### 5. Interactive Interface

The planned Streamlit interface allows users to upload a PDF resume, paste a job description, initiate an analysis, and review the results.

### 6. API Support

A FastAPI backend may expose reusable analysis functionality through HTTP endpoints. The exact endpoints and request schemas depend on the implementation in the repository.

### 7. Testing and Maintainability

The project can use automated tests to verify document extraction, similarity calculations, skill matching, input validation, and API behavior where applicable.

Git, GitHub, Ruff, Pytest, HTTPX, and GitHub Actions support version control and development quality.

---

## How It Works

The intended analysis pipeline is:

```text
                 +----------------------+
                 |   Upload PDF Resume  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Extract PDF Text   |
                 +----------+-----------+
                            |
                            v
+----------------+  +----------------------+
| Job Description|->|  Text Preprocessing  |
+----------------+  +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   TF-IDF Vectorizer  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Cosine Similarity   |
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
     +----------------------+      +----------------------+
     |   Skill-Gap Analysis |      | Similarity Summary   |
     +----------+-----------+      +----------------------+
                |
                v
     +----------------------+
     | Career Recommendations|
     +----------+-----------+
                |
                v
     +----------------------+
     | Display Analysis     |
     +----------------------+
```

### TF-IDF

Term Frequency–Inverse Document Frequency (TF-IDF) converts text into numerical features based on term frequency and inverse document frequency.

### Cosine Similarity

For two nonzero vectors \(A\) and \(B\), cosine similarity is calculated as:

\[
\operatorname{sim}(A,B)=
\frac{A\cdot B}{\|A\|\|B\|}
\]

The result measures the orientation similarity of the selected text vectors. The score depends on the text representation, vocabulary, and preprocessing method.

### Skill Coverage

A basic skill coverage measure can be calculated as:

\[
\operatorname{Coverage}=
\frac{\text{Matched Job Skills}}
{\text{Total Detected Job Skills}}\times100
\]

This formula assumes that the denominator contains at least one detected job skill. The implementation should handle empty skill sets safely.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| PyMuPDF | PDF text extraction |
| Scikit-learn | TF-IDF and cosine similarity |
| Pandas / NumPy | Data processing when required |
| Streamlit | Interactive web interface |
| FastAPI | HTTP API, if implemented |
| Uvicorn | ASGI server for FastAPI |
| Pytest | Automated testing |
| HTTPX | API testing |
| Ruff | Linting and code quality |
| Git and GitHub | Version control and collaboration |
| GitHub Actions | Continuous integration, if configured |
| Docker | Containerization, if configured |

The required packages should match the actual application modules. Optional components do not need to be installed if they are not used.

---

## Project Structure

A suggested repository layout is:

```text
CareerPilot-AI/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── pyproject.toml
├── Dockerfile
│
├── src/
│   └── careerpilot/
│       ├── __init__.py
│       ├── pdf_parser.py
│       ├── preprocessing.py
│       ├── similarity.py
│       ├── skill_analyzer.py
│       └── recommender.py
│
├── tests/
│   ├── test_pdf_parser.py
│   ├── test_similarity.py
│   ├── test_skill_analyzer.py
│   └── test_api.py
│
├── screenshots/
│   ├── Upload.png
│   ├── Analysis.png
│   ├── skill2.png
│   └── skill.png
│
├── docs/
│   └── project-report/
│
└── .github/
    └── workflows/
        └── ci.yml
```

**Note:** This is a suggested structure, not a claim that every listed file already exists. Keep the README aligned with the actual files and entry points in the repository.

---

## Installation and Setup

### Prerequisites

Install the following tools as required by your selected configuration:

- Python 3.11 or another version compatible with the project dependencies.
- Git.
- pip.
- A code editor such as Visual Studio Code.

Docker is optional if containerization is configured.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ferdaus71/CareerPilot-AI.git
cd CareerPilot-AI
```

### Step 2: Create a Virtual Environment

**Windows — Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

If the repository contains a complete and compatible `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If the file is missing, create it from the dependencies actually used by the project before installing packages.

### Step 5: Verify the Installation

```bash
python --version
python -m pip list
```

Confirm that the required dependencies installed successfully.

---

## Running the Application

Use the entry point that exists in the repository.

### Streamlit Frontend

If the Streamlit entry point is `app.py`:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, commonly:

```text
http://localhost:8501
```

### FastAPI Backend

If `main.py` contains a FastAPI instance named `app`:

```bash
uvicorn main:app --reload
```

The local API is commonly available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is commonly available at:

```text
http://127.0.0.1:8000/docs
```

These commands are examples. Adjust the module names and commands to match the implemented application.

---

## API Usage

If a FastAPI backend is implemented, its available endpoints can be inspected through the interactive documentation:

```text
http://127.0.0.1:8000/docs
```

To inspect the API definition programmatically, use:

```bash
curl http://127.0.0.1:8000/openapi.json
```

The actual endpoint paths, HTTP methods, accepted fields, response formats, and validation behavior should be documented from the running API.

Do not assume that a particular endpoint exists unless it is implemented in the repository.

---

## Example Analysis

A typical analysis may display the following information:

| Result | Description |
|---|---|
| Similarity score | Text similarity between the resume and job description |
| Matched skills | Skills detected in both texts |
| Missing skills | Job-description skills not detected in the resume |
| Skill coverage | Coverage calculated from detected job skills |
| Best-fit role | A role suggested by the configured recommendation rules |
| Learning roadmap | Suggested activities for addressing selected skill gaps |

For example, the application interface may display a similarity score of `26.8%`, five matched skills, six missing skills, and skill coverage of `45.5%`.

These values are illustrative of an application result and are not universal benchmarks. Actual values depend on the uploaded resume, job description, skill dictionary, and implementation.

---

## Testing

Run the project's automated tests from the repository root:

```bash
python -m pytest -v
```

If the test suite is located in a specific directory:

```bash
python -m pytest tests/ -v
```

### Recommended Test Coverage

| Test Area | Expected Behavior |
|---|---|
| Valid PDF | Readable text is extracted |
| Invalid file | Input is rejected or handled safely |
| Empty PDF | An appropriate validation result is returned |
| Empty job description | The analysis does not proceed silently |
| Similarity calculation | A valid score is returned for supported inputs |
| Empty text vectors | No division-by-zero or unhandled error occurs |
| Skill matching | Expected skills are detected |
| Missing skills | Potential gaps are identified correctly |
| API validation | Invalid requests receive appropriate responses |
| Application startup | The configured application starts successfully |

These are recommended checks. Actual test results should be reported only after running the tests.

---

## Code Quality

If Ruff is configured in the repository, run:

```bash
ruff check .
```

To apply safe automatic fixes:

```bash
ruff check . --fix
```

If formatting is configured:

```bash
ruff format --check .
```

Run the checks from the project root and resolve reported issues before merging or publishing changes.

---

## Privacy and Security

Resumes can contain personally identifiable information. CareerPilot AI should process uploaded documents responsibly.

Recommended safeguards include:

- Do not commit personal resumes, confidential documents, or credentials to GitHub.
- Validate file types and reasonable upload-size limits.
- Handle invalid or malformed PDF files safely.
- Avoid logging full resume text or unnecessary personal information.
- Avoid retaining uploaded files unless required and explicitly documented.
- Keep secrets in environment variables or secure deployment settings.
- Use a `.gitignore` file to exclude virtual environments, caches, local configuration, and private test documents.
- Explain how uploaded data is processed and retained.
- Review access controls before making the application available publicly.

Example `.gitignore` entries:

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/

# Virtual environments
.venv/
venv/
env/

# Environment variables and secrets
.env
.env.*

# Test and tool caches
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# Editors and operating systems
.vscode/
.idea/
.DS_Store
Thumbs.db

# Local uploads and private documents
uploads/
private_data/
```

If a file is already tracked by Git, adding it to `.gitignore` does not automatically remove it from version control. Remove private files from tracking safely before pushing, and rotate any credentials that have been exposed.

---

## Limitations

- TF-IDF primarily captures term-based similarity rather than deep semantic meaning.
- Different wording and synonyms may reduce similarity even when the underlying skills are related.
- PDF extraction quality depends on the document structure and whether its text is selectable.
- Scanned PDFs may require OCR.
- Skill matching depends on the configured dictionary and matching logic.
- Career recommendations depend on the rules and data available to the system.
- A similarity score cannot establish a candidate's actual suitability, future performance, or probability of being hired.
- Results should be reviewed by the user and should not replace independent judgment.

---

## Future Improvements

Potential improvements include:

- OCR support for scanned resumes.
- Semantic embeddings for better contextual matching.
- Expanded skill taxonomies and synonym handling.
- More detailed evidence for matched and missing skills.
- Personalized learning roadmaps.
- Improved error handling and accessibility.
- More comprehensive automated tests.
- Docker-based deployment.
- Continuous integration with GitHub Actions.
- Performance monitoring and structured logging.
- Clearer controls for privacy and document retention.

Future improvements should be added incrementally and validated with tests.

---

## Contributing

Contributions, suggestions, and bug reports are welcome.

### Suggested Workflow

1. Fork the repository.
2. Create a feature branch.
3. Implement a focused change.
4. Add or update relevant tests.
5. Run the test suite and code-quality checks.
6. Commit your changes with a clear message.
7. Open a pull request describing the change.

Example:

```bash
git checkout -b feature/improve-skill-matching
git add .
git commit -m "Improve skill matching logic"
git push -u origin feature/improve-skill-matching
```

Review staged files before committing, and never include private resumes, credentials, or unrelated local files.

---

## Author

**Md. Ferdaus Hossen**

- GitHub: [@Ferdaus71](https://github.com/Ferdaus71)
- LinkedIn: [ferdaus71](https://www.linkedin.com/in/ferdaus71/)
- Google Scholar: [Research Publications](https://scholar.google.com/citations?user=7N3hKAgAAAAJ&hl=en)

Computer Science and Engineering  
Green University of Bangladesh

---

## License

No license has been specified in this README.

Before distributing or reusing the project, select an appropriate open-source license and add the corresponding `LICENSE` file to the repository. Without an explicit license, others generally do not receive permission to reuse, modify, or redistribute the project beyond rights provided by applicable law.

---

## Acknowledgments

This project is part of an applied AI engineering learning journey focused on Python, machine learning, natural language processing, software development, and practical career-support applications.

---

**CareerPilot AI — Understand your skill gaps. Plan your next career move.**
