# Form Validation Example

> **Context**: E-commerce checkout form with React Hook Form + Zod
> **Stack**: React 19 + TypeScript + React Hook Form + Zod
> **Last Updated**: 2026-04-23

---

## Overview

Comprehensive form validation example cho checkout flow, bao gồm:
- Client-side validation với Zod schema
- Real-time error feedback
- Async validation (email uniqueness)
- Multi-step form handling
- Accessibility compliance

---

## Zod Schema Definition

```typescript
// schemas/checkout.schema.ts
import { z } from 'zod'

// Phone number regex (Vietnam format)
const phoneRegex = /^(0|\+84)[0-9]{9}$/

// Validation schemas
export const shippingInfoSchema = z.object({
  fullName: z
    .string()
    .min(2, 'Tên phải có ít nhất 2 ký tự')
    .max(50, 'Tên không được quá 50 ký tự')
    .regex(/^[a-zA-ZÀ-ỹ\s]+$/, 'Tên chỉ được chứa chữ cái'),
  
  email: z
    .string()
    .email('Email không hợp lệ')
    .toLowerCase(),
  
  phone: z
    .string()
    .regex(phoneRegex, 'Số điện thoại không hợp lệ (VD: 0912345678)'),
  
  address: z
    .string()
    .min(10, 'Địa chỉ phải có ít nhất 10 ký tự')
    .max(200, 'Địa chỉ không được quá 200 ký tự'),
  
  city: z
    .string()
    .min(1, 'Vui lòng chọn Tỉnh/Thành phố'),
  
  district: z
    .string()
    .min(1, 'Vui lòng chọn Quận/Huyện'),
  
  ward: z
    .string()
    .min(1, 'Vui lòng chọn Phường/Xã'),
  
  note: z
    .string()
    .max(500, 'Ghi chú không được quá 500 ký tự')
    .optional(),
})

export const paymentInfoSchema = z.object({
  paymentMethod: z.enum(['cod', 'bank_transfer', 'momo', 'vnpay'], {
    required_error: 'Vui lòng chọn phương thức thanh toán',
  }),
  
  voucherCode: z
    .string()
    .regex(/^[A-Z0-9]{6,12}$/, 'Mã giảm giá không hợp lệ')
    .optional()
    .or(z.literal('')),
})

export const checkoutSchema = z.object({
  shipping: shippingInfoSchema,
  payment: paymentInfoSchema,
  agreeToTerms: z
    .boolean()
    .refine((val) => val === true, {
      message: 'Bạn phải đồng ý với điều khoản sử dụng',
    }),
})

// TypeScript types từ schema
export type ShippingInfo = z.infer<typeof shippingInfoSchema>
export type PaymentInfo = z.infer<typeof paymentInfoSchema>
export type CheckoutFormData = z.infer<typeof checkoutSchema>
```

---

## Form Component

