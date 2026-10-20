"""
Standalone Command-Line Interface (CLI) for Caesar Cipher & Cryptanalysis.
Can be executed directly in the terminal without starting the web server.
"""

def caesar_shift(text: str, shift: int) -> str:
    """Shift letters by `shift` positions preserving upper/lowercase."""
    out = []
    shift = shift % 26
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def main():
    print("=" * 60)
    print("  Caesar Cipher & Cryptanalysis CLI Tool")
    print("=" * 60)

    while True:
        print("\nSelect an operation:")
        print("  1. Encrypt message")
        print("  2. Decrypt message")
        print("  3. Brute-force crack (show all 25 shifts)")
        print("  4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            text = input("Enter plaintext to encrypt: ")
            try:
                shift = int(input("Enter shift value (e.g. 3): "))
                print(f"\n[+] Encrypted message: {caesar_shift(text, shift)}")
            except ValueError:
                print("[!] Error: Shift must be an integer.")

        elif choice == "2":
            cipher = input("Enter ciphertext to decrypt: ")
            try:
                shift = int(input("Enter shift value (e.g. 3): "))
                print(f"\n[+] Decrypted message: {caesar_shift(cipher, -shift)}")
            except ValueError:
                print("[!] Error: Shift must be an integer.")

        elif choice == "3":
            cipher = input("Enter unknown ciphertext to crack: ")
            print(f"\nAll 25 possible shifts:")
            print("-" * 40)
            for s in range(1, 26):
                candidate = caesar_shift(cipher, -s)
                print(f"Shift {s:2d}: {candidate}")
            print("-" * 40)

        elif choice == "4":
            print("Exiting Caesar CLI. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
