# Classical Cryptography Suite & Automated Cryptanalysis Engine 🔐

> A full-stack classical cipher playground, statistical cryptanalysis engine, and REST API built with **FastAPI**, **Pydantic**, and a responsive **Tailwind CSS & Chart.js** frontend.

---

## 📑 Abstract

This project presents an interactive, full-stack cryptographic platform developed in Python that bridges theoretical classical cryptography with modern web-based cryptanalysis tools. Built on a modular architecture using FastAPI and Pydantic on the backend alongside a responsive Tailwind CSS and Chart.js frontend, the system implements key classical substitution ciphers, including the Caesar, Vigenère, Atbash, and ROT13 algorithms. 

To explore cryptographic vulnerabilities, the application incorporates an automated cryptanalysis engine capable of cracking unknown Caesar ciphertexts without prior knowledge of the shift key. The cracking subsystem evaluates all 25 possible permutations using a Chi-Squared ($\chi^2$) goodness-of-fit test against standard English letter frequency distributions (ETAOIN SHRDLU), augmented by dictionary-based pattern matching to rank candidates and assign statistical confidence scores. Additionally, the platform provides real-time letter frequency visualizations, stream-based file encryption and decryption for text documents, and a comprehensive automated unit-testing framework. The system serves as an educational and analytical tool demonstrating fundamental substitution cipher mathematics, modular arithmetic, and the inherent statistical weaknesses of monoalphabetic encryption.

**Keywords:** Classical Cryptography, Caesar Cipher, Vigenère Cipher, Frequency Analysis, Chi-Squared ($\chi^2$) Test, Cryptanalysis, Brute-Force Cracking, FastAPI, Python.

---

## Features

- **Interactive Web UI** — Real-time shift slider, Caesar alphabet wheel, one-click copy and text swap.
- **FastAPI Backend** — Fully typed REST API with Pydantic validation and interactive Swagger UI at `/docs`.
- **Smart Brute-Force Cracker**
  - Tests all 25 shift possibilities automatically.
  - Uses the **Chi-Squared (chi2) statistic** and English letter frequency analysis to rank candidates.
  - Confidence scoring: High / Medium / Low.
- **Letter Frequency Analysis** — Live histogram comparing ciphertext distribution against standard English (ETAOIN).
- **Extended Classical Ciphers**
  - **Vigenere Cipher** — Polyalphabetic keyword-based encryption and decryption.
  - **Atbash Cipher** — Alphabet inversion substitution cipher.
  - **ROT13** — Symmetric 13-shift Caesar variant.
- **File Processing** — Upload `.txt` files, encrypt or decrypt, and download the result.
- **Unit Test Suite** — Automated tests with `unittest` covering all algorithms, edge cases, and wraparound logic.

---

## Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/RishiY7/End-to-End-Encrypted-Chat.git
cd End-to-End-Encrypted-Chat
pip install -r requirements.txt
```

### 2. Launch the Application

Run the FastAPI server with auto-reload:

```bash
uvicorn app.main:app --reload
```

### 3. Open in Browser

| URL | Purpose |
| :--- | :--- |
| http://127.0.0.1:8000 | Web Dashboard UI |
| http://127.0.0.1:8000/docs | Interactive Swagger API Docs |
| http://127.0.0.1:8000/redoc | ReDoc API Reference |

---

## Testing & Verification

Run the full test suite:

```bash
python -m unittest discover tests -v
```

### Verified Test Vectors

| Test Vector | Expected Output | Status |
| :--- | :--- | :--- |
| Caesar: `HELLO`, shift 3 | `KHOOR` | Passed |
| Caesar: `XYZ`, shift 3 | `ABC` | Passed |
| Caesar: `ABC`, shift 0 / 26 | `ABC` | Passed |
| Caesar: `Hello, World!`, shift 3 | `Khoor, Zruog!` | Passed |
| Vigenere: `ATTACKATDAWN`, key `LEMON` | `LXFOPVEFRNHR` | Passed |
| Atbash: `Attack at dawn!` | `Zggzxp zg wzdm!` | Passed |
| ROT13: Round-trip | Plaintext preserved | Passed |

---

## Project Structure

```
End-to-End Encrypted Chat/
|
+-- app/                              # FastAPI application package
|   +-- main.py                       # Server entry point & all REST API routes
|   +-- schemas.py                    # Pydantic request & response models
|   +-- crypto/                       # Cryptographic algorithms module
|   |   +-- __init__.py
|   |   +-- caesar.py                 # Caesar cipher, Chi2 scoring, brute-force cracker
|   |   +-- ciphers.py                # Vigenere, Atbash, ROT13 implementations
|   +-- static/                       # Web UI assets (served by FastAPI)
|       +-- index.html                # Dark-theme Tailwind CSS dashboard (4 tabs)
|       +-- app.js                    # Client-side logic, Chart.js, API calls
|
+-- tests/                            # Automated unit test suite
|   +-- test_ciphers.py               # unittest cases for all cipher algorithms
|
+-- notebooks/                        # Jupyter notebooks for demos & exploration
|   +-- caesar_demo.ipynb             # Interactive Caesar cipher walkthrough
|
+-- scripts/                          # Standalone command-line utilities
|   +-- caesar_cli.py                 # CLI encrypt / decrypt / brute-force tool
|
+-- docs/                             # Project documentation
|   +-- ONBOARDING.md                 # Developer setup & architecture guide
|
+-- requirements.txt                  # Production dependencies
+-- README.md                         # Project overview (this file)
```

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/caesar/encrypt` | Encrypt text with a shift value |
| `POST` | `/api/v1/caesar/decrypt` | Decrypt text with a shift value |
| `POST` | `/api/v1/caesar/brute-force` | Brute-force crack with Chi-Squared ranking |
| `POST` | `/api/v1/caesar/frequency` | Character count & observed frequency vs English |
| `POST` | `/api/v1/ciphers/vigenere` | Vigenere encryption/decryption with keyword |
| `POST` | `/api/v1/ciphers/atbash` | Atbash inverted cipher |
| `POST` | `/api/v1/ciphers/rot13` | ROT13 cipher |
| `POST` | `/api/v1/files/caesar` | Stream encrypt/decrypt uploaded text files |

---

## Developer Guide

For complete local environment setup, virtual environments, and contribution guidelines, see [docs/ONBOARDING.md](docs/ONBOARDING.md).
