import { fireEvent, render, screen } from '@testing-library/react'
import { vi } from 'vitest'

import BandApplicationPage from '../pages/BandApplicationPage.jsx'

// รองรับ AC-APP-01, FR-APP-05 และ AC-APP-04: ไม่บันทึกใบสมัครเมื่อเกินจำนวนเพลงสูงสุดและให้แก้ข้อมูลก่อนส่ง
test('test_TC_APP_01_7_reject_application_over_song_limit', async () => {
  // Given: วงเข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร มี 9 เพลงและความยาวรวมไม่เกินข้อจำกัด
  const validateBandApplication = vi.fn().mockResolvedValue({
    success: false,
    errors: ['จำนวนเพลงเกินข้อจำกัดของอีเว้นต์'],
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

  await screen.findByLabelText('ชื่อเพลง *')
  for (let index = 1; index < 9; index += 1) {
    fireEvent.click(screen.getByRole('button', { name: '+ เพิ่มเพลง' }))
  }

  const songNames = screen.getAllByLabelText('ชื่อเพลง *')
  const songTypes = screen.getAllByLabelText('ประเภทเพลง *')
  songNames.forEach((input, index) => {
    fireEvent.change(input, { target: { value: `เพลง ${index + 1}` } })
    fireEvent.change(songTypes[index], { target: { value: 'ต้นฉบับ' } })
  })
  fireEvent.change(screen.getByLabelText('ความยาวการแสดงรวม *'), { target: { value: '20' } })

  // When: วงส่งใบสมัคร
  fireEvent.click(screen.getByRole('button', { name: 'ส่งใบสมัคร' }))

  // Then: ระบบให้แก้ไขข้อมูลก่อนส่ง และไม่บันทึกใบสมัคร
  expect(await screen.findByRole('alert')).toBeTruthy()
  expect(validateBandApplication).toHaveBeenCalledWith(
    expect.objectContaining({ payload: expect.objectContaining({ songs: expect.any(Array) }) }),
  )
  expect(validateBandApplication.mock.calls[0][0].payload.songs).toHaveLength(9)
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(true)
  fireEvent.change(songNames[0], { target: { value: 'เพลงที่แก้ไข' } })
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(false)
  expect(createBandApplication).not.toHaveBeenCalled()
})
