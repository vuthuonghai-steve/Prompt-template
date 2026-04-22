# User Stories - Checkout Flow (SiinStore)

> **Epic**: Checkout & Payment
> **Priority**: P0 (Must Have)
> **Date**: 2026-04-22

---

## Epic Overview

**Goal**: Tạo checkout flow mượt mà, giảm cart abandonment rate từ 70% xuống 40%

**Success Metrics**:
- Checkout completion rate: > 60%
- Average checkout time: < 3 minutes
- Payment success rate: > 95%

---

## User Stories

### US-CH-001: Guest Checkout

```yaml
As a: First-time customer
I want to: Checkout without creating an account
So that: I can complete my purchase quickly without friction

Story Points: 5
Priority: P0

Acceptance Criteria:
  - [ ] "Continue as Guest" button visible on cart page
  - [ ] Only require essential info: Name, Phone, Email, Address
  - [ ] No password required
  - [ ] Order confirmation sent via Email + SMS
  - [ ] Option to create account after purchase (with order history)

Technical Notes:
  - Create guest user record với flag `isGuest: true`
  - Generate temporary token cho order tracking
  - Sau 30 ngày, prompt convert to full account

Dependencies:
  - Email service integration
  - SMS service integration

Test Cases:
  - Guest checkout với valid info → Success
  - Guest checkout với invalid phone → Error message
  - Guest checkout → Receive confirmation email/SMS
  - Guest order tracking với order ID + phone
```

---

### US-CH-002: Delivery Date/Time Picker

```yaml
As a: Customer buying flowers for a special occasion
I want to: Choose specific delivery date and time
So that: Flowers arrive exactly when I need them

Story Points: 8
Priority: P0

Acceptance Criteria:
  - [ ] Calendar picker cho delivery date (today + 30 days)
  - [ ] Time slots: Morning (8-12h), Afternoon (13-17h), Evening (18-21h)
  - [ ] Show available slots (disable fully booked slots)
  - [ ] Same-day delivery nếu order trước 10h sáng
  - [ ] Price adjustment cho express delivery (+50K VND)

Technical Notes:
  - Check inventory availability cho selected date
  - Integrate với shipping partner API (GHN/GHTK)
  - Real-time slot availability từ database

Business Rules:
  - Same-day delivery: Order trước 10h, giao sau 14h
  - Express delivery: +50K VND, giao trong 2-4h
  - Standard delivery: Free, giao trong 24-48h
  - Không giao vào: Tết (29-3 Âm lịch)

Test Cases:
  - Select today + Morning slot → Show express fee
  - Select tomorrow + Afternoon → Standard delivery
  - Select fully booked slot → Disabled
  - Select date > 30 days → Error
```

---

### US-CH-003: Multiple Payment Methods

```yaml
As a: Customer
I want to: Choose from multiple payment options
So that: I can pay using my preferred method

Story Points: 13
Priority: P0

Acceptance Criteria:
  - [ ] Payment methods: COD, VNPay, MoMo, Banking Transfer
  - [ ] Show payment method icons
  - [ ] COD: No extra fee
  - [ ] VNPay/MoMo: Redirect to gateway, return with status
  - [ ] Banking Transfer: Show QR code + account info
  - [ ] Payment timeout: 15 minutes
  - [ ] Retry payment nếu failed

Technical Notes:
  - VNPay SDK integration
  - MoMo API integration
  - Generate QR code cho banking transfer (VietQR standard)
  - Webhook để nhận payment status

Payment Flow:
  1. Customer chọn payment method
  2. If VNPay/MoMo → Redirect to gateway
  3. Customer complete payment
  4. Gateway callback webhook
  5. Update order status
  6. Send confirmation

Error Handling:
  - Payment timeout → Cancel order, release inventory
  - Payment failed → Show retry button
  - Webhook failed → Retry 3 times với exponential backoff

Test Cases:
  - COD payment → Order confirmed immediately
  - VNPay payment success → Order confirmed
  - VNPay payment failed → Show error, allow retry
  - MoMo payment timeout → Order cancelled
  - Banking transfer → Show QR code + instructions
```

---

### US-CH-004: Gift Message

```yaml
As a: Customer sending flowers as a gift
I want to: Add a personalized message
So that: The recipient knows who sent the flowers

Story Points: 3
Priority: P1

Acceptance Criteria:
  - [ ] Text area cho gift message (max 200 characters)
  - [ ] Character counter
  - [ ] Preview message trên card
  - [ ] Option: "Keep sender anonymous"
  - [ ] Free service (no extra charge)

Technical Notes:
  - Store message trong Order.giftMessage field
  - Print message trên card khi prepare order
  - Sanitize input (prevent XSS)

Business Rules:
  - Max 200 characters (fit trên card 10x15cm)
  - Không cho phép: URLs, phone numbers, profanity
  - Default message: "Chúc mừng sinh nhật! 🎉"

Test Cases:
  - Add message < 200 chars → Success
  - Add message > 200 chars → Show error
  - Add message với URL → Sanitized
  - Anonymous option → Sender name hidden
```

