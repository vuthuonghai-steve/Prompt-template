# Design — Database (MongoDB Aggregation Pipelines)

> **Status**: Approved
> **Version**: 1.0.0
> **Last Updated**: 2026-03-21

---

## 1. Overview

Dashboard sử dụng MongoDB aggregation pipelines thay vì nhiều `payload.count()` queries. Mỗi service gọi một hoặc nhiều aggregation pipelines để lấy dữ liệu từ các collections: `orders`, `customers`, `withdrawRequests`.

**Database**: MongoDB via PayloadCMS `@payloadcms/db-mongodb` adapter.

**Connection**: PayloadCMS internal — dùng `payload.db` adapter methods.

---

## 2. Design Decisions

### 2.1 Aggregation Strategy

**Single-pass aggregation**: Mỗi service cố gắng lấy tất cả metrics cần thiết trong một pipeline duy nhất để giảm round-trips.

**Fallback**: Nếu metrics quá khác nhau → tách thành 2 pipelines nhưng vẫn trong một service.

### 2.2 Order Status Filter

**Confirmed orders** (revenue): `status === 'confirmed'`

- Đây là trạng thái order đã giao thành công, không còn dispute
- Tiền đã được transfer vào wallet chủ shop

**All orders** (stats): `status` IN `['pending', 'processing', 'shipped', 'delivered', 'confirmed', 'cancelled']`

**Hold exclusion**: `{ 'status.hold': { $ne: true } }` trong TẤT CẢ pipelines

### 2.3 Revenue Calculation

Revenue được tính ở **item-level** (không phải order-level):

```
order.revenue = SUM(item.finalPrice * item.quantity) cho mỗi item trong confirmed order
```

**Lý do**: Orders có thể bị partial refund → item-level đảm bảo accurate hơn.

### 2.4 Date Field for Revenue

Dùng `status.confirmedAt` làm date anchor cho revenue (thời điểm tiền được xác nhận).

---

## 3. MongoDB Aggregation Pipelines

### 3.1 AggregateOrdersService Pipeline

```typescript
// services/stats/aggregate-orders.service.ts

// Pipeline: Lấy orders stats + new customers trong một $facet
const ordersAggregation = [
  // Stage 1: Date filter
  {
    $match: {
      status: { $nin: ['cancelled'] },
      'status.hold': { $ne: true },
      'status.confirmedAt': {
        $gte: fromDate,
        $lte: toDate
      }
    }
  },

  // Stage 2: Facet — multiple pipelines in one
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

        // Format result
        {
          $group: {
            _id: null,
            statuses: {
              $push: {
                status: '$_id',
                count: '$count'
              }
            },
            total: { $sum: '$count' }
          }
        },

        // Map to named fields
        {
          $project: {
            _id: 0,
            total: 1,
            pending: {
              $ifNull: [
                { $arrayElemAt: [{ $map: { input: '$statuses', as: 's', in: { $cond: [{ $eq: ['$$s.status', 'pending'] }, '$$s.count', null] } } }, 0] }, 0
              ]
            },
            confirmed: {
              $ifNull: [
                { $arrayElemAt: [{ $map: { input: '$statuses', as: 's', in: { $cond: [{ $eq: ['$$s.status', 'confirmed'] }, '$$s.count', null] } } }, 0] }, 0
              ]
            },
            // ... other statuses
          }
        }
      ],

      // Branch 2: New customers
      newCustomers: [
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
]

// Execute
const result = await payload.db.collection('orders').aggregate(ordersAggregation).toArray()
```

### 3.2 AggregateRevenueService Pipeline

```typescript
// services/stats/aggregate-revenue.service.ts

// Pipeline: Item-level revenue + commission
const revenueAggregation = [
  // Stage 1: Match confirmed orders in date range
  {
    $match: {
      status: 'confirmed',
      'status.hold': { $ne: true },
      'status.confirmedAt': {
        $gte: fromDate,
        $lte: toDate
      }
    }
  },

  // Stage 2: Unwind items (flatten order.items array)
  {
    $unwind: {
      path: '$items',
      preserveNullAndEmptyArrays: false
    }
  },

  // Stage 3: Calculate item revenue
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

  // Stage 4: Group back — sum revenue
  {
    $group: {
      _id: null,
      totalRevenue: { $sum: '$itemRevenue' },
      totalOrders: { $addToSet: '$_id' },
      totalItems: { $sum: '$items.quantity' }
    }
  },

  // Stage 5: Calculate AOV
  {
    $addFields: {
      totalOrders: { $size: '$totalOrders' },
      aov: {
        $cond: {
          if: { $gt: [{ $size: '$totalOrders' }, 0] },
          then: { $divide: ['$totalRevenue', { $size: '$totalOrders' }] },
          else: 0
        }
      }
    }
  },

  // Stage 6: Project final shape
  {
    $project: {
      _id: 0,
      totalRevenue: 1,
      totalOrders: 1,
      aov: { $round: ['$aov', 0] },
      totalItems: 1
    }
  }
]
```

