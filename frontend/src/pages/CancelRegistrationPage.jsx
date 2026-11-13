import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-CXL-01, FR-CXL-02 และ FR-CXL-04
export function navigateTo(path) {
  window.location.href = path
}

export default function CancelRegistrationPage({
  user = { id: 42, full_name_or_band_name: 'สมชาย ใจดี', role: 'student' },
  initialRegistrations = null,
  onNavigate = navigateTo,
  apiClient = api,
} = {}) {
  const [registrations, setRegistrations] = useState(initialRegistrations ?? [])
  const [selectedRegistration, setSelectedRegistration] = useState(null)
  const [isLoading, setIsLoading] = useState(!initialRegistrations)
  const [error, setError] = useState('')
  const [isCancelled, setIsCancelled] = useState(false)

  useEffect(() => {
    if (initialRegistrations !== null) {
      return
    }

    let active = true
    const fetchRegistrations = async () => {
      try {
        setIsLoading(true)
        const response = await apiClient.getMyRegistrations({ user_id: user?.id ?? null })
        if (!active) {
          return
        }

        const items = Array.isArray(response?.registrations) ? response.registrations : []
        if (response?.success === false || items.length === 0) {
          setRegistrations([])
          setError('ไม่พบข้อมูลการลงทะเบียน')
          return
        }

        setRegistrations(items)
        setError('')
      } catch (_error) {
        if (!active) {
          return
        }

        setRegistrations([])
        setError('ไม่พบข้อมูลการลงทะเบียน')
      } finally {
        if (active) {
          setIsLoading(false)
        }
      }
    }

    fetchRegistrations()
    return () => {
      active = false
    }
  }, [apiClient, initialRegistrations, user])

  const activeRegistrations = registrations.filter(
    (registration) => (registration.status || 'ลงทะเบียน') !== 'ยกเลิก',
  )

  const handleCancel = async () => {
    if (!selectedRegistration) {
      return
    }

    try {
      const response = await apiClient.cancelRegistration({
        user_id: user?.id ?? null,
        registration_id: selectedRegistration.registration_id,
      })

      if (response?.success === false) {
        setError('ไม่พบข้อมูลการลงทะเบียน')
        setSelectedRegistration(null)
        setIsCancelled(false)
        return
      }

      setRegistrations((current) =>
        current.map((item) =>
          item.registration_id === selectedRegistration.registration_id
            ? { ...item, status: 'ยกเลิก' }
            : item,
        ),
      )
      setSelectedRegistration(null)
      setIsCancelled(true)
      setError('')
    } catch (_error) {
      setError('ไม่พบข้อมูลการลงทะเบียน')
      setSelectedRegistration(null)
      setIsCancelled(false)
    }
  }

  const handleKeep = () => {
    setSelectedRegistration(null)
    setIsCancelled(false)
  }

  if (isLoading) {
    return <main className="min-h-screen bg-slate-100 p-6 text-slate-800">กำลังโหลดข้อมูล...</main>
  }

  if (isCancelled && activeRegistrations.length === 0) {
    return (
      <main className="min-h-screen bg-slate-100 p-6 text-slate-800">
        <section className="mx-auto w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">การลงทะเบียนของฉัน</div>
          <h1 className="text-2xl font-bold text-slate-800">การลงทะเบียนของฉัน</h1>
          <div className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
            <p className="font-bold">ยกเลิกการลงทะเบียนแล้ว</p>
            <p className="mt-1">สถานะเปลี่ยนเป็น "ยกเลิก" และคืนที่นั่งให้อีเว้นต์แล้ว</p>
          </div>
          <button
            type="button"
            onClick={() => onNavigate('/dashboard')}
            className="mt-5 w-full rounded-xl border border-teal-700 bg-white px-4 py-3 font-semibold text-teal-700"
          >
            กลับ
          </button>
        </section>
      </main>
    )
  }

  if (activeRegistrations.length === 0) {
    return (
      <main className="min-h-screen bg-slate-100 p-6 text-slate-800">
        <section className="mx-auto w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">การลงทะเบียนของฉัน</div>
          <h1 className="text-2xl font-bold text-slate-800">การลงทะเบียนของฉัน</h1>
          <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
            <p className="font-bold">ไม่พบข้อมูล</p>
            <p className="mt-1">ไม่พบข้อมูลการลงทะเบียน จึงไม่มีรายการให้ยกเลิก</p>
          </div>
          <button
            type="button"
            onClick={() => onNavigate('/dashboard')}
            className="mt-5 w-full rounded-xl border border-teal-700 bg-white px-4 py-3 font-semibold text-teal-700"
          >
            กลับ
          </button>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-800">
      <section className="mx-auto w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">การลงทะเบียนของฉัน</p>
            <h1 className="mt-1 text-2xl font-bold text-slate-800">การลงทะเบียนของฉัน</h1>
          </div>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            {user?.role === 'student' ? 'นักศึกษา' : 'ผู้ชม'}
          </span>
        </div>

        <div className="mb-4 flex items-center justify-between rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
          <span>{user?.full_name_or_band_name || 'สมชาย ใจดี'}</span>
          <span>{user?.role === 'student' ? 'นักศึกษา' : 'ผู้ชม'}</span>
        </div>

        <p className="mb-4 text-sm text-slate-600">เลือกรายการที่ต้องการยกเลิก</p>

        {error && (
          <div className="mb-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
            {error}
          </div>
        )}

        {isCancelled && (
          <div className="mb-4 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
            <p className="font-bold">ยกเลิกการลงทะเบียนแล้ว</p>
            <p className="mt-1">สถานะเปลี่ยนเป็น "ยกเลิก" และคืนที่นั่งให้อีเว้นต์แล้ว</p>
          </div>
        )}

        <div className="space-y-3">
          {activeRegistrations.map((registration) => (
            <article
              key={registration.registration_id ?? registration.event_id}
              className="rounded-2xl border border-slate-200 bg-slate-50 p-4"
            >
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-semibold text-slate-800">{registration.event_name || registration.event_id}</p>
                  <p className="text-xs text-slate-500">{registration.registered_at || '10 พ.ย. 2569'}</p>
                </div>
                <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-medium text-emerald-700">
                  {registration.status || 'ลงทะเบียน'}
                </span>
              </div>

              <p className="mt-2 text-xs text-slate-500">
                ผู้ลงทะเบียนปัจจุบัน: {registration.registered_count ?? 0} คน
              </p>

              <button
                type="button"
                onClick={() => setSelectedRegistration(registration)}
                className="mt-4 w-full rounded-xl border border-red-500 bg-white px-4 py-3 font-semibold text-red-600"
              >
                ยกเลิกการลงทะเบียน
              </button>
            </article>
          ))}
        </div>
      </section>

      {selectedRegistration && (
        <div className="fixed inset-0 z-20 flex items-center justify-center bg-slate-900/50 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <h2 className="text-xl font-bold text-slate-800">ยืนยันการยกเลิกการลงทะเบียน?</h2>
            <p className="mt-3 text-sm text-slate-600">
              คุณกำลังยกเลิกการลงทะเบียน <span className="font-bold text-slate-800">{selectedRegistration.event_name || selectedRegistration.event_id}</span>
            </p>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={handleKeep}
                className="rounded-xl border border-teal-700 bg-white px-4 py-3 font-semibold text-teal-700"
              >
                ไม่ยืนยัน
              </button>
              <button
                type="button"
                onClick={handleCancel}
                className="rounded-xl bg-red-600 px-4 py-3 font-semibold text-white"
              >
                ยืนยันการยกเลิก
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
