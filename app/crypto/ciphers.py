def rot13(text: str) -> str:
    """Standard ROT13 cipher (Caesar shift 13)."""
    from .caesar import caesar_shift
    return caesar_shift(text, 13)


def atbash_cipher(text: str) -> str:
    """
    Atbash cipher: Inverts standard Latin alphabet letters (A <-> Z, B <-> Y, a <-> z, etc.).
    Preserves non-Latin and special characters.
    """
    result = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            result.append(chr(ord('Z') - (ord(ch) - ord('A'))))
        elif 'a' <= ch <= 'z':
            result.append(chr(ord('z') - (ord(ch) - ord('a'))))
        else:
            result.append(ch)
    return "".join(result)


def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """
    Vigenère cipher encryption/decryption using an alphabetic keyword.
    Preserves non-Latin and special characters.
    """
    clean_key = [ch.upper() for ch in key if 'A' <= ch.upper() <= 'Z']
    if not clean_key:
        raise ValueError("Key must contain at least one alphabetic character (A-Z).")

    key_shifts = [ord(k) - ord('A') for k in clean_key]
    key_len = len(key_shifts)
    
    result = []
    key_idx = 0
    
    for ch in text:
        if 'A' <= ch <= 'Z':
            current_shift = key_shifts[key_idx % key_len]
            if decrypt:
                current_shift = -current_shift
            shifted_char = chr((ord(ch) - 65 + current_shift) % 26 + 65)
            result.append(shifted_char)
            key_idx += 1
        elif 'a' <= ch <= 'z':
            current_shift = key_shifts[key_idx % key_len]
            if decrypt:
                current_shift = -current_shift
            shifted_char = chr((ord(ch) - 97 + current_shift) % 26 + 97)
            result.append(shifted_char)
            key_idx += 1
        else:
            result.append(ch)
            
    return "".join(result)