### 3.3 AggregateWithdrawService Pipeline

```typescript
// services/stats/aggregate-withdraw.service.ts

const withdrawAggregation = [
  // Stage 1: Match withdraw requests in date range
  {
    $match: {
      status: { $in: ['pending', 'approved', 'rejected'] },
      createdAt: {
        $gte: fromDate,
        $lte: toDate
      }
    }
  },

  // Stage 2: Group by status
  {
    $group: {
      _id: '$status',
      count: { $sum: 1 },
      totalAmount: { $sum: '$amount' }
    }
  },

  // Stage 3: Reshape
  {
    $group: {
      _id: null,
      statuses: {
        $push: {
          status: '$_id',
          count: '$count',
          totalAmount: '$totalAmount'
        }
      },
      totalCount: { $sum: '$count' },
      totalAmount: { $sum: '$totalAmount' }
    }
  },

  // Stage 4: Pivot to named fields
  {
    $project: {
      _id: 0,
      totalCount: 1,
      totalAmount: 1,
      pending: {
        $ifNull: [
          { $arrayElemAt: [{ $map: { input: '$statuses', as: 's', in: { $cond: [{ $eq: ['$$s.status', 'pending'] }, '$$s', null] } } }, 0] }, { count: 0, totalAmount: 0 }
        ]
      },
      approved: {
        $ifNull: [
          { $arrayElemAt: [{ $map: { input: '$statuses', as: 's', in: { $cond: [{ $eq: ['$$s.status', 'approved'] }, '$$s', null] } } }, 0] }, { count: 0, totalAmount: 0 }
        ]
      }
    }
  }
]
```

### 3.4 RevenueChartService Pipeline

```typescript
// services/detail/revenue-chart.service.ts

// Dynamic grouping key theo granularity
const getDateGrouping = (granularity: string) => {
  switch (granularity) {
    case 'day':
      return {
        date: {
          $dateToString: { format: '%Y-%m-%d', date: '$status.confirmedAt' }
        }
      }
    case 'week':
      return {
        date: {
          $dateToString: { format: '%Y-W%V', date: '$status.confirmedAt' }
        }
      }
    case 'month':
      return {
        date: {
          $dateToString: { format: '%Y-%m', date: '$status.confirmedAt' }
        }
      }
  }
}

const revenueChartAggregation = [
  // Stage 1: Match confirmed orders
  {
    $match: {
      status: 'confirmed',
      'status.hold': { $ne: true },
      'status.confirmedAt': {
        $gte: fromDate,
        $lte: toDate
      }
    }
  },

  // Stage 2: Group by date (granularity)
  {
    $group: {
      _id: getDateGrouping(granularity),
      revenue: {
        $sum: {
          $sum: {
            $map: {
              input: '$items',
              as: 'item',
              in: { $multiply: [{ $ifNull: ['$$item.finalPrice', 0] }, { $ifNull: ['$$item.quantity', 0] }] }
            }
          }
        }
      },
      orders: { $sum: 1 }
    }
  },

  // Stage 3: Sort by date
  {
    $sort: { '_id.date': 1 as const }
  },

  // Stage 4: Project final shape
  {
    $project: {
      _id: 0,
      date: '$_id.date',
      revenue: 1,
      orders: 1
    }
  }
]
```

### 3.5 TopProductsService Pipeline

