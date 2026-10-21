import unittest
from app.crypto.caesar import caesar_shift, brute_force_crack, get_frequency_analysis
from app.crypto.ciphers import rot13, atbash_cipher, vigenere_cipher


class TestCiphers(unittest.TestCase):

    def test_caesar_encrypt(self):
        self.assertEqual(caesar_shift("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(caesar_shift("abc", 1), "bcd")
        self.assertEqual(caesar_shift("xyz", 3), "abc")

    def test_caesar_decrypt(self):
        self.assertEqual(caesar_shift("Khoor, Zruog!", -3), "Hello, World!")

    def test_caesar_large_and_negative_shifts(self):
        self.assertEqual(caesar_shift("abc", 26), "abc")
        self.assertEqual(caesar_shift("abc", 52), "abc")
        self.assertEqual(caesar_shift("abc", -1), "zab")

    def test_caesar_non_ascii_preservation(self):
        # Accented characters, numbers, and emojis should be preserved untouched
        sample = "café 123! 🚀"
        encrypted = caesar_shift(sample, 3)
        self.assertEqual(encrypted, "fdié 123! 🚀")
        decrypted = caesar_shift(encrypted, -3)
        self.assertEqual(decrypted, sample)

    def test_caesar_preserve_case_flag(self):
        self.assertEqual(caesar_shift("Hello", 3, preserve_case=True), "Khoor")
        self.assertEqual(caesar_shift("Hello", 3, preserve_case=False), "KHOOR")

    def test_smart_brute_force_cracker(self):
        secret = "The quick brown fox jumps over the lazy dog."
        encrypted = caesar_shift(secret, 5)
        candidates = brute_force_crack(encrypted)
        
        self.assertEqual(len(candidates), 25)
        top_candidate = candidates[0]
        # The best candidate should recover the message with shift 5
        self.assertEqual(top_candidate["shift"], 5)
        self.assertEqual(top_candidate["decrypted_text"], secret)

    def test_frequency_analysis(self):
        freqs = get_frequency_analysis("EEEAAA")
        self.assertEqual(freqs["E"]["count"], 3)
        self.assertEqual(freqs["A"]["count"], 3)
        self.assertEqual(freqs["B"]["count"], 0)

    def test_frequency_analysis_non_ascii(self):
        # Non-ASCII characters should not cause a KeyError
        freqs = get_frequency_analysis("café")
        self.assertEqual(freqs["C"]["count"], 1)
        self.assertEqual(freqs["A"]["count"], 1)
        self.assertEqual(freqs["F"]["count"], 1)

    def test_rot13(self):
        text = "Hello, World!"
        self.assertEqual(rot13(rot13(text)), text)

    def test_atbash(self):
        self.assertEqual(atbash_cipher("ABC"), "ZYX")
        self.assertEqual(atbash_cipher("abc"), "zyx")
        self.assertEqual(atbash_cipher("Attack at dawn!"), "Zggzxp zg wzdm!")

    def test_atbash_non_ascii_preservation(self):
        # Should preserve non-ASCII letters without crashing
        self.assertEqual(atbash_cipher("café 123!"), "xzué 123!")

    def test_vigenere(self):
        text = "ATTACKATDAWN"
        key = "LEMON"
        encrypted = vigenere_cipher(text, key, decrypt=False)
        self.assertEqual(encrypted, "LXFOPVEFRNHR")
        decrypted = vigenere_cipher(encrypted, key, decrypt=True)
        self.assertEqual(decrypted, text)

    def test_vigenere_non_ascii_and_validation(self):
        # Preserves non-ASCII and special characters ('c'+10='m', 'a'+4='e', 'f'+24='d')
        self.assertEqual(vigenere_cipher("café 123!", "KEY"), "medé 123!")
        # Empty or non-alphabetic key raises ValueError
        with self.assertRaises(ValueError):
            vigenere_cipher("Hello", "123!@#")


if __name__ == "__main__":
    unittest.main()
