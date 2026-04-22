---
trigger: always_on
paths:
  - "src/components/**/*.tsx"
  - "src/screens/**/*.tsx"
---

# Design System Components

> **Last Updated**: 2026-03-05

---

## Forbidden Libraries

**NEVER import from these:**

```typescript
// ❌ ABSOLUTELY NO
import { Modal, Button, Input } from 'antd'
import { Button, TextField } from '@mui/material'
import { Button, Input } from '@chakra-ui/react'
import { Button, TextInput } from '@mantine/core'
```

---

## Approved Components

```typescript
// ✅ ALWAYS USE
import { AlertDialog } from '@/components/ui/alert-dialog'
import { Dialog } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { BaseSelect } from '@/components/selects/BaseSelect'
```

---

## Usage Examples

### Button

```typescript
<Button variant="default">Primary Action</Button>
<Button variant="outline">Secondary Action</Button>
<Button variant="ghost">Tertiary Action</Button>
<Button variant="destructive">Delete</Button>
```

### Select

```typescript
<BaseSelect
  options={productTypes}
  value={selectedType}
  onValueChange={setSelectedType}
  placeholder="Select..."
/>
```

### Dialog

```typescript
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm</DialogTitle>
    </DialogHeader>
    <DialogFooter>
      <Button onClick={() => setIsOpen(false)}>Cancel</Button>
      <Button variant="destructive">Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

---

## Compose-Only Pattern cho Screens

Mọi `index.tsx` trong thư mục `src/screens/**/` phải ở dạng compose-only - chỉ chứa composition, KHÔNG có logic nghiệp vụ.

### Quy tắc

```typescript
// ✅ CORRECT - Chỉ compose, không có logic
import { ProductListScreen } from './ProductListScreen'

export { ProductListScreen }

// ❌ WRONG - Có logic trong index.tsx
export const ProductListScreen = () => {
  const { data } = useQuery(...)
  // ... business logic
}
```

### Cấu trúc đúng

```
screens/
├── ProductListScreen/
│   ├── index.tsx           # Chỉ export, KHÔNG có logic
│   ├── ProductListScreen.tsx   # Component chính
│   ├── components/        # Sub-components
│   │   ├── QuickFilterPills.tsx
│   │   └── ProductListPagination.tsx
│   ├── hooks/             # Custom hooks
│   │   └── hook.use-product-list.ts
│   ├── types/             # Type definitions
│   │   └── type.product-list.ts
│   └── constants/         # Constants
│       └── constant.filter.ts
```

### Checklist

- [ ] `index.tsx` chỉ re-export các component/function
- [ ] Logic nghiệp vụ nằm trong hooks riêng
- [ ] Types được tách ra thư mục `types/`
- [ ] Constants được tách ra thư mục `constants/`

---

## Styling Guidelines

```typescript
// ✅ CORRECT - Tailwind with design tokens
<div className="rounded-lg bg-primary-50 p-4 shadow-md">
  <h2 className="text-lg font-semibold text-primary-700">Title</h2>
</div>

// ❌ WRONG - Inline styles
<div style={{ backgroundColor: '#FF8CAF' }}>Content</div>
```

---

**Related**:
- [design-system.colors.md](./design-system.colors.md)
