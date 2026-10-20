def caesar_shift(text, shift):
    out = ""
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            out += chr((ord(ch) - base + shift) % 26 + base)
        else:
            out += ch
    return out

# Encryption
text = input("Enter message: ")
shift = int(input("Enter shift value: "))
encrypted = ""
for char in text:
    if char.isalpha():
        base = 65 if char.isupper() else 97
        encrypted += chr((ord(char) - base + shift) % 26 + base)
    else:
        encrypted += char
print("Encrypted message:", encrypted)

# Decryption
cipher = input("Enter encrypted message: ")
shift = int(input("Enter shift value: "))
decrypted = ""
for char in cipher:
    if char.isalpha():
        base = 65 if char.isupper() else 97
        decrypted += chr((ord(char) - base - shift) % 26 + base)
    else:
        decrypted += char
print("Decrypted message:", decrypted)

# Brute-force attack
cipher = input("Enter encrypted text: ")
print("\nAll 26 possible decryptions:\n")
for s in range(1, 27):
    candidate = caesar_shift(cipher, -s)
    print(f"shift {s:2d}: {candidate}")
