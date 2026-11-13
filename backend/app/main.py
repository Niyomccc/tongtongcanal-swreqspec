from fastapi import FastAPI

from app.auth.login import router as login_router
from app.auth.register import router as register_router
from app.auth.routes import router as auth_routes


# รองรับ PRE-REG-01 และ FR-REG-01: แอปเปิดได้พร้อมเส้นทางพื้นฐานสำหรับผู้ใช้ที่เข้าสู่ระบบแล้ว
app = FastAPI(title="Authentication API")


@app.get("/")
def app_root() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "ระบบพร้อมใช้งาน",
    }


app.include_router(register_router)
app.include_router(login_router)
app.include_router(auth_routes)
