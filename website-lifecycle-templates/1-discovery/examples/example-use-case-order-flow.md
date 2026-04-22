# Use Case - Order Flow (SiinStore)

> **Use Case ID**: UC-001
> **Name**: Complete Flower Order Flow
> **Actor**: Customer (Guest/Registered)
> **Date**: 2026-04-22

---

## 1. Use Case Overview

### 1.1 Description
Customer duyệt sản phẩm hoa, thêm vào giỏ hàng, và hoàn tất đơn hàng với delivery date/time cụ thể.

### 1.2 Goal
Tạo đơn hàng thành công và nhận confirmation trong vòng 3 phút.

### 1.3 Preconditions
- Website đang hoạt động
- Có ít nhất 1 sản phẩm trong inventory
- Payment gateway available

### 1.4 Postconditions
- Order được tạo trong database
- Inventory được reserve
- Customer nhận confirmation email/SMS
- Admin nhận notification

---

## 2. Main Success Scenario (Happy Path)

### Step-by-Step Flow

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 1 | Customer | Truy cập homepage | Hiển thị featured products |
| 2 | Customer | Click "Hoa Sinh Nhật" category | Hiển thị 24 products với filter |
| 3 | Customer | Filter: Giá 500K-1M, Màu Hồng | Hiển thị 8 matching products |
| 4 | Customer | Click product "Bó Hồng Phấn Pastel" | Hiển thị product detail page |
| 5 | Customer | Xem 6 ảnh, đọc description | - |
| 6 | Customer | Select quantity: 2 | Update price: 1,600,000 VND |
| 7 | Customer | Click "Thêm vào giỏ" | Show toast: "Đã thêm vào giỏ" |
| 8 | Customer | Click cart icon (badge: 2) | Navigate to cart page |
| 9 | Customer | Review cart items | Show: 2 items, Total: 1,600,000 VND |
| 10 | Customer | Click "Thanh toán" | Navigate to checkout |
| 11 | Customer | Select "Tiếp tục với Guest" | Show guest info form |
| 12 | Customer | Fill: Name, Phone, Email, Address | Validate fields real-time |
| 13 | Customer | Click "Tiếp tục" | Navigate to delivery picker |
| 14 | Customer | Select date: Tomorrow (23/04) | Show available time slots |
| 15 | Customer | Select time: Afternoon (13-17h) | Calculate shipping: 30,000 VND |
| 16 | Customer | Click "Tiếp tục" | Navigate to gift message |
| 17 | Customer | Enter: "Chúc mừng sinh nhật em!" | Character count: 26/200 |
| 18 | Customer | Click "Tiếp tục" | Navigate to order summary |
| 19 | Customer | Review order details | Show breakdown |
| 20 | Customer | Enter voucher: "SINHNHAT10" | Apply 10% discount: -160,000 VND |
| 21 | Customer | Check "Đồng ý điều khoản" | Enable "Đặt hàng" button |
| 22 | Customer | Click "Đặt hàng" | Reserve inventory, create order |
| 23 | System | - | Navigate to payment selection |
| 24 | Customer | Select "VNPay" | Redirect to VNPay gateway |
| 25 | Customer | Complete payment | VNPay callback webhook |
| 26 | System | - | Update order status: PAID |
| 27 | System | - | Send confirmation email/SMS |
| 28 | System | - | Notify admin dashboard |
| 29 | Customer | Return to website | Show order confirmation page |
| 30 | Customer | View order tracking | Show status: "Đang xử lý" |

---

## 3. Order Summary Breakdown

```yaml
Order ID: ORD-20260423-001234
Status: PAID

Products:
  - Bó Hồng Phấn Pastel x2
    Price: 800,000 VND each
    Subtotal: 1,600,000 VND

Delivery:
  Date: 23/04/2026
  Time: 13:00 - 17:00
  Address: 123 Nguyễn Huệ, Q1, TP.HCM
  Fee: 30,000 VND

Gift Message:
  "Chúc mừng sinh nhật em!"

Pricing:
  Subtotal: 1,600,000 VND
  Shipping: 30,000 VND
  Discount (SINHNHAT10): -160,000 VND
  Total: 1,470,000 VND

Payment:
  Method: VNPay
  Status: SUCCESS
  Transaction ID: VNP-20260423-567890
```

