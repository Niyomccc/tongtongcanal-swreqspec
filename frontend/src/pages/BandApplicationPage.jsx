import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

const EMPTY_SONG = { song_name: '', song_type: '', original_artist: '' }

// รองรับ FR-APP-02, FR-APP-03 และ FR-APP-05: แสดงข้อมูลวงและแจ้งผลตรวจข้อมูลก่อนส่งใบสมัคร
export default function BandApplicationPage({
  selectedEvent,
  sessionId,
  apiClient = api,
  onBack = () => {},
} = {}) {
  const [bandProfile, setBandProfile] = useState(null)
  const [isBandProfileComplete, setIsBandProfileComplete] = useState(false)
  const [songs, setSongs] = useState([{ ...EMPTY_SONG }])
  const [performance, setPerformance] = useState({
    total_duration_minutes: '',
    equipment_requirements: '',
    work_sample_link: '',
    notes: '',
  })
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [validationErrors, setValidationErrors] = useState([])
  const [validationMessage, setValidationMessage] = useState('')
  const [isValidating, setIsValidating] = useState(false)

  useEffect(() => {
    let active = true

    const loadProfile = async () => {
      setIsLoading(true)
      setError('')
      setValidationErrors([])
      setValidationMessage('')
      if (!sessionId) {
        setBandProfile(null)
        setIsBandProfileComplete(false)
        setError('กรุณาเข้าสู่ระบบก่อนใช้งาน')
        setIsLoading(false)
        return
      }

      try {
        const response = await apiClient.getBandApplicationProfile({ sessionId })
        if (!active) {
          return
        }
        if (!response?.success) {
          throw new Error(response?.message || 'โหลดข้อมูลวงไม่สำเร็จ')
        }
        if (!response.band_profile || typeof response.band_profile !== 'object') {
          throw new Error('รูปแบบข้อมูลวงไม่ถูกต้อง')
        }

        setBandProfile(response.band_profile)
        setIsBandProfileComplete(response.is_complete !== false)
        setError('')
      } catch (loadError) {
        if (active) {
          setBandProfile(null)
          setIsBandProfileComplete(false)
          setError(loadError.message || 'โหลดข้อมูลวงไม่สำเร็จ')
        }
      } finally {
        if (active) {
          setIsLoading(false)
        }
      }
    }

    loadProfile()
    return () => {
      active = false
    }
  }, [apiClient, sessionId])

  // รองรับ FR-APP-03 และ FR-APP-05: ล้างข้อความ validation เมื่อข้อมูลเพลงเปลี่ยน
  const updateSong = (index, field, value) => {
    setValidationErrors([])
    setValidationMessage('')
    setSongs((current) =>
      current.map((song, songIndex) => (songIndex === index ? { ...song, [field]: value } : song)),
    )
  }

  // รองรับ FR-APP-02: อัปเดตข้อมูลการแสดงที่วงกรอกได้
  const updatePerformance = (field, value) => {
    setValidationErrors([])
    setValidationMessage('')
    setPerformance((current) => ({ ...current, [field]: value }))
  }

  // รองรับ FR-APP-02: เพิ่มรายการเพลงใหม่ในข้อมูลการแสดง
  const addSong = () => {
    setValidationErrors([])
    setValidationMessage('')
    setSongs((current) => [...current, { ...EMPTY_SONG }])
  }

  // รองรับ FR-APP-03 และ FR-APP-05: เรียก validation โดยไม่บันทึกใบสมัคร
  const validateApplication = async () => {
    setValidationErrors([])
    setValidationMessage('')
    setIsValidating(true)
    try {
      const response = await apiClient.validateBandApplication({
        sessionId,
        payload: {
          event_id: selectedEvent?.event_id,
          songs,
          total_duration_minutes: performance.total_duration_minutes,
        },
      })
      if (!response?.success) {
        setValidationErrors(
          Array.isArray(response?.errors) && response.errors.length > 0
            ? response.errors
            : [response?.message || 'ข้อมูลใบสมัครไม่ถูกต้อง'],
        )
        return
      }

      setValidationMessage('ข้อมูลผ่านการตรวจสอบแล้ว แต่ยังไม่ได้บันทึกใบสมัคร')
    } catch (validationError) {
      setValidationErrors([validationError.message || 'ตรวจสอบข้อมูลใบสมัครไม่สำเร็จ'])
    } finally {
      setIsValidating(false)
    }
  }

  const eventName = selectedEvent?.metadata?.name || selectedEvent?.name || selectedEvent?.event_id || ''
  const contact = bandProfile
    ? [bandProfile.contact_name, bandProfile.contact_phone].filter(Boolean).join(' · ')
    : ''

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-800">
      <section className="mx-auto w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold">สมัครเข้าร่วมแสดง</h1>
        <dl className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
          <div className="flex justify-between gap-4">
            <dt className="text-sm text-slate-600">อีเว้นต์</dt>
            <dd className="text-right font-medium">{eventName}</dd>
          </div>
        </dl>

        {isLoading && <p className="mt-5 text-sm text-slate-600">กำลังโหลดข้อมูลวง...</p>}
        {error && (
          <p role="alert" className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </p>
        )}
        {validationErrors.length > 0 && (
          <div role="alert" className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            <strong>ข้อมูลใบสมัครไม่ถูกต้อง</strong>
            <ul className="mt-1 list-disc pl-5">
              {validationErrors.map((validationError, index) => (
                <li key={`${validationError}-${index}`}>{validationError}</li>
              ))}
            </ul>
          </div>
        )}
        {validationMessage && (
          <p role="status" className="mt-5 rounded-xl border border-green-200 bg-green-50 p-3 text-sm text-green-700">
            {validationMessage}
          </p>
        )}

        {!isLoading && !error && bandProfile && (
          <>
            {!isBandProfileComplete && (
              <p role="alert" className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
                ข้อมูลวงยังไม่ครบ กรุณาแก้ไขข้อมูลวงที่เมนูข้อมูลวงก่อนส่งใบสมัคร
              </p>
            )}
            <h2 className="mt-5 font-semibold">ข้อมูลวง (ดึงจากเมนูข้อมูลวง แก้ไขในหน้านี้ไม่ได้)</h2>
            <dl className="mt-2 space-y-2 rounded-xl border border-slate-200 p-4">
              <div className="flex justify-between gap-4">
                <dt className="text-sm text-slate-600">ชื่อวง</dt>
                <dd className="text-right">{bandProfile.band_name || 'ยังไม่ได้กรอก'}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-sm text-slate-600">แนวเพลง</dt>
                <dd className="text-right">{bandProfile.genre || 'ยังไม่ได้กรอก'}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-sm text-slate-600">สมาชิก</dt>
                <dd className="text-right">{bandProfile.members || 'ยังไม่ได้กรอก'}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-sm text-slate-600">ผู้ติดต่อ</dt>
                <dd className="text-right">{contact || 'ยังไม่ได้กรอก'}</dd>
              </div>
            </dl>

            <section className="mt-6">
              <h2 className="font-semibold">รายชื่อเพลง (อย่างน้อย 1 เพลง) <span aria-hidden="true">*</span></h2>
              <div className="mt-3 space-y-4">
                {songs.map((song, index) => (
                  <fieldset key={index} className="rounded-xl border border-slate-200 p-4">
                    <legend className="px-1 text-sm font-medium">เพลง {index + 1}</legend>
                    <label className="mt-2 block text-sm font-medium" htmlFor={`song-name-${index}`}>
                      ชื่อเพลง *
                    </label>
                    <input
                      id={`song-name-${index}`}
                      value={song.song_name}
                      onChange={(event) => updateSong(index, 'song_name', event.target.value)}
                      className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2"
                    />

                    <label className="mt-3 block text-sm font-medium" htmlFor={`song-type-${index}`}>
                      ประเภทเพลง *
                    </label>
                    <select
                      id={`song-type-${index}`}
                      value={song.song_type}
                      onChange={(event) => updateSong(index, 'song_type', event.target.value)}
                      className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2"
                    >
                      <option value="">เลือกประเภทเพลง</option>
                      <option value="ต้นฉบับ">ต้นฉบับ</option>
                      <option value="คัฟเวอร์">คัฟเวอร์</option>
                    </select>

                    {song.song_type === 'คัฟเวอร์' && (
                      <>
                        <label className="mt-3 block text-sm font-medium" htmlFor={`song-artist-${index}`}>
                          ศิลปินเดิม *
                        </label>
                        <input
                          id={`song-artist-${index}`}
                          value={song.original_artist}
                          onChange={(event) => updateSong(index, 'original_artist', event.target.value)}
                          className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2"
                        />
                      </>
                    )}
                  </fieldset>
                ))}
              </div>
              <button
                type="button"
                onClick={addSong}
                className="mt-3 rounded-lg border border-teal-700 px-3 py-2 text-sm font-semibold text-teal-700"
              >
                + เพิ่มเพลง
              </button>
            </section>

            <section className="mt-6 space-y-3">
              <label className="block text-sm font-medium" htmlFor="total-duration">
                ความยาวการแสดงรวม *
              </label>
              <div className="flex items-center gap-2">
                <input
                  id="total-duration"
                  type="number"
                  value={performance.total_duration_minutes}
                  onChange={(event) => updatePerformance('total_duration_minutes', event.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2"
                />
                <span className="text-sm text-slate-600">นาที</span>
              </div>

              <label className="block text-sm font-medium" htmlFor="equipment-requirements">
                ความต้องการอุปกรณ์ / เวที (ไม่บังคับ)
              </label>
              <textarea
                id="equipment-requirements"
                value={performance.equipment_requirements}
                onChange={(event) => updatePerformance('equipment_requirements', event.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2"
                rows="2"
              />

              <label className="block text-sm font-medium" htmlFor="work-sample-link">
                ลิงก์ตัวอย่างผลงาน (ไม่บังคับ)
              </label>
              <input
                id="work-sample-link"
                value={performance.work_sample_link}
                onChange={(event) => updatePerformance('work_sample_link', event.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2"
              />

              <label className="block text-sm font-medium" htmlFor="application-notes">
                หมายเหตุ (ไม่บังคับ)
              </label>
              <textarea
                id="application-notes"
                value={performance.notes}
                onChange={(event) => updatePerformance('notes', event.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2"
                rows="2"
              />
            </section>
          </>
        )}

        <button
          type="button"
          onClick={validateApplication}
          disabled={
            isLoading ||
            isValidating ||
            validationErrors.length > 0 ||
            !sessionId ||
            !selectedEvent?.event_id ||
            !isBandProfileComplete
          }
          className="mt-6 w-full rounded-xl bg-teal-700 px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-600"
        >
          {isValidating ? 'กำลังตรวจสอบ...' : 'ส่งใบสมัคร'}
        </button>
        <button
          type="button"
          onClick={onBack}
          className="mt-6 w-full rounded-xl border border-teal-700 bg-white px-4 py-3 font-semibold text-teal-700"
        >
          กลับ
        </button>
      </section>
    </main>
  )
}
