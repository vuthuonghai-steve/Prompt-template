# Design — Service Layer

> **Status**: Approved
> **Version**: 1.0.0
> **Last Updated**: 2026-03-21

---

## 1. aggregate-orders.service

### 1.1 Purpose

Lấy order statistics và new customers count trong một aggregation pipeline duy nhất.

### 1.2 Signature

```typescript
// services/stats/aggregate-orders.service.ts

interface AggregateOrdersInput {
  from: Date
  to: Date
}

interface AggregateOrdersOutput {
  totalOrders: number
  confirmedOrders: number
  pendingOrders: number
  cancelledOrders: number
  completionRate: number      // 0-100
  newCustomers: number
}

async function aggregateOrdersService(
  payload: Payload,
  input: AggregateOrdersInput
): Promise<AggregateOrdersOutput>
```

### 1.3 Implementation

```typescript
export async function aggregateOrdersService(
  payload: Payload,
  { from, to }: AggregateOrdersInput
): Promise<AggregateOrdersOutput> {
  // Query param — lọc orders không bị hold
  const baseMatch = {
    'status.hold': { $ne: true },
    'status.confirmedAt': { $gte: from, $lte: to }
  }

  const result = await payload.db.collection('orders').aggregate([
    // Stage 1: Match non-cancelled, non-hold orders trong date range
    {
      $match: {
        ...baseMatch,
        status: { $nin: ['cancelled'] }
      }
    },

    // Stage 2: Facet — chạy song song 2 pipelines
    {
      $facet: {
        // Branch 1: Order counts by status
        orderCounts: [
          {
            $group: {
              _id: '$status',
              count: { $sum: 1 }
            }
          },
          {
            $group: {
              _id: null,
              statuses: {
                $push: { status: '$_id', count: '$count' }
              },
              total: { $sum: '$count' }
            }
          }
        ],

        // Branch 2: Unique customers count
        uniqueCustomers: [
          {
            $group: {
              _id: '$customer'
            }
          },
          {
            $count: 'count'
          }
        ]
      }
    }
  ]).toArray()

  // Parse kết quả
  const facetResult = result[0] ?? { orderCounts: [{}], uniqueCustomers: [] }
  const counts = facetResult.orderCounts[0] ?? {}
  const statuses: Record<string, number> = {}

  // Map statuses array to object
  if (Array.isArray(counts.statuses)) {
    for (const item of counts.statuses) {
      statuses[item.status] = item.count
    }
  }

  const total = counts.total ?? 0
  const confirmed = statuses['confirmed'] ?? 0
  const pending = statuses['pending'] ?? 0
  const cancelled = statuses['cancelled'] ?? 0
  const nonCancelled = total - cancelled

  // New customers từ facet branch 2
  const newCustomers = facetResult.uniqueCustomers[0]?.count ?? 0

  // Completion rate
  const completionRate = nonCancelled > 0
    ? Math.round((confirmed / nonCancelled) * 10000) / 100
    : 0

  return {
    totalOrders: total,
    confirmedOrders: confirmed,
    pendingOrders: pending,
    cancelledOrders: cancelled,
    completionRate,
    newCustomers
  }
}
```

---

## 2. aggregate-revenue.service

### 2.1 Purpose

Tính tổng revenue từ confirmed orders ở item-level. Revenue = SUM(item.finalPrice * item.quantity).

### 2.2 Signature

```typescript
// services/stats/aggregate-revenue.service.ts

interface AggregateRevenueInput {
  from: Date
  to: Date
}

interface AggregateRevenueOutput {
  totalRevenue: number         // Integer VND
  totalOrders: number
  aov: number                  // Average Order Value
}

async function aggregateRevenueService(
  payload: Payload,
  input: AggregateRevenueInput
): Promise<AggregateRevenueOutput>
```

### 2.3 Implementation

