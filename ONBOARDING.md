# Developer Onboarding Guide

Welcome to the **Caesar Cipher & Classical Cryptography Suite**! This guide walks you through setting up your local environment, running the application, executing tests, and understanding the project architecture.

---

## 1. Prerequisites

- **Python 3.10+** (Tested on Python 3.12 / 3.14)
- **pip** (Python package manager)
- **Git**

---

## 2. Environment Setup

### 2.1 Clone the Repository
```bash
git clone https://github.com/Vishnuj-n/caesar-cipher-python.git
cd caesar-cipher-python
```

### 2.2 Create & Activate a Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

*(Optional dev tools for testing & linting)*:
```bash
pip install pytest
```

---

## 3. Running the Application

### 3.1 Start the FastAPI Server
Run the application with auto-reloading enabled:
```bash
uvicorn app.main:app --reload
```

### 3.2 Access the Services
- **Web UI Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs (OpenAPI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 4. Running the Tests

To run the full suite using Python's built-in `unittest` framework:
```bash
python -m unittest discover tests -v
```

Or using `pytest`:
```bash
python -m pytest tests -v
```

---

## 5. Project Architecture & Code Map

```text
caesar-cipher-python/
├── app/
│   ├── main.py             # FastAPI entrypoint, router configuration, file upload endpoints
│   ├── schemas.py          # Pydantic request/response data contracts
│   ├── core/
│   │   ├── __init__.py
│   │   ├── caesar.py       # Caesar shift logic, Chi-squared (χ²) scoring, brute-force cracker
│   │   └── ciphers.py      # Vigenère, Atbash, and ROT13 implementations
│   └── static/
│       ├── index.html      # Responsive web UI (Tailwind CSS, FontAwesome)
│       └── app.js          # Client-side reactivity, Chart.js frequency distribution
├── tests/
│   └── test_ciphers.py     # Unit test suite verifying all cipher math and edge cases
├── caesar-cipher-python.py # Standalone legacy CLI script
├── requirements.txt        # Production dependencies
├── CONTRIBUTING.md / ONBOARDING.md
└── README.md               # User & project overview
```

---

## 6. Development Workflow & Git Best Practices

1. **Keep Secrets & Cache out of Git**: Never commit `.env`, `venv/`, or `__pycache__` directories. The repository includes a `.gitignore` that handles these automatically.
2. **Verify tests before committing**:
   ```bash
   python -m unittest discover tests
   ```
3. **Branching & Pull Requests**:
   - Create a feature branch: `git checkout -b feat/your-feature-name`
   - Commit clean changes: `git commit -m "feat: add feature description"`
   - Push and open a PR against `main`.