```typescript
// services/detail/top-products.service.ts

const topProductsAggregation = [
  // Stage 1: Match confirmed orders in date range
  {
    $match: {
      status: 'confirmed',
      'status.hold': { $ne: true },
      'status.confirmedAt': {
        $gte: fromDate,
        $lte: toDate
      }
    }
  },

  // Stage 2: Unwind items
  {
    $unwind: {
      path: '$items',
      preserveNullAndEmptyArrays: false
    }
  },

  // Stage 3: Group by product
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

  // Stage 4: Sort by totalSold descending
  {
    $sort: { totalSold: -1 as const }
  },

  // Stage 5: Limit
  {
    $limit: topProductsLimit
  },

  // Stage 6: Project final shape
  {
    $project: {
      _id: 0,
      productId: { $toString: '$_id' },
      name: 1,
      thumbnail: 1,
      totalSold: 1,
      totalRevenue: 1
    }
  }
]
```

---

## 4. Required Indexes

### 4.1 Index Definitions

```typescript
// MongoDB indexes cần thiết cho dashboard aggregation

const indexes = [
  // Orders — confirmedAt for revenue chart
  {
    collection: 'orders',
    name: 'idx_orders_status_confirmedAt',
    key: {
      status: 1,
      'status.confirmedAt': 1
    },
    partialFilter: {
      status: 'confirmed',
      'status.hold': { $exists: false }
    }
  },

  // Orders — status for count aggregation
  {
    collection: 'orders',
    name: 'idx_orders_status_hold',
    key: {
      status: 1,
      'status.hold': 1
    }
  },

  // Orders — customer for new customers
  {
    collection: 'orders',
    name: 'idx_orders_customer_confirmedAt',
    key: {
      customer: 1,
      'status.confirmedAt': 1
    },
    partialFilter: {
      status: 'confirmed',
      'status.hold': { $exists: false }
    }
  },

  // WithdrawRequests — status + createdAt
  {
    collection: 'withdrawRequests',
    name: 'idx_withdraw_status_createdAt',
    key: {
      status: 1,
      createdAt: 1
    }
  }
]
```

---

## 5. Migration Script Structure

### 5.1 File Location

```
payload.config.ts     # Hoặc src/migrations/
└── 003_add_dashboard_indexes.ts
```

### 5.2 Migration Script Template

```typescript
// Migrations 003_add_dashboard_indexes.ts
// Script tạo indexes cho dashboard aggregation performance

import type { Migration } from 'payload'

export const addDashboardIndexes: Migration = {
  // Tên migration
  name: '003_add_dashboard_indexes',

  // Chạy khi nào
  up: async ({ payload }) => {
    // Log bắt đầu
    payload.logger.info('[Migration 003] Creating dashboard indexes...')

    try {
      // Get MongoDB collection
      const ordersCollection = payload.db.collection('orders')
      const withdrawCollection = payload.db.collection('withdrawRequests')

      // Create indexes for orders
      await Promise.all([
        ordersCollection.createIndex(
          { status: 1, 'status.confirmedAt': 1 },
          {
            name: 'idx_orders_status_confirmedAt',
            background: true,
            partialFilterExpression: {
              status: 'confirmed',
              'status.hold': { $exists: false }
            }
          }
        ),
        ordersCollection.createIndex(
          { status: 1, 'status.hold': 1 },
          {
            name: 'idx_orders_status_hold',
            background: true
          }
        ),
        ordersCollection.createIndex(
          { customer: 1, 'status.confirmedAt': 1 },
          {
            name: 'idx_orders_customer_confirmedAt',
            background: true,
            partialFilterExpression: {
              status: 'confirmed',
              'status.hold': { $exists: false }
            }
          }
        )
      ])

      // Create indexes for withdrawRequests
      await withdrawCollection.createIndex(
        { status: 1, createdAt: 1 },
        {
          name: 'idx_withdraw_status_createdAt',
          background: true
        }
      )

      payload.logger.info('[Migration 003] Dashboard indexes created successfully')
    } catch (error) {
      payload.logger.error('[Migration 003] Failed to create indexes:', error)
      throw error
    }
  },

  down: async ({ payload }) => {
    payload.logger.info('[Migration 003] Dropping dashboard indexes...')

    try {
      const ordersCollection = payload.db.collection('orders')
      const withdrawCollection = payload.db.collection('withdrawRequests')

      // Drop indexes
      await ordersCollection.dropIndex('idx_orders_status_confirmedAt')
      await ordersCollection.dropIndex('idx_orders_status_hold')
      await ordersCollection.dropIndex('idx_orders_customer_confirmedAt')
      await withdrawCollection.dropIndex('idx_withdraw_status_createdAt')

      payload.logger.info('[Migration 003] Dashboard indexes dropped successfully')
    } catch (error) {
      payload.logger.error('[Migration 003] Failed to drop indexes:', error)
      throw error
    }
  }
}
```