```typescript
export async function aggregateRevenueService(
  payload: Payload,
  { from, to }: AggregateRevenueInput
): Promise<AggregateRevenueOutput> {
  // Match confirmed orders không bị hold
  const result = await payload.db.collection('orders').aggregate([
    {
      $match: {
        status: 'confirmed',
        'status.hold': { $ne: true },
        'status.confirmedAt': { $gte: from, $lte: to }
      }
    },

    // Unwind items array
    {
      $unwind: {
        path: '$items',
        preserveNullAndEmptyArrays: false
      }
    },

    // Tính item revenue
    {
      $addFields: {
        itemRevenue: {
          $multiply: [
            { $ifNull: ['$items.finalPrice', 0] },
            { $ifNull: ['$items.quantity', 0] }
          ]
        }
      }
    },

    // Group theo order để đếm orders + sum revenue
    {
      $group: {
        _id: '$_id',
        orderRevenue: { $sum: '$itemRevenue' }
      }
    },

    // Tổng hợp
    {
      $group: {
        _id: null,
        totalRevenue: { $sum: '$orderRevenue' },
        orderCount: { $sum: 1 }
      }
    },

    // Tính AOV
    {
      $addFields: {
        aov: {
          $cond: {
            if: { $gt: ['$orderCount', 0] },
            then: {
              $round: [
                { $divide: ['$totalRevenue', '$orderCount'] },
                0
              ]
            },
            else: 0
          }
        }
      }
    },

    // Format output
    {
      $project: {
        _id: 0,
        totalRevenue: 1,
        totalOrders: '$orderCount',
        aov: 1
      }
    }
  ]).toArray()

  if (!result.length) {
    return { totalRevenue: 0, totalOrders: 0, aov: 0 }
  }

  return result[0]
}
```

---

## 3. aggregate-withdraw.service

### 3.1 Purpose

Lấy withdraw request statistics: pending count, total amounts theo status.

### 3.2 Signature

```typescript
// services/stats/aggregate-withdraw.service.ts

interface AggregateWithdrawInput {
  from: Date
  to: Date
}

interface AggregateWithdrawOutput {
  pendingCount: number
  approvedCount: number
  rejectedCount: number
  totalPendingAmount: number
  totalApprovedAmount: number
  totalRejectedAmount: number
}

async function aggregateWithdrawService(
  payload: Payload,
  input: AggregateWithdrawInput
): Promise<AggregateWithdrawOutput>
```

### 3.3 Implementation

```typescript
export async function aggregateWithdrawService(
  payload: Payload,
  { from, to }: AggregateWithdrawInput
): Promise<AggregateWithdrawOutput> {
  const result = await payload.db.collection('withdrawRequests').aggregate([
    {
      $match: {
        createdAt: { $gte: from, $lte: to }
      }
    },

    {
      $group: {
        _id: '$status',
        count: { $sum: 1 },
        totalAmount: { $sum: '$amount' }
      }
    },

    {
      $group: {
        _id: null,
        statuses: {
          $push: {
            status: '$_id',
            count: '$count',
            totalAmount: '$totalAmount'
          }
        }
      }
    }
  ]).toArray()

  const defaultOutput = {
    pendingCount: 0,
    approvedCount: 0,
    rejectedCount: 0,
    totalPendingAmount: 0,
    totalApprovedAmount: 0,
    totalRejectedAmount: 0
  }

  if (!result.length || !result[0].statuses) {
    return defaultOutput
  }

  const output = { ...defaultOutput }

  for (const item of result[0].statuses) {
    switch (item.status) {
      case 'pending':
        output.pendingCount = item.count
        output.totalPendingAmount = item.totalAmount
        break
      case 'approved':
        output.approvedCount = item.count
        output.totalApprovedAmount = item.totalAmount
        break
      case 'rejected':
        output.rejectedCount = item.count
        output.totalRejectedAmount = item.totalAmount
        break
    }
  }

  return output
}
```

---

## 4. revenue-chart.service

### 4.1 Purpose

Lấy revenue data theo ngày/tuần/tháng dựa trên granularity.

### 4.2 Signature

```typescript
// services/detail/revenue-chart.service.ts

interface RevenueChartInput {
  from: Date
  to: Date
  granularity: 'day' | 'week' | 'month'
}

interface RevenueChartOutput {
  granularity: 'day' | 'week' | 'month'
  data: Array<{
    date: string
    revenue: number
    orders: number
  }>
  summary: {
    totalRevenue: number
    totalOrders: number
  }
}

async function revenueChartService(
  payload: Payload,
  input: RevenueChartInput
): Promise<RevenueChartOutput>
```

### 4.3 Granularity Date Format

