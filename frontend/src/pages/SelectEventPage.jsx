import { useEffect, useState } from 'react'

import { api } from '../api/client.js'
import BandApplicationPage from './BandApplicationPage.jsx'

// รองรับ FR-APP-01: แสดงอีเว้นต์ที่เปิดรับสมัครและให้วงเลือกอีเว้นต์
export default function SelectEventPage({ sessionId, apiClient = api } = {}) {
  const [events, setEvents] = useState([])
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true

    const loadEvents = async () => {
      setIsLoading(true)
      setError('')
      if (!sessionId) {
        setEvents([])
        setError('กรุณาเข้าสู่ระบบก่อนใช้งาน')
        setIsLoading(false)
        return
      }

      try {
        const response = await apiClient.getOpenApplicationEvents({ sessionId })
        if (!active) {
          return
        }
        if (!response?.success) {
          throw new Error(response?.message || 'โหลดรายการอีเว้นต์ไม่สำเร็จ')
        }
        if (!Array.isArray(response.events)) {
          throw new Error('รูปแบบรายการอีเว้นต์ไม่ถูกต้อง')
        }

        setEvents(response.events)
        setError('')
      } catch (loadError) {
        if (active) {
          setEvents([])
          setError(loadError.message || 'โหลดรายการอีเว้นต์ไม่สำเร็จ')
        }
      } finally {
        if (active) {
          setIsLoading(false)
        }
      }
    }

    loadEvents()
    return () => {
      active = false
    }
  }, [apiClient, sessionId])

  if (selectedEvent) {
    return (
      <BandApplicationPage
        selectedEvent={selectedEvent}
        sessionId={sessionId}
        apiClient={apiClient}
        onBack={() => setSelectedEvent(null)}
      />
    )
  }

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-800">
      <section className="mx-auto w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold">สมัครเข้าร่วมแสดง</h1>
        <p className="mt-2 text-sm text-slate-600">เลือกอีเว้นต์ที่เปิดรับสมัครวง</p>

        {isLoading && <p className="mt-5 text-sm text-slate-600">กำลังโหลดรายการอีเว้นต์...</p>}
        {error && (
          <p role="alert" className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </p>
        )}
        {!isLoading && !error && events.length === 0 && (
          <p className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600">
            ไม่พบอีเว้นต์ที่เปิดรับสมัคร
          </p>
        )}

        <ul className="mt-4 space-y-3">
          {events.map((event) => {
            const name = event.metadata?.name || event.name || event.event_id
            const venue = event.metadata?.venue || event.venue

            return (
              <li key={event.event_id}>
                <button
                  type="button"
                  onClick={() => setSelectedEvent(event)}
                  className="w-full rounded-xl border border-slate-200 p-4 text-left transition hover:border-teal-600 hover:bg-teal-50"
                >
                  <span className="flex items-center justify-between gap-3">
                    <span className="font-semibold">{name}</span>
                    <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-medium text-emerald-700">
                      เปิดรับสมัคร
                    </span>
                  </span>
                  {venue && <span className="mt-1 block text-sm text-slate-600">{venue}</span>}
                </button>
              </li>
            )
          })}
        </ul>
      </section>
    </main>
  )
}
