import { fireEvent, render, screen } from '@testing-library/react'
import { vi } from 'vitest'

import BandApplicationPage from '../pages/BandApplicationPage.jsx'

// รองรับ AC-APP-01, FR-APP-05 และ AC-APP-04: ไม่บันทึกใบสมัครเมื่อเกินเวลาสูงสุดและให้แก้ข้อมูลก่อนส่ง
test('test_TC_APP_01_6_reject_application_over_duration_limit', async () => {
  // Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร มี 1 เพลง และความยาวรวม 31 นาที
  const validateBandApplication = vi.fn().mockResolvedValue({
    success: false,
    errors: ['ความยาวการแสดงรวมเกินข้อจำกัดของอีเว้นต์'],
  })
  const createBandApplication = vi.fn()
  const apiClient = {
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      is_complete: true,
      band_profile: {
        band_name: 'Moonlight Band',
        genre: 'Indie Pop',
        members: 'นักร้องและกีตาร์',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '089-876-5432',
      },
    }),
    validateBandApplication,
    createBandApplication,
  }

  render(
    <BandApplicationPage
      selectedEvent={{ event_id: 'event-open' }}
      sessionId="valid-session"
      apiClient={apiClient}
    />,
  )

  const songName = await screen.findByLabelText('ชื่อเพลง *')
  fireEvent.change(songName, { target: { value: 'เพลงต้นฉบับ' } })
  fireEvent.change(screen.getByLabelText('ประเภทเพลง *'), { target: { value: 'ต้นฉบับ' } })
  const duration = screen.getByLabelText('ความยาวการแสดงรวม *')
  fireEvent.change(duration, { target: { value: '31' } })

  // When: วงส่งใบสมัคร
  fireEvent.click(screen.getByRole('button', { name: 'ส่งใบสมัคร' }))

  // Then: ระบบให้แก้ไขข้อมูลก่อนส่ง และไม่บันทึกใบสมัคร
  expect(await screen.findByRole('alert')).toBeTruthy()
  expect(validateBandApplication).toHaveBeenCalledWith(
    expect.objectContaining({
      payload: expect.objectContaining({ total_duration_minutes: '31' }),
    }),
  )
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(true)
  fireEvent.change(duration, { target: { value: '20' } })
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(false)
  expect(createBandApplication).not.toHaveBeenCalled()
})
