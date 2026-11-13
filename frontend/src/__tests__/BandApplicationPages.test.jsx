import { fireEvent, render, screen } from '@testing-library/react'
import { vi } from 'vitest'

import BandApplicationPage from '../pages/BandApplicationPage.jsx'
import SelectEventPage from '../pages/SelectEventPage.jsx'

// รองรับ FR-APP-01 และ FR-APP-02: ตรวจการเลือกอีเว้นต์และแสดงข้อมูลวงแบบแก้ไขไม่ได้
test('test_T04_select_event_and_show_readonly_band_profile', async () => {
  const apiClient = {
    getOpenApplicationEvents: vi.fn().mockResolvedValue({
      success: true,
      events: [
        {
          event_id: 'event-open',
          registration_open: true,
          metadata: { name: 'งานดนตรีตัวอย่าง', venue: 'ลานกิจกรรม' },
        },
      ],
    }),
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      band_profile: {
        band_name: 'วงตัวอย่าง',
        genre: 'แจ๊ส',
        members: 'สมาชิกหนึ่งคน (กีตาร์)',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '0800000000',
      },
    }),
  }

  render(<SelectEventPage sessionId="valid-session" apiClient={apiClient} />)

  expect(await screen.findByText('งานดนตรีตัวอย่าง')).toBeTruthy()
  expect(apiClient.getOpenApplicationEvents).toHaveBeenCalledWith({ sessionId: 'valid-session' })

  fireEvent.click(screen.getByRole('button', { name: /งานดนตรีตัวอย่าง/ }))

  expect(await screen.findByText('วงตัวอย่าง')).toBeTruthy()
  expect(screen.getByText('แจ๊ส')).toBeTruthy()
  expect(screen.getByText('สมาชิกหนึ่งคน (กีตาร์)')).toBeTruthy()
  expect(screen.getByText('ผู้ติดต่อ · 0800000000')).toBeTruthy()
  expect(apiClient.getBandApplicationProfile).toHaveBeenCalledWith({ sessionId: 'valid-session' })
  expect(screen.getByLabelText('ชื่อเพลง *')).toBeTruthy()
  expect(screen.getByLabelText('ประเภทเพลง *')).toBeTruthy()
  expect(screen.getByLabelText('ความยาวการแสดงรวม *')).toBeTruthy()
})

// รองรับ FR-APP-02: ฟอร์มแสดงข้อมูลวงแบบอ่านอย่างเดียวและรับข้อมูลการแสดง
test('test_T04_shows_band_data_read_only_and_cover_artist_field', async () => {
  const apiClient = {
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      band_profile: {
        band_name: 'วงตัวอย่าง',
        genre: 'แจ๊ส',
        members: 'สมาชิกหนึ่งคน (กีตาร์)',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '0800000000',
      },
    }),
  }

  render(
    <BandApplicationPage
      selectedEvent={{ event_id: 'event-open', metadata: { name: 'งานดนตรีตัวอย่าง' } }}
      sessionId="valid-session"
      apiClient={apiClient}
    />,
  )

  expect(await screen.findByText('วงตัวอย่าง')).toBeTruthy()
  expect(screen.getByText('งานดนตรีตัวอย่าง')).toBeTruthy()
  expect(screen.queryByDisplayValue('วงตัวอย่าง')).toBeNull()
  expect(screen.queryByDisplayValue('แจ๊ส')).toBeNull()

  fireEvent.change(screen.getByLabelText('ประเภทเพลง *'), { target: { value: 'คัฟเวอร์' } })
  expect(screen.getByLabelText('ศิลปินเดิม *')).toBeTruthy()
})

// รองรับ FR-APP-03 และ FR-APP-05: แจ้งข้อมูลบังคับที่ขาดและไม่บันทึกใบสมัคร
test('test_AC_APP_04_shows_required_field_validation_errors', async () => {
  const validateBandApplication = vi.fn().mockResolvedValue({
    success: false,
    errors: ['ต้องระบุเพลงอย่างน้อย 1 เพลง', 'กรุณาระบุความยาวการแสดงรวมเป็นจำนวนนาที'],
  })
  const apiClient = {
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      is_complete: true,
      band_profile: {
        band_name: 'วงตัวอย่าง',
        genre: 'แจ๊ส',
        members: 'สมาชิกหนึ่งคน (กีตาร์)',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '0800000000',
      },
    }),
    validateBandApplication,
  }

  render(
    <BandApplicationPage
      selectedEvent={{ event_id: 'event-open', metadata: { name: 'งานดนตรีตัวอย่าง' } }}
      sessionId="valid-session"
      apiClient={apiClient}
    />,
  )

  fireEvent.click(await screen.findByRole('button', { name: 'ส่งใบสมัคร' }))

  expect(await screen.findByText('ต้องระบุเพลงอย่างน้อย 1 เพลง')).toBeTruthy()
  expect(screen.getByText('กรุณาระบุความยาวการแสดงรวมเป็นจำนวนนาที')).toBeTruthy()
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(true)
  expect(validateBandApplication).toHaveBeenCalledWith({
    sessionId: 'valid-session',
    payload: {
      event_id: 'event-open',
      songs: [{ song_name: '', song_type: '', original_artist: '' }],
      total_duration_minutes: '',
    },
  })
})