---

### US-CH-005: Order Summary & Review

```yaml
As a: Customer
I want to: Review my order before payment
So that: I can verify all details are correct

Story Points: 5
Priority: P0

Acceptance Criteria:
  - [ ] Show: Products, Quantities, Prices
  - [ ] Show: Delivery address, Date/Time
  - [ ] Show: Gift message (if any)
  - [ ] Show: Subtotal, Shipping fee, Discount, Total
  - [ ] "Edit" buttons cho mỗi section
  - [ ] Terms & Conditions checkbox
  - [ ] "Place Order" button (disabled until T&C checked)

Technical Notes:
  - Calculate total real-time
  - Apply voucher discount
  - Validate inventory trước khi place order

Price Breakdown:
  - Subtotal: Sum of product prices
  - Shipping: Based on distance + delivery speed
  - Discount: Voucher + Loyalty points
  - Total: Subtotal + Shipping - Discount

Test Cases:
  - Review order → All info correct
  - Click "Edit Address" → Navigate to address form
  - Uncheck T&C → "Place Order" disabled
  - Place order → Inventory reserved
```

---

### US-CH-006: Apply Voucher Code

```yaml
As a: Customer
I want to: Apply a discount voucher
So that: I can save money on my purchase

Story Points: 8
Priority: P1

Acceptance Criteria:
  - [ ] Voucher input field với "Apply" button
  - [ ] Validate voucher code real-time
  - [ ] Show discount amount
  - [ ] Show voucher conditions (min order, expiry)
  - [ ] Allow remove voucher
  - [ ] Show error nếu voucher invalid/expired

Technical Notes:
  - API: POST /api/vouchers/validate
  - Check: Code exists, Not expired, Min order met, Usage limit
  - Apply discount: Percentage or Fixed amount

Voucher Types:
  - Percentage: 10% off, 20% off (max 100K VND)
  - Fixed: 50K off, 100K off
  - Free shipping
  - Buy 1 Get 1

Business Rules:
  - 1 voucher per order
  - Cannot combine với loyalty points
  - Voucher không áp dụng cho shipping fee

Test Cases:
  - Apply valid voucher → Discount applied
  - Apply expired voucher → Error message
  - Apply voucher với min order not met → Error
  - Remove voucher → Discount removed
```

---

### US-CH-007: Save Address for Future

```yaml
As a: Returning customer
I want to: Save my delivery addresses
So that: I don't have to re-enter them every time

Story Points: 5
Priority: P1

Acceptance Criteria:
  - [ ] Checkbox: "Save this address"
  - [ ] Label address: "Home", "Office", "Mom's house", etc.
  - [ ] Set default address
  - [ ] Manage addresses trong account settings
  - [ ] Quick select saved address trong checkout

Technical Notes:
  - Store trong User.addresses array
  - Max 5 saved addresses
  - Validate address format (Google Maps API)

Address Fields:
  - Label: String (required)
  - Full name: String (required)
  - Phone: String (required)
  - Address line 1: String (required)
  - Address line 2: String (optional)
  - City: String (required)
  - District: String (required)
  - Ward: String (required)
  - isDefault: Boolean

Test Cases:
  - Save address → Appears in account settings
  - Set default address → Auto-selected in checkout
  - Delete address → Removed from list
  - Edit address → Updated successfully
```

---

## User Flow Diagram

```
[Cart Page]
    │
    ├─ Continue as Guest
    │   └─> [Guest Info Form]
    │
    └─ Login/Register
        └─> [Saved Addresses]
            │
            ▼
    [Delivery Date/Time Picker]
            │
            ▼
    [Gift Message (Optional)]
            │
            ▼
    [Apply Voucher (Optional)]
            │
            ▼
    [Order Summary & Review]
            │
            ├─ Edit → Back to previous step
            │
            └─ Place Order
                │
                ▼
        [Payment Method Selection]
                │
                ├─ COD → [Order Confirmed]
                ├─ VNPay → [VNPay Gateway] → [Order Confirmed]
                ├─ MoMo → [MoMo Gateway] → [Order Confirmed]
                └─ Banking → [QR Code] → [Order Confirmed]
                        │
                        ▼
                [Order Tracking Page]
```

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Unit tests coverage > 80%
- [ ] Integration tests passed
- [ ] UI matches design mockups
- [ ] Mobile responsive
- [ ] Accessibility (WCAG AA)
- [ ] Performance: Checkout < 3s
- [ ] Security: Input validation, XSS prevention
- [ ] Code review approved
- [ ] QA testing passed
- [ ] Product Owner approval

---

## Related Documents

- [example-requirements-flower-shop.md](./example-requirements-flower-shop.md)
- [example-use-case-order-flow.md](./example-use-case-order-flow.md)
- Design: `3-design/examples/example-checkout-flow-wireframe.md`
- API: `5-development/examples/example-api-product-endpoint.ts`
