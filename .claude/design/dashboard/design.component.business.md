# Design — Business Logic

> **Status**: Approved
> **Version**: 1.0.0
> **Last Updated**: 2026-03-21

---

## 1. Revenue Logic

### 1.1 Revenue Definition

**Chỉ tính orders có `status === 'confirmed'`**.

- `confirmed` = đã giao hàng thành công, không còn dispute, tiền đã vào wallet chủ shop
- **Không dùng** `delivered + completed` như store-dashboard vì không chính xác với dispute flow

### 1.2 Revenue = Item-Level Sum

Revenue được tính ở **item-level** không phải order-level:

```
orderRevenue = SUM(item.finalPrice × item.quantity) cho tất cả item trong order
```

**Ví dụ**:
```
Order #123 có 3 items:
- Hoa Hồng Đỏ: finalPrice=50000, quantity=3  → 150000
- Hoa Lan Trắng: finalPrice=120000, quantity=1 → 120000
- Lá Xanh: finalPrice=35000, quantity=2       → 70000
─────────────────────────────────────────────────────
Order #123 Revenue = 340000 VND
```

**Lý do item-level**:
- Partial refunds hoạt động ở item-level → revenue phản ánh đúng số thực nhận
- Nếu 1 trong 3 items bị refund → order-level sum sai, item-level đúng

### 1.3 Revenue Date Anchor

Dùng `status.confirmedAt` làm thời điểm ghi nhận revenue:

```typescript
const confirmedMatch = {
  status: 'confirmed',
  'status.confirmedAt': {
    $gte: fromDate,
    $lte: toDate
  }
}
```

**Không dùng** `createdAt` vì order có thể tạo tháng trước nhưng confirmed tháng này.

### 1.4 Hold = Excluded

Orders có `status.hold === true` bị **exclude hoàn toàn** khỏi revenue:

```typescript
const confirmedMatch = {
  status: 'confirmed',
  'status.hold': { $ne: true },  // Bắt buộc — hold orders không tính revenue
  'status.confirmedAt': { $gte: fromDate, $lte: toDate }
}
```

---

## 2. Comparison Logic

### 2.1 Immediately Preceding Period

Comparison luôn so sánh với **kỳ ngay trước có cùng span length**:

```
currentFrom = 2026-03-01, currentTo = 2026-03-21 → spanDays = 20
prevTo      = currentFrom - 1ms = 2026-02-28 23:59:59.999
prevFrom    = prevTo - (spanDays - 1) = 2026-02-09
```

### 2.2 Calculation Formula

```typescript
// Tính span trước
const spanMs = currentTo.getTime() - currentFrom.getTime()
const spanDays = Math.ceil(spanMs / (1000 * 60 * 60 * 24))

// Previous period dates
const prevTo = new Date(currentFrom.getTime() - 1)
const prevFrom = new Date(prevTo.getTime() - (spanDays - 1) * 86400000)
```

### 2.3 Change Percent Formula

```typescript
const changePercent = ((currentValue - previousValue) / previousValue) * 100
```

**Edge cases**:
| Scenario | changePercent | trend |
|----------|-------------|-------|
| prev=0, current>0 | `null` | `up` |
| prev=0, current=0 | `0` | `neutral` |
| prev>0, current=0 | `-100` | `down` |
| prev=100, current=120 | `20` | `up` |
| prev=100, current=80 | `-20` | `down` |

### 2.4 Trend Direction

Trend phụ thuộc vào **context của KPI**:

```typescript
// Positive is good
const HIGHER_IS_BETTER = ['revenue', 'totalOrders', 'newCustomers', 'aov', 'completionRate']

// Positive is bad
const LOWER_IS_BETTER = ['pendingOrders']
```

```typescript
const trend = (changePercent: number, higherIsBetter: boolean): 'up' | 'down' | 'neutral' => {
  if (changePercent > 0) return higherIsBetter ? 'up' : 'down'
  if (changePercent < 0) return higherIsBetter ? 'down' : 'up'
  return 'neutral'
}
```

### 2.5 Example Comparison

```
Current period (2026-03-01 → 2026-03-21, 20 days):
- revenue = 125.000.000 VND

Previous period (2026-02-09 → 2026-02-28, 20 days):
- revenue = 98.000.000 VND

Change = ((125 - 98) / 98) * 100 = +27.55%
Trend = up (higher is better for revenue)
```

---

## 3. 6 KPIs Tier 1 Fixed List

### 3.1 KPI Definitions

