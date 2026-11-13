import { useMemo, useState } from 'react'

import { api } from '../api/client.js'
import { registrationUiConfig } from '../config.js'

// รองรับ FR-AUTH-01, FR-AUTH-02, FR-AUTH-03 และ FR-AUTH-05
const ROLE_OPTIONS = [
  { value: 'student', label: 'นักศึกษา' },
  { value: 'audience', label: 'ผู้ชม' },
  { value: 'band', label: 'วงดนตรี' },
]

const defaultEvents = [
  {
    id: 'evt-01',
    name: 'ดนตรีในสวน ครั้งที่ 5',
    date: 'ศ 20 พ.ย. 2569 · 16.00 น.',
    location: 'ลานกิจกรรม อาคาร 5',
    remainingSeats: 120,
    capacity: 150,
  },
  {
    id: 'evt-02',
    name: 'งานแสดงดนตรีสโมสรนักศึกษา',
    date: 'อา 22 พ.ย. 2569 · 18.30 น.',
    location: 'อาคารศูนย์รวม',
    remainingSeats: 8,
    capacity: 150,
  },
  {
    id: 'evt-03',
    name: 'Night Market Music Festival',
    date: 'พ 24 พ.ย. 2569 · 19.00 น.',
    location: 'ศูนย์แสดงสินค้า',
    remainingSeats: 0,
    capacity: 90,
  },
]

const initialForm = {
  role: 'student',
  email: '',
  password: '',
  confirmPassword: '',
  fullName: '',
  studentId: '',
  universityCode: '',
  phoneNumber: '',
  bandName: '',
  contactName: '',
}

export function navigateTo(path) {
  window.location.href = path
}

function getRoleLabel(role) {
  return ROLE_OPTIONS.find((option) => option.value === role)?.label ?? 'นักศึกษา'
}

