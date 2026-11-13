from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AuthBase(DeclarativeBase):
    """ฐานโมเดลสำหรับข้อมูล Auth ตาม FR-AUTH-02 และ FR-AUTH-05"""


class User(AuthBase):
    """ข้อมูลบัญชีผู้ใช้ตาม FR-AUTH-02, FR-AUTH-03, FR-AUTH-05 และ NFR-SEC-01"""

    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    salt: Mapped[str] = mapped_column(Text, nullable=False)
    full_name_or_band_name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    failed_login_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lock_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class StudentProfile(AuthBase):
    """ข้อมูลโปรไฟล์นักศึกษาตาม FR-AUTH-02 และ FR-AUTH-03"""

    __tablename__ = "auth_student_profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), primary_key=True)
    student_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    university_code: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AudienceProfile(AuthBase):
    """ข้อมูลโปรไฟล์ผู้ชมตาม FR-AUTH-02 และ FR-AUTH-03"""

    __tablename__ = "auth_audience_profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), primary_key=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class BandProfile(AuthBase):
    """ข้อมูลโปรไฟล์วงดนตรีตาม FR-AUTH-02, FR-AUTH-03 และ FR-AUTH-05"""

    __tablename__ = "auth_band_profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), primary_key=True)
    band_name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    contact_name: Mapped[str] = mapped_column(Text, nullable=False)
    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    member_count: Mapped[int | None] = mapped_column(Integer)
    genre: Mapped[str | None] = mapped_column(Text)
    performance_list: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RolePermission(AuthBase):
    """สิทธิ์ที่ผูกกับบทบาทตาม FR-AUTH-05"""

    __tablename__ = "auth_role_permissions"

    role: Mapped[str] = mapped_column(String, primary_key=True)
    permission_code: Mapped[str] = mapped_column(String, primary_key=True)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Session(AuthBase):
    """ข้อมูล session ตาม FR-AUTH-03 และ NFR-SEC-01"""

    __tablename__ = "auth_sessions"

    session_id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
