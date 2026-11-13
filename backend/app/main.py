from fastapi import FastAPI

from app.auth.login import router as login_router
from app.auth.register import router as register_router
from app.auth.routes import router as permission_router


# โครง API สำหรับ FR-AUTH-01 และ FR-AUTH-03; หน้า /auth ให้บริการโดย React/Vite
app = FastAPI(title="Authentication API")
app.include_router(register_router)
app.include_router(login_router)
app.include_router(permission_router)
