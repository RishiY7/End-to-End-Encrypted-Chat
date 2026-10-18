def rot13(text: str) -> str:
    """Standard ROT13 cipher (Caesar shift 13)."""
    from .caesar import caesar_shift
    return caesar_shift(text, 13)


def atbash_cipher(text: str) -> str:
    """
    Atbash cipher: Inverts alphabet letters (A <-> Z, B <-> Y, a <-> z, etc.)
    """
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr(ord('Z') - (ord(ch) - ord('A'))))
        elif ch.islower():
            result.append(chr(ord('z') - (ord(ch) - ord('a'))))
        else:
            result.append(ch)
    return "".join(result)


def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """
    Vigenère cipher encryption/decryption using a keyword.
    """
    clean_key = [ch.upper() for ch in key if ch.isalpha()]
    if not clean_key:
        raise ValueError("Key must contain at least one alphabetic character.")

    key_shifts = [ord(k) - ord('A') for k in clean_key]
    key_len = len(key_shifts)
    
    result = []
    key_idx = 0
    
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            current_shift = key_shifts[key_idx % key_len]
            if decrypt:
                current_shift = -current_shift
            shifted_char = chr((ord(ch) - base + current_shift) % 26 + base)
            result.append(shifted_char)
            key_idx += 1
        else:
            result.append(ch)
            
    return "".join(result)
