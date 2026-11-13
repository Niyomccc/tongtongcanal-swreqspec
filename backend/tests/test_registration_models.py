from fastapi.testclient import TestClient

from app.main import app
from app.models.auth import Event, Registration


def test_REG_app_startup():
    client = TestClient(app)

    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json() == {"status": "ok", "message": "ระบบพร้อมใช้งาน"}

    ready_response = client.get("/api/registration/ready")
    assert ready_response.status_code == 200
    assert ready_response.json()["ready"] is True


def test_REG_models_and_availability():
    event_columns = set(Event.__table__.columns.keys())
    assert {"event_id", "registration_open", "capacity", "remaining_seats", "registered_count"}.issubset(
        event_columns
    )

    registration_columns = set(Registration.__table__.columns.keys())
    assert {"event_id", "user_id", "status", "registered_at", "cancelled_at"}.issubset(registration_columns)

    unique_pairs = {
        tuple(constraint.columns.keys())
        for constraint in Registration.__table__.constraints
        if hasattr(constraint, "columns")
    }
    assert ("user_id", "event_id") in unique_pairs

    fk_targets = {
        str(foreign_key.target_fullname)
        for column in Registration.__table__.columns
        for foreign_key in column.foreign_keys
    }
    assert "registration_events.event_id" in fk_targets
