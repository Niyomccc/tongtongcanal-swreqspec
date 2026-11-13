from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.auth.permissions import get_user_permission_summary, require_permission

# รองรับ FR-AUTH-05
router = APIRouter()


class PermissionCheckInput(BaseModel):
    role: str
    permission: str


@router.post("/api/auth/permissions/check")
def check_permission_endpoint(payload: PermissionCheckInput) -> dict[str, object]:
    try:
        require_permission(payload.role, payload.permission)
        return {
            "success": True,
            "allowed": True,
            "role": payload.role,
            "permission": payload.permission,
        }
    except PermissionError:
        return {
            "success": False,
            "allowed": False,
            "role": payload.role,
            "permission": payload.permission,
            "message": "คุณไม่มีสิทธิ์ดำเนินการนี้",
        }


@router.get("/api/auth/me")
def me_endpoint(role: str | None = None) -> dict[str, object]:
    return {
        "success": True,
        "user": {
            "role": role,
            "permissions": get_user_permission_summary({"role": role})["permissions"],
        },
    }


__all__ = ["router", "check_permission_endpoint", "me_endpoint", "PermissionCheckInput"]