function AuthRegistrationView({ onNavigate = navigateTo } = {}) {
  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState('')

  const activeRole = form.role
  const roleSummary = useMemo(() => getRoleLabel(activeRole), [activeRole])

  const mapApiErrors = (apiErrors = {}) => {
    const fieldMap = {
      fullNameOrBandName: 'fullName',
      fullName: 'fullName',
      studentId: 'studentId',
      universityCode: 'universityCode',
      phoneNumber: 'phoneNumber',
      bandName: 'bandName',
      contactName: 'contactName',
    }

    return Object.entries(apiErrors).reduce((acc, [key, value]) => {
      const field = fieldMap[key] ?? key
      if (value) {
        acc[field] = value
      }
      return acc
    }, {})
  }

  const updateField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }))
    setErrors((current) => ({ ...current, [field]: '' }))
    setSubmitError('')
  }

  const validate = () => {
    const nextErrors = {}

    if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      nextErrors.email = 'อีเมลไม่ถูกต้อง'
    }

    if (!form.password || form.password.length < 8) {
      nextErrors.password = 'รหัสผ่านต้องยาวอย่างน้อย 8 ตัวอักษร'
    }

    if (!form.confirmPassword || form.confirmPassword !== form.password) {
      nextErrors.confirmPassword = 'ยืนยันรหัสผ่านไม่ตรงกับรหัสผ่าน'
    }

    if (!form.fullName.trim()) {
      nextErrors.fullName = 'กรุณาระบุชื่อ-สกุล หรือชื่อวง'
    }

    if (activeRole === 'student') {
      if (!form.studentId.trim()) {
        nextErrors.studentId = 'กรุณาระบุรหัสนักศึกษา'
      }
      if (!form.universityCode.trim()) {
        nextErrors.universityCode = 'กรุณาระบุรหัสมหาวิทยาลัย'
      }
    }

    if (activeRole === 'audience' && !form.phoneNumber.trim()) {
      nextErrors.phoneNumber = 'กรุณาระบุเบอร์โทรศัพท์'
    }

    if (activeRole === 'band') {
      if (!form.bandName.trim()) {
        nextErrors.bandName = 'กรุณาระบุชื่อวง'
      }
      if (!form.contactName.trim()) {
        nextErrors.contactName = 'กรุณาระบุชื่อผู้ติดต่อ'
      }
      if (!form.phoneNumber.trim()) {
        nextErrors.phoneNumber = 'กรุณาระบุเบอร์โทรศัพท์'
      }
    }

    return nextErrors
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const nextErrors = validate()
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) {
      return
    }

    setIsSubmitting(true)
    setSubmitError('')

    try {
      const payload = {
        email: form.email.trim(),
        password: form.password,
        confirmPassword: form.confirmPassword,
        role: form.role,
        fullNameOrBandName: form.fullName.trim(),
        studentId: form.studentId.trim(),
        universityCode: form.universityCode.trim(),
        phoneNumber: form.phoneNumber.trim(),
        bandName: form.bandName.trim(),
        contactName: form.contactName.trim(),
      }

      const result = await api.register(payload)
      if (!result?.success) {
        const nextFieldErrors = mapApiErrors(result?.errors || {})
        if (Object.keys(nextFieldErrors).length > 0) {
          setErrors((current) => ({ ...current, ...nextFieldErrors }))
        }

        const message = result?.message || 'สมัครสมาชิกไม่สำเร็จ กรุณาลองใหม่'
        setSubmitError(message)
        return
      }

      const redirectTo = result.redirectTo || '/dashboard'
      onNavigate(redirectTo)
    } catch (error) {
      setSubmitError(error?.message || 'สมัครสมาชิกไม่สำเร็จ กรุณาลองใหม่')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">ระบบอีเว้นต์ดนตรีนักศึกษา</p>
            <h1 className="mt-1 text-2xl font-bold text-slate-800">สมัครสมาชิก</h1>
          </div>
          <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-medium text-teal-800">{roleSummary}</span>
        </div>

        <div className="mb-5 flex gap-2 rounded-full bg-slate-100 p-1">
          <button
            type="button"
            className="flex-1 rounded-full px-3 py-2 text-sm font-medium text-slate-600"
            onClick={() => onNavigate('/auth')}
          >
            เข้าสู่ระบบ
          </button>
          <button type="button" className="flex-1 rounded-full bg-teal-700 px-3 py-2 text-sm font-semibold text-white shadow-sm">
            สมัครสมาชิก
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4" noValidate>
          <div>
            <p className="mb-2 block text-sm font-medium text-slate-700">
              สมัครในบทบาท <span className="text-red-500">*</span>
            </p>
            <div className="grid grid-cols-3 gap-2">
              {ROLE_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => updateField('role', option.value)}
                  className={`rounded-xl border px-3 py-2 text-sm font-medium transition ${
                    form.role === option.value
                      ? 'border-teal-700 bg-teal-700 text-white'
                      : 'border-slate-200 bg-slate-50 text-slate-600'
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label htmlFor="register-full-name" className="mb-1 block text-sm font-medium text-slate-700">
              ชื่อ-สกุล / ชื่อวง <span className="text-red-500">*</span>
            </label>
            <input
              id="register-full-name"
              value={form.fullName}
              onChange={(event) => updateField('fullName', event.target.value)}
              className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                errors.fullName ? 'border-red-400 bg-red-50' : 'border-slate-300'
              }`}
              placeholder={activeRole === 'band' ? 'ชื่อวง' : 'ชื่อ-สกุล'}
            />
            {errors.fullName && <p className="mt-1 text-xs text-red-600">{errors.fullName}</p>}
          </div>

          <div>
            <label htmlFor="register-email" className="mb-1 block text-sm font-medium text-slate-700">
              อีเมล <span className="text-red-500">*</span>
            </label>
            <input
              id="register-email"
              type="email"
              autoComplete="email"
              value={form.email}
              onChange={(event) => updateField('email', event.target.value)}
              className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                errors.email ? 'border-red-400 bg-red-50' : 'border-slate-300'
              }`}
              placeholder="name@example.com"
            />
            {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email}</p>}
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label htmlFor="register-password" className="mb-1 block text-sm font-medium text-slate-700">
                รหัสผ่าน <span className="text-red-500">*</span>
              </label>
              <input
                id="register-password"
                type="password"
                autoComplete="new-password"
                value={form.password}
                onChange={(event) => updateField('password', event.target.value)}
                className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                  errors.password ? 'border-red-400 bg-red-50' : 'border-slate-300'
                }`}
              />
              {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password}</p>}
            </div>

            <div>
              <label htmlFor="register-confirm-password" className="mb-1 block text-sm font-medium text-slate-700">
                ยืนยันรหัสผ่าน <span className="text-red-500">*</span>
              </label>
              <input
                id="register-confirm-password"
                type="password"
                autoComplete="new-password"
                value={form.confirmPassword}
                onChange={(event) => updateField('confirmPassword', event.target.value)}
                className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                  errors.confirmPassword ? 'border-red-400 bg-red-50' : 'border-slate-300'
                }`}
              />
              {errors.confirmPassword && <p className="mt-1 text-xs text-red-600">{errors.confirmPassword}</p>}
            </div>
          </div>

          {activeRole === 'student' && (
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label htmlFor="register-student-id" className="mb-1 block text-sm font-medium text-slate-700">
                  รหัสนักศึกษา <span className="text-red-500">*</span>
                </label>
                <input
                  id="register-student-id"
                  value={form.studentId}
                  onChange={(event) => updateField('studentId', event.target.value)}
                  className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                    errors.studentId ? 'border-red-400 bg-red-50' : 'border-slate-300'
                  }`}
                />
                {errors.studentId && <p className="mt-1 text-xs text-red-600">{errors.studentId}</p>}
              </div>

              <div>
                <label htmlFor="register-university-code" className="mb-1 block text-sm font-medium text-slate-700">
                  รหัสมหาวิทยาลัย <span className="text-red-500">*</span>
                </label>
                <input
                  id="register-university-code"
                  value={form.universityCode}
                  onChange={(event) => updateField('universityCode', event.target.value)}
                  className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                    errors.universityCode ? 'border-red-400 bg-red-50' : 'border-slate-300'
                  }`}
                />
                {errors.universityCode && <p className="mt-1 text-xs text-red-600">{errors.universityCode}</p>}
              </div>
            </div>
          )}

          {activeRole === 'audience' && (
            <div>
              <label htmlFor="register-phone-number" className="mb-1 block text-sm font-medium text-slate-700">
                เบอร์โทรศัพท์ <span className="text-red-500">*</span>
              </label>
              <input
                id="register-phone-number"
                type="tel"
                value={form.phoneNumber}
                onChange={(event) => updateField('phoneNumber', event.target.value)}
                className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                  errors.phoneNumber ? 'border-red-400 bg-red-50' : 'border-slate-300'
                }`}
              />
              {errors.phoneNumber && <p className="mt-1 text-xs text-red-600">{errors.phoneNumber}</p>}
            </div>
          )}

          {activeRole === 'band' && (
            <div className="space-y-4">
              <div>
                <label htmlFor="register-band-name" className="mb-1 block text-sm font-medium text-slate-700">
                  ชื่อวง <span className="text-red-500">*</span>
                </label>
                <input
                  id="register-band-name"
                  value={form.bandName}
                  onChange={(event) => updateField('bandName', event.target.value)}
                  className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                    errors.bandName ? 'border-red-400 bg-red-50' : 'border-slate-300'
                  }`}
                />
                {errors.bandName && <p className="mt-1 text-xs text-red-600">{errors.bandName}</p>}
              </div>

              <div>
                <label htmlFor="register-contact-name" className="mb-1 block text-sm font-medium text-slate-700">
                  ชื่อผู้ติดต่อ <span className="text-red-500">*</span>
                </label>
                <input
                  id="register-contact-name"
                  value={form.contactName}
                  onChange={(event) => updateField('contactName', event.target.value)}
                  className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                    errors.contactName ? 'border-red-400 bg-red-50' : 'border-slate-300'
                  }`}
                />
                {errors.contactName && <p className="mt-1 text-xs text-red-600">{errors.contactName}</p>}
              </div>

              <div>
                <label htmlFor="register-band-phone" className="mb-1 block text-sm font-medium text-slate-700">
                  เบอร์โทรศัพท์ <span className="text-red-500">*</span>
                </label>
                <input
                  id="register-band-phone"
                  type="tel"
                  value={form.phoneNumber}
                  onChange={(event) => updateField('phoneNumber', event.target.value)}
                  className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                    errors.phoneNumber ? 'border-red-400 bg-red-50' : 'border-slate-300'
                  }`}
                />
                {errors.phoneNumber && <p className="mt-1 text-xs text-red-600">{errors.phoneNumber}</p>}
              </div>
            </div>
          )}

          {submitError && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {submitError}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-teal-700 px-4 py-3 text-base font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {isSubmitting ? 'กำลังสมัครสมาชิก...' : 'สมัครสมาชิก'}
          </button>
        </form>
      </section>
    </main>
  )
}

function EventRegistrationView({
  events = defaultEvents,
  user = { id: 1, fullName: 'สมชาย ใจดี', role: 'student' },
  onNavigate = navigateTo,
  onRegisterSuccess,
  existingRegistrationEventIds = [],
} = {}) {
  const [selectedEventId, setSelectedEventId] = useState(events[0]?.id ?? '')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState('')
  const [registeredEvent, setRegisteredEvent] = useState(null)
  const [rejectedEvent, setRejectedEvent] = useState(null)

  const selectedEvent = useMemo(
    () => events.find((event) => event.id === selectedEventId) ?? events[0],
    [events, selectedEventId],
  )

  const remainingSeats = selectedEvent?.remainingSeats ?? 0
  const lowSeats = remainingSeats > 0 && remainingSeats <= registrationUiConfig.lowSeatThreshold
  const isFull = remainingSeats <= 0
  const alreadyRegistered = Boolean(selectedEvent && existingRegistrationEventIds.includes(selectedEvent.id))

  const ticketTypeLabel = user?.role === 'audience' ? 'บัตรผู้ชม' : 'บัตรนักศึกษา'

  const handleConfirmRegistration = async () => {
    if (!selectedEvent) {
      setSubmitError('กรุณาเลือกอีเว้นต์ก่อนยืนยัน')
      return
    }

    if (alreadyRegistered) {
      setSubmitError('ลงทะเบียนซ้ำไม่ได้ คุณลงทะเบียนอีเว้นต์นี้ไว้แล้ว')
      return
    }

    setIsSubmitting(true)
    setSubmitError('')

    try {
      const payload = {
        user_id: user?.id ?? 1,
        event_id: selectedEvent.id,
        confirmation_snapshot: {
          full_name: user?.fullName || user?.name || 'ผู้ใช้',
          role: user?.role || 'student',
          event_name: selectedEvent.name,
          date: selectedEvent.date,
          location: selectedEvent.location,
        },
      }

      const result = await api.registerEvent(payload)
      if (!result?.success) {
        const message = result?.message || 'ไม่สามารถลงทะเบียนได้ กรุณาลองใหม่'
        setRejectedEvent({
          ...selectedEvent,
          rejectionMessage: message,
          isFullSeatFailure: /ที่นั่งเต็ม/i.test(message),
        })
        setSubmitError(message)
        return
      }

      const registrationId = result?.registration?.registration_id || result?.registrationId || `REG-${selectedEvent.id}-${user?.id ?? 'guest'}`
      const confirmedEvent = {
        ...selectedEvent,
        confirmation: result?.registration || payload.confirmation_snapshot,
        registrationId,
        ticketType: ticketTypeLabel,
        userName: user?.fullName || user?.name || 'ผู้ใช้',
        successMessage: 'ลงทะเบียนสำเร็จแล้ว',
      }
      setRegisteredEvent(confirmedEvent)
      if (onRegisterSuccess) {
        onRegisterSuccess(result)
      }
      if (result?.redirectTo) {
        onNavigate(result.redirectTo)
      }
    } catch (error) {
      const message = error?.message || 'ไม่สามารถลงทะเบียนได้ กรุณาลองใหม่'
      setRejectedEvent({
        ...selectedEvent,
        rejectionMessage: message,
        isFullSeatFailure: /ที่นั่งเต็ม/i.test(message),
      })
      setSubmitError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (registeredEvent) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-700">ลงทะเบียนสำเร็จ</p>
            <h1 className="mt-2 text-2xl font-bold text-slate-800">{registeredEvent.successMessage}</h1>
            <p className="mt-2 text-sm text-slate-600">{registeredEvent.name}</p>
            <p className="mt-1 text-sm text-slate-600">{registeredEvent.date}</p>
            <p className="mt-1 text-sm text-slate-600">{registeredEvent.location}</p>
          </div>

          <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 pb-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.eventName}</span>
              <span>{registeredEvent.name}</span>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 py-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.dateTime}</span>
              <span>{registeredEvent.date}</span>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 py-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.ticketType}</span>
              <span>{registeredEvent.ticketType}</span>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 py-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.userName}</span>
              <span>{registeredEvent.userName}</span>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 py-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.confirmationMessage}</span>
              <span>{registeredEvent.successMessage}</span>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 py-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.registrationId}</span>
              <span>{registeredEvent.registrationId}</span>
            </div>
            <div className="flex items-center justify-between gap-3 pt-2">
              <span className="font-medium">{registrationUiConfig.successResultLabels.status}</span>
              <span className="font-semibold text-emerald-700">ยืนยันสำเร็จ</span>
            </div>
          </div>

          <button
            type="button"
            onClick={() => onNavigate('/dashboard')}
            className="mt-5 w-full rounded-xl bg-teal-700 px-4 py-3 text-base font-semibold text-white"
          >
            กลับสู่หน้าหลัก
          </button>
        </section>
      </main>
    )
  }

  if (rejectedEvent) {
    return (
      <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
        <section className="mx-auto w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="rounded-2xl border border-red-200 bg-red-50 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-red-700">ผลการลงทะเบียน</p>
            <h1 className="mt-2 text-2xl font-bold text-slate-800">
              {rejectedEvent.isFullSeatFailure ? 'ที่นั่งเต็ม' : 'ลงทะเบียนไม่สำเร็จ'}
            </h1>
            <p className="mt-2 text-sm text-red-700">{rejectedEvent.rejectionMessage}</p>
          </div>

          <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 pb-2">
              <span className="font-medium">อีเว้นต์</span>
              <span>{rejectedEvent.name}</span>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-slate-200 py-2">
              <span className="font-medium">วันที่</span>
              <span>{rejectedEvent.date}</span>
            </div>
            <div className="flex items-center justify-between gap-3 pt-2">
              <span className="font-medium">สถานที่</span>
              <span>{rejectedEvent.location}</span>
            </div>
          </div>

          <button
            type="button"
            onClick={() => setRejectedEvent(null)}
            className="mt-5 w-full rounded-xl bg-teal-700 px-4 py-3 text-base font-semibold text-white"
          >
            กลับไปหน้าอีเว้นต์
          </button>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">ระบบลงทะเบียนเข้าชมงาน</p>
            <h1 className="mt-1 text-2xl font-bold text-slate-800">ลงทะเบียนเข้าชมงาน</h1>
          </div>
          <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-medium text-teal-800">
            {user?.role === 'audience' ? 'ผู้ชม' : 'นักศึกษา'}
          </span>
        </div>

        <div className="mb-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm font-medium text-slate-700">ผู้ใช้</span>
            <span className="text-sm text-slate-600">{user?.fullName || user?.name || 'สมชาย ใจดี'}</span>
          </div>
        </div>

        <div className="space-y-3">
          {events.map((event) => {
            const choiceIsSelected = selectedEvent?.id === event.id
            const eventIsFull = (event.remainingSeats ?? 0) <= 0
            return (
              <button
                key={event.id}
                type="button"
                onClick={() => setSelectedEventId(event.id)}
                className={`w-full rounded-2xl border p-4 text-left transition ${
                  choiceIsSelected
                    ? 'border-teal-700 bg-teal-50 shadow-sm'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                } ${eventIsFull ? 'opacity-70' : ''}`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-base font-semibold text-slate-800">{event.name}</p>
                    <p className="mt-1 text-sm text-slate-600">{event.date}</p>
                    <p className="mt-1 text-sm text-slate-600">{event.location}</p>
                  </div>
                  <span className={`rounded-full px-2 py-1 text-xs font-medium ${eventIsFull ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'}`}>
                    {eventIsFull ? 'เต็ม' : `${event.remainingSeats} ที่นั่ง`}
                  </span>
                </div>
              </button>
            )
          })}
        </div>

        {selectedEvent && (
          <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-slate-700">ที่นั่งคงเหลือ</span>
              <span className="text-lg font-bold text-slate-800">{selectedEvent.remainingSeats} ที่นั่ง</span>
            </div>
            {lowSeats && !isFull && (
              <div className="mt-3 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
                ที่นั่งเหลือน้อย เหลือเพียง {selectedEvent.remainingSeats} ที่นั่ง
              </div>
            )}
            {alreadyRegistered && (
              <div className="mt-3 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
                <b>ลงทะเบียนซ้ำไม่ได้</b> คุณลงทะเบียนอีเว้นต์นี้ไว้แล้ว
              </div>
            )}
            {isFull && (
              <div className="mt-3 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                ที่นั่งเต็ม อีเว้นต์นี้มีผู้ลงทะเบียนครบจำนวนแล้ว ไม่สามารถลงทะเบียนได้
              </div>
            )}
          </div>
        )}

        {submitError && (
          <div className="mt-4 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {submitError}
          </div>
        )}

        <button
          type="button"
          disabled={isSubmitting || isFull || alreadyRegistered}
          onClick={handleConfirmRegistration}
          className="mt-5 w-full rounded-xl bg-teal-700 px-4 py-3 text-base font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isSubmitting ? 'กำลังยืนยัน...' : alreadyRegistered ? 'ลงทะเบียนซ้ำไม่ได้' : isFull ? 'ที่นั่งเต็ม' : 'ยืนยันการลงทะเบียน'}
        </button>
      </section>
    </main>
  )
}

export default function RegisterPage({
  onNavigate = navigateTo,
  mode = 'auth',
  events,
  user,
  onRegisterSuccess,
  existingRegistrationEventIds = [],
} = {}) {
  const shouldUseEventMode = mode === 'event' || user !== undefined || events !== undefined

  if (shouldUseEventMode) {
    return (
      <EventRegistrationView
        events={events ?? defaultEvents}
        user={user}
        onNavigate={onNavigate}
        onRegisterSuccess={onRegisterSuccess}
        existingRegistrationEventIds={existingRegistrationEventIds}
      />
    )
  }

  return <AuthRegistrationView onNavigate={onNavigate} />
}
