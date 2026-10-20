# Secure End-to-End Encrypted Chat Using Hybrid Cryptography and Caesar Cipher 🔐

A high-performance classical cryptography playground and REST API built with **FastAPI**, **Pydantic**, and a responsive **Tailwind CSS & Chart.js** frontend.

---

## ✨ Features

- **Interactive Web UI**: Real-time slider shift adjustment, Caesar wheel visual mapping, one-click copy, and text swapping.
- **FastAPI Backend**: Fully typed REST API with Pydantic validation schemas and interactive Swagger UI documentation at `/docs`.
- **Smart English Brute-Force Cracker**:
  - Tests all 25 shift possibilities in real time.
  - Utilizes **Chi-Squared ($\chi^2$) statistic** and English letter frequency analysis to accurately rank and identify the original plaintext.
  - Confidence scoring categorized into High, Medium, and Low based on correlation thresholds.
- **Letter Frequency Analysis**:
  - Live interactive histogram comparing ciphertext letter distributions against standard English (ETAOIN).
- **Extended Classical Ciphers**:
  - **Vigenère Cipher**: Polyalphabetic key-based encryption and decryption.
  - **Atbash Cipher**: Alphabet substitution / inversion cipher.
  - **ROT13**: Symmetric 13-shift cipher.
- **File Processing**:
  - Upload `.txt` files to stream encrypt or decrypt and download the output.
- **Comprehensive Test Suite**: Automated unit tests with standard `unittest` covering edge cases, modular wraparounds, punctuation handling, and cracker logic.

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Vishnuj-n/caesar-cipher-python.git
cd caesar-cipher-python
pip install -r requirements.txt
```

### 2. Launch the Application
Run the FastAPI web server with Uvicorn:
```bash
uvicorn app.main:app --reload
```

### 3. Open in Browser
- **Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testing & Verification

Run the cryptographic test suite:
```bash
python -m unittest discover tests -v
```

### Verified Test Vectors

| Test Vector | Expected Output | Status |
| :--- | :--- | :--- |
| **Caesar: `HELLO`, shift 3** | `KHOOR` |  Passed |
| **Caesar: `XYZ`, shift 3** | `ABC` |  Passed |
| **Caesar: `ABC`, shift 0 / 26** | `ABC` |  Passed |
| **Caesar: `Hello, World!`, shift 3** | `Khoor, Zruog!` |  Passed |
| **Vigenère: `ATTACKATDAWN`, key `LEMON`** | `LXFOPVEFRNHR` |  Passed |
| **Atbash: `Attack at dawn!`** | `Zggzxp zg wzdm!` |  Passed |
| **ROT13: Round-trip** | Plaintext preserved |  Passed |

---

## 📁 Project Structure

```text
caesar-cipher-python/
│
├── app/
│   ├── main.py                  # FastAPI server entry point & REST endpoints
│   ├── schemas.py               # Pydantic request & response models
│   ├── core/
│   │   ├── __init__.py
│   │   ├── caesar.py            # Caesar encryption, decryption, chi2 scoring
│   │   └── ciphers.py           # Vigenère, Atbash, ROT13 ciphers
│   └── static/
│       ├── index.html           # Modern dark-theme UI dashboard
│       └── app.js               # Frontend interaction, chart rendering, API calls
│
├── tests/
│   └── test_ciphers.py          # Unit tests for all algorithms
│
├── caesar-cipher-python.py      # Standalone legacy CLI script
├── requirements.txt             # Project dependencies
├── ONBOARDING.md                # Developer onboarding guide
└── README.md
```

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/caesar/encrypt` | Encrypt text with a shift value |
| `POST` | `/api/v1/caesar/decrypt` | Decrypt text with a shift value |
| `POST` | `/api/v1/caesar/brute-force` | Brute-force crack with Chi-Squared ranking |
| `POST` | `/api/v1/caesar/frequency` | Character count & observed frequency vs English |
| `POST` | `/api/v1/ciphers/vigenere` | Vigenère encryption/decryption with keyword |
| `POST` | `/api/v1/ciphers/atbash` | Atbash inverted cipher |
| `POST` | `/api/v1/ciphers/rot13` | ROT13 cipher |
| `POST` | `/api/v1/files/caesar` | Stream encrypt/decrypt uploaded text files |

---

## 📖 Developer Guide

For complete local environment setup, virtual environments, and contribution guidelines, see [docs/ONBOARDING.md](docs/ONBOARDING.md).
