import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-SCV-01, FR-SCV-02, FR-SCV-03, FR-SCV-04, NFR-DAT-01: ให้เลือกอีเว้นต์และแสดงตารางที่เผยแพร่แล้ว ตามลำดับ วัน เวลา และสถานที่ที่ถูกต้อง
export default function ScheduleViewPage({ eventId = 'EVT-001', onBack = () => {} } = {}) {
  const [schedule, setSchedule] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadSchedule() {
      try {
        const data = await api.getScheduleByEventId(eventId)
        if (isMounted) {
          setSchedule(data)
        }
      } catch (loadError) {
        if (isMounted) {
          setError(loadError?.message || 'แสดงตารางไม่ได้')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadSchedule()

    return () => {
      isMounted = false
    }
  }, [eventId])

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">ตารางการแสดง</h1>
          <p className="mt-3 text-slate-600">กำลังโหลดข้อมูลตาราง…</p>
        </section>
      </main>
    )
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-3xl rounded-2xl border border-red-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">ตารางการแสดง</h1>
          <p className="mt-3 text-red-600">{error}</p>
          <button
            type="button"
            onClick={onBack}
            className="mt-5 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 font-medium text-slate-700 hover:border-slate-300"
          >
            กลับ
          </button>
        </section>
      </main>
    )
  }

  if (!schedule || schedule.status !== 'published') {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800">ตารางการแสดง</h1>
          <p className="mt-3 text-slate-600">ยังไม่มีตารางการแสดง</p>
        </section>
      </main>
    )
  }

  const entries = [...(schedule.entries || [])]
    .sort((a, b) => Number(a.show_order) - Number(b.show_order))
    .map((entry) => ({
      ...entry,
      band_name: entry.band_name || '—',
      show_date: entry.show_date || '—',
      start_time: entry.start_time || '—',
      end_time: entry.end_time || '—',
      venue: entry.venue || '—',
    }))

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <button
          type="button"
          onClick={onBack}
          className="mb-4 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300"
        >
          กลับ
        </button>

        <h1 className="text-3xl font-bold text-slate-800">ตารางการแสดง</h1>

        <div className="mt-5 overflow-hidden rounded-2xl border border-slate-200">
          <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700">ลำดับ</th>
                <th className="px-4 py-3 font-semibold text-slate-700">วง</th>
                <th className="px-4 py-3 font-semibold text-slate-700">วัน</th>
                <th className="px-4 py-3 font-semibold text-slate-700">เวลา</th>
                <th className="px-4 py-3 font-semibold text-slate-700">สถานที่</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white">
              {entries.map((entry) => (
                <tr key={`${schedule.event_id}-${entry.show_order}`}>
                  <td className="px-4 py-3 text-slate-700">{entry.show_order}</td>
                  <td className="px-4 py-3 font-medium text-slate-800">{entry.band_name}</td>
                  <td className="px-4 py-3 text-slate-700">{entry.show_date}</td>
                  <td className="px-4 py-3 text-slate-700">{entry.start_time} - {entry.end_time}</td>
                  <td className="px-4 py-3 text-slate-700">{entry.venue}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  )
}
