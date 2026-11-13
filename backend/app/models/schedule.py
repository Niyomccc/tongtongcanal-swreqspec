from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScheduleEntry:
    """รองรับ FR-SCV-03 และ FR-SCV-04: รายการวงในตารางการแสดงพร้อมลำดับ วัน เวลา และสถานที่"""

    band_name: str
    show_order: int
    show_date: str
    start_time: str
    end_time: str
    venue: str


@dataclass(frozen=True)
class EventSchedule:
    """รองรับ PRE-SCV-01 และ FR-SCV-02: ข้อมูลตารางการแสดงของอีเว้นต์ตามสถานะการเผยแพร่"""

    event_id: str
    schedule_id: str
    status: str
    entries: tuple[ScheduleEntry, ...] = field(default_factory=tuple)
