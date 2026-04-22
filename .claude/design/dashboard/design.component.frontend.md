# Design — Frontend Components

> **Status**: Approved
> **Version**: 1.0.0
> **Last Updated**: 2026-03-21

---

## 1. DateFilterBar

### 1.1 Purpose

Cho phép admin chọn date range để filter dashboard data. Hỗ trợ 14 presets + custom date picker.

### 1.2 Props

```typescript
interface DateFilterBarProps {
  // Controlled state
  preset: string
  from: string | null
  to: string | null

  // Change handlers
  onPresetChange: (preset: string) => void
  onCustomRangeChange: (from: string, to: string) => void

  // Optional
  className?: string
}
```

### 1.3 Internal State

```typescript
// Local UI state
const [showCustomPicker, setShowCustomPicker] = useState(false)
const [tempFrom, setTempFrom] = useState(from)
const [tempTo, setTempTo] = useState(to)
```

### 1.4 UI Structure

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  [📅 Tuần này ▼]  [📅 Tháng này ▼]  [📅 Quý này ▼]  [📅 Năm nay ▼]  [📅 Custom ▼]  │
│                                                                               │
│  Khi "Custom" được chọn → hiện 2 date inputs + Apply button                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.5 Preset Dropdown Items

```typescript
const PRESET_ITEMS = [
  { id: 'today', label: 'Hôm nay', icon: CalendarIcon },
  { id: 'yesterday', label: 'Hôm qua', icon: CalendarIcon },
  { id: 'last_7_days', label: '7 ngày qua', icon: CalendarDaysIcon },
  { id: 'last_14_days', label: '14 ngày qua', icon: CalendarDaysIcon },
  { id: 'last_28_days', label: '28 ngày qua', icon: CalendarDaysIcon },
  { id: 'last_30_days', label: '30 ngày qua', icon: CalendarDaysIcon },
  { id: 'last_60_days', label: '60 ngày qua', icon: CalendarDaysIcon },
  { id: 'last_90_days', label: '90 ngày qua', icon: CalendarDaysIcon },
  { id: 'this_week', label: 'Tuần này', icon: CalendarIcon },
  { id: 'this_month', label: 'Tháng này', icon: CalendarIcon },
  { id: 'last_week', label: 'Tuần trước', icon: CalendarIcon },
  { id: 'last_month', label: 'Tháng trước', icon: CalendarIcon },
  { id: 'this_quarter', label: 'Quý này', icon: CalendarIcon },
  { id: 'this_year', label: 'Năm nay', icon: CalendarIcon },
] as const
```

### 1.6 Custom Picker Behavior

- Toggle `showCustomPicker` khi click "Custom" button
- Hiện 2 `<input type="date">` với `tempFrom`/`tempTo`
- "Áp dụng" button → gọi `onCustomRangeChange(tempFrom, tempTo)` + set `preset = null`
- "Hủy" button → reset temp state + hide picker
- Validate: `tempFrom <= tempTo`, max 365 days span

### 1.7 Selected Preset Display

Khi preset được chọn, hiển thị label thay vì ID:

```typescript
const getPresetLabel = (preset: string) => {
  return PRESET_ITEMS.find(item => item.id === preset)?.label ?? preset
}
```

---

## 2. KPI Card Components

### 2.1 Base KpiCard

Wrapper component cho tất cả KPI cards.

```typescript
interface KpiCardProps {
  title: string
  value: string | number
  unit?: string
  icon: ReactNode
  alert?: 'high' | 'medium' | null
  comparison?: {
    value: number | string
    changePercent: number | null
    trend: 'up' | 'down' | 'neutral'
  }
  loading?: boolean
  className?: string
}
```

**Layout**:
```
┌─────────────────────────────────────┐
│  [Icon]  Title              [Alert] │
│                                     │
│  Value                    [Badge]   │
│  Unit                      Comp.%   │
└─────────────────────────────────────┘
```

### 2.2 KpiCardRevenue

```typescript
interface KpiCardRevenueProps {
  value: number        // VD: 125000000
  comparison: KpiComparison
  loading?: boolean
}

// Format: 125.000.000 ₫
// Comparison: +27.5% ▲
```

### 2.3 KpiCardOrders

```typescript
interface KpiCardOrdersProps {
  value: number
  comparison: KpiComparison
  loading?: boolean
}

// Format: 342 đơn
// Comparison: +14.8% ▲
```

### 2.4 KpiCardNewCustomers

```typescript
interface KpiCardNewCustomersProps {
  value: number
  comparison: KpiComparison
  loading?: boolean
}

// Format: 87 khách
// Comparison: +33.9% ▲
```

### 2.5 KpiCardAov

```typescript
interface KpiCardAovProps {
  value: number        // VD: 365497
  comparison: KpiComparison
  loading?: boolean
}

// Format: 365.497 ₫
// Comparison: +11.1% ▲
```

### 2.6 KpiCardPending

```typescript
interface KpiCardPendingProps {
  value: number
  comparison: KpiComparison
  loading?: boolean
}

// Format: 23 đơn
// Comparison: -25.8% ▼
// Alert: 'medium' | 'high' | null
```

