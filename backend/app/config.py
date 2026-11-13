"""ค่าที่กำหนดจากข้อกำหนด Auth และ Registration"""

# Registration model rules: capacity and remaining seats come from the Event record,
# while the duplicate guard is enforced by the unique user_id + event_id pair.
# ข้อมูลถูกระบุใน Event และ Registration model ตาม FR-REG-01, FR-REG-02, FR-REG-05, ASM-01, ASM-02 และ ASM-03
EVENT_REGISTRATION_UNIQUE_FIELDS = ("user_id", "event_id")
EVENT_REGISTRATION_OPEN_FLAG = "registration_open"

# NFR-SEC-01
PASSWORD_MIN_LENGTH = 8
MINIMUM_TLS_VERSION = "1.2"
SESSION_IDLE_TIMEOUT_MINUTES = 30
FAILED_LOGIN_ATTEMPT_LIMIT = 5
ACCOUNT_LOCKOUT_DURATION_MINUTES = 15
GENERIC_LOGIN_ERROR_MESSAGE = "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

# Q-01: เกณฑ์แจ้งเตือนว่าที่นั่งเหลือน้อยกำหนดเป็นจำนวนที่นั่งที่เหลือไม่เกิน 5 ที่นั่ง
EVENT_REGISTRATION_LOW_SEAT_THRESHOLD = 5

# FR-APP-01 และ FR-APP-02: Data seed สำหรับอีเว้นต์ที่เปิดรับสมัครและข้อมูล snapshot ของวง
BAND_APPLICATION_EVENT_IDS = ("event-band-01", "event-band-02")
BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS = (
    "band_name",
    "genre",
    "members",
    "contact_name",
    "contact_phone",
)
# Q-02: ใช้ข้อจำกัดเดียวกันทุกอีเว้นต์
BAND_APPLICATION_MAX_PERFORMANCE_MINUTES = 30
BAND_APPLICATION_MAX_SONG_COUNT = 8
# NFR-SEC-01, NFR-PERF-01, Q-03
BAND_APPLICATION_CONCURRENT_BANDS_TARGET = 20
BAND_APPLICATION_RESPONSE_P95_TARGET_SECONDS = 2.0

# PRE-CXL-01, FR-CXL-01, FR-CXL-03, ASM-01, ASM-03, ASM-04
REGISTRATION_STATUS_REGISTERED = "ลงทะเบียน"
REGISTRATION_STATUS_CANCELLED = "ยกเลิก"

# NFR-PERF-01
RESPONSE_TIME_P95_TARGET_SECONDS = 3
PERFORMANCE_CONCURRENT_USERS = 50
