import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-SCV-01: ให้ผู้ใช้เลือกอีเว้นต์ก่อนเข้าดูตารางการแสดง
export default function ScheduleListPage({ onSelectEvent = () => {} } = {}) {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadEvents() {
      try {
        const data = await api.getEventList()
        if (isMounted) {
          setEvents(Array.isArray(data) ? data : [])
        }
      } catch (loadError) {
        if (isMounted) {
          setError(loadError?.message || 'แสดงรายการอีเว้นต์ไม่ได้')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadEvents()

    return () => {
      isMounted = false
    }
  }, [])

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">ตารางการแสดง</h1>
          <p className="mt-3 text-slate-600">กำลังโหลดอีเว้นต์…</p>
        </section>
      </main>
    )
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-2xl rounded-2xl border border-red-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">ตารางการแสดง</h1>
          <p className="mt-3 text-red-600">{error}</p>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">เลือกอีเว้นต์</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-800">ตารางการแสดง</h1>
        <div className="mt-5 space-y-3">
          {events.map((event) => (
            <button
              key={event.event_id}
              type="button"
              onClick={() => onSelectEvent(event.event_id)}
              className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-left transition hover:border-teal-400 hover:bg-teal-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-800">{event.title}</p>
                  <p className="mt-1 text-sm text-slate-600">{event.event_date}</p>
                </div>
                <span className="text-xl text-slate-500">›</span>
              </div>
            </button>
          ))}
        </div>
      </section>
    </main>
  )
}
