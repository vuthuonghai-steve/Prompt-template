# Design — API Contract

> **Status**: Approved
> **Version**: 1.0.0
> **Last Updated**: 2026-03-21

---

## 1. Overview

Dashboard API gồm 2 endpoint riêng biệt — stats và detail — được thiết kế theo module-first pattern. Mỗi endpoint là thin transport layer chỉ chịu trách nhiệm parse request, validate, gọi service, map response.

**Base URL**: `/api/v1/admin/dashboard`

**Authentication**: `payload.auth()` middleware — kiểm tra JWT token từ Authorization header.

**RBAC**: Roles được phép truy cập — `['admin', 'manager', 'super_admin']`.

---

## 2. Design Decisions

### 2.1 Hai Endpoint Riêng Biệt

Stats và detail không được gộp vào một endpoint vì:

- **Frequency khác nhau**: Stats thay đổi chậm hơn (30s cache), detail thay đổi nhanh hơn (60s cache)
- **Use case khác nhau**: Dashboard load cần stats ngay, chart có thể lazy-load
- **Granularity khác nhau**: Stats trả về aggregate numbers, detail trả về time-series data
- **Performance**: Tách ra cho phép independent caching và parallel fetching

### 2.2 Date Range Preset System

14 presets + custom picker:

| ID | Label | Calculation |
|----|-------|-------------|
| `today` | Hôm nay | today 00:00 → now |
| `yesterday` | Hôm qua | yesterday 00:00 → yesterday 23:59 |
| `last_7_days` | 7 ngày qua | today - 7d → today |
| `last_14_days` | 14 ngày qua | today - 14d → today |
| `last_28_days` | 28 ngày qua | today - 28d → today |
| `last_30_days` | 30 ngày qua | today - 30d → today |
| `last_60_days` | 60 ngày qua | today - 60d → today |
| `last_90_days` | 90 ngày qua | today - 90d → today |
| `this_week` | Tuần này | Monday 00:00 → now |
| `this_month` | Tháng này | 1st of month 00:00 → now |
| `last_week` | Tuần trước | Last Monday → Last Sunday |
| `last_month` | Tháng trước | 1st of last month → last day of last month |
| `this_quarter` | Quý này | 1st of quarter → now |
| `this_year` | Năm nay | 1st Jan → now |

### 2.3 Cache Headers

```
Stats:      Cache-Control: public, max-age=30, stale-while-revalidate=60
Detail:     Cache-Control: public, max-age=60, stale-while-revalidate=120
```

- `max-age`: Thời gian browser/CDN được cache trước khi revalidate
- `stale-while-revalidate`: Cho phép serve stale data trong khi background revalidate

### 2.4 Error Response Format

Tất cả error responses tuân theo format thống nhất:

```typescript
interface ErrorResponse {
  code: string          // Mã lỗi machine-readable
  message: string       // Thông điệp mô tả (tiếng Việt)
  details?: unknown     // Chi tiết bổ sung (optional)
}
```

---

## 3. API Contract

### 3.1 GET /api/v1/admin/dashboard/stats

Lấy 6 KPIs + comparison với kỳ trước.

#### Request

```
GET /api/v1/admin/dashboard/stats
Authorization: Bearer <jwt_token>
```

**Query Parameters**:

| Parameter | Type | Required | Default | Mô tả |
|-----------|------|----------|---------|-------|
| `preset` | string | No | `last_30_days` | Preset date range |
| `from` | string (ISO date) | No | — | Custom start date (YYYY-MM-DD) |
| `to` | string (ISO date) | No | — | Custom end date (YYYY-MM-DD) |

**Validation**:
- Nếu `preset` được set → ignore `from`/`to`
- Nếu `from` và `to` được set → dùng custom range
- Nếu không có gì → dùng `last_30_days` default

#### Response 200 OK

