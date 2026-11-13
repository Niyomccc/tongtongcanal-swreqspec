import { fireEvent, render, screen } from '@testing-library/react'
import { vi } from 'vitest'

import BandApplicationPage from '../pages/BandApplicationPage.jsx'

// รองรับ AC-APP-01, FR-APP-05 และ AC-APP-04: ไม่บันทึกใบสมัครเมื่อไม่มีเพลงและให้แก้ข้อมูลก่อนส่ง
test('test_TC_APP_01_5_reject_application_without_song', async () => {
  // Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร และไม่มีข้อมูลเพลง
  const validateBandApplication = vi.fn().mockResolvedValue({
    success: false,
    errors: ['ต้องระบุเพลงอย่างน้อย 1 เพลง'],
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

  // When: วงส่งใบสมัคร
  fireEvent.click(screen.getByRole('button', { name: 'ส่งใบสมัคร' }))

  // Then: ระบบให้แก้ไขข้อมูลก่อนส่ง และไม่บันทึกใบสมัคร
  expect(await screen.findByRole('alert')).toBeTruthy()
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(true)
  fireEvent.change(songName, { target: { value: 'เพลงที่กรอกเพิ่ม' } })
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(false)
  expect(createBandApplication).not.toHaveBeenCalled()
})