| KPI | Definition | Unit | Higher is Better? | Alert |
|-----|-----------|------|-----------------|-------|
| `revenue` | SUM(item.finalPrice × quantity) cho confirmed orders | VND | ✅ Yes | ❌ No |
| `totalOrders` | Tổng confirmed orders trong period | count | ✅ Yes | ❌ No |
| `newCustomers` | Unique customers có order confirmed lần đầu | count | ✅ Yes | ❌ No |
| `aov` | revenue / totalOrders (confirmed) | VND | ✅ Yes | ❌ No |
| `pendingOrders` | Orders có status='pending' và không hold | count | ❌ No | ✅ Yes |
| `completionRate` | confirmed / (total - cancelled) × 100 | % | ✅ Yes | ❌ No |

### 3.2 KPI Formulas

```typescript
// Revenue
const revenue = confirmedOrders.reduce((sum, order) => {
  return sum + order.items.reduce((itemSum, item) =>
    itemSum + (item.finalPrice * item.quantity), 0)
}, 0)

// Total Orders (confirmed)
const totalOrders = confirmedOrders.length

// New Customers
const newCustomers = new Set(confirmedOrders.map(o => o.customerId)).size

// AOV
const aov = totalOrders > 0 ? Math.round(revenue / totalOrders) : 0

// Pending Orders
const pendingOrders = pending.filter(o => o.status.hold !== true).length

// Completion Rate
const totalNonCancelled = totalOrders + cancelled
const completionRate = totalNonCancelled > 0
  ? Math.round((confirmed / totalNonCancelled) * 10000) / 100
  : 0
```

### 3.3 KPI Response Structure

```typescript
interface KpiData {
  revenue: {
    value: number
    currency: 'VND'
    comparison: ComparisonData
  }
  totalOrders: {
    value: number
    comparison: ComparisonData
  }
  newCustomers: {
    value: number
    comparison: ComparisonData
  }
  aov: {
    value: number
    currency: 'VND'
    comparison: ComparisonData
  }
  pendingOrders: {
    value: number
    comparison: ComparisonData
    alert: 'high' | 'medium' | null
  }
  completionRate: {
    value: number
    unit: '%'
    comparison: ComparisonData
  }
}
```

---

## 4. Alert Thresholds

### 4.1 Pending Orders Alerts

Pending orders = orders đang chờ xử lý (chưa confirmed). Alert khi có quá nhiều đơn chờ → có thể ảnh hưởng trải nghiệm khách hàng.

| Threshold | Level | Label | Màu |
|-----------|-------|-------|-----|
| `> 50` | `high` | `${value} đơn chờ` | Red `#ef4444` |
| `> 0` | `medium` | `${value} đơn chờ` | Amber `#f59e0b` |
| `= 0` | `null` | — | Hidden |

```typescript
const getPendingAlertLevel = (pending: number): 'high' | 'medium' | null => {
  if (pending > 50) return 'high'
  if (pending > 0) return 'medium'
  return null
}
```

### 4.2 Alert Display Rules

```typescript
// Chỉ hiển thị alert khi level !== null
{pendingAlert && (
  <AlertBadge level={pendingAlert} label={`${pending} đơn chờ`} />
)}
```

### 4.3 Alert in Stats Response

```typescript
// Trong route.ts — thêm alert vào pendingOrders KPI
const pendingAlert = getPendingAlertLevel(stats.pendingOrders)

return res.json({
  data: {
    kpis: {
      pendingOrders: {
        value: stats.pendingOrders,
        comparison: pendingComparison,
        alert: pendingAlert  // Chỉ set khi !== null
      }
    }
  }
})
```

---

## 5. Hold Mechanism

### 5.1 Hold Definition

**Hold** = Order đang trong trạng thái dispute/chờ resolution. Tiền chưa được transfer vào wallet chủ shop.

### 5.2 Hold Duration

- **24 giờ**: Thời gian tối đa order có thể ở trạng thái hold
- Sau 24h không resolved → hệ thống tự động unhold hoặc escalate lên admin

### 5.3 Hold Status Structure

```typescript
interface OrderStatus {
  pending: boolean
  processing: boolean
  shipped: boolean
  delivered: boolean
  confirmed: boolean
  cancelled: boolean
  hold: boolean              // TRUE = đang dispute
  holdAt?: Date              // Thời điểm bắt đầu hold
  holdReason?: string         // Lý do hold (dispute reason)
  confirmedAt?: Date          // Thời điểm confirmed
  deliveredAt?: Date          // Thời điểm delivered
}
```

### 5.4 Hold Exclusion Rules

| Context | Hold Behavior |
|---------|-------------|
| Revenue stats | Hold orders bị exclude hoàn toàn |
| Pending orders count | Hold orders không được count là pending |
| Chart data | Hold orders không xuất hiện |
| Total orders count | Hold orders không được count |

