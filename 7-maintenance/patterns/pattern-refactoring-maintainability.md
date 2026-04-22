# Pattern: Refactoring for Maintainability

## Problem
Spaghetti code, duplicate logic, poor organization → hard to maintain.

## Solution
Refactor code để improve efficiency và maintainability. Consider refactoring với mỗi request.

**Core principles:**
- Always consider if code needs refactoring
- Create small, focused components
- Avoid monolithic files
- Extract reusable logic
- Follow DRY (Don't Repeat Yourself)

## Example

### ❌ Bad: Monolithic Component
```tsx
// DON'T do this - 500 lines in one file
export default function Dashboard() {
  // 100 lines of state
  const [users, setUsers] = useState([])
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  // ... 20 more states
  
  // 100 lines of API calls
  const fetchUsers = async () => { ... }
  const fetchProducts = async () => { ... }
  // ... 10 more fetch functions
  
  // 300 lines of JSX
  return (
    <div>
      {/* Massive nested JSX */}
    </div>
  )
}
```

### ✅ Good: Refactored Structure
```tsx
// dashboard/page.tsx - 20 lines
import { UserSection } from './components/UserSection'
import { ProductSection } from './components/ProductSection'
import { OrderSection } from './components/OrderSection'

export default function Dashboard() {
  return (
    <div className="grid gap-6">
      <UserSection />
      <ProductSection />
      <OrderSection />
    </div>
  )
}

// dashboard/components/UserSection.tsx - 50 lines
import { useUsers } from '@/hooks/useUsers'
import { UserCard } from './UserCard'

export function UserSection() {
  const { users, loading } = useUsers()
  
  return (
    <section>
      <h2>Users</h2>
      {users.map(user => <UserCard key={user.id} user={user} />)}
    </section>
  )
}

// hooks/useUsers.ts - 30 lines
export function useUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    fetchUsers()
  }, [])
  
  return { users, loading }
}
```

## Refactoring Checklist

### When to Refactor
- [ ] File > 200 lines?
- [ ] Duplicate code in 3+ places?
- [ ] Complex nested logic?
- [ ] Hard to understand?
- [ ] Adding new feature to messy code?

### What to Refactor
- [ ] Extract components
- [ ] Extract hooks
- [ ] Extract utilities
- [ ] Remove duplication
- [ ] Simplify logic

## Refactoring Patterns

### 1. Extract Component
```tsx
// Before: Monolithic
function Dashboard() {
  return (
    <div>
      <div className="user-section">
        {/* 100 lines of user UI */}
      </div>
      <div className="product-section">
        {/* 100 lines of product UI */}
      </div>
    </div>
  )
}

// After: Extracted
function Dashboard() {
  return (
    <div>
      <UserSection />
      <ProductSection />
    </div>
  )
}
```

### 2. Extract Hook
```tsx
// Before: Logic in component
function UserList() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    setLoading(true)
    fetch('/api/users')
      .then(res => res.json())
      .then(setUsers)
      .finally(() => setLoading(false))
  }, [])
  
  return <div>...</div>
}

// After: Extracted hook
function UserList() {
  const { users, loading } = useUsers()
  return <div>...</div>
}

function useUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    setLoading(true)
    fetch('/api/users')
      .then(res => res.json())
      .then(setUsers)
      .finally(() => setLoading(false))
  }, [])
  
  return { users, loading }
}
```

### 3. Extract Utility
```tsx
// Before: Duplicate logic
function UserCard({ user }) {
  const fullName = `${user.firstName} ${user.lastName}`
  return <div>{fullName}</div>
}

function UserProfile({ user }) {
  const fullName = `${user.firstName} ${user.lastName}`
  return <h1>{fullName}</h1>
}

// After: Extracted utility
function UserCard({ user }) {
  return <div>{formatUserName(user)}</div>
}

function UserProfile({ user }) {
  return <h1>{formatUserName(user)}</h1>
}

// utils/user.ts
export function formatUserName(user: User) {
  return `${user.firstName} ${user.lastName}`
}
```

### 4. Simplify Logic
```tsx
// Before: Complex nested conditions
function getStatus(user) {
  if (user.isActive) {
    if (user.isPremium) {
      if (user.hasSubscription) {
        return 'premium-active'
      } else {
        return 'premium-inactive'
      }
    } else {
      return 'active'
    }
  } else {
    return 'inactive'
  }
}

// After: Early returns
function getStatus(user) {
  if (!user.isActive) return 'inactive'
  if (!user.isPremium) return 'active'
  if (user.hasSubscription) return 'premium-active'
  return 'premium-inactive'
}
```

## File Organization

### ✅ Good Structure
```
features/
├── dashboard/
│   ├── page.tsx              # 20 lines
│   ├── components/
│   │   ├── UserSection.tsx   # 50 lines
│   │   ├── ProductSection.tsx
│   │   └── OrderSection.tsx
│   └── hooks/
│       ├── useUsers.ts       # 30 lines
│       └── useProducts.ts
```

### ❌ Bad Structure
```
features/
└── dashboard/
    └── page.tsx              # 500 lines
```

## Refactoring Workflow

```
Receive Request
    ↓
Analyze Current Code
    ↓
├─ Code Clean → Implement
│
└─ Code Messy
    ↓
    Refactor First
    ↓
    Then Implement
```

## Best Practices

### 1. Small, Focused Components
```tsx
// Each component does ONE thing
<UserCard />      // Display user
<UserList />      // List users
<UserForm />      // Edit user
```

### 2. Reusable Logic
```tsx
// Extract to hooks
useUsers()
useProducts()
useAuth()
```

### 3. Utility Functions
```tsx
// Extract to utils
formatCurrency()
formatDate()
validateEmail()
```

### 4. Avoid Duplication
```tsx
// If used 3+ times, extract it
// Rule of Three
```

## Anti-patterns
- ❌ Monolithic files (> 200 lines)
- ❌ Duplicate code
- ❌ Complex nested logic
- ❌ Everything in one component
- ❌ No separation of concerns

## Checklist
- [ ] Components < 200 lines?
- [ ] No duplicate code?
- [ ] Logic extracted to hooks?
- [ ] Utilities extracted?
- [ ] Easy to understand?
- [ ] Easy to test?

## Source
- Lovable - "PERFECT ARCHITECTURE: Always consider whether code needs refactoring"
- Cursor Agent Prompt 2.0 - "Think creatively and explore"
- v0 (Vercel) - "Split code into multiple components"
