from dataclasses import dataclass


@dataclass(frozen=True)
class EventDetail:
    """รองรับ PRE-EVD-01 และ FR-EVD-02: ข้อมูลอีเว้นต์ที่แสดงในหน้า Event Detail"""

    event_id: str
    title: str
    event_date: str
    start_time: str
    end_time: str
    location: str
    description: str