```typescript
const GRANULARITY_FORMAT: Record<string, string> = {
  day:   '%Y-%m-%d',     // 2026-03-21
  week:  '%Y-W%V',       // 2026-W12
  month: '%Y-%m'         // 2026-03
}

const getDateGrouping = (granularity: string) => ({
  date: {
    $dateToString: {
      format: GRANULARITY_FORMAT[granularity] ?? '%Y-%m-%d',
      date: '$status.confirmedAt'
    }
  }
})
```

### 4.4 Implementation

```typescript
export async function revenueChartService(
  payload: Payload,
  { from, to, granularity }: RevenueChartInput
): Promise<RevenueChartOutput> {
  // Auto-adjust granularity nếu span quá nhỏ
  const spanDays = Math.ceil((to.getTime() - from.getTime()) / (1000 * 60 * 60 * 24))
  const adjustedGranularity = spanDays < 7 ? 'day' : granularity

  const result = await payload.db.collection('orders').aggregate([
    {
      $match: {
        status: 'confirmed',
        'status.hold': { $ne: true },
        'status.confirmedAt': { $gte: from, $lte: to }
      }
    },

    // Unwind items
    {
      $unwind: {
        path: '$items',
        preserveNullAndEmptyArrays: false
      }
    },

    // Tính item revenue
    {
      $addFields: {
        itemRevenue: {
          $multiply: [
            { $ifNull: ['$items.finalPrice', 0] },
            { $ifNull: ['$items.quantity', 0] }
          ]
        }
      }
    },

    // Group by date (granularity)
    {
      $group: {
        _id: getDateGrouping(adjustedGranularity),
        revenue: { $sum: '$itemRevenue' },
        orders: { $sum: 1 }
      }
    },

    // Sort by date ascending
    {
      $sort: { '_id.date': 1 }
    },

    // Project final shape
    {
      $project: {
        _id: 0,
        date: '$_id.date',
        revenue: 1,
        orders: 1
      }
    }
  ]).toArray()

  // Summary totals
  const summary = result.reduce(
    (acc, item) => ({
      totalRevenue: acc.totalRevenue + item.revenue,
      totalOrders: acc.totalOrders + item.orders
    }),
    { totalRevenue: 0, totalOrders: 0 }
  )

  return {
    granularity: adjustedGranularity,
    data: result,
    summary
  }
}
```

---

## 5. top-products.service

### 5.1 Purpose

Lấy top N selling products trong date range.

### 5.2 Signature

```typescript
// services/detail/top-products.service.ts

interface TopProductsInput {
  from: Date
  to: Date
  limit: number          // max 50
}

interface TopProductItem {
  productId: string
  name: string
  thumbnail: string | null
  totalSold: number
  totalRevenue: number
}

interface TopProductsOutput {
  limit: number
  data: TopProductItem[]
}

async function topProductsService(
  payload: Payload,
  input: TopProductsInput
): Promise<TopProductsOutput>
```

### 5.3 Implementation

```typescript
export async function topProductsService(
  payload: Payload,
  { from, to, limit }: TopProductsInput
): Promise<TopProductsOutput> {
  const safeLimit = Math.min(Math.max(1, limit), 50)

  const result = await payload.db.collection('orders').aggregate([
    // Match confirmed orders
    {
      $match: {
        status: 'confirmed',
        'status.hold': { $ne: true },
        'status.confirmedAt': { $gte: from, $lte: to }
      }
    },

    // Unwind items
    {
      $unwind: {
        path: '$items',
        preserveNullAndEmptyArrays: false
      }
    },

    // Group by product
    {
      $group: {
        _id: '$items.product',
        name: { $first: '$items.name' },
        thumbnail: { $first: '$items.thumbnail' },
        totalSold: { $sum: '$items.quantity' },
        totalRevenue: {
          $sum: {
            $multiply: [
              { $ifNull: ['$items.finalPrice', 0] },
              { $ifNull: ['$items.quantity', 0] }
            ]
          }
        }
      }
    },

    // Sort by totalSold descending
    {
      $sort: { totalSold: -1 }
    },

    // Limit
    {
      $limit: safeLimit
    },

    // Project final shape
    {
      $project: {
        _id: 0,
        productId: { $toString: '$_id' },
        name: 1,
        thumbnail: { $ifNull: ['$thumbnail', null] },
        totalSold: 1,
        totalRevenue: 1
      }
    }
  ]).toArray()

  return {
    limit: safeLimit,
    data: result
  }
}
```

