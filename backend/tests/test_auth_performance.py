import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.auth.login import login_user
from app.auth.register import register_user
from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import (
    BAND_APPLICATION_CONCURRENT_BANDS_TARGET,
    BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    BAND_APPLICATION_RESPONSE_P95_TARGET_SECONDS,
)
from app.main import app


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(0.95 * len(ordered)) - 1))
    return ordered[index]


@pytest.mark.parametrize("scenario", ["register"], ids=["register"])
def test_AC_AUTH_06_response_time_under_3s(scenario: str):
    """ตรวจวัด p95 ภายใต้โหลด 50 คน สำหรับนักศึกษาที่สมัครสมาชิกตาม AC-AUTH-06"""
    repo = AuthRepository()
    repo.reset()
    reset_sessions()

    barrier = threading.Barrier(50)
    durations: list[float] = []

    def submit(index: int) -> None:
        payload = {
            "email": f"student{index:02d}@ku.th",
            "password": "P@ssword123",
            "confirmPassword": "P@ssword123",
            "role": "นักศึกษา",
            "fullNameOrBandName": f"นักศึกษา {index}",
            "studentId": f"650{index:02d}",
            "universityCode": "KU",
        }
        barrier.wait()
        started_at = time.perf_counter()
        register_user(payload, repository=repo)
        durations.append(time.perf_counter() - started_at)

    threads = [threading.Thread(target=submit, args=(index,)) for index in range(50)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    p95 = _p95(durations)

    assert scenario == "register"
    assert p95 <= 3.0, f"p95 registration latency is {p95:.3f}s for 50 concurrent users"


@pytest.mark.parametrize("scenario", ["login"], ids=["login"])
def test_AC_AUTH_06_response_time_under_3s_login(scenario: str):
    """ตรวจวัด p95 ภายใต้โหลด 50 คน สำหรับการเข้าสู่ระบบตาม AC-AUTH-06"""
    repo = AuthRepository()
    repo.reset()
    reset_sessions()

    for index in range(50):
        register_user(
            {
                "email": f"student{index:02d}@ku.th",
                "password": "P@ssword123",
                "confirmPassword": "P@ssword123",
                "role": "นักศึกษา",
                "fullNameOrBandName": f"นักศึกษา {index}",
                "studentId": f"650{index:02d}",
                "universityCode": "KU",
            },
            repository=repo,
        )

    barrier = threading.Barrier(50)
    durations: list[float] = []

    def submit(index: int) -> None:
        email = f"student{index:02d}@ku.th"
        barrier.wait()
        started_at = time.perf_counter()
        result = login_user({"email": email, "password": "P@ssword123"}, repository=repo)
        durations.append(time.perf_counter() - started_at)
        assert result["success"] is True

    threads = [threading.Thread(target=submit, args=(index,)) for index in range(50)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    p95 = _p95(durations)

    assert scenario == "login"
    assert p95 <= 3.0, f"p95 login latency is {p95:.3f}s for 50 concurrent users"


# รองรับ NFR-SEC-01 และ Q-03: ห้ามเข้าถึงข้อมูลวงที่ใช้สร้าง snapshot โดยไม่มี session
def test_T_13_requires_authentication_before_snapshot_access():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    band = repo.create_user(
        email="snapshot-access@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Snapshot Band",
        role="band",
        profile={
            "band_name": "Snapshot Band",
            "genre": "Pop",
            "members": "นักร้อง",
            "contact_name": "ผู้ติดต่อ",
            "contact_phone": "089-000-0000",
        },
    )

    response = TestClient(app).get(
        "/api/bands/me/application-profile",
        params={"user_id": band["id"]},
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["band_profile"] == {}
    assert "กรุณาเข้าสู่ระบบก่อนใช้งาน" == response.json()["message"]


# รองรับ NFR-PERF-01 และ Q-03: ตรวจ P95 ของการส่งใบสมัครจากจำนวนวงเป้าหมาย
def test_T_13_application_submission_p95_under_target_for_concurrent_bands():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    event_id = repo.seed_open_band_application_events()[0]["event_id"]
    session_ids = []

    for index in range(BAND_APPLICATION_CONCURRENT_BANDS_TARGET):
        band = repo.create_user(
            email=f"performance-band-{index}@ku.th",
            password_hash="hash",
            salt="salt",
            full_name_or_band_name=f"Performance Band {index}",
            role="band",
            profile={
                "band_name": f"Performance Band {index}",
                "genre": "Pop",
                "members": "นักร้อง",
                "contact_name": "ผู้ติดต่อ",
                "contact_phone": "089-000-0000",
            },
        )
        session_ids.append(create_session(band["id"], role="band")["session_id"])

    barrier = threading.Barrier(BAND_APPLICATION_CONCURRENT_BANDS_TARGET)
    payload = {
        "event_id": event_id,
        "songs": [{"song_name": "เพลงต้นฉบับ", "song_type": "ต้นฉบับ"}],
        "total_duration_minutes": BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    }

    def submit(session_id: str) -> tuple[float, int, dict]:
        with TestClient(app) as client:
            barrier.wait()
            started_at = time.perf_counter()
            response = client.post(
                f"/api/applications?session_id={session_id}",
                json=payload,
            )
            elapsed = time.perf_counter() - started_at
            return elapsed, response.status_code, response.json()

    with ThreadPoolExecutor(max_workers=BAND_APPLICATION_CONCURRENT_BANDS_TARGET) as executor:
        results = list(executor.map(submit, session_ids))

    durations = [duration for duration, _, _ in results]
    responses = [(status_code, body) for _, status_code, body in results]
    p95 = _p95(durations)

    assert all(status_code == 200 and body["success"] is True for status_code, body in responses)
    application_ids = {body["application"]["application_id"] for _, body in responses}
    assert len(application_ids) == BAND_APPLICATION_CONCURRENT_BANDS_TARGET
    assert p95 <= BAND_APPLICATION_RESPONSE_P95_TARGET_SECONDS, (
        f"p95 application submission latency is {p95:.3f}s for "
        f"{BAND_APPLICATION_CONCURRENT_BANDS_TARGET} concurrent bands"
    )