```tsx
// components/CheckoutForm.tsx
import React, { useState } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { checkoutSchema, type CheckoutFormData } from '@/schemas/checkout.schema'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Alert } from '@/components/ui/alert'
import { checkEmailExists } from '@/services/user.service'
import { submitOrder } from '@/services/order.service'
import { useDebounce } from '@/hooks/use-debounce'

interface CheckoutFormProps {
  cartTotal: number
  onSuccess: (orderId: string) => void
}

export function CheckoutForm({ cartTotal, onSuccess }: CheckoutFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const {
    register,
    control,
    handleSubmit,
    watch,
    setError,
    formState: { errors, isValid },
  } = useForm<CheckoutFormData>({
    resolver: zodResolver(checkoutSchema),
    mode: 'onBlur',
    defaultValues: {
      shipping: {
        fullName: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        district: '',
        ward: '',
        note: '',
      },
      payment: {
        paymentMethod: 'cod',
        voucherCode: '',
      },
      agreeToTerms: false,
    },
  })

  // Watch email field cho async validation
  const emailValue = watch('shipping.email')
  const debouncedEmail = useDebounce(emailValue, 500)

  // Async email validation
  React.useEffect(() => {
    if (debouncedEmail && !errors.shipping?.email) {
      checkEmailExists(debouncedEmail).then((exists) => {
        if (exists) {
          setError('shipping.email', {
            type: 'manual',
            message: 'Email này đã được sử dụng',
          })
        }
      })
    }
  }, [debouncedEmail, setError, errors.shipping?.email])

  const onSubmit = async (data: CheckoutFormData) => {
    setIsSubmitting(true)
    setSubmitError(null)

    try {
      const orderId = await submitOrder({
        shippingInfo: data.shipping,
        paymentMethod: data.payment.paymentMethod,
        voucherCode: data.payment.voucherCode,
        total: cartTotal,
      })

      onSuccess(orderId)
    } catch (error) {
      setSubmitError(
        error instanceof Error 
          ? error.message 
          : 'Đã có lỗi xảy ra. Vui lòng thử lại.'
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {/* Shipping Information Section */}
      <section className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-serif font-semibold text-gray-900 mb-6">
          Thông tin giao hàng
        </h2>

        <div className="space-y-4">
          {/* Full Name */}
          <div>
            <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-1">
              Họ và tên <span className="text-red-500">*</span>
            </label>
            <Input
              id="fullName"
              {...register('shipping.fullName')}
              placeholder="Nguyễn Văn A"
              error={errors.shipping?.fullName?.message}
              aria-invalid={!!errors.shipping?.fullName}
              aria-describedby={errors.shipping?.fullName ? 'fullName-error' : undefined}
            />
            {errors.shipping?.fullName && (
              <p id="fullName-error" className="mt-1 text-sm text-red-600">
                {errors.shipping.fullName.message}
              </p>
            )}
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email <span className="text-red-500">*</span>
            </label>
            <Input
              id="email"
              type="email"
              {...register('shipping.email')}
              placeholder="example@email.com"
              error={errors.shipping?.email?.message}
              aria-invalid={!!errors.shipping?.email}
              aria-describedby={errors.shipping?.email ? 'email-error' : undefined}
            />
            {errors.shipping?.email && (
              <p id="email-error" className="mt-1 text-sm text-red-600">
                {errors.shipping.email.message}
              </p>
            )}
          </div>

          {/* Phone */}
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
              Số điện thoại <span className="text-red-500">*</span>
            </label>
            <Input
              id="phone"
              type="tel"
              {...register('shipping.phone')}
              placeholder="0912345678"
              error={errors.shipping?.phone?.message}
              aria-invalid={!!errors.shipping?.phone}
              aria-describedby={errors.shipping?.phone ? 'phone-error' : undefined}
            />
            {errors.shipping?.phone && (
              <p id="phone-error" className="mt-1 text-sm text-red-600">
                {errors.shipping.phone.message}
              </p>
            )}
          </div>

          {/* Address */}
          <div>
            <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-1">
              Địa chỉ <span className="text-red-500">*</span>
            </label>
            <Input
              id="address"
              {...register('shipping.address')}
              placeholder="Số nhà, tên đường"
              error={errors.shipping?.address?.message}
              aria-invalid={!!errors.shipping?.address}
              aria-describedby={errors.shipping?.address ? 'address-error' : undefined}
            />
            {errors.shipping?.address && (
              <p id="address-error" className="mt-1 text-sm text-red-600">
                {errors.shipping.address.message}
              </p>
            )}
          </div>

          {/* City, District, Ward */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-1">
                Tỉnh/Thành phố <span className="text-red-500">*</span>
              </label>
              <Controller
                name="shipping.city"
                control={control}
                render={({ field }) => (
                  <Select
                    {...field}
                    options={[
                      { value: 'hanoi', label: 'Hà Nội' },
                      { value: 'hcm', label: 'TP. Hồ Chí Minh' },
                      { value: 'danang', label: 'Đà Nẵng' },
                    ]}
                    placeholder="Chọn Tỉnh/TP"
                    error={errors.shipping?.city?.message}
                  />
                )}
              />
            </div>

            <div>
              <label htmlFor="district" className="block text-sm font-medium text-gray-700 mb-1">
                Quận/Huyện <span className="text-red-500">*</span>
              </label>
              <Controller
                name="shipping.district"
                control={control}
                render={({ field }) => (
                  <Select
                    {...field}
                    options={[
                      { value: 'district1', label: 'Quận 1' },
                      { value: 'district3', label: 'Quận 3' },
                    ]}
                    placeholder="Chọn Quận/Huyện"
                    error={errors.shipping?.district?.message}
                  />
                )}
              />
            </div>

            <div>
              <label htmlFor="ward" className="block text-sm font-medium text-gray-700 mb-1">
                Phường/Xã <span className="text-red-500">*</span>
              </label>
              <Controller
                name="shipping.ward"
                control={control}
                render={({ field }) => (
                  <Select
                    {...field}
                    options={[
                      { value: 'ward1', label: 'Phường 1' },
                      { value: 'ward2', label: 'Phường 2' },
                    ]}
                    placeholder="Chọn Phường/Xã"
                    error={errors.shipping?.ward?.message}
                  />
                )}
              />
            </div>
          </div>

          {/* Note */}
          <div>
            <label htmlFor="note" className="block text-sm font-medium text-gray-700 mb-1">
              Ghi chú (tùy chọn)
            </label>
            <Textarea
              id="note"
              {...register('shipping.note')}
              placeholder="Ghi chú thêm về đơn hàng..."
              rows={3}
              error={errors.shipping?.note?.message}
            />
          </div>
        </div>
      </section>

      {/* Payment Information Section */}
      <section className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-serif font-semibold text-gray-900 mb-6">
          Phương thức thanh toán
        </h2>

        <div className="space-y-4">
          {/* Payment Method */}
          <Controller
            name="payment.paymentMethod"
            control={control}
            render={({ field }) => (
              <div className="space-y-2">
                {[
                  { value: 'cod', label: 'Thanh toán khi nhận hàng (COD)' },
                  { value: 'bank_transfer', label: 'Chuyển khoản ngân hàng' },
                  { value: 'momo', label: 'Ví MoMo' },
                  { value: 'vnpay', label: 'VNPay' },
                ].map((option) => (
                  <label
                    key={option.value}
                    className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50"
                  >
                    <input
                      type="radio"
                      {...field}
                      value={option.value}
                      checked={field.value === option.value}
                      className="w-4 h-4 text-primary-600"
                    />
                    <span className="ml-3 text-sm font-medium text-gray-900">
                      {option.label}
                    </span>
                  </label>
                ))}
              </div>
            )}
          />

          {/* Voucher Code */}
          <div>
            <label htmlFor="voucherCode" className="block text-sm font-medium text-gray-700 mb-1">
              Mã giảm giá (tùy chọn)
            </label>
            <Input
              id="voucherCode"
              {...register('payment.voucherCode')}
              placeholder="VD: SUMMER2026"
              error={errors.payment?.voucherCode?.message}
            />
          </div>
        </div>
      </section>

      {/* Terms Agreement */}
      <div className="flex items-start">
        <Controller
          name="agreeToTerms"
          control={control}
          render={({ field }) => (
            <Checkbox
              id="agreeToTerms"
              checked={field.value}
              onCheckedChange={field.onChange}
              aria-invalid={!!errors.agreeToTerms}
              aria-describedby={errors.agreeToTerms ? 'terms-error' : undefined}
            />
          )}
        />
        <label htmlFor="agreeToTerms" className="ml-2 text-sm text-gray-700">
          Tôi đồng ý với{' '}
          <a href="/terms" className="text-primary-600 hover:underline">
            điều khoản sử dụng
          </a>{' '}
          và{' '}
          <a href="/privacy" className="text-primary-600 hover:underline">
            chính sách bảo mật
          </a>
        </label>
      </div>
      {errors.agreeToTerms && (
        <p id="terms-error" className="text-sm text-red-600">
          {errors.agreeToTerms.message}
        </p>
      )}

      {/* Submit Error */}
      {submitError && (
        <Alert variant="error">
          {submitError}
        </Alert>
      )}

      {/* Submit Button */}
      <Button
        type="submit"
        disabled={!isValid || isSubmitting}
        className="w-full"
        size="lg"
      >
        {isSubmitting ? 'Đang xử lý...' : `Đặt hàng - ${cartTotal.toLocaleString('vi-VN')}đ`}
      </Button>
    </form>
  )
}
```

