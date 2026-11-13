# Tasks: ดูตารางการแสดง (Schedule View)

- Feature: ดูตารางการแสดง (Schedule View)
- Spec ID: SPEC-SCV-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-11-13

สรุป:
- เฟส: 4 (เฟส 0–2 และเฟสรอคำตอบ)
- Tasks: 8; รอ Open Questions: 5
- เฟสแรกที่ลองใช้งานจริง: เฟส 1 แสดงตารางที่เผยแพร่แล้วครบถ้วนตามข้อมูลจริง

## เฟส 0 ฐานราก: มีข้อมูลตารางและเส้นทางดึงข้อมูล (PRE-SCV-01)

### T-01 ตั้งข้อมูลตารางตัวอย่างและ service loading
- รองรับ: PRE-SCV-01, FR-SCV-02, NFR-DAT-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-04
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/models/`, `backend/app/services/schedule_service.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: มีข้อมูลตัวอย่างตารางการแสดงที่เผยแพร่แล้วในระบบ และ service คืนสเตตัสและรายการตารางตาม `event_id` ที่เลือกได้
- สถานะ: เสร็จ 

### T-02 สร้าง route และ client ดึงข้อมูลตาราง
- รองรับ: FR-SCV-02, ASM-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-04
- ไฟล์ที่แตะ: `backend/app/main.py`, `backend/app/routes/schedule_view.py`, `frontend/src/api/client.js`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: backend มี endpoint สำหรับดึงข้อมูลตารางตามอีเว้นต์ที่เลือกและ frontend client เรียกได้ตามสัญญา API
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 0
- test ที่ต้องผ่านทั้งหมด: `test_SCV_data_seed`, `test_SCV_fetch_schedule_api`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม PRE-SCV-01:
  Given มีข้อมูลตารางเผยแพร่แล้วหรือยังไม่เผยแพร่
  When เปิดหน้าเมนูตารางการแสดงหรือเรียก API
  Then ได้ข้อมูลตารางตัวอย่างหรือสถานะ “ยังไม่มีตารางการแสดง” ตามข้อมูลจริง
- ยังขาด: ไม่มี

## เฟส 1: แสดงตารางที่เผยแพร่แล้วสำเร็จ (AC-SCV-01, AC-SCV-02, AC-SCV-03)

### T-03 ทำหน้าแสดงตารางการแสดงแบบเผยแพร่แล้ว
- รองรับ: FR-SCV-02, FR-SCV-03, FR-SCV-04, NFR-DAT-01
- ตรวจด้วย: AC-SCV-01, AC-SCV-02, AC-SCV-03
- ไฟล์ที่แตะ: `frontend/src/pages/ScheduleViewPage.jsx`, `frontend/src/__tests__/ScheduleViewPage.test.jsx`
- แบบหน้าจอ: UI-SCV-01 `mockups/UI-SCV-01-schedule.html`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: หน้าแสดงรายชื่อวงตามลำดับ วัน เวลา และสถานที่ครบถ้วน และข้อมูลตรงกับข้อมูลที่ผู้จัดงานเผยแพร่
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 1
- test ที่ต้องผ่านทั้งหมด: `test_SCV_data_seed`, `test_SCV_fetch_schedule_api`, `test_AC_SCV_01_show_bands_in_schedule_order`, `test_AC_SCV_02_show_date_time_and_venue`, `test_AC_SCV_03_schedule_matches_published_data`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-SCV-01 ถึง AC-SCV-03:
  Given ผู้จัดงานเผยแพร่ตารางของอีเว้นต์แล้ว
  When ผู้ใช้เปิดหน้า Schedule View
  Then จะเห็นรายชื่อวงตามลำดับ วัน เวลา และสถานที่ครบถ้วนตรงกับข้อมูลจริง
- ยังขาด: ไม่มี

## เฟส 2: กรณีไม่มีตารางและกรณีเรียกข้อมูลล้มเหลว (AC-SCV-04, AC-SCV-05)

### T-04 จัดการกรณียังไม่มีการประกาศตาราง
- รองรับ: FR-SCV-05, PRE-SCV-01, ASM-02
- ตรวจด้วย: AC-SCV-04
- ไฟล์ที่แตะ: `backend/app/routes/schedule_view.py`, `frontend/src/pages/ScheduleViewPage.jsx`, `frontend/src/__tests__/ScheduleViewPage.test.jsx`
- แบบหน้าจอ: UI-SCV-01 `mockups/UI-SCV-01-schedule.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่ออีเว้นต์ยังไม่มีการเผยแพร่ตาราง ระบบแจ้งว่า “ยังไม่มีตารางการแสดง” และไม่แสดงรายการวงใด ๆ
- สถานะ: พร้อมทำ

### T-05 จัดการกรณีเรียกข้อมูลตารางไม่ได้
- รองรับ: FR-SCV-06, ASM-01
- ตรวจด้วย: AC-SCV-05
- ไฟล์ที่แตะ: `backend/app/routes/schedule_view.py`, `frontend/src/pages/ScheduleViewPage.jsx`, `frontend/src/__tests__/ScheduleViewPage.test.jsx`
- แบบหน้าจอ: UI-SCV-01 `mockups/UI-SCV-01-schedule.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อข้อมูลไม่สามารถเรียกได้ ระบบแจ้งผู้ใช้ว่า “แสดงตารางไม่ได้” และไม่พาให้เห็นข้อมูลที่ไม่ครบถ้วน
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 2
- test ที่ต้องผ่านทั้งหมด: `test_AC_SCV_04_unpublished_schedule_message`, `test_AC_SCV_05_schedule_load_failure_message`, และ test ของเฟสก่อนหน้า
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-SCV-04 และ AC-SCV-05:
  Given อีเว้นต์ยังไม่มีตารางหรือระบบเรียกข้อมูลไม่ได้
  When ผู้ใช้เปิดตารางการแสดง
  Then จะเห็นข้อความที่ถูกต้องตามสถานะจริง ไม่แสดงข้อมูลที่ยังไม่เผยแพร่หรือข้อมูลที่ไม่สมบูรณ์
