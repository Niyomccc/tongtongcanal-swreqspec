# Tasks: ดูรายละเอียดอีเว้นต์ (Event Detail)

- Feature: ดูรายละเอียดอีเว้นต์ (Event Detail)
- Spec ID: SPEC-EVD-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-11-13

หมายเหตุ: Spec ยังอยู่ในสถานะ Draft v1 และมี NFR-PERF-01 ที่รอค่า Q-02 ก่อนทดสอบประสิทธิภาพจริง จึงควรพิจารณาให้ทีมยืนยันก่อนเริ่ม implementation อย่างเป็นทางการ

สรุป:
- เฟส: 4 (เฟส 0–2 และเฟสรอคำตอบ)
- Tasks: 8; รอ Open Questions: 1
- เฟสแรกที่ลองใช้งานจริง: เฟส 1 เลือกอีเว้นต์แล้วดูรายละเอียดสำเร็จ

## เฟส 0 ฐานราก: มีข้อมูลอีเว้นต์และเส้นทางดูรายละเอียด (PRE-EVD-01)

### T-01 ตั้งข้อมูลอีเว้นต์ตัวอย่างและ service loading
- รองรับ: PRE-EVD-01, FR-EVD-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-05
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/models/event.py`, `backend/app/services/event_service.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: มีข้อมูลอีเว้นต์ตัวอย่างในระบบและ service ที่คืนข้อมูลอีเว้นต์ตาม ID พร้อมใช้สำหรับหน้ารายละเอียด
- สถานะ: เสร็จ 

### T-02 สร้าง route และ client ดึงรายละเอียดอีเว้นต์
- รองรับ: FR-EVD-01, FR-EVD-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-04 และ T-05
- ไฟล์ที่แตะ: `backend/app/main.py`, `backend/app/routes/event_detail.py`, `frontend/src/api/client.js`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: backend มี endpoint สำหรับดึงข้อมูลอีเว้นต์ตาม ID และ frontend client เรียก endpoint ได้
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 0
- test ที่ต้องผ่านทั้งหมด: `test_EVD_data_seed`, `test_EVD_fetch_event_detail_api`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม PRE-EVD-01:
  Given มีข้อมูลอีเว้นต์อยู่ในระบบ
  When เปิดหน้าอีเว้นต์หรือเรียก API
  Then ได้ข้อมูลอีเว้นต์ตัวอย่างและสามารถต่อจากการเลือกอีเว้นต์ได้
- ยังขาด: ไม่มี

## เฟส 1: เลือกอีเว้นต์แล้วดูรายละเอียดสำเร็จ (AC-EVD-01, AC-EVD-02)

### T-03 ทดสอบและสร้าง backend ค้นหาข้อมูลอีเว้นต์ตามการเลือก
- รองรับ: FR-EVD-02
- ตรวจด้วย: AC-EVD-01, AC-EVD-02
- ไฟล์ที่แตะ: `backend/app/services/event_service.py`, `backend/tests/test_event_detail.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: `test_AC_EVD_01_event_name_detail` และ `test_AC_EVD_02_event_date_time_location` ผ่าน โดยข้อมูลที่คืนตรงกับฐานข้อมูลของอีเว้นต์ที่เลือก
- สถานะ: เสร็จ 

### T-04 ทำหน้าเลือกอีเว้นต์จากหน้ารายการ
- รองรับ: FR-EVD-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานเชื่อมหน้าเลือกอีเว้นต์
- ไฟล์ที่แตะ: `frontend/src/pages/EventListPage.jsx`, `frontend/src/__tests__/EventListPage.test.jsx`
- แบบหน้าจอ: UI-EVD-01 `mockups/UI-EVD-01-event-list.html`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ผู้ใช้เห็นรายการอีเว้นต์และเลือกอีเว้นต์หนึ่งรายการเพื่อเปิดหน้ารายละเอียด
- สถานะ: เสร็จ 

### T-05 ทำหน้ารายละเอียดอีเว้นต์แสดงชื่อ วัน เวลา สถานที่ และรายละเอียดกิจกรรม
- รองรับ: FR-EVD-02, NFR-DAT-01
- ตรวจด้วย: AC-EVD-01, AC-EVD-02
- ไฟล์ที่แตะ: `frontend/src/pages/EventDetailPage.jsx`, `frontend/src/__tests__/EventDetailPage.test.jsx`
- แบบหน้าจอ: UI-EVD-02 `mockups/UI-EVD-02-event-detail.html`
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: `test_AC_EVD_01_detail_content` และ `test_AC_EVD_02_date_time_location` ผ่าน และหน้าจอแสดงชื่อและรายละเอียดกิจกรรม, วัน เวลา สถานที่ครบทุกส่วน
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 1
- test ที่ต้องผ่านทั้งหมด: `test_EVD_data_seed`, `test_EVD_fetch_event_detail_api`, `test_AC_EVD_01_event_name_detail`, `test_AC_EVD_02_event_date_time_location`, `test_AC_EVD_01_detail_content`, `test_AC_EVD_02_date_time_location`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-EVD-01 และ AC-EVD-02:
  Given มีอีเว้นต์อยู่ในระบบและเลือกอีเว้นต์จากรายการ
  When ผู้ใช้เปิดหน้าอีเว้นต์
  Then จะเห็นชื่อและรายละเอียดกิจกรรม, วัน เวลา และสถานที่ของงานครบถ้วน
- ยังขาด: ไม่มี

## เฟส 2: ข้อมูลล่าสุดและกรณีไม่พบข้อมูล (AC-EVD-03, AC-EVD-04)

### T-06 จัดการข้อมูลล่าสุดเมื่ออีเว้นต์ถูกแก้ไข
- รองรับ: FR-EVD-03, NFR-DAT-01
- ตรวจด้วย: AC-EVD-03
- ไฟล์ที่แตะ: `backend/app/services/event_service.py`, `backend/tests/test_event_detail.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `test_AC_EVD_03_latest_event_data` ผ่าน โดยเมื่อข้อมูลอีเว้นต์ถูกแก้ไขแล้วหน้ารายละเอียดเปิดใหม่ใช้ข้อมูลล่าสุด
- สถานะ: เสร็จ 

