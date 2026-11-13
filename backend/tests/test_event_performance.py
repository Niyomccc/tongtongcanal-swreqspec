import time
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.config import PERFORMANCE_CONCURRENT_USERS, RESPONSE_TIME_P95_TARGET_SECONDS
from app.main import app


def _calculate_p95(values: list[float]) -> float:
    if not values:
        return 0.0

    sorted_values = sorted(values)
    index = max(0, min(len(sorted_values) - 1, int(__import__('math').ceil(0.95 * len(sorted_values))) - 1))
    return sorted_values[index]


def _request_event_detail() -> float:
    client = TestClient(app)
    started_at = time.perf_counter()
    response = client.get("/api/events/EVT-001")
    elapsed_ms = (time.perf_counter() - started_at) * 1000
    assert response.status_code == 200
    return elapsed_ms


def test_NFR_PERF_01_event_detail_response_time_p95_under_limit():
    durations: list[float] = []

    with ThreadPoolExecutor(max_workers=PERFORMANCE_CONCURRENT_USERS) as executor:
        for elapsed_ms in executor.map(lambda _: _request_event_detail(), range(PERFORMANCE_CONCURRENT_USERS)):
            durations.append(elapsed_ms)

    p95 = _calculate_p95(durations)
    assert p95 <= RESPONSE_TIME_P95_TARGET_SECONDS * 1000