---

## Custom Hook: useDebounce

```typescript
// hooks/use-debounce.ts
import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}
```

---

## Service Layer

```typescript
// services/user.service.ts
import { apiClient } from '@/lib/api-client'

export async function checkEmailExists(email: string): Promise<boolean> {
  try {
    const response = await apiClient.get(`/users/check-email?email=${email}`)
    return response.data.exists
  } catch (error) {
    console.error('Error checking email:', error)
    return false
  }
}

// services/order.service.ts
import { apiClient } from '@/lib/api-client'
import type { ShippingInfo } from '@/schemas/checkout.schema'

interface SubmitOrderPayload {
  shippingInfo: ShippingInfo
  paymentMethod: string
  voucherCode?: string
  total: number
}

export async function submitOrder(payload: SubmitOrderPayload): Promise<string> {
  const response = await apiClient.post('/orders', payload)
  return response.data.orderId
}
```

---

## Benefits

| Feature | Implementation |
|---------|----------------|
| **Type Safety** | Zod schema → TypeScript types |
| **Real-time Validation** | `mode: 'onBlur'` cho UX tốt |
| **Async Validation** | Email uniqueness check |
| **Error Handling** | Granular error messages |
| **Accessibility** | ARIA labels, error announcements |
| **Performance** | Debounced async validation |

---

## Related

- [template-form-patterns.md](../templates/template-form-patterns.md)
- [example-state-management-redux.md](./example-state-management-redux.md)
