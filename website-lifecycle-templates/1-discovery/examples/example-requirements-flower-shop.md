# Requirements Document - SiinStore Flower Shop

> **Project**: E-commerce website bán hoa tươi
> **Date**: 2026-04-23
> **Stakeholder**: SiinStore Management Team

---

## 1. Business Requirements

### 1.1 Business Goals
- Tăng doanh số online 40% trong Q3 2026
- Mở rộng thị trường từ TP.HCM ra 3 tỉnh lân cận
- Giảm chi phí vận hành cửa hàng vật lý 25%
- Tăng customer retention rate lên 60%

### 1.2 Target Audience
| Segment | Demographics | Behavior |
|---------|--------------|----------|
| **Primary** | Nữ 25-40, thu nhập 15-30M/tháng | Mua hoa tặng dịp lễ, sinh nhật |
| **Secondary** | Nam 30-45, thu nhập 20-50M/tháng | Mua hoa tặng vợ/bạn gái |
| **Tertiary** | Doanh nghiệp | Đặt hoa sự kiện, khai trương |

### 1.3 Success Metrics
- **Revenue**: 500M VND/tháng trong 6 tháng đầu
- **Conversion Rate**: 3-5%
- **Average Order Value**: 800K VND
- **Customer Acquisition Cost**: < 150K VND

---

## 2. Functional Requirements

### 2.1 Product Catalog
```yaml
Must Have:
  - Hiển thị 200+ sản phẩm hoa tươi
  - Filter theo: Dịp (sinh nhật, cưới hỏi), Giá, Màu sắc, Loại hoa
  - Search với autocomplete
  - Product detail với 5-8 ảnh chất lượng cao
  - Related products suggestion

Nice to Have:
  - 360° product view
  - AR preview (xem hoa trong không gian thực)
  - Video hướng dẫn chăm sóc hoa
```

### 2.2 Shopping Cart & Checkout
```yaml
Must Have:
  - Add to cart với quantity selector
  - Cart persistence (localStorage + backend sync)
  - Guest checkout (không bắt buộc đăng ký)
  - Multiple payment methods:
    - COD (Cash on Delivery)
    - VNPay
    - MoMo
    - Banking transfer
  - Delivery date/time picker (chọn giờ giao hàng)
  - Gift message (lời nhắn kèm hoa)

Nice to Have:
  - Save cart for later
  - One-click reorder
  - Split payment (chia tiền với bạn)
```

### 2.3 User Account
```yaml
Must Have:
  - Register/Login (Email, Phone, Google, Facebook)
  - Order history với tracking
  - Saved addresses (nhà, công ty, địa chỉ người thân)
  - Wishlist
  - Loyalty points system

Nice to Have:
  - Subscription (giao hoa định kỳ hàng tuần)
  - Referral program (giới thiệu bạn bè)
  - Birthday reminders (nhắc sinh nhật người thân)
```

### 2.4 Admin Dashboard
```yaml
Must Have:
  - Product management (CRUD)
  - Order management (status update, tracking)
  - Customer management
  - Inventory tracking
  - Sales reports (daily, weekly, monthly)
  - Voucher/Promotion management

Nice to Have:
  - Predictive analytics (dự đoán nhu cầu)
  - Automated restock alerts
  - Customer segmentation
```

---

## 3. Non-Functional Requirements

### 3.1 Performance
- **Page Load**: < 2s (3G connection)
- **Time to Interactive**: < 3s
- **API Response**: < 500ms (p95)
- **Image Optimization**: WebP format, lazy loading

### 3.2 Security
- **SSL/TLS**: HTTPS bắt buộc
- **Payment**: PCI DSS compliant
- **Data Protection**: GDPR-like compliance
- **Authentication**: JWT với refresh token
- **Rate Limiting**: 100 requests/minute/IP

### 3.3 Scalability
- **Concurrent Users**: 1000+ users đồng thời
- **Peak Load**: Tết, Valentine, 8/3, 20/10
- **Database**: MongoDB với sharding
- **CDN**: Cloudflare cho static assets

### 3.4 Availability
- **Uptime**: 99.9% (8.76 giờ downtime/năm)
- **Backup**: Daily automated backup
- **Disaster Recovery**: RTO < 4 hours, RPO < 1 hour

---

## 4. Technical Constraints

### 4.1 Technology Stack
```yaml
Frontend:
  - Next.js 15 (App Router)
  - React 19
  - TypeScript
  - TailwindCSS
  - Radix UI

Backend:
  - PayloadCMS 3.x
  - MongoDB
  - Node.js 20+

Infrastructure:
  - Vercel (Frontend hosting)
  - MongoDB Atlas (Database)
  - Cloudflare (CDN)
  - AWS S3 (Image storage)
```

### 4.2 Integration Requirements
- **Payment Gateways**: VNPay, MoMo API
- **Shipping**: Giao Hàng Nhanh (GHN), Giao Hàng Tiết Kiệm (GHTK)
- **SMS**: Twilio hoặc SMSAPI.vn
- **Email**: SendGrid
- **Analytics**: Google Analytics 4, Facebook Pixel

---

## 5. User Stories (High Priority)

### US-001: Browse Products
```
As a customer
I want to browse flower products by occasion
So that I can quickly find suitable flowers for my event

Acceptance Criteria:
- Filter by occasion (Birthday, Wedding, Anniversary, etc.)
- See product image, name, price
- Sort by: Price, Popularity, Newest
- Pagination (24 products/page)
```

### US-002: Quick Checkout
```
As a busy customer
I want to checkout without creating an account
So that I can complete my purchase quickly

Acceptance Criteria:
- Guest checkout option visible
- Only require: Name, Phone, Address, Payment method
- Order confirmation via SMS + Email
- Estimated delivery time shown
```

### US-003: Track Order
```
As a customer
I want to track my order in real-time
So that I know when my flowers will arrive

Acceptance Criteria:
- Order status: Processing, Preparing, Delivering, Delivered
- Real-time updates via SMS
- Delivery person contact info
- Estimated arrival time
```

---

## 6. Out of Scope (Phase 1)

- Mobile app (iOS/Android)
- International shipping
- Flower subscription service
- Live chat support
- Multi-language support
- Cryptocurrency payment

---

## 7. Timeline & Budget

### 7.1 Timeline
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Discovery | 2 weeks | Requirements doc, User research |
| Planning | 2 weeks | Tech stack, Architecture, Sitemap |
| Design | 3 weeks | Design system, Mockups, Prototype |
| Development | 8 weeks | MVP with core features |
| Testing | 2 weeks | QA, UAT, Performance testing |
| Launch | 1 week | Deployment, Monitoring |

**Total**: 18 weeks (~4.5 months)

### 7.2 Budget
- **Development**: 300M VND
- **Design**: 50M VND
- **Infrastructure**: 20M VND/năm
- **Marketing**: 100M VND (first 3 months)
- **Contingency**: 30M VND

**Total**: 500M VND

---

## 8. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Payment gateway downtime | High | Medium | Fallback to COD, multiple gateways |
| Peak load (Tết, Valentine) | High | High | Load testing, auto-scaling, CDN |
| Flower inventory shortage | Medium | Medium | Real-time inventory sync, pre-order |
| Delivery delays | Medium | High | Multiple shipping partners, buffer time |

---

## 9. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | Nguyễn Văn A | _________ | 2026-04-23 |
| Tech Lead | Trần Thị B | _________ | 2026-04-23 |
| Stakeholder | Lê Văn C | _________ | 2026-04-23 |

---

**Next Steps**:
1. Stakeholder review & approval
2. User research & interviews
3. Competitor analysis
4. Technical feasibility study
