import { render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { api } from '../api/client.js'
import ScheduleViewPage from '../pages/ScheduleViewPage.jsx'

const publishedSchedule = {
  event_id: 'EVT-001',
  schedule_id: 'SCH-001',
  status: 'published',
  entries: [
    {
      band_name: 'The Echoes',
      show_order: 1,
      show_date: '2026-11-20',
      start_time: '17:00',
      end_time: '17:45',
      venue: 'เวทีหลัก',
    },
    {
      band_name: 'Neon Valley',
      show_order: 2,
      show_date: '2026-11-20',
      start_time: '18:15',
      end_time: '19:00',
      venue: 'เวทีหลัก',
    },
    {
      band_name: 'Midnight Harbor',
      show_order: 3,
      show_date: '2026-11-20',
      start_time: '19:30',
      end_time: '20:30',
      venue: 'อาคารศิลปะกลาง',
    },
  ],
}

afterEach(() => {
  vi.restoreAllMocks()
})

describe('ScheduleViewPage', () => {
  it('test_AC_SCV_01_show_bands_in_schedule_order', async () => {
    vi.spyOn(api, 'getScheduleByEventId').mockResolvedValue(publishedSchedule)

    render(<ScheduleViewPage eventId="EVT-001" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('The Echoes')).toBeTruthy()
    })

    expect(screen.getByText('The Echoes')).toBeTruthy()
    expect(screen.getByText('Neon Valley')).toBeTruthy()
    expect(screen.getByText('Midnight Harbor')).toBeTruthy()
    expect(screen.getAllByRole('row').length).toBeGreaterThan(3)
  })

  it('test_AC_SCV_02_show_date_time_and_venue', async () => {
    vi.spyOn(api, 'getScheduleByEventId').mockResolvedValue(publishedSchedule)

    render(<ScheduleViewPage eventId="EVT-001" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getAllByText('2026-11-20').length).toBeGreaterThan(0)
    })

    expect(screen.getAllByText('17:00 - 17:45').length).toBeGreaterThan(0)
    expect(screen.getAllByText('เวทีหลัก').length).toBeGreaterThan(0)
    expect(screen.getByText('อาคารศิลปะกลาง')).toBeTruthy()
  })

  it('test_AC_SCV_03_schedule_matches_published_data', async () => {
    vi.spyOn(api, 'getScheduleByEventId').mockResolvedValue(publishedSchedule)

    render(<ScheduleViewPage eventId="EVT-001" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('Midnight Harbor')).toBeTruthy()
    })

    expect(screen.getByText('The Echoes')).toBeTruthy()
    expect(screen.getByText('Neon Valley')).toBeTruthy()
    expect(screen.getAllByText('17:00 - 17:45').length).toBeGreaterThan(0)
    expect(screen.getByText('19:30 - 20:30')).toBeTruthy()
    expect(screen.getAllByText('เวทีหลัก').length).toBeGreaterThan(0)
  })

  it('test_AC_SCV_04_unpublished_schedule_message', async () => {
    vi.spyOn(api, 'getScheduleByEventId').mockResolvedValue({
      event_id: 'EVT-002',
      schedule_id: 'SCH-002',
      status: 'unpublished',
      entries: [],
    })

    render(<ScheduleViewPage eventId="EVT-002" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('ยังไม่มีตารางการแสดง')).toBeTruthy()
    })

    expect(screen.queryByText('The Echoes')).toBeNull()
  })

  it('test_AC_SCV_05_schedule_load_failure_message', async () => {
    vi.spyOn(api, 'getScheduleByEventId').mockRejectedValue(new Error('แสดงตารางไม่ได้'))

    render(<ScheduleViewPage eventId="EVT-999" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('แสดงตารางไม่ได้')).toBeTruthy()
    })

    expect(screen.queryByText('The Echoes')).toBeNull()
  })
})