### 5.5 Hold Filter in Aggregations

```typescript
// Tất cả aggregation pipelines phải include filter này
const HOLD_FILTER = { 'status.hold': { $ne: true } }

// Trong $match stage
{
  $match: {
    status: 'confirmed',
    'status.hold': { $ne: true },
    'status.confirmedAt': { $gte: from, $lte: to }
  }
}
```

---

## 6. Completion Rate Formula

### 6.1 Definition

Tỷ lệ phần trăm orders được confirmed (thành công) trên tổng orders không bị cancelled.

### 6.2 Formula

```
completionRate = (confirmedOrders / nonCancelledOrders) × 100

nonCancelledOrders = totalOrders - cancelledOrders
```

### 6.3 Examples

```
Ví dụ 1:
- total = 400
- cancelled = 50
- confirmed = 306
- nonCancelled = 400 - 50 = 350
- completionRate = (306 / 350) × 100 = 87.43%

Ví dụ 2 (edge case — không có cancelled):
- total = 300
- cancelled = 0
- confirmed = 250
- completionRate = (250 / 300) × 100 = 83.33%

Ví dụ 3 (edge case — không có confirmed):
- total = 100
- cancelled = 20
- confirmed = 0
- completionRate = (0 / 80) × 100 = 0%

Ví dụ 4 (edge case — 100% completion):
- total = 300
- cancelled = 0
- confirmed = 300
- completionRate = (300 / 300) × 100 = 100%
```

### 6.4 Implementation

```typescript
const completionRate = (confirmed: number, cancelled: number, total: number): number => {
  const nonCancelled = total - cancelled

  if (nonCancelled === 0) return 0

  const rate = (confirmed / nonCancelled) * 100

  // Round to 2 decimal places
  return Math.round(rate * 100) / 100
}
```

---

## 7. Empty State Handling

### 7.1 Summary Table

- Date range không có orders → return empty arrays/zero values
- Date range trong tương lai → return empty arrays
- Database errors → return error response (không phải empty state)

### 7.2 Empty KPI Response

```typescript
// Khi không có data
const emptyStats: AggregateOrdersOutput = {
  totalOrders: 0,
  confirmedOrders: 0,
  pendingOrders: 0,
  cancelledOrders: 0,
  completionRate: 0,
  newCustomers: 0
}

const emptyRevenue: AggregateRevenueOutput = {
  totalRevenue: 0,
  totalOrders: 0,
  aov: 0
}
```

### 7.3 Empty Chart Response

```typescript
// KHÔNG generate fake 12 zero months
// Return empty array thay vì filled zeros

const emptyChart: RevenueChartOutput = {
  granularity: 'day',
  data: [],     // ✅ Empty array — no fake data
  summary: {
    totalRevenue: 0,
    totalOrders: 0
  }
}
```

### 7.4 Empty Top Products Response

```typescript
const emptyTopProducts: TopProductsOutput = {
  limit: 10,
  data: []
}
```

### 7.5 Frontend Empty States

```tsx
// Chart empty state
{chartData.length === 0 ? (
  <EmptyState
    title="Không có dữ liệu"
    description="Không có doanh thu trong khoảng thời gian này"
  />
) : (
  <RevenueChart data={chartData} />
)}

// Top products empty state
{topProducts.length === 0 ? (
  <EmptyState
    title="Chưa có sản phẩm"
    description="Chưa có sản phẩm nào được bán trong khoảng thời gian này"
  />
) : (
  <ProductList products={topProducts} />
)}
```

### 7.6 Zero vs Empty

| Metric | Zero Value | Empty Representation |
|--------|-----------|---------------------|
| Revenue | `0` | `0 VND` |
| Orders | `0` | `0 đơn` |
| Chart data | `[]` | Empty array |
| Top products | `[]` | Empty array |

### 7.7 Business Rules Summary Table

| Rule | Decision | Rationale |
|------|----------|----------|
| Revenue status | `confirmed` only | Tiền đã vào wallet, không dispute |
| Revenue calculation | Item-level SUM | Accurate với partial refunds |
| Revenue date anchor | `status.confirmedAt` | Đúng thời điểm ghi nhận |
| Hold orders | Excluded from all stats | Tiền chưa vào wallet |
| Comparison period | Immediately preceding | Same span, previous dates |
| 6 KPIs fixed | revenue/orders/customers/aov/pending/completion | Core business metrics |
| Completion rate formula | confirmed / nonCancelled × 100 | Loại trừ cancelled |
| Empty chart | Return `[]`, no fake data | Accurate reporting |
| Alert: pending > 50 | `high` | Too many pending orders |
| Alert: pending > 0 | `medium` | Some pending orders |
