# RTM: ลงทะเบียนเข้าชมงาน
อ้างอิง: spec.md Status | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-11-13 18:30 | test: 21 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| PRE-REG-01 | - | T-01, T-02, T-03, T-04 | backend/app/auth/register.py: register_for_event, backend/app/auth/repository.py: AuthRepository.register_for_event | backend/tests/test_auth_registration.py: ผ่าน (AC-REG-01 ถึง AC-REG-05) | ครบ |
| FR-REG-01 | AC-REG-03 | T-05, T-09 | backend/app/auth/register.py: get_event_availability | test_AC_REG_03_show_remaining_seats_when_below_threshold: ผ่าน | ครบ |
| FR-REG-02 | AC-REG-01, AC-REG-02 | T-03, T-04 | backend/app/auth/register.py: register_for_event, frontend/src/pages/RegisterPage.jsx: EventRegistrationView.handleConfirmRegistration | test_AC_REG_01_register_available_event, test_AC_REG_02_store_confirmed_registration_data: ผ่าน | ครบ |
| FR-REG-03 | AC-REG-03 | T-05, T-09 | backend/app/auth/register.py: get_event_availability, frontend/src/config.js: registrationUiConfig | test_AC_REG_03_show_remaining_seats_when_below_threshold: ผ่าน | ครบ |
| FR-REG-04 | AC-REG-05 | T-07, T-08 | backend/app/auth/repository.py: AuthRepository.register_for_event, frontend/src/pages/RegisterPage.jsx: EventRegistrationView.handleConfirmRegistration | test_AC_REG_05_reject_full_event_and_race_for_last_seat: ผ่าน; frontend RegisterPage.test.jsx: ผ่าน | ครบ |
| FR-REG-05 | AC-REG-04 | T-06 | backend/app/auth/repository.py: AuthRepository.register_for_event, frontend/src/pages/RegisterPage.jsx: EventRegistrationView.handleConfirmRegistration | test_AC_REG_04_reject_duplicate_registration: ผ่าน | ครบ |
| NFR-DAT-01 | AC-REG-02 | T-03, T-10 | backend/app/auth/repository.py: AuthRepository.register_for_event | test_AC_REG_02_store_confirmed_registration_data: ผ่าน | ครบ |
| NFR-SEC-01 | - | T-10 | backend/app/models/auth.py, backend/app/auth/repository.py | ไม่พบ test เฉพาะสำหรับสิทธิ์เพิ่มเติม; ข้อสรุปตาม spec Q-03/Q-05 ว่าไม่มีมาตรการเพิ่มที่จำเป็น | ครบ |
| AC-REG-01 | - | T-03, T-04 | backend/app/auth/register.py, frontend/src/pages/RegisterPage.jsx | test_AC_REG_01_register_available_event; frontend RegisterPage.test.jsx: ผ่าน | ครบ |
| AC-REG-02 | - | T-03, T-04 | backend/app/auth/repository.py: AuthRepository.register_for_event | test_AC_REG_02_store_confirmed_registration_data: ผ่าน | ครบ |
| AC-REG-03 | - | T-05, T-09 | backend/app/auth/register.py: get_event_availability, frontend/src/config.js | test_AC_REG_03_show_remaining_seats_when_below_threshold: ผ่าน | ครบ |
| AC-REG-04 | - | T-06 | backend/app/auth/repository.py: AuthRepository.register_for_event, frontend/src/pages/RegisterPage.jsx | test_AC_REG_04_reject_duplicate_registration: ผ่าน | ครบ |
| AC-REG-05 | - | T-07, T-08 | backend/app/auth/repository.py: AuthRepository.register_for_event, frontend/src/pages/RegisterPage.jsx | test_AC_REG_05_reject_full_event_and_race_for_last_seat: ผ่าน; frontend RegisterPage.test.jsx: ผ่าน | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/auth/repository.py: AuthRepository.register_for_event | FR-REG-02, FR-REG-04, FR-REG-05, NFR-DAT-01 | ใช่ | บันทึก `user_id`, `event_id`, และ `confirmation_snapshot` พร้อมตรวจซ้ำและความจุด้วย lock |
| backend/app/auth/register.py: get_event_availability | FR-REG-01, FR-REG-03, AC-REG-03 | ใช่ | คำนวณ `remaining_seats` และ `low_seat_warning` จากค่าที่กำหนดใน config, ตรงกับ Q-01 |
| frontend/src/pages/RegisterPage.jsx: EventRegistrationView.handleConfirmRegistration | FR-REG-02, FR-REG-04, FR-REG-05 | ใช่ | แสดงผลสมัครสำเร็จ/ไม่สำเร็จและปฏิเสธซ้ำ/เต็มตาม AC ได้ดี แต่รายละเอียดในผลสำเร็จยังรอ Q-04 |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-REG-01 | เดา Q-xx | spec.md / Q-04, frontend/src/pages/RegisterPage.jsx | ผลการลงทะเบียนสำเร็จต้องแสดงข้อมูลใดบ้าง | โค้ดเลือกแสดง event, date, ticket type, user name, registrationId และ status อย่างสมเหตุสมผล แต่ spec ยังไม่ได้กำหนดว่าต้องแสดง field ใดบ้าง จึงยังไม่สามารถถือว่า “ครบ” อย่างเป็นทางการ | เพิ่ม Q-xx |
| F-REG-02 | ไม่ใช่ปัญหา (suite-level) | frontend/src/__tests__/setup.test.jsx | การรันฝั่ง frontend ทั้งชุด | test เริ่มต้นคาดหวังข้อความ `ระบบจองคิวตรวจสุขภาพ` ในหน้าแอปหลัก แต่แอปจริงแสดงหน้า “ลงทะเบียนเข้าชมงาน” ทำให้ frontend suite ทั้งชุดมี 1 failed แม้ไม่ใช่ bug ของฟีเจอร์ registration | ไม่ใช่ปัญหา |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
