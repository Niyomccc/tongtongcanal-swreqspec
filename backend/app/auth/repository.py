from __future__ import annotations

from threading import RLock
from typing import Any


# รองรับ FR-AUTH-02, FR-AUTH-03, FR-AUTH-05 และ NFR-SEC-01
class AuthRepository:
    """คลังข้อมูลบัญชีผู้ใช้แบบในหน่วยความจำสำหรับ API สมัครสมาชิก"""

    _instance: "AuthRepository | None" = None
    _lock = RLock()

    def __new__(cls) -> "AuthRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self._users_by_email: dict[str, dict[str, Any]] = {}
        self._users_by_id: dict[int, dict[str, Any]] = {}
        self._student_ids: dict[str, int] = {}
        self._band_names: dict[str, int] = {}
        self._next_user_id = 1

    def reset(self) -> None:
        self._users_by_email.clear()
        self._users_by_id.clear()
        self._student_ids.clear()
        self._band_names.clear()
        self._next_user_id = 1

    def create_user(
        self,
        *,
        email: str,
        password_hash: str,
        salt: str,
        full_name_or_band_name: str,
        role: str,
        profile: dict[str, Any],
    ) -> dict[str, Any]:
        normalized_email = email.strip().lower()
        if self._users_by_email.get(normalized_email):
            raise ValueError("อีเมลนี้มีผู้ใช้อยู่แล้ว")

        role = role.strip().lower()
        if role == "student":
            student_id = str(profile.get("student_id") or "").strip()
            if not student_id:
                raise ValueError("ต้องระบุรหัสนักศึกษา")
            if student_id in self._student_ids:
                raise ValueError("รหัสนักศึกษานี้มีผู้ใช้อยู่แล้ว")
            self._student_ids[student_id] = self._next_user_id
        elif role == "band":
            band_name = str(profile.get("band_name") or "").strip()
            if not band_name:
                raise ValueError("ต้องระบุชื่อวง")
            if band_name.lower() in {name.lower() for name in self._band_names}:
                raise ValueError("ชื่อวงนี้มีผู้ใช้อยู่แล้ว")
            self._band_names[band_name.lower()] = self._next_user_id

        user_id = self._next_user_id
        self._next_user_id += 1

        user_record: dict[str, Any] = {
            "id": user_id,
            "email": normalized_email,
            "password_hash": password_hash,
            "salt": salt,
            "full_name_or_band_name": full_name_or_band_name.strip(),
            "role": role,
            "status": "active",
            "created_at": None,
            "profile": profile,
        }

        self._users_by_email[normalized_email] = user_record
        self._users_by_id[user_id] = user_record
        return user_record

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        return self._users_by_email.get(email.strip().lower())

    def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        return self._users_by_id.get(user_id)

    def get_by_student_id(self, student_id: str) -> dict[str, Any] | None:
        user_id = self._student_ids.get(student_id.strip())
        if user_id is None:
            return None
        return self._users_by_id.get(user_id)

    def get_by_band_name(self, band_name: str) -> dict[str, Any] | None:
        user_id = self._band_names.get(band_name.strip().lower())
        if user_id is None:
            return None
        return self._users_by_id.get(user_id)