---

## 4. Alternative Flows

### 4.1 Alternative Flow A: Registered User Checkout

| Step | Difference from Main Flow |
|------|---------------------------|
| 11 | Customer clicks "Đăng nhập" |
| 12 | System shows saved addresses |
| 13 | Customer selects "Nhà riêng" address |
| 14 | Auto-fill: Name, Phone, Address |
| 15 | Continue to delivery picker |

**Benefit**: Faster checkout (skip manual entry)

---

### 4.2 Alternative Flow B: COD Payment

| Step | Difference from Main Flow |
|------|---------------------------|
| 24 | Customer selects "COD" |
| 25 | System creates order với status: PENDING |
| 26 | Send confirmation: "Đơn hàng đang xử lý" |
| 27 | Admin confirms order manually |
| 28 | Status update: CONFIRMED |

**Note**: COD orders require admin confirmation

---

### 4.3 Alternative Flow C: Same-Day Express Delivery

| Step | Difference from Main Flow |
|------|---------------------------|
| 2 | Current time: 09:30 AM |
| 14 | Customer selects date: Today (22/04) |
| 15 | System shows: "Express delivery +50,000 VND" |
| 16 | Customer selects time: Evening (18-21h) |
| 17 | Shipping fee: 80,000 VND (30K + 50K express) |

**Business Rule**: Same-day delivery chỉ available nếu order trước 10:00 AM

---

## 5. Exception Flows

### 5.1 Exception E1: Out of Stock

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 7 | Customer | Click "Thêm vào giỏ" | Check inventory |
| 8 | System | - | Stock: 0 available |
| 9 | System | - | Show error: "Sản phẩm tạm hết hàng" |
| 10 | System | - | Suggest: "Đăng ký nhận thông báo khi có hàng" |

**Recovery**: Customer có thể đăng ký email notification

---

### 5.2 Exception E2: Payment Failed

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 25 | Customer | Complete payment | VNPay returns: FAILED |
| 26 | System | - | Show error: "Thanh toán thất bại" |
| 27 | System | - | Keep order với status: PAYMENT_PENDING |
| 28 | System | - | Show "Thử lại" button |
| 29 | Customer | Click "Thử lại" | Redirect to payment again |

**Timeout**: Nếu không retry trong 15 phút → Cancel order, release inventory

---

### 5.3 Exception E3: Invalid Voucher

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 20 | Customer | Enter voucher: "EXPIRED123" | Validate voucher |
| 21 | System | - | Check: Voucher expired |
| 22 | System | - | Show error: "Mã giảm giá đã hết hạn" |
| 23 | System | - | Suggest: "Xem mã khuyến mãi khác" |

**Recovery**: Customer có thể thử voucher khác hoặc continue without discount

---

### 5.4 Exception E4: Delivery Slot Full

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 15 | Customer | Select time: Afternoon (13-17h) | Check slot availability |
| 16 | System | - | Slot capacity: 50/50 orders |
| 17 | System | - | Disable slot, show: "Đã đầy" |
| 18 | System | - | Suggest: "Chọn khung giờ khác" |

**Business Rule**: Max 50 orders per time slot per day

---

## 6. Business Rules

### 6.1 Inventory Management
```yaml
Rule: Reserve inventory khi customer clicks "Đặt hàng"
Duration: 15 minutes (payment timeout)
Action: Release nếu payment không complete
```

### 6.2 Delivery Scheduling
```yaml
Same-Day:
  Condition: Order trước 10:00 AM
  Fee: +50,000 VND
  Delivery: Sau 14:00 cùng ngày

Standard:
  Condition: Order bất kỳ lúc nào
  Fee: 30,000 VND (trong nội thành)
  Delivery: 24-48 giờ

Express:
  Condition: Order trước 10:00 AM
  Fee: +50,000 VND
  Delivery: 2-4 giờ
```

### 6.3 Voucher Rules
```yaml
Validation:
  - Code exists trong database
  - Not expired (check validUntil)
  - Min order value met
  - Usage limit not exceeded
  - Applicable to product category

Application:
  - 1 voucher per order
  - Cannot combine với loyalty points
  - Apply trước shipping fee
```