// รองรับ FR-APP-03: แสดงผลเมื่อข้อมูลเกินข้อจำกัด โดยไม่เรียก API บันทึกใบสมัคร
test('test_AC_APP_04_shows_event_limit_validation_errors', async () => {
  const validateBandApplication = vi.fn().mockResolvedValue({
    success: false,
    errors: ['จำนวนเพลงเกินข้อจำกัดของอีเว้นต์', 'ความยาวการแสดงรวมเกินข้อจำกัดของอีเว้นต์'],
  })
  const apiClient = {
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      is_complete: true,
      band_profile: {
        band_name: 'วงตัวอย่าง',
        genre: 'แจ๊ส',
        members: 'สมาชิกหนึ่งคน (กีตาร์)',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '0800000000',
      },
    }),
    validateBandApplication,
  }

  render(
    <BandApplicationPage
      selectedEvent={{ event_id: 'event-open', metadata: { name: 'งานดนตรีตัวอย่าง' } }}
      sessionId="valid-session"
      apiClient={apiClient}
    />,
  )

  fireEvent.click(await screen.findByRole('button', { name: 'ส่งใบสมัคร' }))

  expect(await screen.findByText('จำนวนเพลงเกินข้อจำกัดของอีเว้นต์')).toBeTruthy()
  expect(screen.getByText('ความยาวการแสดงรวมเกินข้อจำกัดของอีเว้นต์')).toBeTruthy()
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(true)
  expect(validateBandApplication).toHaveBeenCalledTimes(1)
})

// รองรับ FR-APP-03: ผล validation สำเร็จต้องไม่สื่อว่าใบสมัครถูกบันทึกแล้ว
test('test_AC_APP_04_reports_valid_data_without_claiming_application_was_saved', async () => {
  const validateBandApplication = vi.fn().mockResolvedValue({ success: true })
  const apiClient = {
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      is_complete: true,
      band_profile: {
        band_name: 'วงตัวอย่าง',
        genre: 'แจ๊ส',
        members: 'สมาชิกหนึ่งคน (กีตาร์)',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '0800000000',
      },
    }),
    validateBandApplication,
  }

  render(
    <BandApplicationPage
      selectedEvent={{ event_id: 'event-open', metadata: { name: 'งานดนตรีตัวอย่าง' } }}
      sessionId="valid-session"
      apiClient={apiClient}
    />,
  )

  expect(await screen.findByLabelText('ชื่อเพลง *')).toBeTruthy()
  fireEvent.change(screen.getByLabelText('ชื่อเพลง *'), { target: { value: 'เพลงตัวอย่าง' } })
  fireEvent.change(screen.getByLabelText('ประเภทเพลง *'), { target: { value: 'ต้นฉบับ' } })
  fireEvent.change(screen.getByLabelText('ความยาวการแสดงรวม *'), { target: { value: '20' } })
  fireEvent.click(await screen.findByRole('button', { name: 'ส่งใบสมัคร' }))

  expect(await screen.findByText(/ข้อมูลผ่านการตรวจสอบแล้ว/)).toBeTruthy()
  expect(screen.getByText(/ยังไม่ได้บันทึกใบสมัคร/)).toBeTruthy()
  expect(validateBandApplication).toHaveBeenCalledTimes(1)
})

// รองรับ FR-APP-05: ปิดการส่งไว้จนกว่าข้อมูลวงจาก UC-07 จะครบถ้วน
test('test_AC_APP_04_disables_application_validation_for_incomplete_band_profile', async () => {
  const validateBandApplication = vi.fn()
  const apiClient = {
    getBandApplicationProfile: vi.fn().mockResolvedValue({
      success: true,
      is_complete: false,
      missing_fields: ['genre', 'members'],
      band_profile: {
        band_name: 'วงตัวอย่าง',
        genre: '',
        members: '',
        contact_name: 'ผู้ติดต่อ',
        contact_phone: '0800000000',
      },
    }),
    validateBandApplication,
  }

  render(
    <BandApplicationPage
      selectedEvent={{ event_id: 'event-open', metadata: { name: 'งานดนตรีตัวอย่าง' } }}
      sessionId="valid-session"
      apiClient={apiClient}
    />,
  )

  expect(await screen.findByText(/ข้อมูลวงยังไม่ครบ/)).toBeTruthy()
  expect(screen.getByRole('button', { name: 'ส่งใบสมัคร' }).disabled).toBe(true)
  expect(screen.queryByRole('button', { name: /ไปที่ข้อมูลวง/ })).toBeNull()
  expect(validateBandApplication).not.toHaveBeenCalled()
})
