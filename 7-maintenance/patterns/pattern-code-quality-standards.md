# Pattern: Code Quality Standards

## Problem
Inconsistent code style, poor practices, security issues.

## Solution
Follow coding best practices, security standards, và quality guidelines.

**Core principles:**
- Follow existing conventions
- Security first
- Performance optimization
- Accessibility compliance
- Clean, readable code

## Example

### ✅ Good: Quality Code
```typescript
// Clear naming
export async function fetchUserProfile(userId: string): Promise<User> {
  // Input validation
  if (!userId) {
    throw new Error('User ID is required')
  }
  
  // Secure API call
  const response = await api.get(`/users/${userId}`, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  })
  
  // Error handling
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.statusText}`)
  }
  
  return response.data
}
```

### ❌ Bad: Poor Quality
```typescript
// Vague naming, no validation, no error handling
export async function get(id) {
  const r = await fetch(`/users/${id}`)
  return r.json()
}
```

## Quality Standards

### 1. Security Best Practices

#### ✅ Environment Variables
```typescript
// Use env vars for secrets
const apiKey = process.env.API_KEY

// NEVER hardcode
const apiKey = "sk-1234567890"  // ❌
```

#### ✅ Input Validation
```typescript
// Validate all inputs
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

const validated = schema.parse(input)
```

#### ✅ SQL Injection Prevention
```typescript
// Use parameterized queries
db.query('SELECT * FROM users WHERE id = ?', [userId])

// NEVER string concatenation
db.query(`SELECT * FROM users WHERE id = ${userId}`)  // ❌
```

#### ✅ XSS Prevention
```typescript
// Sanitize user input
import DOMPurify from 'dompurify'
const clean = DOMPurify.sanitize(userInput)

// Use framework escaping
<div>{userInput}</div>  // React auto-escapes
```

### 2. Performance Optimization

#### ✅ Lazy Loading
```tsx
// Lazy load components
const HeavyComponent = lazy(() => import('./HeavyComponent'))

// Lazy load images
<img src="image.jpg" loading="lazy" />
```

#### ✅ Memoization
```tsx
// Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data)
}, [data])

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(id)
}, [id])
```

#### ✅ Code Splitting
```typescript
// Split by route
const Dashboard = lazy(() => import('./Dashboard'))
const Settings = lazy(() => import('./Settings'))
```

### 3. Accessibility (a11y)

#### ✅ Semantic HTML
```tsx
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <h1>Page Title</h1>
  <article>...</article>
</main>

<footer>...</footer>
```

#### ✅ ARIA Attributes
```tsx
// Screen reader text
<span className="sr-only">Skip to main content</span>

// Button labels
<button aria-label="Close dialog">×</button>

// Form labels
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

#### ✅ Keyboard Navigation
```tsx
// Focusable elements
<button onClick={handleClick}>Click</button>

// Tab order
<div tabIndex={0}>Focusable div</div>
```

### 4. Code Conventions

#### ✅ Follow Existing Patterns
```typescript
// Check existing code first
// Match naming conventions
// Use same libraries
// Follow same structure
```

#### ✅ Descriptive Naming
```typescript
// ✅ Clear intent
function calculateTotalPrice(items: Item[]): number

// ❌ Vague
function calc(arr: any[]): number
```

#### ✅ Error Handling
```typescript
// Always handle errors
try {
  await riskyOperation()
} catch (error) {
  logger.error('Operation failed', error)
  toast.error('Something went wrong')
}
```

#### ✅ Type Safety
```typescript
// Use TypeScript properly
interface User {
  id: string
  name: string
  email: string
}

function getUser(id: string): Promise<User>

// Avoid any
function getData(): any  // ❌
```

## Quality Checklist

### Security
- [ ] No hardcoded secrets?
- [ ] Input validation?
- [ ] SQL injection prevention?
- [ ] XSS prevention?
- [ ] CSRF protection?
- [ ] Secure authentication?

### Performance
- [ ] Lazy loading images?
- [ ] Code splitting?
- [ ] Memoization where needed?
- [ ] No unnecessary re-renders?
- [ ] Optimized bundle size?

### Accessibility
- [ ] Semantic HTML?
- [ ] ARIA attributes?
- [ ] Keyboard navigation?
- [ ] Screen reader support?
- [ ] Color contrast?
- [ ] Alt text for images?

### Code Quality
- [ ] Follows conventions?
- [ ] Descriptive naming?
- [ ] Error handling?
- [ ] Type safety?
- [ ] No duplicate code?
- [ ] Readable and maintainable?

## Anti-patterns
- ❌ Hardcoded secrets
- ❌ No input validation
- ❌ String concatenation in SQL
- ❌ No error handling
- ❌ Using `any` type
- ❌ Non-semantic HTML
- ❌ Missing accessibility features

## Source
- Cursor Agent Prompt 2.0 - "Follow best practices"
- Windsurf Cascade - "Security best practices"
- v0 (Vercel) - "Always implement best practices"
- Lovable - "Beautiful designs, valid code"