### T-07 จัดการกรณีไม่พบข้อมูลอีเว้นต์
- รองรับ: FR-EVD-04
- ตรวจด้วย: AC-EVD-04
- ไฟล์ที่แตะ: `backend/app/routes/event_detail.py`, `frontend/src/pages/EventDetailPage.jsx`, `frontend/src/__tests__/EventDetailPage.test.jsx`
- แบบหน้าจอ: UI-EVD-02 `mockups/UI-EVD-02-event-detail.html`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: `test_AC_EVD_04_event_not_found` ผ่าน และผู้ใช้เห็นข้อความ "ไม่พบข้อมูลอีเว้นต์" เมื่อเลือกอีเว้นต์ที่ไม่มีอยู่
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 2
- test ที่ต้องผ่านทั้งหมด: `test_AC_EVD_03_latest_event_data`, `test_AC_EVD_04_event_not_found`, และ test ของเฟสก่อนหน้า
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-EVD-03 และ AC-EVD-04:
  Given ผู้จัดงานแก้ไขข้อมูลอีเว้นต์แล้ว หรือเลือกอีเว้นต์ที่ไม่มีอยู่
  When ผู้ใช้เปิดดูรายละเอียดอีเว้นต์นั้น
  Then จะแสดงข้อมูลล่าสุด หรือแจ้งว่าไม่พบข้อมูลอีเว้นต์ตามสถานะจริง
- ยังขาด: ไม่มี

## เฟส 3: รอคำตอบ (Q-02)

### T-08 กำหนดค่าและทดสอบประสิทธิภาพ NFR-PERF-01
- รองรับ: NFR-PERF-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เพราะค่าที่วัดได้ได้กำหนดเป็น p95 ไม่เกิน 3 วินาที เมื่อผู้ใช้พร้อมกัน 50 คน
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/tests/test_event_performance.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `test_NFR_PERF_01_event_detail_response_time_p95_under_limit` ผ่าน โดย `p95` ของการเรียก `/api/events/EVT-001` ไม่เกิน 3 วินาที เมื่อมีผู้ใช้พร้อมกัน 50 คน
- สถานะ: เสร็จ 

### ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-EVD-01 | T-03, T-05 |
| AC-EVD-02 | T-03, T-05 |
| AC-EVD-03 | T-06 |
| AC-EVD-04 | T-07 |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| PRE-EVD-01 | T-01, T-03 |

| FR ID | AC ที่ตรวจ FR นี้ | เฟส |
|---|---|---|
| FR-EVD-01 | ไม่มี AC ควรเสนอทีมเพิ่ม | เฟส 1 |
| FR-EVD-02 | AC-EVD-01, AC-EVD-02 | เฟส 1 |
| FR-EVD-03 | AC-EVD-03 | เฟส 2 |
| FR-EVD-04 | AC-EVD-04 | เฟส 2 |
| NFR-DAT-01 | AC-EVD-03 | เฟส 2 |
| NFR-PERF-01 | รอ Q-02 | เฟส 3 |

### สิ่งที่ยังไม่ทำ
- ASM-01: พฤติกรรมเมื่อไม่พบข้อมูล (แจ้งข้อความให้ผู้ใช้ทราบ) เป็นข้อสันนิษฐานของผู้เขียน spec
- Q-02: ต้องกำหนดค่าที่วัดได้สำหรับ NFR-PERF-01 ก่อนจัดทำ test ประสิทธิภาพ
