# RTM: ยกเลิกการลงทะเบียน
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-11-13 19:07 | test: 44 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| PRE-CXL-01 | - | T-01, T-03, T-04, T-05, T-07 | backend/app/auth/repository.py: list_registrations_for_user, cancel_registration_for_user; backend/app/auth/routes.py: my_registrations_endpoint | backend/tests/test_auth_cancel_registration.py: test_AC_CXL_02_change_registration_status_to_cancelled, test_AC_CXL_03_update_event_registration_count, test_AC_CXL_05_reject_cancellation_when_registration_not_found | ครบ |
| FR-CXL-01 | AC-CXL-01, AC-CXL-04 | T-03, T-04 | backend/app/auth/cancel.py: get_active_registrations_for_user; backend/app/auth/routes.py: my_registrations_endpoint; frontend/src/pages/CancelRegistrationPage.jsx | frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_01_cancel_registration_after_confirmation, test_AC_CXL_04_keep_registration_when_not_confirmed | ครบ |
| FR-CXL-02 | AC-CXL-01 | T-04 | frontend/src/pages/CancelRegistrationPage.jsx: selectedRegistration modal | frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_01_cancel_registration_after_confirmation | ครบ |
| FR-CXL-03 | AC-CXL-01, AC-CXL-02, AC-CXL-03 | T-05, T-06 | backend/app/auth/repository.py: cancel_registration_for_user; backend/app/auth/routes.py: cancel_registration_endpoint; frontend/src/pages/CancelRegistrationPage.jsx: handleCancel | backend/tests/test_auth_cancel_registration.py: test_AC_CXL_02_change_registration_status_to_cancelled, test_AC_CXL_03_update_event_registration_count; frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_01_cancel_registration_after_confirmation | ครบ |
| FR-CXL-04 | AC-CXL-04 | T-03, T-04 | frontend/src/pages/CancelRegistrationPage.jsx: handleKeep | frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_04_keep_registration_when_not_confirmed | ครบ |
| FR-CXL-05 | AC-CXL-05 | T-07 | backend/app/auth/routes.py: my_registrations_endpoint, cancel_registration_endpoint; backend/app/auth/repository.py: cancel_registration_for_user | backend/tests/test_auth_cancel_registration.py: test_AC_CXL_05_reject_cancellation_when_registration_not_found; frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_05_reject_cancellation_when_registration_not_found | ครบ |
| NFR-DAT-01 | AC-CXL-02 | T-05, T-10 | backend/app/models/auth.py: Registration.cancelled_at; backend/app/auth/repository.py: cancel_registration_for_user; backend/tests/test_auth_cancel_registration.py: test_T_10_tracks_cancelled_audit_metadata_and_current_count | backend/tests/test_auth_cancel_registration.py: test_T_10_tracks_cancelled_audit_metadata_and_current_count, test_AC_CXL_02_change_registration_status_to_cancelled | ครบ |
| AC-CXL-01 | - | T-03, T-04 | backend/app/auth/routes.py: cancel_registration_endpoint; frontend/src/pages/CancelRegistrationPage.jsx | frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_01_cancel_registration_after_confirmation | ครบ |
| AC-CXL-02 | - | T-05, T-06 | backend/app/auth/repository.py: cancel_registration_for_user; backend/app/models/auth.py: Registration.status | backend/tests/test_auth_cancel_registration.py: test_AC_CXL_02_change_registration_status_to_cancelled | ครบ |
| AC-CXL-03 | - | T-05, T-06 | backend/app/auth/repository.py: cancel_registration_for_user | backend/tests/test_auth_cancel_registration.py: test_AC_CXL_03_update_event_registration_count | ครบ |
| AC-CXL-04 | - | T-03, T-04 | frontend/src/pages/CancelRegistrationPage.jsx: handleKeep | frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_04_keep_registration_when_not_confirmed | ครบ |
| AC-CXL-05 | - | T-07 | backend/app/auth/routes.py: cancel_registration_endpoint; frontend/src/pages/CancelRegistrationPage.jsx | backend/tests/test_auth_cancel_registration.py: test_AC_CXL_05_reject_cancellation_when_registration_not_found; frontend/src/__tests__/CancelRegistrationPage.test.jsx: test_AC_CXL_05_reject_cancellation_when_registration_not_found | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/auth/routes.py: my_registrations_endpoint | FR-CXL-01, FR-CXL-05 | ใช่ | คืนรายการการลงทะเบียนของผู้ใช้ที่ยังไม่ยกเลิก และเมื่อไม่มีรายการให้ตอบว่า “ไม่พบข้อมูลการลงทะเบียน” |
| backend/app/auth/routes.py: cancel_registration_endpoint | FR-CXL-03, FR-CXL-05 | ใช่ | ตรวจ session/owner ก่อนยกเลิก ตาม Q-04 ที่ทีมเลือกแล้ว; ถ้าไม่พบหรือไม่ใช่เจ้าของ ให้ตอบ “ไม่พบข้อมูล” / “คุณไม่มีสิทธิ์” |
| backend/app/auth/repository.py: cancel_registration_for_user | FR-CXL-03, NFR-DAT-01 | ใช่ | เปลี่ยนสมบัติ `status` เป็น “ยกเลิก”, อัปเดต `registered_count`, และบันทึก `cancelled_at` พร้อมค่า `user_id` / `event_id` |
| frontend/src/pages/CancelRegistrationPage.jsx: handleCancel / handleKeep | FR-CXL-02, FR-CXL-04 | ใช่ | มี modal ขอให้ยืนยันและเมื่อไม่ยืนยันจะคงข้อมูลเดิมไว้ |
| frontend/src/pages/CancelRegistrationPage.jsx: แสดงผู้ลงทะเบียนปัจจุบัน | Q-06, Q-07 | ไม่ใช่ spec ตรง ๆ | โค้ดแสดง “ผู้ลงทะเบียนปัจจุบัน: X คน” และ “สถานะเปลี่ยนเป็น 'ยกเลิก'” แต่ spec ยังเปิด Q-06/Q-07 จึงไม่ได้มี AC หรือ FR ที่ระบุข้อความหรือฟิลด์เหล่านี้อย่างชัดเจน |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-CXL-01 | เดา Q-xx | spec.md: Q-04-Q-08; backend/app/auth/repository.py: cancel_registration_for_user; frontend/src/pages/CancelRegistrationPage.jsx | คำตอบของ Q-04 ถึง Q-08 ยังไม่ได้ถูกใส่ใน spec.md ที่ใช้เป็น source of truth | โค้ดเคย implement หลักเกณฑ์ตรวจเจ้าของรายการ, atomic update, count display, audit metadata, และข้อความ “ไม่พบข้อมูล” อย่างชัดเจน แต่ spec.md ยังคงมี Q-04–Q-08 เปิดและไม่มี FR/AC ที่อ้างถึงพฤติกรรมเหล่านี้โดยตรง จึงเป็นการตัดสินใจนอก source of truth | เพิ่ม Q-xx |
| F-CXL-02 | ของแถม | backend/app/models/auth.py: Registration; frontend/src/pages/CancelRegistrationPage.jsx | FR-CXL-03, NFR-DAT-01 ที่แท้จริงยังไม่ได้ระบุฟิลด์ชัดเจน | โค้ดเพิ่ม `user_id`, `event_id`, `cancelled_at` และเรียกแสดงจำนวนผู้ลงทะเบียนปัจจุบันในหน้า UI ตามความเห็นของทีม แต่ไม่มี AC หรือ FR ที่กล่าวชัดว่าต้องมี field หรือข้อความนี้ใน spec หลัก | เพิ่ม Q-xx |
| F-CXL-03 | ไม่ใช่ปัญหา (suite-level) | frontend/src/__tests__/setup.test.jsx | ปัญหาการทดสอบหน้า App ทั่วไปที่ไม่ใช่ฟีเจอร์ cancel-registration | test `โครงหน้าจอเปิดได้` คาดหวังข้อความ `ระบบจองคิวตรวจสุขภาพ` แต่ App จริงแสดง `ระบบลงทะเบียนเข้าชมงาน` ทำให้ frontend suite มี 1 failed ท่ามกลาง test ของฟีเจอร์นี้ | ไม่ใช่ปัญหา |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
