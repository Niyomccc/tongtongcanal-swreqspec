from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import REGISTRATION_STATUS_CANCELLED, REGISTRATION_STATUS_REGISTERED


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
    """ข้อมูล session และบทบาทสำหรับตรวจสิทธิ์ตาม FR-AUTH-03 และ NFR-SEC-01"""

    __tablename__ = "auth_sessions"

    session_id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), nullable=False)
    role: Mapped[str | None] = mapped_column(String)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Event(AuthBase):
    """ข้อมูลอีเว้นต์สำหรับลงทะเบียนตาม FR-REG-01, FR-REG-02, ASM-01 และ PRE-REG-01"""

    __tablename__ = "registration_events"

    event_id: Mapped[str] = mapped_column(String, primary_key=True)
    registration_open: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    remaining_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    registered_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Registration(AuthBase):
    """ข้อมูล user_id, event_id และ snapshot ที่ผู้ใช้ยืนยันตาม FR-REG-02, NFR-DAT-01 และ Q-02"""

    __tablename__ = "event_registrations"

    registration_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(
        ForeignKey("registration_events.event_id"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=REGISTRATION_STATUS_REGISTERED,
    )
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    confirmation_snapshot: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_event_registration_user_event"),
    )

    @property
    def is_cancelled(self) -> bool:
        """รองรับ PRE-CXL-01, FR-CXL-03 และ ASM-01: รายการที่ยกเลิกแล้วไม่ถูกนับเป็นคนลงทะเบียนที่ยังทำงานอยู่"""
        return self.status == REGISTRATION_STATUS_CANCELLED
