// จุดเดียวที่หน้าจอใช้เรียก API หลังบ้าน (ตามสัญญา API ใน plan.md ข้อ 4)
// ตอน test ให้ส่ง client จำลองเข้าไปในหน้าจอแทน ไม่ต้องรันหลังบ้านจริง
// เรียกผ่าน /api (ดู proxy ใน vite.config.js) หลังบ้านต้องรันอยู่ที่ port 8000
const BASE = import.meta.env.VITE_API_BASE ?? '/api'

async function requestJson(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })

  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body?.detail || body?.message || 'การเชื่อมต่อกับเซิร์ฟเวอร์ไม่สำเร็จ')
  }

  return res.json()
}

export const api = {
  async login({ email, password }) {
    return requestJson(`${BASE}/auth/login`, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
  },

  async register(payload) {
    return requestJson(`${BASE}/auth/register`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async registerEvent({ user_id, userId, event_id, eventId, confirmation_snapshot, confirmationSnapshot }) {
    return requestJson(`${BASE}/registration/register`, {
      method: 'POST',
      body: JSON.stringify({
        user_id: user_id ?? userId,
        event_id: event_id ?? eventId,
        confirmation_snapshot: confirmation_snapshot ?? confirmationSnapshot ?? {},
      }),
    })
  },

  async getSlots({ dateFrom, packageCode }) {
    const q = new URLSearchParams({ date_from: dateFrom, package_code: packageCode })
    const res = await fetch(`${BASE}/slots?${q}`)
    return res.json()
  },

  async getEventList() {
    return requestJson(`${BASE}/events`)
  },

  async getEventById(eventId) {
    return requestJson(`${BASE}/events/${encodeURIComponent(eventId)}`)
  },

  async getMyRegistrations({ user_id }) {
    const q = new URLSearchParams({ user_id: String(user_id) })
    const res = await fetch(`${BASE}/cancel-registration/me?${q}`)
    if (!res.ok) {
      return { success: false, registrations: [] }
    }

    return res.json()
  },

  async cancelRegistration({ user_id, registration_id }) {
    return requestJson(`${BASE}/cancel-registration/cancel`, {
      method: 'POST',
      body: JSON.stringify({ user_id, registration_id }),
    })
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
