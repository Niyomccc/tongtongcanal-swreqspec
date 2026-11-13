// API paths follow the Auth API contract in plan.md and support FR-AUTH-02, FR-AUTH-03, and FR-AUTH-05.
export const authApiPaths = {
  register: '/auth/register',
  login: '/auth/login',
  logout: '/auth/logout',
  me: '/auth/me',
  lockoutCheck: '/auth/lockout-check',
}

// Q-01: เกณฑ์แจ้งเตือนว่าที่นั่งเหลือน้อยกำหนดเป็นจำนวนที่นั่งที่เหลือไม่เกิน 5 ที่นั่ง
// Q-04: ผลลัพธ์สำเร็จต้องแสดงข้อความยืนยันและข้อมูลผู้ใช้/อีเว้นต์ที่สัมพันธ์กับการลงทะเบียน
export const registrationUiConfig = {
  lowSeatThreshold: 5,
  lowSeatWarningText: (remainingSeats) => `เหลือเพียง ${remainingSeats} ที่นั่ง`,
  successMessage: 'ลงทะเบียนสำเร็จแล้ว',
  successResultLabels: {
    eventName: 'ชื่ออีเว้นต์',
    dateTime: 'วันที่และเวลา',
    ticketType: 'ประเภทบัตร/บัตรเข้าชม',
    userName: 'ชื่อผู้ใช้',
    confirmationMessage: 'ข้อความยืนยันสำเร็จ',
    registrationId: 'รหัสลงทะเบียน',
    status: 'สถานะการลงทะเบียน',
  },
}
