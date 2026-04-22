---
trigger: always_on
paths:
  - "src/stores/**/*.ts"
  - "src/contexts/**/*.ts"
  - "src/hooks/**/*.ts"
---

# State Management

> **Last Updated**: 2026-03-05

---

## Redux Toolkit

```typescript
// ✅ CORRECT - Slice pattern
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UserState {
  id: string | null
  email: string | null
  isAuthenticated: boolean
}

const initialState: UserState = {
  id: null,
  email: null,
  isAuthenticated: false,
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<{ id: string; email: string }>) => {
      state.id = action.payload.id
      state.email = action.payload.email
      state.isAuthenticated = true
    },
    clearUser: (state) => {
      state.id = null
      state.email = null
      state.isAuthenticated = false
    },
  },
})

export const { setUser, clearUser } = userSlice.actions
export default userSlice.reducer
```

---

## Local State vs Global State

```typescript
// ✅ CORRECT - Local state cho UI
const [isOpen, setIsOpen] = useState(false)
const [selectedTab, setSelectedTab] = useState('products')

// ✅ CORRECT - Redux cho shared state
const user = useSelector((state: RootState) => state.user)
const dispatch = useDispatch()
dispatch(setUser({ id: '123', email: 'user@example.com' }))

// ❌ WRONG - UI state trong Redux
dispatch(setIsModalOpen(true))
```

---

## Context API

```typescript
// ✅ CORRECT - Theme, page title, etc.
export const PageTitleContext = createContext<PageTitleContextType | undefined>(undefined)

export const usePageTitle = () => {
  const context = useContext(PageTitleContext)
  if (!context) {
    throw new Error('usePageTitle must be used within PageTitleProvider')
  }
  return context
}
```

---

## Best Practices

| Scenario | Solution |
|----------|----------|
| UI state (modal, tabs) | useState |
| Shared state (user, cart) | Redux |
| Theme, page title | Context |
| Server state | React Query / SWR |

---

**Related**:
- [component.patterns.md](./component.patterns.md)
- [api.patterns.md](./api.patterns.md)
