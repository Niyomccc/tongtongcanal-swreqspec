import pytest
from fastapi.testclient import TestClient

from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import BAND_APPLICATION_MAX_PERFORMANCE_MINUTES
from app.main import app


class FailingApplicationStore(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        raise MemoryError("simulated storage failure")


@pytest.fixture(autouse=True)
def clear_application_state():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    yield
    repo.reset()
    reset_sessions()


def test_AC_APP_05_do_not_create_partial_application_on_save_failure():
    repo = AuthRepository()
    band = repo.create_user(
        email="application-failure@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Moonlight Band",
        role="band",
        profile={
            "band_name": "Moonlight Band",
            "genre": "Indie Pop",
            "members": "นักร้องและกีตาร์, กลอง, เบส",
            "contact_name": "ผู้ติดต่อ",
            "contact_phone": "089-876-5432",
        },
    )
    session = create_session(band["id"], role="band")
    event = repo.seed_open_band_application_events()[0]
    repo._band_applications_by_id = FailingApplicationStore()
    payload = {
        "event_id": event["event_id"],
        "songs": [{"song_name": "เพลงต้นฉบับ", "song_type": "ต้นฉบับ"}],
        "total_duration_minutes": BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    }

    response = TestClient(app).post(
        f"/api/applications?session_id={session['session_id']}",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": False,
        "message": "ส่งใบสมัครไม่สำเร็จ",
    }
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None
    assert repo._next_band_application_id == 1
    assert repo._next_band_snapshot_id == 1
