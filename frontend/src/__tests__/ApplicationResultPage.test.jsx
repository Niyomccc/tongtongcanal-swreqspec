import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

import { api } from '../api/client.js'
import ApplicationResultPage from '../pages/ApplicationResultPage.jsx'

afterEach(() => {
  vi.unstubAllGlobals()
})

// รองรับ AC-APP-03: ส่งสำเร็จแล้วแสดงสถานะ "รอตรวจสอบ"
test('test_AC_APP_03_shows_pending_review_after_successful_submission', async () => {
  const createBandApplication = vi.fn().mockResolvedValue({
    success: true,
    status: 'รอตรวจสอบ',
    application: {
      status: 'รอตรวจสอบ',
      band_snapshot: { band_name: 'วงตัวอย่าง' },
    },
  })

  render(
    <ApplicationResultPage
      sessionId="valid-session"
      payload={{ event_id: 'event-open' }}
      selectedEvent={{ event_id: 'event-open', metadata: { name: 'งานตัวอย่าง' } }}
      apiClient={{ createBandApplication }}
    />,
  )

  expect(await screen.findByText('ส่งใบสมัครแล้ว')).toBeTruthy()
  expect(screen.getByRole('status').textContent).toBe('รอตรวจสอบ')
  expect(screen.getByText('งานตัวอย่าง')).toBeTruthy()
  expect(screen.getByText('วงตัวอย่าง')).toBeTruthy()
  expect(screen.queryByRole('button', { name: 'ดูสถานะการสมัคร' })).toBeNull()
  expect(createBandApplication).toHaveBeenCalledTimes(1)
  expect(createBandApplication).toHaveBeenCalledWith({
    sessionId: 'valid-session',
    payload: { event_id: 'event-open' },
  })
})

// รองรับ AC-APP-05: เมื่อบันทึกไม่สำเร็จให้แจ้งผู้ใช้และเสนอการกลับไปแก้ไขเมื่อมี callback
test('test_AC_APP_05_shows_failure_and_calls_retry_callback', async () => {
  const createBandApplication = vi.fn().mockRejectedValue(new Error('save failed'))
  const onRetry = vi.fn()

  render(
    <ApplicationResultPage
      sessionId="valid-session"
      payload={{ event_id: 'event-open' }}
      apiClient={{ createBandApplication }}
      onRetry={onRetry}
    />,
  )

  const alert = await screen.findByRole('alert')
  expect(alert.textContent.includes('ส่งใบสมัครไม่สำเร็จ')).toBe(true)
  expect(alert.textContent.includes('ยังไม่มีการสร้างใบสมัคร')).toBe(true)
  fireEvent.click(screen.getByRole('button', { name: 'กลับไปแก้ไขและส่งอีกครั้ง' }))
  expect(onRetry).toHaveBeenCalledTimes(1)
})

// รองรับ FR-APP-04 และ PRE-APP-01: API client แนบ session และส่งข้อมูลใบสมัคร
test('test_create_band_application_posts_payload_with_session_id', async () => {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ success: true }),
  })
  vi.stubGlobal('fetch', fetchMock)
  const payload = { event_id: 'event-open', songs: [] }

  await api.createBandApplication({ sessionId: 'valid-session', payload })

  expect(fetchMock).toHaveBeenCalledWith(
    '/api/applications?session_id=valid-session',
    expect.objectContaining({
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  )
})
