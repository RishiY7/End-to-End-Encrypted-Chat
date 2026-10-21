import math
from typing import Dict, List, Tuple

# Standard English letter frequencies (percentages)
ENGLISH_FREQUENCIES: Dict[str, float] = {
    'A': 8.2,  'B': 1.5,  'C': 2.8,  'D': 4.3,  'E': 12.7, 'F': 2.2,
    'G': 2.0,  'H': 6.1,  'I': 7.0,  'J': 0.15, 'K': 0.77, 'L': 4.0,
    'M': 2.4,  'N': 6.7,  'O': 7.5,  'P': 1.9,  'Q': 0.095,'R': 6.0,
    'S': 6.3,  'T': 9.1,  'U': 2.8,  'V': 0.98, 'W': 2.4,  'X': 0.15,
    'Y': 2.0,  'Z': 0.074
}

# Common English words dictionary for validation boost
COMMON_ENGLISH_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there",
    "their", "what", "so", "up", "out", "if", "about", "who", "get",
    "which", "go", "me", "when", "make", "can", "like", "time", "no",
    "just", "him", "know", "take", "people", "into", "year", "your",
    "good", "some", "could", "them", "see", "other", "than", "then",
    "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first",
    "well", "way", "even", "new", "want", "because", "any", "these",
    "give", "day", "most", "us", "hello", "world", "secret", "cipher"
}


def caesar_shift(text: str, shift: int, preserve_case: bool = True) -> str:
    """
    Encrypts or decrypts text using the Caesar cipher.
    Shift can be positive or negative.
    Preserves non-ASCII characters, digits, and punctuation.
    """
    shift = shift % 26
    result = []
    
    for ch in text:
        if 'A' <= ch <= 'Z':
            shifted_char = chr((ord(ch) - 65 + shift) % 26 + 65)
            result.append(shifted_char)
        elif 'a' <= ch <= 'z':
            shifted_char = chr((ord(ch) - 97 + shift) % 26 + 97)
            if not preserve_case:
                shifted_char = shifted_char.upper()
            result.append(shifted_char)
        else:
            result.append(ch)
            
    return "".join(result)


def get_frequency_analysis(text: str) -> Dict[str, Dict[str, float]]:
    """
    Calculates letter counts, observed percentages, and comparison with English standard.
    Analyzes Latin letters A-Z (case-insensitive).
    """
    cleaned = [ch.upper() for ch in text if 'A' <= ch.upper() <= 'Z']
    total = len(cleaned)
    counts = {chr(c): 0 for c in range(ord('A'), ord('Z') + 1)}
    
    for ch in cleaned:
        counts[ch] += 1
        
    analysis = {}
    for letter, count in sorted(counts.items()):
        observed_pct = (count / total * 100) if total > 0 else 0.0
        expected_pct = ENGLISH_FREQUENCIES[letter]
        analysis[letter] = {
            "count": count,
            "observed_pct": round(observed_pct, 2),
            "expected_pct": expected_pct
        }
        
    return analysis


def score_english(text: str) -> float:
    """
    Scores how likely a piece of text is standard English using Chi-Squared statistic
    and dictionary matching. Lower score = better match with English.
    """
    letters = [ch.upper() for ch in text if 'A' <= ch.upper() <= 'Z']
    total_letters = len(letters)
    if total_letters == 0:
        return 9999.0
    
    counts = {chr(c): 0 for c in range(ord('A'), ord('Z') + 1)}
    for ch in letters:
        counts[ch] += 1

    # Chi-squared statistic: sum((observed - expected)^2 / expected)
    chi2 = 0.0
    for letter, exp_pct in ENGLISH_FREQUENCIES.items():
        expected_count = (exp_pct / 100.0) * total_letters
        observed_count = counts[letter]
        chi2 += ((observed_count - expected_count) ** 2) / (expected_count + 1e-5)

    # Word match bonus (check words in text)
    words = [w.strip(".,!?:;\"'()[]{}").lower() for w in text.split()]
    matched_words = sum(1 for w in words if w in COMMON_ENGLISH_WORDS)
    if words:
        word_ratio = matched_words / len(words)
        # Give substantial bonus (lowering chi2 score) if known common English words appear
        chi2 -= word_ratio * 150.0

    return round(max(chi2, 0.0), 2)


def brute_force_crack(ciphertext: str) -> List[Dict]:
    """
    Generates all 25 non-trivial shifts and ranks them by English likelihood.
    """
    candidates = []
    
    for shift in range(1, 26):
        decrypted = caesar_shift(ciphertext, -shift)
        chi2_score = score_english(decrypted)
        candidates.append({
            "shift": shift,
            "decrypted_text": decrypted,
            "chi2_score": chi2_score
        })
    
    # Sort by chi2_score ascending (lowest is best match)
    candidates.sort(key=lambda x: x["chi2_score"])
    
    # Mark rank and confidence
    for idx, c in enumerate(candidates):
        c["rank"] = idx + 1
        c["confidence"] = "High" if idx == 0 and c["chi2_score"] < 100 else ("Medium" if idx < 3 else "Low")
        
    return candidates