### 2.7 KpiCardCompletionRate

```typescript
interface KpiCardCompletionRateProps {
  value: number        // 0-100
  comparison: KpiComparison
  loading?: boolean
}

// Format: 87.5%
// Comparison: +3.9% ▲
```

### 2.8 Shared Comparison Type

```typescript
interface KpiComparison {
  value: number | string
  changePercent: number | null
  trend: 'up' | 'down' | 'neutral'
}
```

---

## 3. ComparisonBadge

### 3.1 Purpose

Hiển thị phần trăm thay đổi so với kỳ trước với màu sắc và icon phù hợp.

### 3.2 Props

```typescript
interface ComparisonBadgeProps {
  changePercent: number | null
  trend: 'up' | 'down' | 'neutral'
  size?: 'sm' | 'md'
  showIcon?: boolean
}
```

### 3.3 Visual Rules

| Trend | Positive Good? | Color | Icon | Condition |
|-------|--------------|-------|------|----------|
| `up` | Yes (revenue, orders, customers, aov, completion) | `#22c55e` (green) | ↑ | Positive is good |
| `up` | No (pending orders) | `#ef4444` (red) | ↑ | Positive is bad |
| `down` | Yes (revenue, orders) | `#ef4444` (red) | ↓ | Negative is bad |
| `down` | No (pending orders) | `#22c55e` (green) | ↓ | Negative is good |
| `neutral` | — | `#94a3b8` (gray) | — | 0% change |

### 3.4 Example Usage

```tsx
// Revenue: up is good
<ComparisonBadge trend="up" changePercent={27.55} />

// Pending: up is BAD (more pending = worse)
<ComparisonBadge trend="up" changePercent={15} isNegativeGood />

// Neutral
<ComparisonBadge trend="neutral" changePercent={0} />
```

### 3.5 Display Format

- `changePercent = 27.55` → `+27.5%`
- `changePercent = -25.81` → `-25.8%`
- `changePercent = null` → `—`
- `changePercent = 0` → `0%`

---

## 4. AlertBadge

### 4.1 Purpose

Hiển thị cảnh báo threshold cho các KPI cần chú ý.

### 4.2 Props

```typescript
interface AlertBadgeProps {
  level: 'high' | 'medium' | null
  label?: string
}
```

### 4.3 Thresholds (defined in business logic)

| KPI | High Threshold | Medium Threshold | Label |
|-----|--------------|-----------------|-------|
| `pendingOrders` | `> 50` | `> 0` | `${value} đơn chờ` |

### 4.4 Visual Rules

| Level | Color | Icon | Background |
|-------|-------|------|------------|
| `high` | `#ef4444` (red-500) | AlertTriangle | `bg-red-50` |
| `medium` | `#f59e0b` (amber-500) | AlertCircle | `bg-amber-50` |
| `null` | — | — | Hidden |

### 4.5 Example

```tsx
{pendingOrders > 0 && (
  <AlertBadge level={pendingOrders > 50 ? 'high' : 'medium'} />
)}
```

---

## 5. useAdminDashboardStats Hook

### 5.1 Purpose

Fetch và cache stats data từ `/api/v1/admin/dashboard/stats`.

### 5.2 Hook Signature

```typescript
interface UseAdminDashboardStatsOptions {
  preset: string
  from: string | null
  to: string | null
  enabled?: boolean
}

interface UseAdminDashboardStatsReturn {
  // Data
  stats: AdminDashboardStats | null
  kpis: KpiData | null

  // State
  loading: boolean
  error: Error | null

  // Actions
  refetch: () => void

  // Meta
  meta: {
    preset: string
    from: string
    to: string
    spanDays: number
    generatedAt: string
  } | null
}
```

### 5.3 Internal Logic

```typescript
// Debounce date changes (prevent excessive API calls)
const debouncedParams = useDebounce({ preset, from, to }, 300)

// Fetch on params change
useEffect(() => {
  if (!enabled) return

  setLoading(true)
  ApiService.get(ENDPOINTS.ADMIN_DASHBOARD.STATS, {
    params: {
      preset: debouncedParams.preset ?? undefined,
      from: debouncedParams.from ?? undefined,
      to: debouncedParams.to ?? undefined,
    }
  })
    .then(res => {
      setStats(res.data.data)
      setError(null)
    })
    .catch(err => setError(err))
    .finally(() => setLoading(false))
}, [debouncedParams, enabled])
```

### 5.4 Loading Skeleton

```tsx
const StatsSkeleton = () => (
  <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
    {Array.from({ length: 6 }).map((_, i) => (
      <div key={i} className="animate-pulse bg-gray-100 rounded-xl h-32" />
    ))}
  </div>
)
```

### 5.5 Error State

```tsx
if (error) {
  return (
    <div className="text-center py-8">
      <p className="text-red-500">Không thể tải dữ liệu dashboard</p>
      <Button onClick={refetch}>Thử lại</Button>
    </div>
  )
}
```

---

## 6. useAdminDashboardDetail Hook