- ยังขาด: ไม่มี

## เฟส 3: รอคำตอบ (Q-02, Q-03, Q-04, Q-05, Q-06)

### T-06 กำหนดเมนูและการเลือกอีเว้นต์เพื่อดูตาราง (Q-03)
- รองรับ: FR-SCV-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เพราะยังต้องตัดสินใจว่าจะใช้ AC ใดเพื่อยืนยันเมนูและการเลือกอีเว้นต์
- ไฟล์ที่แตะ: `frontend/src/pages/ScheduleListPage.jsx` หรือ `frontend/src/pages/ScheduleViewPage.jsx`
- แบบหน้าจอ: UI-SCV-01 `mockups/UI-SCV-01-schedule.html`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ทีมกำหนดว่ามี AC ใดที่ตรวจการเลือกเมนูตารางการแสดงและการเลือกอีเว้นต์ และ task สอดคล้องกับ AC นั้น
- สถานะ: เสร็จ 

### T-07 กำหนดการเรียงลำดับและค่าเริ่มต้นของวันที่/เวลา/สถานที่ (Q-04, Q-05)
- รองรับ: FR-SCV-03, FR-SCV-04, NFR-DAT-01
- ตรวจด้วย: AC-SCV-01, AC-SCV-02, AC-SCV-03
- ไฟล์ที่แตะ: `backend/app/services/schedule_service.py`, `frontend/src/pages/ScheduleViewPage.jsx`
- แบบหน้าจอ: UI-SCV-01 `mockups/UI-SCV-01-schedule.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ทีมกำหนดว่าสถานะการเรียงลำดับใช้แบบไหน และด้านข้อมูลที่ขาดหายไปจะแสดงอย่างไร ก่อนเริ่มเขียนทดสอบลำดับหรือการแสดงข้อมูลหาย
- สถานะ: เสร็จ 

### T-08 กำหนดค่าประสิทธิภาพและเงื่อนไขกรณีเรียกข้อมูลล้มเหลว (Q-02, Q-06)
- รองรับ: NFR-PERF-01, FR-SCV-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เพราะค่าทางประสิทธิภาพและเงื่อนไขของ DB failure ยังไม่กำหนดชัดเจน
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/tests/test_schedule_performance.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ทีมกำหนดค่า `[N]`, `[P]`, `[X]` สำหรับ NFR-PERF-01 และกำหนดเงื่อนไขว่า “เรียกข้อมูลจากฐานข้อมูลไม่ได้” หมายถึงอะไรก่อนทำ performance test
- สถานะ: เสร็จ 

### ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-SCV-01 | T-03 |
| AC-SCV-02 | T-03 |
| AC-SCV-03 | T-03 |
| AC-SCV-04 | T-04 |
| AC-SCV-05 | T-05 |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| PRE-SCV-01 | T-01, T-04 |

| FR ID | AC ที่ตรวจ FR นี้ | เฟส |
|---|---|---|
| FR-SCV-01 | ไม่มี AC ควรเสนอทีมเพิ่ม | เฟส 3 |
| FR-SCV-02 | AC-SCV-03 | เฟส 1 |
| FR-SCV-03 | AC-SCV-01 | เฟส 1 |
| FR-SCV-04 | AC-SCV-02 | เฟส 1 |
| FR-SCV-05 | AC-SCV-04 | เฟส 2 |
| FR-SCV-06 | AC-SCV-05 | เฟส 2 |
| NFR-DAT-01 | AC-SCV-03 | เฟส 1 |
| NFR-PERF-01 | ไม่มี AC ควรเสนอทีมเพิ่ม | เฟส 3 |

### สิ่งที่ยังไม่ทำ
- Q-02: ต้องกำหนดค่าจริงของ `[N]`, `[P]` และ `[X]` ก่อนทดสอบประสิทธิภาพ
- Q-03: ต้องใช้ AC ใดเพื่อยืนยันการเลือกเมนูตารางการแสดงและการเลือกอีเว้นต์
- Q-04: ระบุว่าลำดับการแสดงใช้ลำดับที่ผู้จัดงานกำหนดหรือเรียงตามวันและเวลา
- Q-05: ต้องกำหนดว่าข้อมูลวัน เวลา และสถานที่หากมีค่าหายหรือว่างต้องแสดงอย่างไร
- Q-06: ต้องกำหนดว่าสถานะ “เรียกข้อมูลจากฐานข้อมูลไม่ได้” ครอบคลุมกรณีใดบ้าง
