# Tasks: ลงทะเบียนเข้าชมงาน (Event Registration)

- Feature: ลงทะเบียนเข้าชมงาน (Event Registration)
- Spec ID: SPEC-REG-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-11-13

สรุป:
- เฟส: 5 (เฟส 0–3 และเฟสรอคำตอบ)
- Tasks: 10; รอ Open Questions: 1 (Q-04)
- เฟสแรกที่ลองใช้งานจริง: เฟส 1 ลงทะเบียนสำเร็จ

## เฟส 0 ฐานราก

### T-01 ตั้งโครงพื้นฐานสำหรับ registration flow
- รองรับ: PRE-REG-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-07
- ไฟล์ที่แตะ: `backend/app/main.py`, `backend/app/auth/routes.py`, `frontend/src/App.jsx`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ระบบเปิดได้และมีเส้นทางเริ่มต้นสำหรับผู้ใช้ที่เข้าสู่ระบบแล้วไปยังหน้าลงทะเบียนอีเว้นต์ตาม precondition
- สถานะ: เสร็จ 

### T-02 กำหนดโครงข้อมูล Event และ Registration
- รองรับ: FR-REG-01, FR-REG-02, FR-REG-05, ASM-01, ASM-02, ASM-03
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03, T-05, T-06 และ T-07
- ไฟล์ที่แตะ: `backend/app/models/auth.py`, `backend/app/config.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: โครงข้อมูลอีเว้นต์และการลงทะเบียนพร้อม champs สำหรับ event_id, user_id, capacity, remaining seats และตรวจว่าคู่ user_id + event_id ซ้ำไม่เกิดขึ้นได้
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 0
- test ที่ต้องผ่านทั้งหมด: `test_REG_app_startup`, `test_REG_models_and_availability`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม PRE-REG-01:
  Given ผู้ใช้เข้าสู่ระบบแล้ว
  When เปิดหน้าลงทะเบียนอีเว้นต์
  Then จะเห็นการเลือกอีเว้นต์และสถานะความจุที่ระบบสามารถตรวจสอบได้
- ยังขาด: ไม่มี

## เฟส 1 ลงทะเบียนสำเร็จ (AC-REG-01, AC-REG-02)

### T-03 สร้าง API ลงทะเบียนสำเร็จ
- รองรับ: FR-REG-02, NFR-DAT-01, PRE-REG-01
- ตรวจด้วย: AC-REG-01, AC-REG-02
- ไฟล์ที่แตะ: `backend/app/auth/register.py`, `backend/app/auth/repository.py`, `backend/tests/test_auth_registration.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: `test_AC_REG_01_register_available_event` และ `test_AC_REG_02_store_confirmed_registration_data` ผ่าน โดยบันทึกผู้ใช้เป็นผู้ลงทะเบียนของอีเว้นต์และคงข้อมูลยืนยันให้ตรงกับผู้ใช้
- สถานะ: เสร็จ 

### T-04 ทำหน้าเลือกอีเว้นต์และยืนยันลงทะเบียน
- รองรับ: FR-REG-01, FR-REG-02
- ตรวจด้วย: AC-REG-01, AC-REG-02
- ไฟล์ที่แตะ: `frontend/src/pages/RegisterPage.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/RegisterPage.test.jsx`
- แบบหน้าจอ: UI-REG-01 `mockups/UI-REG-01-register.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: การเลือกอีเว้นต์และกดยืนยันผ่าน API client แล้วแสดงผลการลงทะเบียนสำเร็จตาม mockup ที่ระบุและมี test UI สำหรับ AC-REG-01 และ AC-REG-02 ผ่าน
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 1
- test ที่ต้องผ่านทั้งหมด: `test_REG_app_startup`, `test_REG_models_and_availability`, `test_AC_REG_01_register_available_event`, `test_AC_REG_02_store_confirmed_registration_data`, `test_AC_REG_01_register_form`, `test_AC_REG_02_register_success_ui`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-REG-01:
  Given ผู้ใช้เข้าสู่ระบบแล้ว และอีเว้นต์เปิดให้ลงทะเบียนและมีที่ว่าง
  When ผู้ใช้ยืนยันการลงทะเบียน
  Then ระบบบันทึกสำเร็จ ผู้ใช้เป็นผู้ลงทะเบียนของอีเว้นต์ และแสดงผลลงทะเบียนสำเร็จ
- ยังขาด: ไม่มี

## เฟส 2 แจ้งจำนวนที่นั่งเหลือน้อยและป้องกันซ้ำ (AC-REG-03, AC-REG-04)

### T-05 ตรวจจำนวนที่ว่างและแจ้งเมื่อเหลือน้อย
- รองรับ: FR-REG-01, FR-REG-03, AC-REG-03
- ตรวจด้วย: AC-REG-03
- ไฟล์ที่แตะ: `backend/app/auth/register.py`, `backend/app/config.py`, `backend/tests/test_auth_registration.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ระบบคำนวณจำนวนที่ว่างและแจ้งเตือนเมื่ออีเว้นต์เหลือที่นั่งไม่เกินเกณฑ์ที่กำหนดตาม N = 5 ที่นั่งที่เหลือ
- สถานะ: เสร็จ 