### 6.4 Payment Timeout
```yaml
Timeout: 15 minutes từ khi click "Đặt hàng"
Action:
  - Cancel order
  - Release inventory
  - Send notification: "Đơn hàng đã hủy do quá thời gian thanh toán"
```

---

## 7. Data Requirements

### 7.1 Order Entity
```typescript
interface Order {
  id: string                    // ORD-20260423-001234
  customerId?: string           // null nếu guest
  guestInfo?: {
    name: string
    phone: string
    email: string
  }
  items: OrderItem[]
  delivery: {
    address: Address
    date: Date                  // 2026-04-23
    timeSlot: 'morning' | 'afternoon' | 'evening'
    fee: number                 // 30000
  }
  giftMessage?: string
  pricing: {
    subtotal: number            // 1600000
    shipping: number            // 30000
    discount: number            // 160000
    total: number               // 1470000
  }
  voucher?: {
    code: string                // SINHNHAT10
    discountAmount: number      // 160000
  }
  payment: {
    method: 'COD' | 'VNPay' | 'MoMo' | 'Banking'
    status: 'PENDING' | 'PAID' | 'FAILED'
    transactionId?: string
    paidAt?: Date
  }
  status: OrderStatus
  createdAt: Date
  updatedAt: Date
}

type OrderStatus = 
  | 'PAYMENT_PENDING'   // Chờ thanh toán
  | 'PAID'              // Đã thanh toán
  | 'CONFIRMED'         // Admin xác nhận
  | 'PREPARING'         // Đang chuẩn bị hoa
  | 'DELIVERING'        // Đang giao hàng
  | 'DELIVERED'         // Đã giao
  | 'CANCELLED'         // Đã hủy
```

---

## 8. Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Page Load Time | < 2s | Lighthouse |
| API Response Time | < 500ms | p95 |
| Checkout Completion | < 3 min | User testing |
| Payment Success Rate | > 95% | Analytics |
| Cart Abandonment | < 40% | Google Analytics |

---

## 9. Security Requirements

### 9.1 Input Validation
- Sanitize gift message (prevent XSS)
- Validate phone number format (10 digits)
- Validate email format (RFC 5322)
- Validate address (Google Maps API)

### 9.2 Payment Security
- HTTPS only
- PCI DSS compliant
- No credit card storage
- Tokenized payment (VNPay/MoMo)

### 9.3 Rate Limiting
- 100 requests/minute per IP
- 10 checkout attempts/hour per user
- 5 payment retries per order

---

## 10. Integration Points

### 10.1 External Services
```yaml
Payment Gateways:
  - VNPay API v2.1.0
  - MoMo API v2.0

Shipping Partners:
  - Giao Hàng Nhanh (GHN) API
  - Giao Hàng Tiết Kiệm (GHTK) API

Notifications:
  - SendGrid (Email)
  - Twilio (SMS)

Analytics:
  - Google Analytics 4
  - Facebook Pixel
```

### 10.2 Internal Services
```yaml
Services:
  - ProductService: Check inventory
  - OrderService: Create order
  - PaymentService: Process payment
  - NotificationService: Send email/SMS
  - VoucherService: Validate voucher
  - ShippingService: Calculate fee, book delivery
```

---

## 11. Test Scenarios

### 11.1 Happy Path Test
```gherkin
Given customer is on homepage
When customer adds 2 products to cart
And proceeds to checkout as guest
And fills delivery info
And selects delivery date/time
And applies valid voucher
And completes VNPay payment
Then order is created with status PAID
And customer receives confirmation email/SMS
And admin sees order in dashboard
```

### 11.2 Edge Case Tests
- Out of stock during checkout
- Payment timeout (15 minutes)
- Invalid voucher code
- Delivery slot full
- Payment gateway downtime
- Network error during payment
- Duplicate order submission

---

## 12. Related Documents

- **Requirements**: [example-requirements-flower-shop.md](./example-requirements-flower-shop.md)
- **User Stories**: [example-user-stories-checkout.md](./example-user-stories-checkout.md)
- **API Spec**: `5-development/examples/example-api-product-endpoint.ts`
- **Database Schema**: `5-development/examples/example-database-schema-orders.sql`
- **Test Cases**: `6-testing/examples/example-test-checkout-flow.spec.ts`

---

## 13. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-22 | Product Team | Initial version |
| 1.1 | 2026-04-22 | Tech Lead | Add technical details |
