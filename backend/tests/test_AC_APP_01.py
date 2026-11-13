import pytest
from fastapi.testclient import TestClient

from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import BAND_APPLICATION_MAX_PERFORMANCE_MINUTES, BAND_APPLICATION_MAX_SONG_COUNT
from app.main import app


@pytest.fixture(autouse=True)
def clear_application_state():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    yield
    repo.reset()
    reset_sessions()


def create_band_context():
    repo = AuthRepository()
    band = repo.create_user(
        email="application@ku.th",
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
    return repo, session["session_id"], event["event_id"]


def valid_payload(event_id, *, song_count=2, duration=20):
    return {
        "event_id": event_id,
        "songs": [
            {"song_name": f"เพลง {index}", "song_type": "ต้นฉบับ"}
            for index in range(1, song_count + 1)
        ],
        "total_duration_minutes": duration,
    }


def test_TC_APP_01_1_create_application_for_open_event():
    # Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร และกรอกข้อมูลบังคับครบถ้วนโดยไม่เกินข้อจำกัดของอีเว้นต์
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(event_id)

    # When: วงส่งใบสมัคร
    response = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    )
    result = response.json()

    # Then: ระบบบันทึกใบสมัครสำเร็จ และผูกใบสมัครกับอีเว้นต์ที่เลือก
    assert response.status_code == 200
    assert result["success"] is True
    assert result["application"]["event_id"] == event_id
    assert repo.get_band_application(result["application"]["application_id"]) == result["application"]


def test_TC_APP_01_2_create_application_at_event_limits():
    # Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร และใช้ค่าข้อจำกัดสูงสุด 30 นาทีและ 8 เพลง
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(
        event_id,
        song_count=BAND_APPLICATION_MAX_SONG_COUNT,
        duration=BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    )

    # When: วงส่งใบสมัคร
    result = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    ).json()

    # Then: ระบบบันทึกใบสมัครสำเร็จ และผูกใบสมัครกับอีเว้นต์ที่เลือก
    assert result["success"] is True
    application = repo.get_band_application(result["application"]["application_id"])
    assert application is not None
    assert application["event_id"] == event_id


def test_TC_APP_01_3_submit_without_login():
    # Given: วงยังไม่ได้เข้าสู่ระบบ เลือกอีเว้นต์ที่เปิดรับสมัคร และกรอกข้อมูลครบถ้วนโดยไม่เกินข้อจำกัด
    repo, _, event_id = create_band_context()
    payload = valid_payload(event_id)

    # When: วงส่งใบสมัครโดยไม่มี session
    TestClient(app).post("/api/applications", json=payload)

    # Then: ต้องไม่เข้าถึง snapshot ก่อนยืนยันตัวตน และไม่สร้างใบสมัคร
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None


def test_TC_APP_01_4_submit_to_closed_event():
    # Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่ปิดรับสมัคร และกรอกข้อมูลครบถ้วนโดยไม่เกินข้อจำกัด
    repo, session_id, event_id = create_band_context()
    repo.get_event(event_id)["registration_open"] = False
    payload = valid_payload(event_id)

    # When: วงส่งใบสมัคร
    result = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    ).json()

    # Then: ระบบปฏิเสธการส่งไปยังอีเว้นต์ที่ปิดรับสมัครและไม่บันทึกใบสมัคร
    assert result["success"] is False
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None


def test_TC_APP_01_5_reject_application_without_song():
    # Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร และกรอกข้อมูลอื่นครบถ้วนแต่ไม่มีเพลง
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(event_id)
    payload["songs"] = []

    # When: วงส่งใบสมัคร
    result = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    ).json()

    # Then: ระบบไม่บันทึกใบสมัคร
    assert result["success"] is False
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None


def test_TC_APP_01_6_reject_application_over_duration_limit():
    # Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร มี 1 เพลง และความยาวรวมเกิน 30 นาที
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(
        event_id,
        song_count=1,
        duration=BAND_APPLICATION_MAX_PERFORMANCE_MINUTES + 1,
    )

    # When: วงส่งใบสมัคร
    result = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    ).json()

    # Then: ระบบไม่บันทึกใบสมัคร
    assert result["success"] is False
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None


def test_TC_APP_01_7_reject_application_over_song_limit():
    # Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร มีจำนวนเพลงเกิน 8 เพลงและความยาวรวมไม่เกินข้อจำกัด
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(
        event_id,
        song_count=BAND_APPLICATION_MAX_SONG_COUNT + 1,
        duration=BAND_APPLICATION_MAX_PERFORMANCE_MINUTES - 1,
    )

    # When: วงส่งใบสมัคร
    result = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    ).json()

    # Then: ระบบไม่บันทึกใบสมัคร
    assert result["success"] is False
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None
