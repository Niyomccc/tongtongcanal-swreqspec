import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-EVD-02 และ NFR-DAT-01: แสดงข้อมูลอีเว้นต์ที่เลือกตามข้อมูลจริงจาก backend
export default function EventDetailPage({ eventId = 'EVT-001', onBack = () => {} } = {}) {
  const [event, setEvent] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadEvent() {
      try {
        const detail = await api.getEventById(eventId)
        if (isMounted) {
          setEvent(detail)
        }
      } catch (loadError) {
        if (isMounted) {
          setError(loadError?.message || 'ไม่สามารถโหลดข้อมูลอีเว้นต์ได้')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadEvent()

    return () => {
      isMounted = false
    }
  }, [eventId])

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">รายละเอียดอีเว้นต์</h1>
          <p className="mt-3 text-slate-600">กำลังโหลดข้อมูลอีเว้นต์…</p>
        </section>
      </main>
    )
  }

  if (error || !event) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-2xl rounded-2xl border border-red-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">รายละเอียดอีเว้นต์</h1>
          <p className="mt-3 text-red-600">{error || 'ไม่สามารถโหลดข้อมูลอีเว้นต์ได้'}</p>
          <button
            type="button"
            onClick={onBack}
            className="mt-5 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 font-medium text-slate-700 hover:border-slate-300"
          >
            กลับไปหน้าอีเว้นต์
          </button>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <button
          type="button"
          onClick={onBack}
          className="mb-4 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300"
        >
          กลับไปหน้าอีเว้นต์
        </button>

        <h1 className="text-3xl font-bold text-slate-800">{event.title}</h1>

        <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <div className="grid gap-3 text-sm text-slate-700">
            <div className="flex items-center justify-between gap-4 border-b border-slate-200 pb-2">
              <span className="font-medium text-slate-600">วันที่</span>
              <span>{event.event_date}</span>
            </div>
            <div className="flex items-center justify-between gap-4 border-b border-slate-200 pb-2">
              <span className="font-medium text-slate-600">เวลา</span>
              <span>
                {event.start_time} – {event.end_time} น.
              </span>
            </div>
            <div className="flex items-center justify-between gap-4">
              <span className="font-medium text-slate-600">สถานที่</span>
              <span className="text-right">{event.location}</span>
            </div>
          </div>
        </div>

        <div className="mt-6">
          <h2 className="text-lg font-semibold text-slate-800">รายละเอียดกิจกรรม</h2>
          <p className="mt-2 leading-7 text-slate-700">{event.description}</p>
        </div>
      </section>
    </main>
  )
}