### 5.3 Migration Execution

```bash
# Run migrations
bun run payload migrate

# Hoặc generate types sau migration
bun gen
```

### 5.4 Index Verification

```typescript
// Verify indexes sau khi migration chạy
const verifyIndexes = async () => {
  const ordersIndexes = await payload.db.collection('orders').indexes()
  console.log('Orders indexes:', ordersIndexes)

  const withdrawIndexes = await payload.db.collection('withdrawRequests').indexes()
  console.log('Withdraw indexes:', withdrawIndexes)
}
```

---

## 7. Hold Mechanism

### 7.1 Hold Status Structure

```typescript
// Trong Order collection — status field
interface OrderStatus {
  pending: boolean
  processing: boolean
  shipped: boolean
  delivered: boolean
  confirmed: boolean
  cancelled: boolean
  hold: boolean        // TRUE = order đang trong dispute
  holdAt?: Date        // Thời điểm bắt đầu hold
  holdReason?: string  // Lý do hold (dispute reason)
  confirmedAt?: Date
  deliveredAt?: Date
}
```

### 7.2 Hold Duration

- **24 giờ**: Thời gian tối đa order có thể ở trạng thái hold
- Sau 24h không resolved → tự động unhold hoặc escalate

### 7.3 Hold Exclusion in Aggregations

```typescript
// Tất cả aggregations phải có filter này
const HOLD_EXCLUSION = {
  'status.hold': { $ne: true }
}

// Ví dụ trong $match stage
{
  $match: {
    status: 'confirmed',
    'status.hold': { $ne: true },
    'status.confirmedAt': { $gte: fromDate, $lte: toDate }
  }
}
```

### 7.4 Hold Not Counted in Stats

- `pendingOrders` chỉ count orders có `status: 'pending'` VÀ `status.hold !== true`
- Revenue pipeline KHÔNG bao gồm hold orders
- Chart không hiển thị hold orders

---

## 8. Revenue Calculation Detail

### 8.1 Item-Level Revenue Formula

```
orderRevenue = SUM(item.finalPrice * item.quantity) cho tất cả item trong order

Ví dụ:
- Item 1: finalPrice = 50000, quantity = 3  → 150000
- Item 2: finalPrice = 120000, quantity = 1 → 120000
- Item 3: finalPrice = 35000, quantity = 2  → 70000
─────────────────────────────────────────────
Total orderRevenue = 340000
```

### 8.2 Commission Calculation (Optional — v4)

```typescript
// Nếu cần tính commission cho platform
const commissionRate = 0.10  // 10%

const commissionAggregation = [
  {
    $addFields: {
      itemRevenue: {
        $sum: {
          $map: {
            input: '$items',
            as: 'item',
            in: {
              $multiply: [
                { $ifNull: ['$$item.finalPrice', 0] },
                { $ifNull: ['$$item.quantity', 0] }
              ]
            }
          }
        }
      }
    }
  },
  {
    $addFields: {
      commission: {
        $multiply: ['$itemRevenue', commissionRate]
      }
    }
  }
]
```

### 8.3 AOV Calculation

```typescript
// AOV = Total Revenue / Total Confirmed Orders
const aov = totalRevenue / totalConfirmedOrders

// Handle division by zero
const safeAov = totalOrders > 0
  ? Math.round(totalRevenue / totalOrders)
  : 0
```

### 8.4 Completion Rate Formula

```
completionRate = (confirmedOrders / totalNonCancelledOrders) * 100

totalNonCancelledOrders = total - cancelled

Ví dụ:
- total = 400
- cancelled = 50
- confirmed = 306
- completionRate = (306 / 350) * 100 = 87.43%
```

---

### 7.5 Validation Checklist

- [x] Aggregation pipelines tested với `$facet` cho parallel computation
- [x] Date parsing dùng `new Date(y, m-1, d)` để tránh UTC shift
- [x] Hold exclusion filter `{ 'status.hold': { $ne: true } }` trong tất cả pipelines
- [x] Revenue tính ở item-level với `finalPrice * quantity`
- [x] Index migration script có `up` và `down` methods
- [x] Error handling cho empty results
- [x] `$ne: true` vs `$exists: false` — dùng `$ne: true` vì field luôn tồn tại
