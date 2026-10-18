from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class CaesarRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Message text to process")
    shift: int = Field(..., description="Shift value (-25 to 25 or any integer)")
    preserve_case: bool = Field(default=True, description="Whether to maintain uppercase/lowercase")


class CaesarResponse(BaseModel):
    result: str
    shift: int
    operation: str


class BruteForceCandidate(BaseModel):
    rank: int
    shift: int
    decrypted_text: str
    chi2_score: float
    confidence: str


class BruteForceResponse(BaseModel):
    total_candidates: int
    best_candidate: Optional[BruteForceCandidate] = None
    candidates: List[BruteForceCandidate]


class FrequencyStat(BaseModel):
    count: int
    observed_pct: float
    expected_pct: float


class FrequencyResponse(BaseModel):
    total_letters: int
    frequencies: Dict[str, FrequencyStat]


class ExtendedCipherRequest(BaseModel):
    text: str = Field(..., min_length=1)
    key: Optional[str] = Field(default="", description="Keyword required for Vigenère")
    decrypt: bool = Field(default=False)
