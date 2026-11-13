import { useEffect, useRef, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-APP-04 และ FR-APP-06: ส่งใบสมัครและแสดงผลสำเร็จหรือไม่สำเร็จ
export default function ApplicationResultPage({
  sessionId,
  payload,
  selectedEvent,
  apiClient = api,
  onRetry,
} = {}) {
  const requestStarted = useRef(false)
  const [result, setResult] = useState(null)
  const [hasFailed, setHasFailed] = useState(false)

  useEffect(() => {
    if (requestStarted.current) {
      return
    }
    requestStarted.current = true

    apiClient
      .createBandApplication({ sessionId, payload })
      .then((response) => {
        const status = response?.status || response?.application?.status
        if (!response?.success || status !== 'รอตรวจสอบ') {
          setHasFailed(true)
          return
        }
        setResult(response)
      })
      .catch(() => {
        setHasFailed(true)
      })
  }, [apiClient, payload, sessionId])

  const eventName =
    selectedEvent?.metadata?.name || selectedEvent?.name || selectedEvent?.event_id || payload?.event_id
  const bandName = result?.application?.band_snapshot?.band_name

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-800">
      <section
        className="mx-auto w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
        aria-busy={!result && !hasFailed}
      >
        <h1 className="text-2xl font-bold">ผลการส่งใบสมัคร</h1>

        {!result && !hasFailed && (
          <p role="status" className="mt-5 text-sm text-slate-600">
            กำลังส่งใบสมัคร...
          </p>
        )}

        {result && (
          <>
            <p className="mt-5 text-center text-xl font-bold text-green-700">ส่งใบสมัครแล้ว</p>
            <dl className="mt-5 space-y-2 rounded-xl border border-slate-200 p-4">
              {eventName && (
                <div className="flex justify-between gap-4">
                  <dt className="text-sm text-slate-600">อีเว้นต์</dt>
                  <dd className="text-right">{eventName}</dd>
                </div>
              )}
              {bandName && (
                <div className="flex justify-between gap-4">
                  <dt className="text-sm text-slate-600">วง</dt>
                  <dd className="text-right">{bandName}</dd>
                </div>
              )}
              <div className="flex justify-between gap-4">
                <dt className="text-sm text-slate-600">สถานะ</dt>
                <dd role="status" className="font-semibold text-amber-800">
                  {result.status || result.application.status}
                </dd>
              </div>
            </dl>
          </>
        )}

        {hasFailed && (
          <div
            role="alert"
            className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
          >
            <strong className="block text-base">ส่งใบสมัครไม่สำเร็จ</strong>
            ระบบบันทึกใบสมัครไม่ได้ ยังไม่มีการสร้างใบสมัคร กรุณาลองส่งอีกครั้ง
            {typeof onRetry === 'function' && (
              <button
                type="button"
                onClick={onRetry}
                className="mt-4 w-full rounded-xl bg-teal-700 px-4 py-3 font-semibold text-white"
              >
                กลับไปแก้ไขและส่งอีกครั้ง
              </button>
            )}
          </div>
        )}
      </section>
    </main>
  )
}
