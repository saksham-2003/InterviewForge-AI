import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, Optional

import bcrypt


class AuthService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "users.db")
        self._initialize_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _normalize_email(self, email: str) -> str:
        return email.strip().lower()

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        normalized_email = self._normalize_email(email)
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, full_name, email, password_hash, created_at FROM users WHERE lower(email) = ?",
                (normalized_email,),
            ).fetchone()
        if row is None:
            return None
        return dict(row)

    def register_user(
        self,
        full_name: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> Dict[str, Any]:
        full_name = full_name.strip()
        email = self._normalize_email(email)

        if not full_name or not email or not password or not confirm_password:
            return {"success": False, "message": "Please complete all fields to create an account."}

        if password != confirm_password:
            return {"success": False, "message": "Passwords do not match. Please try again."}

        if len(password) < 8:
            return {"success": False, "message": "Password must be at least 8 characters long."}

        if "@" not in email or "." not in email.split("@")[-1]:
            return {"success": False, "message": "Please enter a valid email address."}

        if self.get_user_by_email(email):
            return {"success": False, "message": "An account with this email already exists."}

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        created_at = datetime.utcnow().isoformat(timespec="seconds")

        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO users (full_name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (full_name, email, password_hash, created_at),
            )
            conn.commit()

        return {
            "success": True,
            "message": "Account created successfully. Please sign in.",
            "user": {
                "id": cursor.lastrowid,
                "full_name": full_name,
                "email": email,
                "created_at": created_at,
            },
        }

    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        email = self._normalize_email(email)
        if not email or not password:
            return {"success": False, "message": "Please enter both your email and password."}

        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "message": "No account was found for that email."}

        stored_hash = user.get("password_hash", "")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return {
                "success": True,
                "message": "Welcome back!",
                "user": {
                    "id": user["id"],
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "created_at": user["created_at"],
                },
            }

        return {"success": False, "message": "Incorrect password. Please try again."}
