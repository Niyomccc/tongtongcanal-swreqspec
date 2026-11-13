// จุดเดียวที่หน้าจอใช้เรียก API หลังบ้าน (ตามสัญญา API ใน plan.md ข้อ 4)
// ตอน test ให้ส่ง client จำลองเข้าไปในหน้าจอแทน ไม่ต้องรันหลังบ้านจริง
// เรียกผ่าน /api (ดู proxy ใน vite.config.js) หลังบ้านต้องรันอยู่ที่ port 8000
const BASE = import.meta.env.VITE_API_BASE ?? '/api'

export const api = {
  async register(payload) {
    const res = await fetch(`${BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      return { success: false, message: data.message || 'สมัครสมาชิกไม่สำเร็จ', status: res.status }
    }

    return { success: true, status: res.status, ...data }
  },

  async login(payload) {
    const res = await fetch(`${BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      return { success: false, message: data.message || 'เข้าสู่ระบบไม่สำเร็จ', status: res.status }
    }

    return { success: true, status: res.status, ...data }
  },

  async getCurrentUser(role = '') {
    const query = new URLSearchParams()
    if (role) query.set('role', role)

    const res = await fetch(`${BASE}/auth/me${query.toString() ? `?${query}` : ''}`)
    const data = await res.json().catch(() => ({}))

    if (!res.ok) {
      return { success: false, message: data.message || 'ไม่สามารถโหลดข้อมูลผู้ใช้ได้', status: res.status }
    }

    return { success: true, status: res.status, ...data }
  },

  async getSlots({ dateFrom, packageCode }) {
    const q = new URLSearchParams({ date_from: dateFrom, package_code: packageCode })
    const res = await fetch(`${BASE}/slots?${q}`)
    return res.json()
  },
  async createBooking({ slotId }) {
    const res = await fetch(`${BASE}/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slot_id: slotId }),
    })
    return { status: res.status, body: await res.json() }
  },
}
