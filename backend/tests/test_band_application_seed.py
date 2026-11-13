from app.auth.application import get_band_application_profile, get_open_application_events
from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions


def test_T02_seed_open_band_application_events():
    """ตรวจว่าระบบมีข้อมูลอีเว้นต์เปิดรับสมัครสำหรับ flow สมัครวงตาม T-02"""
    repo = AuthRepository()
    repo.reset()

    events = repo.seed_open_band_application_events()

    assert len(events) == 2
    assert {event["event_id"] for event in events} == {"event-band-01", "event-band-02"}
    assert all(event["registration_open"] is True for event in events)
    assert all(event["capacity"] > 0 for event in events)


def test_T02_create_band_snapshot_from_profile():
    """ตรวจว่าระบบสามารถสร้าง snapshot ของข้อมูลวงจาก UC-07 ให้พร้อมใช้งานกับใบสมัคร"""
    repo = AuthRepository()
    repo.reset()

    user = repo.create_user(
        email="moonlight@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Moonlight Band",
        role="band",
        profile={
            "band_name": "Moonlight Band",
            "genre": "Indie Pop",
            "members": "ณัฐพล (ร้อง/กีตาร์), ปิยะ (กลอง), มินตรา (เบส)",
            "contact_name": "ณัฐพล สุขใจ",
            "contact_phone": "089-876-5432",
        },
    )

    snapshot = repo.create_band_snapshot(
        band_id=user["id"],
        band_profile=user["profile"],
    )

    assert snapshot["band_name"] == "Moonlight Band"
    assert snapshot["genre"] == "Indie Pop"
    assert snapshot["contact_phone"] == "089-876-5432"
    assert repo.get_band_snapshot(snapshot["snapshot_id"]) == snapshot


def test_T03_get_open_events_and_band_profile_for_band_user():
    """ตรวจว่า GET /events/open และ GET /bands/me/application-profile คืนข้อมูลอีเว้นต์และความครบถ้วนของข้อมูลวงตาม T-03"""
    repo = AuthRepository()
    repo.reset()
    reset_sessions()

    user = repo.create_user(
        email="bandapp@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Moonlight Band",
        role="band",
        profile={
            "band_name": "Moonlight Band",
            "genre": "Indie Pop",
            "members": "ณัฐพล (ร้อง/กีตาร์), ปิยะ (กลอง), มินตรา (เบส)",
            "contact_name": "ณัฐพล สุขใจ",
            "contact_phone": "089-876-5432",
        },
    )
    session = create_session(user["id"], role="band")

    events = get_open_application_events(session_id=session["session_id"], repository=repo)
    assert events["success"] is True
    assert {event["event_id"] for event in events["events"]} == {"event-band-01", "event-band-02"}

    profile = get_band_application_profile(session_id=session["session_id"], repository=repo)
    assert profile["success"] is True
    assert profile["is_complete"] is True
    assert profile["band_profile"]["band_name"] == "Moonlight Band"
    assert profile["band_profile"]["genre"] == "Indie Pop"
    assert profile["missing_fields"] == []


def test_T03_profile_reports_missing_band_fields():
    """ตรวจว่า endpoint ของข้อมูลวงแจ้ง field ที่ขาดก่อนส่งใบสมัครตาม AC-APP-04/FR-APP-05"""
    repo = AuthRepository()
    repo.reset()
    reset_sessions()

    user = repo.create_user(
        email="incompleteband@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Incomplete Band",
        role="band",
        profile={
            "band_name": "Incomplete Band",
            "genre": "Rock",
        },
    )
    session = create_session(user["id"], role="band")

    profile = get_band_application_profile(session_id=session["session_id"], repository=repo)
    assert profile["success"] is True
    assert profile["is_complete"] is False
    assert "members" in profile["missing_fields"]
    assert "contact_name" in profile["missing_fields"]
    assert "contact_phone" in profile["missing_fields"]