### T-06 ป้องกันการลงทะเบียนซ้ำและแสดงข้อปฏิเสธที่เหมาะสม
- รองรับ: FR-REG-05, AC-REG-04
- ตรวจด้วย: AC-REG-04
- ไฟล์ที่แตะ: `backend/app/auth/register.py`, `backend/tests/test_auth_registration.py`, `frontend/src/pages/RegisterPage.jsx`, `frontend/src/__tests__/RegisterPage.test.jsx`
- แบบหน้าจอ: UI-REG-01 `mockups/UI-REG-01-register.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อผู้ใช้มีการลงทะเบียนเดิมที่ยังไม่ยกเลิก ระบบปฏิเสธและไม่สร้างรายการซ้ำ พร้อมแสดงผลว่าลงทะเบียนซ้ำไม่ได้
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 2
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–1 และ `test_AC_REG_03_show_remaining_seats_when_below_threshold`, `test_AC_REG_04_reject_duplicate_registration`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-REG-03 และ AC-REG-04:
  Given อีเว้นต์เหลือไม่เกินเกณฑ์ที่กำหนด หรือผู้ใช้มีการลงทะเบียนอีเว้นต์นี้แล้ว
  When ผู้ใช้เข้าดูจำนวนที่ว่างหรือพยายามยืนยันลงทะเบียนอีกครั้ง
  Then ระบบแจ้งจำนวนที่เหลือ หรือปฏิเสธการลงทะเบียนซ้ำตามเงื่อนไข
- ยังขาด: Q-01 รายละเอียดเกณฑ์ "เหลือน้อย" และ Q-02 ความละเอียดข้อมูลที่ต้องบันทึกเพื่อยืนยันตรงกับผู้ใช้

## เฟส 3 ปฏิเสธเมื่อเต็มและแข่งขันที่นั่งสุดท้าย (AC-REG-05)

### T-07 ตรวจความจุและใช้ transaction ป้องกัน race condition
- รองรับ: FR-REG-04, ASM-03
- ตรวจด้วย: AC-REG-05
- ไฟล์ที่แตะ: `backend/app/auth/register.py`, `backend/tests/test_auth_registration.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03, T-06
- เสร็จเมื่อ: `test_AC_REG_05_reject_full_event_and_race_for_last_seat` ผ่าน โดยเมื่อมีผู้ลงทะเบียนเต็มแล้วหรือมีผู้ใช้หลายคนยืนยันที่นั่งสุดท้ายพร้อมกัน ระบบให้สำเร็จเพียงคนเดียวและปฏิเสธคนอื่น
- สถานะ: เสร็จ 

### T-08 แสดงผลปฏิเสธเมื่อที่นั่งเต็มและมีคนยืนยันก่อน
- รองรับ: FR-REG-04
- ตรวจด้วย: AC-REG-05
- ไฟล์ที่แตะ: `frontend/src/pages/RegisterPage.jsx`, `frontend/src/__tests__/RegisterPage.test.jsx`
- แบบหน้าจอ: UI-REG-02 `mockups/UI-REG-02-result.html`
- ต้องทำหลัง: T-07
- เสร็จเมื่อ: ผู้ใช้เห็นข้อความว่าที่นั่งเต็มเมื่อระบบปฏิเสธและสามารถเห็นผลการลงทะเบียนไม่สำเร็จจาก UI ตาม mockup ที่กำหนด
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 3
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–2 และ `test_AC_REG_05_reject_full_event_and_race_for_last_seat`, `test_AC_REG_05_full_event_ui_message`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-REG-05:
  Given จำนวนผู้ลงทะเบียนของอีเว้นต์เต็มแล้ว
  When ผู้ใช้พยายามลงทะเบียนหรือหลายคนยืนยันที่นั่งสุดท้ายพร้อมกัน
  Then ระบบไม่อนุญาตให้ลงทะเบียน ไม่เกิดรายการเกินจำนวนที่นั่ง และแจ้งว่าที่นั่งเต็ม
