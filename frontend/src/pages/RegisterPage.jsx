import { useMemo, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-AUTH-01, FR-AUTH-02, FR-AUTH-03 และ FR-AUTH-05
const ROLE_OPTIONS = [
  { value: 'student', label: 'นักศึกษา' },
  { value: 'audience', label: 'ผู้ชม' },
  { value: 'band', label: 'วงดนตรี' },
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

export default function RegisterPage({ onNavigate = navigateTo } = {}) {
  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState('')

  const activeRole = form.role
  const roleSummary = useMemo(() => getRoleLabel(activeRole), [activeRole])

  const updateField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }))
    setErrors((current) => ({ ...current, [field]: '' }))
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
          <button
            type="button"
            className="flex-1 rounded-full bg-teal-700 px-3 py-2 text-sm font-semibold text-white shadow-sm"
          >
            สมัครสมาชิก
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4" noValidate>
          <div>
            <p className="mb-2 block text-sm font-medium text-slate-700">สมัครในบทบาท <span className="text-red-500">*</span></p>
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
