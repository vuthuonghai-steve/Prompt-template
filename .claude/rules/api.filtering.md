---
trigger: always_on
paths:
  - "src/screens/**/*.tsx"
---

# Filtering Pattern

> Debounced Search Pattern for List Views
> **Last Updated**: 2026-03-05

---

## Concept

Tranh goi API qua nhieu khi nguoi dung go phim tim kiem nhung van giu phan hoi tuong thu cua cac bo loc khac (Dropdown Select).

---

## Architecture

### State Structure

```typescript
// State "thuc" - thay doi se trigger API
const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS)

// State cho o tim kiem - cap nhat NGAY de UI muot
const [searchInput, setSearchInput] = useState('')
```

### Debounce Logic

```typescript
import { searchDebounceMs } from '@/configs/app'

useEffect(() => {
  const timer = window.setTimeout(() => {
    setFilters((prev) =>
      prev.productName === searchInput ? prev : { ...prev, productName: searchInput }
    )
  }, searchDebounceMs)

  return () => window.clearTimeout(timer)
}, [searchInput, setFilters])
```

### Automated Trigger

```typescript
const fetchList = useCallback(async () => {
  // Logic goi API
}, [filters])

useEffect(() => {
  fetchList()
}, [fetchList])
```

---

## Best Practices

### Dropdown Selection
Cap nhat TRUC TIEP vao `filters` de co ket qua ngay:
```typescript
const handleFilterChange = (key, value) => {
  setFilters(prev => ({ ...prev, [key]: value }))
}
```

### Clear Filters
Reset ca `searchInput` va `filters`:
```typescript
const handleClear = () => {
  setSearchInput('')
  setFilters(DEFAULT_FILTERS)
}
```

---

## Common Pitfalls

- ❌ **Goi API khi go** - Gay lag
- ❌ **Debounce dropdown** - Lam cham UX
- ❌ **Khong reset searchInput** - UI hien thi sai

---

**Related**: [api.patterns.md](./api.patterns.md)
