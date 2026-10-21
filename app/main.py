from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
import os

from app.crypto.caesar import caesar_shift, brute_force_crack, get_frequency_analysis
from app.crypto.ciphers import rot13, atbash_cipher, vigenere_cipher
from app.schemas import (
    CaesarRequest, CaesarResponse,
    BruteForceResponse, FrequencyResponse,
    ExtendedCipherRequest
)

app = FastAPI(
    title="Classical Cryptography Suite & Automated Cryptanalysis Engine",
    description="High-performance cryptographic API featuring Caesar cipher, automated cryptanalysis, and extended classical ciphers.",
    version="2.0.0"
)

# Enable CORS for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for modern web frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Caesar Cipher API v2.0 is live! Visit /docs for Swagger documentation."}


# --- Caesar Cipher Endpoints ---

@app.post("/api/v1/caesar/encrypt", response_model=CaesarResponse, tags=["Caesar Cipher"])
def encrypt_caesar(req: CaesarRequest):
    encrypted = caesar_shift(req.text, req.shift, req.preserve_case)
    return CaesarResponse(result=encrypted, shift=req.shift % 26, operation="encrypt")


@app.post("/api/v1/caesar/decrypt", response_model=CaesarResponse, tags=["Caesar Cipher"])
def decrypt_caesar(req: CaesarRequest):
    decrypted = caesar_shift(req.text, -req.shift, req.preserve_case)
    return CaesarResponse(result=decrypted, shift=req.shift % 26, operation="decrypt")


@app.post("/api/v1/caesar/brute-force", response_model=BruteForceResponse, tags=["Caesar Cipher"])
def brute_force(text: str = Form(..., description="Encrypted message to crack")):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Ciphertext cannot be empty.")
    candidates = brute_force_crack(text)
    best = candidates[0] if candidates else None
    return BruteForceResponse(
        total_candidates=len(candidates),
        best_candidate=best,
        candidates=candidates
    )


@app.post("/api/v1/caesar/frequency", response_model=FrequencyResponse, tags=["Cryptanalysis"])
def frequency_analysis(text: str = Form(..., description="Text to analyze")):
    analysis = get_frequency_analysis(text)
    total_letters = sum(1 for ch in text if ('A' <= ch <= 'Z' or 'a' <= ch <= 'z'))
    return FrequencyResponse(total_letters=total_letters, frequencies=analysis)


# --- Extended Ciphers ---

@app.post("/api/v1/ciphers/rot13", tags=["Extended Ciphers"])
def process_rot13(req: ExtendedCipherRequest):
    return {"result": rot13(req.text), "cipher": "ROT13"}


@app.post("/api/v1/ciphers/atbash", tags=["Extended Ciphers"])
def process_atbash(req: ExtendedCipherRequest):
    return {"result": atbash_cipher(req.text), "cipher": "Atbash"}


@app.post("/api/v1/ciphers/vigenere", tags=["Extended Ciphers"])
def process_vigenere(req: ExtendedCipherRequest):
    if not req.key or not req.key.strip():
        raise HTTPException(status_code=400, detail="Vigenère cipher requires a non-empty alphabetic key.")
    try:
        res = vigenere_cipher(req.text, req.key, decrypt=req.decrypt)
        return {"result": res, "cipher": "Vigenere", "operation": "decrypt" if req.decrypt else "encrypt"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- File Processing ---

@app.post("/api/v1/files/caesar", tags=["File Processing"])
async def process_file(
    file: UploadFile = File(...),
    shift: int = Form(...),
    decrypt: bool = Form(False)
):
    try:
        contents = await file.read()
        text = contents.decode("utf-8", errors="replace")
        actual_shift = -shift if decrypt else shift
        processed_text = caesar_shift(text, actual_shift)
        
        safe_filename = os.path.basename(file.filename or "file.txt")
        return PlainTextResponse(
            content=processed_text,
            media_type="text/plain; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="processed_{safe_filename}"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