### 6.1 Purpose

Fetch revenue chart và top products từ `/api/v1/admin/dashboard/detail`.

### 6.2 Hook Signature

```typescript
interface UseAdminDashboardDetailOptions {
  preset: string
  from: string | null
  to: string | null
  granularity?: 'day' | 'week' | 'month'
  topProductsLimit?: number
  enabled?: boolean
}

interface UseAdminDashboardDetailReturn {
  // Data
  revenueChart: RevenueChartData | null
  topProducts: TopProductData[] | null

  // State
  loading: boolean
  error: Error | null

  // Actions
  refetch: () => void

  // Meta
  meta: {
    preset: string
    from: string
    to: string
    spanDays: number
    generatedAt: string
  } | null
}
```

### 6.3 Auto-Granularity

```typescript
// Tự động chọn granularity dựa trên spanDays
const autoGranularity = (spanDays: number): 'day' | 'week' | 'month' => {
  if (spanDays <= 31) return 'day'
  if (spanDays <= 93) return 'week'
  return 'month'
}
```

### 6.4 Parallel Fetching

Stats và detail được fetch song song (không dependent):

```tsx
// Trong DashboardScreen
const statsQuery = useAdminDashboardStats({ preset, from, to })
const detailQuery = useAdminDashboardDetail({ preset, from, to, granularity, topProductsLimit })

// Dashboard ready when both complete
const loading = statsQuery.loading || detailQuery.loading
```

---

## 7. State Management

### 7.1 Local State (DashboardScreen)

```typescript
// DashboardScreen.tsx
const [preset, setPreset] = useState('last_30_days')
const [from, setFrom] = useState<string | null>(null)
const [to, setTo] = useState<string | null>(null)
const [granularity, setGranularity] = useState<'day' | 'week' | 'month'>('day')
const [topProductsLimit, setTopProductsLimit] = useState(10)
```

### 7.2 URL Sync (Optional)

```typescript
// Sync filter state to URL params
useEffect(() => {
  const params = new URLSearchParams()
  if (preset) params.set('preset', preset)
  if (from) params.set('from', from)
  if (to) params.set('to', to)
  window.history.replaceState(null, '', `?${params.toString()}`)
}, [preset, from, to])

// Restore from URL on mount
useEffect(() => {
  const params = new URLSearchParams(window.location.search)
  if (params.has('preset')) setPreset(params.get('preset')!)
  if (params.has('from')) setFrom(params.get('from'))
  if (params.has('to')) setTo(params.get('to'))
}, [])
```

### 7.3 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ Header: "Dashboard"                                             │
├──────────────────────────────────────────────────────────────────┤
│ DateFilterBar                                                    │
├──────────────────────────────────────────────────────────────────┤
│ KPI Grid (6 cards)                                               │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│ │Revenue │ │ Orders │ │Customer│ │  AOV   │ │Pending │ │Completion│
│ │ 125M   │ │  342    │ │  87    │ │ 365.5K │ │  23 ⚠  │ │  87.5%  ││
│ │ +27.5%▲│ │ +14.8%▲│ │ +33.9%▲│ │+11.1%▲│ │ -25.8%▼│ │ +3.9%▲ ││
│ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│
├──────────────────────────────────────────────────────────────────┤
│ Revenue Chart (ResponsiveContainer)                              │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │                      [Line Chart]                             ││
│ └──────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│ Top Products                                                     │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ [Product Card] [Product Card] [Product Card] ...            ││
│ └──────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

### 7.4 Color Tokens

Dùng Pink Petals primary color `#e8799a` cho các interactive elements:

```typescript
const colors = {
  primary: '#e8799a',       // Pink Petals — CTAs, links
  primaryLight: '#fce7ef',  // Pink Petals light — backgrounds
  chartLine: '#e8799a',     // Chart primary line
  chartArea: '#fce7ef',      // Chart area fill
  positive: '#22c55e',       // Green — good trends
  negative: '#ef4444',       // Red — bad trends
  warning: '#f59e0b',       // Amber — warnings
  neutral: '#94a3b8',        // Gray — neutral
  text: '#1e293b',          // Slate-800
  textMuted: '#64748b',     // Slate-500
}
```

### 7.5 Barrel Exports

```typescript
// components/DateFilterBar/index.ts
export { DateFilterBar } from './DateFilterBar'

// components/KpiCard/index.ts
export { KpiCard } from './KpiCard'
export { KpiCardRevenue } from './KpiCard/KpiCardRevenue'
export { KpiCardOrders } from './KpiCard/KpiCardOrders'
export { KpiCardNewCustomers } from './KpiCard/KpiCardNewCustomers'
export { KpiCardAov } from './KpiCard/KpiCardAov'
export { KpiCardPending } from './KpiCard/KpiCardPending'
export { KpiCardCompletionRate } from './KpiCard/KpiCardCompletionRate'

// components/ComparisonBadge/index.ts
export { ComparisonBadge } from './ComparisonBadge'

// components/AlertBadge/index.ts
export { AlertBadge } from './AlertBadge'
```