```json
{
  "data": {
    "kpis": {
      "revenue": {
        "value": 125000000,
        "currency": "VND",
        "comparison": {
          "value": 98000000,
          "changePercent": 27.55,
          "trend": "up"
        }
      },
      "totalOrders": {
        "value": 342,
        "comparison": {
          "value": 298,
          "changePercent": 14.77,
          "trend": "up"
        }
      },
      "newCustomers": {
        "value": 87,
        "comparison": {
          "value": 65,
          "changePercent": 33.85,
          "trend": "up"
        }
      },
      "aov": {
        "value": 365497,
        "currency": "VND",
        "comparison": {
          "value": 328859,
          "changePercent": 11.14,
          "trend": "up"
        }
      },
      "pendingOrders": {
        "value": 23,
        "comparison": {
          "value": 31,
          "changePercent": -25.81,
          "trend": "down"
        },
        "alert": "medium"
      },
      "completionRate": {
        "value": 87.5,
        "unit": "%",
        "comparison": {
          "value": 84.2,
          "changePercent": 3.92,
          "trend": "up"
        }
      }
    },
    "meta": {
      "preset": "last_30_days",
      "from": "2026-02-19",
      "to": "2026-03-21",
      "spanDays": 30,
      "generatedAt": "2026-03-21T10:30:00.000Z"
    }
  }
}
```

### 3.2 GET /api/v1/admin/dashboard/detail

Lấy revenue chart và top selling products.

#### Request

```
GET /api/v1/admin/dashboard/detail
Authorization: Bearer <jwt_token>
```

**Query Parameters**:

| Parameter | Type | Required | Default | Mô tả |
|-----------|------|----------|---------|-------|
| `preset` | string | No | `last_30_days` | Preset date range |
| `from` | string (ISO date) | No | — | Custom start date |
| `to` | string (ISO date) | No | — | Custom end date |
| `granularity` | string | No | `day` | `day` \| `week` \| `month` |
| `topProductsLimit` | number | No | `10` | Số lượng top products (max 50) |

#### Response 200 OK

```json
{
  "data": {
    "revenueChart": {
      "granularity": "day",
      "data": [
        {
          "date": "2026-03-01",
          "revenue": 4200000,
          "orders": 12
        },
        {
          "date": "2026-03-02",
          "revenue": 5800000,
          "orders": 17
        }
      ],
      "summary": {
        "totalRevenue": 125000000,
        "totalOrders": 342
      }
    },
    "topProducts": {
      "limit": 10,
      "data": [
        {
          "productId": "prod_abc123",
          "name": "Hoa Hồng Đỏ",
          "thumbnail": "https://cdn.siin.vn/products/hoa-hong-do.jpg",
          "totalSold": 156,
          "totalRevenue": 23400000
        }
      ]
    },
    "meta": {
      "preset": "last_30_days",
      "from": "2026-02-19",
      "to": "2026-03-21",
      "spanDays": 30,
      "generatedAt": "2026-03-21T10:30:00.000Z"
    }
  }
}
```

---

## 4. Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Stats Endpoint Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request                                                          │
│    │                                                              │
│    ▼                                                              │
│  ┌──────────────────┐                                             │
│  │  route.ts        │  1. payload.auth() → verify JWT             │
│  │  (thin transport)│  2. Validate query (Zod schema)            │
│  └────────┬─────────┘  3. Parse date range (preset or custom)   │
│           │  4. Call services                                    │
│           ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Stats Services Pipeline (sequential, then merge)    │        │
│  │                                                      │        │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────┐  │        │
│  │  │ aggregate-    │  │ aggregate-    │  │ aggregate │  │        │
│  │  │ orders.       │  │ revenue.      │  │ withdraw. │  │        │
│  │  │ service       │  │ service       │  │ service   │  │        │
│  │  └───────┬───────┘  └───────┬───────┘  └─────┬─────┘  │        │
│  │          └────────────────┬┴────────────────┘          │        │
│  │                           │                           │        │
│  │                           ▼                           │        │
│  │                  ┌─────────────────┐                   │        │
│  │                  │ comparison-    │  ← prev period    │        │
│  │                  │ calculator.ts  │  ← (re-run with   │        │
│  │                  └────────┬────────┘    prev dates)    │        │
│  │                           │                           │        │
│  └───────────────────────────┼───────────────────────────┘        │
│                              │                                     │
│                              ▼                                     │
│                       Map to response                              │
│                              │                                     │
│                              ▼                                     │
│                      Set cache headers                             │
│                              │                                     │
│                              ▼                                     │
│                       Response 200                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Detail Endpoint Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request                                                          │
│    │                                                              │
│    ▼                                                              │
│  ┌──────────────────┐                                             │
│  │  route.ts        │  1. payload.auth() → verify JWT             │
│  │  (thin transport)│  2. Validate query (Zod schema)             │
│  └────────┬─────────┘  3. Parse date range                       │
│           │  4. Call services (parallel)                         │
│           ▼                                                       │
│  ┌────────────────────┐  ┌──────────────────────┐               │
│  │ revenue-chart.     │  │ top-products.        │               │
│  │ service            │  │ service              │               │
│  │ (by granularity)   │  │ (top N products)     │               │
│  └────────┬───────────┘  └──────────┬───────────┘               │
│           │                         │                            │
│           └──────────┬───────────────┘                            │
│                      ▼                                           │
│               Map to response                                     │
│                      │                                            │
│                      ▼                                            │
│              Set cache headers                                    │
│                      │                                            │
│                      ▼                                            │
│               Response 200                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Edge Cases