---

## 6. date-range-parser (Shared Utility)

### 6.1 Purpose

Parse preset ID hoặc custom from/to dates thành Date objects + metadata.

### 6.2 Signature

```typescript
// lib/date-range-parser.ts

interface DateRangeResult {
  from: Date
  to: Date
  spanDays: number
  preset: string | null
}

function parseDateRange(
  preset: string | null,
  from: string | null,
  to: string | null
): DateRangeResult
```

### 6.3 Implementation

```typescript
// lib/date-range-parser.ts

type PresetId = string

const PRESET_PRESETS: Record<PresetId, () => { from: Date; to: Date }> = {
  today: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    return { from: todayStart, to: now }
  },

  yesterday: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const yesterdayStart = new Date(todayStart.getTime() - 24 * 60 * 60 * 1000)
    return {
      from: yesterdayStart,
      to: new Date(todayStart.getTime() - 1)
    }
  },

  last_7_days: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const from = new Date(todayStart.getTime() - 6 * 24 * 60 * 60 * 1000)
    return { from, to: now }
  },

  last_14_days: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const from = new Date(todayStart.getTime() - 13 * 24 * 60 * 60 * 1000)
    return { from, to: now }
  },

  last_28_days: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const from = new Date(todayStart.getTime() - 27 * 24 * 60 * 60 * 1000)
    return { from, to: now }
  },

  last_30_days: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const from = new Date(todayStart.getTime() - 29 * 24 * 60 * 60 * 1000)
    return { from, to: now }
  },

  last_60_days: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const from = new Date(todayStart.getTime() - 59 * 24 * 60 * 60 * 1000)
    return { from, to: now }
  },

  last_90_days: () => {
    const now = new Date()
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const from = new Date(todayStart.getTime() - 89 * 24 * 60 * 60 * 1000)
    return { from, to: now }
  },

  this_week: () => {
    const now = new Date()
    const dayOfWeek = now.getDay()
    const monday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - ((dayOfWeek + 6) % 7))
    return { from: monday, to: now }
  },

  this_month: () => {
    const now = new Date()
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
    return { from: monthStart, to: now }
  },

  last_week: () => {
    const now = new Date()
    const dayOfWeek = now.getDay()
    const thisMonday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - ((dayOfWeek + 6) % 7))
    const lastMonday = new Date(thisMonday.getTime() - 7 * 24 * 60 * 60 * 1000)
    const lastSunday = new Date(thisMonday.getTime() - 1)
    return { from: lastMonday, to: lastSunday }
  },

  last_month: () => {
    const now = new Date()
    const thisMonthStart = new Date(now.getFullYear(), now.getMonth(), 1)
    const lastMonthEnd = new Date(thisMonthStart.getTime() - 1)
    const lastMonthStart = new Date(now.getFullYear(), now.getMonth() - 1, 1)
    return { from: lastMonthStart, to: lastMonthEnd }
  },

  this_quarter: () => {
    const now = new Date()
    const quarter = Math.floor(now.getMonth() / 3)
    const quarterStart = new Date(now.getFullYear(), quarter * 3, 1)
    return { from: quarterStart, to: now }
  },

  this_year: () => {
    const now = new Date()
    const yearStart = new Date(now.getFullYear(), 0, 1)
    return { from: yearStart, to: now }
  }
}

export function parseDateRange(
  preset: string | null,
  from: string | null,
  to: string | null
): DateRangeResult {
  // Priority: preset > custom dates
  if (preset && PRESET_PRESETS[preset]) {
    const { from: parsedFrom, to: parsedTo } = PRESET_PRESETS[preset]()
    const spanDays = Math.ceil((parsedTo.getTime() - parsedFrom.getTime()) / (1000 * 60 * 60 * 24))
    return { from: parsedFrom, to: parsedTo, spanDays, preset }
  }

  // Custom date range
  if (from && to) {
    // Dùng constructor 3 args để tránh UTC shift
    const fromParts = from.split('-').map(Number)
    const toParts = to.split('-').map(Number)

    const parsedFrom = new Date(fromParts[0], fromParts[1] - 1, fromParts[2])
    const parsedTo = new Date(toParts[0], toParts[1] - 1, toParts[2])

    // Clamp to to today
    const now = new Date()
    const clampedTo = parsedTo > now ? now : parsedTo

    const spanDays = Math.ceil((clampedTo.getTime() - parsedFrom.getTime()) / (1000 * 60 * 60 * 24))

    return { from: parsedFrom, to: clampedTo, spanDays, preset: null }
  }

  // Default: last_30_days
  return parseDateRange('last_30_days', null, null)
}
```