- ยังขาด: Q-04 ข้อมูลที่ต้องแสดงในผลการลงทะเบียนสำเร็จ

## เฟส 4 รอคำตอบ

### T-09 กำหนดเกณฑ์ที่นั่งเหลือน้อยและผลลัพธ์แสดงข้อความ
- รองรับ: FR-REG-03, AC-REG-03, Q-01, Q-04
- ตรวจด้วย: AC-REG-03
- ไฟล์ที่แตะ: `backend/app/config.py`, `frontend/src/config.js`, `frontend/src/pages/RegisterPage.jsx`
- แบบหน้าจอ: UI-REG-01 `mockups/UI-REG-01-register.html`; UI-REG-02 `mockups/UI-REG-02-result.html`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: ทีมกำหนดค่า [N] หรือ [P]% ให้ชัดเจนและซิงก์กับข้อความแจ้งจำนวนที่เหลือและผลลัพธ์ที่แสดงต่อผู้ใช้
- สถานะ: เสร็จ 

### T-10 กำหนดนโยบายความปลอดภัยและคำเรียกผู้ใช้
- รองรับ: NFR-SEC-01, Q-02, Q-03, Q-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานรองรับความปลอดภัยและสิทธิ์เข้าถึงข้อมูลผู้ลงทะเบียน
- ไฟล์ที่แตะ: `backend/app/auth/permissions.py`, `backend/app/auth/session.py`, `backend/app/models/auth.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03, T-07
- เสร็จเมื่อ: กำหนดฟิลด์ `user_id`, `event_id` และ `confirmation_snapshot`; จำกัดการเข้าถึงตาม NFR-SEC-01/ASM-04; และใช้คำเรียก "ผู้เข้าชม" สำหรับนักศึกษาและผู้ชมที่มีสิทธิ์ลงทะเบียนเหมือนกัน
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 4
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–3 และ test สำหรับ T-10
- เปิดระบบ: รายละเอียดข้อมูลที่แสดงในผลสำเร็จยังรอคำตอบ Q-04; คำถามนี้ไม่บล็อก T-10
- คนลองเองตามข้อสรุป Q-02, Q-03 และ Q-05:
  Given ผู้ใช้เป็นนักศึกษาหรือผู้ชม และมีข้อมูลยืนยันการลงทะเบียน
  When ตรวจสิทธิ์การเข้าถึงข้อมูลผู้ลงทะเบียน
  Then ผู้ใช้เข้าถึงได้เฉพาะรายการของตนเอง ขณะที่ผู้จัดงานเข้าถึงได้ และทั้งสองกลุ่มมีสิทธิ์ลงทะเบียนเข้าชมเหมือนกัน
- ยังขาด: Q-04

### ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-REG-01 | T-03, T-04 |
| AC-REG-02 | T-03, T-04 |
| AC-REG-03 | T-05, T-09 |
| AC-REG-04 | T-06 |
| AC-REG-05 | T-07, T-08 |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| PRE-REG-01 | T-01, T-02, T-03, T-04 |

| FR ID | AC ที่ตรวจ FR นี้ | เฟส |
|---|---|---|
| FR-REG-01 | AC-REG-03 | เฟส 2 |
| FR-REG-02 | AC-REG-01, AC-REG-02 | เฟส 1 |
| FR-REG-03 | AC-REG-03 | เฟส 2 |
| FR-REG-04 | AC-REG-05 | เฟส 3 |
| FR-REG-05 | AC-REG-04 | เฟส 2 |

### สิ่งที่ยังไม่ทำ

- Q-04: ยังไม่ระบุข้อมูลที่ต้องแสดงในผลการลงทะเบียนสำเร็จ
