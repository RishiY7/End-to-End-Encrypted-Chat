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

    def test_rot13(self):
        text = "Hello, World!"
        self.assertEqual(rot13(rot13(text)), text)

    def test_atbash(self):
        self.assertEqual(atbash_cipher("ABC"), "ZYX")
        self.assertEqual(atbash_cipher("abc"), "zyx")
        self.assertEqual(atbash_cipher("Attack at dawn!"), "Zggzxp zg wzdm!")

    def test_vigenere(self):
        text = "ATTACKATDAWN"
        key = "LEMON"
        encrypted = vigenere_cipher(text, key, decrypt=False)
        self.assertEqual(encrypted, "LXFOPVEFRNHR")
        decrypted = vigenere_cipher(encrypted, key, decrypt=True)
        self.assertEqual(decrypted, text)


if __name__ == "__main__":
    unittest.main()
