import io
import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestAPIEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_serves_html(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/html", res.headers.get("content-type", ""))

    def test_caesar_encrypt_endpoint(self):
        res = self.client.post("/api/v1/caesar/encrypt", json={"text": "Hello, World!", "shift": 3})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"], "Khoor, Zruog!")
        self.assertEqual(data["shift"], 3)
        self.assertEqual(data["operation"], "encrypt")

    def test_caesar_decrypt_endpoint(self):
        res = self.client.post("/api/v1/caesar/decrypt", json={"text": "Khoor, Zruog!", "shift": 3})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"], "Hello, World!")
        self.assertEqual(data["shift"], 3)
        self.assertEqual(data["operation"], "decrypt")

    def test_caesar_brute_force_endpoint(self):
        res = self.client.post("/api/v1/caesar/brute-force", data={"text": "Khoor, Zruog!"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total_candidates"], 25)
        self.assertIsNotNone(data["best_candidate"])
        self.assertEqual(data["best_candidate"]["shift"], 3)

    def test_caesar_brute_force_empty_error(self):
        res = self.client.post("/api/v1/caesar/brute-force", data={"text": "   "})
        self.assertEqual(res.status_code, 400)

    def test_frequency_analysis_endpoint(self):
        res = self.client.post("/api/v1/caesar/frequency", data={"text": "Hello World!"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total_letters"], 10)
        self.assertIn("frequencies", data)
        self.assertIn("H", data["frequencies"])

    def test_rot13_endpoint(self):
        res = self.client.post("/api/v1/ciphers/rot13", json={"text": "Hello"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"], "Uryyb")
        self.assertEqual(data["cipher"], "ROT13")

    def test_atbash_endpoint(self):
        res = self.client.post("/api/v1/ciphers/atbash", json={"text": "ABC"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"], "ZYX")
        self.assertEqual(data["cipher"], "Atbash")

    def test_vigenere_endpoint(self):
        res = self.client.post("/api/v1/ciphers/vigenere", json={"text": "ATTACKATDAWN", "key": "LEMON", "decrypt": False})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"], "LXFOPVEFRNHR")

    def test_vigenere_missing_key(self):
        res = self.client.post("/api/v1/ciphers/vigenere", json={"text": "ATTACKATDAWN", "key": ""})
        self.assertEqual(res.status_code, 400)

    def test_file_upload_caesar(self):
        file_content = b"The quick brown fox jumps over the lazy dog."
        files = {"file": ("sample.txt", io.BytesIO(file_content), "text/plain")}
        res = self.client.post("/api/v1/files/caesar", files=files, data={"shift": 5, "decrypt": False})
        self.assertEqual(res.status_code, 200)
        encrypted_text = res.text
        self.assertEqual(encrypted_text, "Ymj vznhp gwtbs ktc ozrux tajw ymj qfed itl.")

        # Test roundtrip decryption
        decrypt_files = {"file": ("encrypted.txt", io.BytesIO(encrypted_text.encode("utf-8")), "text/plain")}
        res2 = self.client.post("/api/v1/files/caesar", files=decrypt_files, data={"shift": 5, "decrypt": True})
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.text, file_content.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
