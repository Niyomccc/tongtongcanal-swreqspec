import math
import threading
import time

import pytest

from app.auth.login import login_user
from app.auth.register import register_user
from app.auth.repository import AuthRepository
from app.auth.session import reset_sessions


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