### 5.1 Empty Date Range

- Nếu `from > to` → return error `INVALID_DATE_RANGE`
- Nếu không có data trong range → return `{ data: [], meta: { ... } }` với `data` = empty arrays

### 5.2 Preset Conflicts

- Nếu `preset` AND `from/to` cùng được set → ưu tiên `preset`, ignore `from/to`
- Nếu `preset` không hợp lệ → return error `INVALID_PRESET`

### 5.3 Zero Comparison

- Nếu previous period = 0 và current > 0 → `changePercent = null`, `trend = 'up'`
- Nếu previous period = 0 và current = 0 → `changePercent = 0`, `trend = 'neutral'`
- Nếu current = 0 và previous > 0 → `changePercent = -100`, `trend = 'down'`

### 5.4 Hold Orders

- **Luôn excluded** từ stats và revenue: filter `{ 'status.hold': { $ne: true } }`
- Hold orders không xuất hiện trong chart data
- Hold orders không ảnh hưởng `pendingOrders` count (hold ≠ pending)

### 5.5 Maximum Date Range

- Max span: 365 ngày (prevents excessive aggregation on large datasets)
- Nếu `from - to > 365` → return error `INVALID_DATE_RANGE` với message

### 5.6 Concurrent Requests

- Không có locking mechanism → last write wins (acceptable for dashboard)
- Stats và detail có thể show slightly inconsistent data (stats updated at t=0, detail at t=5s)

### 5.7 Future Dates

- Nếu `to` > today → clamp `to` = today
- Future dates trong chart → return empty data points

### 5.8 Currency Formatting

- Revenue stored as integers (VND, no decimals)
- API trả về raw integers, frontend format (VD: `1.250.000 ₫`)

---

## 6. Dependencies

### 6.1 Internal Dependencies

| Dependency | Type | Source |
|-----------|------|--------|
| `payload.auth()` | CMS | PayloadCMS 3.49.1 |
| `payload.db` | Database | PayloadCMS MongoDB adapter |
| `storeDashboardQuerySchema` | Zod | Shared schema (existing) |
| `AdminDashboardStats` | Type | `src/types/dashboard.ts` |
| `AdminDashboardDetailData` | Type | `src/types/dashboard.ts` |

### 6.2 External Dependencies

| Dependency | Version | Purpose |
|-----------|---------|---------|
| `zod` | ^3.x | Schema validation |
| `@payloadcms/db-mongodb` | ^3.49.1 | MongoDB adapter |

### 6.3 MongoDB Collections Used

| Collection | Access Pattern | Indexes Required |
|-----------|---------------|-----------------|
| `orders` | Aggregation pipeline | `status`, `status.deliveredAt`, `status.confirmedAt`, `status.hold`, `customer` |
| `customers` | Aggregation pipeline | `createdAt` |
| `withdrawRequests` | Aggregation pipeline | `status`, `createdAt` |
| `orderItems` (virtual) | Joined from orders | via `orders.items.product` |

---

## 7. Open Questions

| # | Question | Decision Needed | Priority |
|---|---------|----------------|---------|
| 1 | Top products: lấy từ `orderItems` hay precomputed field? | Dùng `orderItems` joined từ orders aggregation | HIGH |
| 2 | Revenue chart: có include cancelled orders trong orders count không? | Không — chỉ `confirmed` orders | MEDIUM |
| 3 | AOV tính trên confirmed orders hay all orders? | Chỉ confirmed orders | MEDIUM |
| 4 | New customers: unique by `customer` field hay email? | Unique by `customer` ObjectId | LOW |
| 5 | Withdraw service: stats riêng hay gộp vào stats endpoint? | Stats riêng — unused by frontend (v4 scope) | LOW |
| 6 | Cache key: include user role hay chỉ date range? | Chỉ date range (stats giống nhau cho mọi role) | LOW |
| 7 | Response language: tiếng Việt cho message hay tiếng Anh? | Tiếng Việt cho message, tiếng Anh cho code | MEDIUM |
