import os
import sqlite3
import tempfile
import unittest

from auth_service import AuthService


class AuthServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "users_test.db")
        self.auth = AuthService(db_path=self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_and_login_user(self):
        result = self.auth.register_user("Ada Lovelace", "ada@example.com", "StrongPass123!", "StrongPass123!")
        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(self.db_path))

        login = self.auth.authenticate_user("ada@example.com", "StrongPass123!")
        self.assertTrue(login["success"])
        self.assertEqual(login["user"]["email"], "ada@example.com")

    def test_duplicate_email_is_rejected(self):
        self.auth.register_user("Ada", "ada@example.com", "StrongPass123!", "StrongPass123!")
        result = self.auth.register_user("Grace", "ada@example.com", "AnotherPass123!", "AnotherPass123!")
        self.assertFalse(result["success"])
        self.assertIn("already exists", result["message"].lower())

    def test_invalid_credentials_are_rejected(self):
        self.auth.register_user("Ada", "ada@example.com", "StrongPass123!", "StrongPass123!")
        login = self.auth.authenticate_user("ada@example.com", "wrong-pass")
        self.assertFalse(login["success"])


if __name__ == "__main__":
    unittest.main()