---

## 7. comparison-calculator (Shared Utility)

### 7.1 Barrel Exports

```typescript
// lib/index.ts
export { parseDateRange } from './date-range-parser'
export { calculateComparison, calculatePreviousPeriod } from './comparison-calculator'
export { ORDER_STATUSES, HOLD_EXCLUSION } from './order-status'

// services/stats/services/index.ts
export { aggregateOrdersService } from './aggregate-orders.service'
export { aggregateRevenueService } from './aggregate-revenue.service'
export { aggregateWithdrawService } from './aggregate-withdraw.service'

// services/detail/services/index.ts
export { revenueChartService } from './revenue-chart.service'
export { topProductsService } from './top-products.service'
```

### 7.2 Purpose

Tính comparison metrics: previous period values, change percent, trend direction.

### 7.3 Implementation

```typescript
// lib/comparison-calculator.ts

interface ComparisonResult {
  value: number
  changePercent: number | null
  trend: 'up' | 'down' | 'neutral'
}

interface ComparisonConfig {
  currentValue: number
  previousValue: number
  // true = positive change is good (revenue, orders)
  // false = positive change is bad (pending orders)
  higherIsBetter: boolean
}

function calculateComparison(config: ComparisonConfig): ComparisonResult

function calculatePreviousPeriod(
  currentFrom: Date,
  currentTo: Date
): { prevFrom: Date; prevTo: Date }
```

### 7.3 Implementation

```typescript
// lib/comparison-calculator.ts

export function calculateComparison(config: ComparisonConfig): ComparisonResult {
  const { currentValue, previousValue, higherIsBetter } = config

  // Handle edge cases
  if (previousValue === 0 && currentValue === 0) {
    return { value: 0, changePercent: 0, trend: 'neutral' }
  }

  if (previousValue === 0 && currentValue > 0) {
    return { value: currentValue, changePercent: null, trend: 'up' }
  }

  if (previousValue === 0 && currentValue < 0) {
    return { value: currentValue, changePercent: null, trend: 'down' }
  }

  // Tính % change
  const changePercent = Math.round(
    ((currentValue - previousValue) / previousValue) * 10000
  ) / 100

  // Determine trend
  let trend: 'up' | 'down' | 'neutral' = 'neutral'
  if (changePercent > 0) {
    trend = higherIsBetter ? 'up' : 'down'
  } else if (changePercent < 0) {
    trend = higherIsBetter ? 'down' : 'up'
  }

  return { value: currentValue, changePercent, trend }
}

export function calculatePreviousPeriod(
  currentFrom: Date,
  currentTo: Date
): { prevFrom: Date; prevTo: Date } {
  const spanMs = currentTo.getTime() - currentFrom.getTime()
  const spanDays = Math.ceil(spanMs / (1000 * 60 * 60 * 24))

  // prevTo = currentFrom - 1ms
  const prevTo = new Date(currentFrom.getTime() - 1)

  // prevFrom = prevTo - spanDays + 1
  const prevFrom = new Date(prevTo.getTime() - (spanDays - 1) * 24 * 60 * 60 * 1000)

  return { prevFrom, prevTo }
}
```

### 7.4 Usage in Services

```typescript
// Trong route.ts — sau khi có current period results
import { calculateComparison, calculatePreviousPeriod } from '../lib/comparison-calculator'

// Chạy aggregations cho previous period
const { prevFrom, prevTo } = calculatePreviousPeriod(from, to)

const prevStats = await aggregateOrdersService(payload, { from: prevFrom, to: prevTo })

// Tính comparison cho mỗi KPI
const revenueComparison = calculateComparison({
  currentValue: revenueData.totalRevenue,
  previousValue: prevRevenueData?.totalRevenue ?? 0,
  higherIsBetter: true
})
```

---
