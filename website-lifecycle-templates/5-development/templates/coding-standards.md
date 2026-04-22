# Coding Standards Template

> Extracted from: Cursor, VSCode Agent, Windsurf, Claude Code
> Phase: Development
> Last Updated: 2026-04-22

---

## 🎯 Core Principles

### 1. Code Quality
- **Readable**: Code is read more than written
- **Maintainable**: Easy to modify and extend
- **Testable**: Easy to write tests for
- **Secure**: Follow security best practices

### 2. Consistency
- Follow project conventions
- Use linters and formatters
- Code reviews mandatory

---

## 📋 Naming Conventions

### Variables & Functions
```typescript
// ✅ GOOD - Descriptive, clear intent
const userAuthToken = generateToken(user)
const isUserAuthenticated = checkAuth(token)
const fetchUserProfile = async (userId: string) => { ... }

// ❌ BAD - Vague, unclear
const data = getStuff()
const flag = check()
const doThing = () => { ... }
```

### Classes & Interfaces
```typescript
// ✅ GOOD
class UserService { }
interface UserDTO { }
type UserRole = 'admin' | 'user'

// ❌ BAD
class user_service { }
interface IUser { }  // Hungarian notation
type userRole = string  // Too generic
```

### Constants
```typescript
// ✅ GOOD
const API_BASE_URL = 'https://api.example.com'
const MAX_RETRY_ATTEMPTS = 3
const DEFAULT_PAGE_SIZE = 20

// ❌ BAD
const apiUrl = 'https://api.example.com'
const max = 3
```

---

## 🔧 Code Organization

### Function Length
```typescript
// ✅ GOOD - Single responsibility, < 50 lines
const validateUser = (user: User): ValidationResult => {
  if (!user.email) return { valid: false, error: 'Email required' }
  if (!isValidEmail(user.email)) return { valid: false, error: 'Invalid email' }
  return { valid: true }
}

// ❌ BAD - Too long, multiple responsibilities
const processUser = (user: User) => {
  // 200+ lines of validation, transformation, API calls, etc.
}
```

### Early Returns
```typescript
// ✅ GOOD - Early returns reduce nesting
const getUser = async (id: string) => {
  if (!id) throw new Error('ID required')
  
  const user = await db.users.findById(id)
  if (!user) throw new Error('User not found')
  
  return user
}

// ❌ BAD - Nested conditions
const getUser = async (id: string) => {
  if (id) {
    const user = await db.users.findById(id)
    if (user) {
      return user
    } else {
      throw new Error('User not found')
    }
  } else {
    throw new Error('ID required')
  }
}
```

---

## 🎨 TypeScript Best Practices

### Type Safety
```typescript
// ✅ GOOD - Explicit types
interface User {
  id: string
  email: string
  role: 'admin' | 'user'
}

const createUser = (data: Omit<User, 'id'>): User => {
  return { id: generateId(), ...data }
}

// ❌ BAD - Any types
const createUser = (data: any): any => {
  return { id: generateId(), ...data }
}
```

### Null Safety
```typescript
// ✅ GOOD - Optional chaining & nullish coalescing
const userName = user?.profile?.name ?? 'Anonymous'
const userAge = user?.age ?? 0

// ❌ BAD - Unsafe access
const userName = user.profile.name || 'Anonymous'
```

---

## 🔐 Security Practices

### Input Validation
```typescript
// ✅ GOOD - Validate all inputs
import { z } from 'zod'

const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().min(18).max(120)
})

const createUser = (data: unknown) => {
  const validated = UserSchema.parse(data)
  // Safe to use validated data
}

// ❌ BAD - No validation
const createUser = (data: any) => {
  // Directly use unvalidated data
}
```

### SQL Injection Prevention
```typescript
// ✅ GOOD - Parameterized queries
const getUser = async (email: string) => {
  return db.query('SELECT * FROM users WHERE email = ?', [email])
}

// ❌ BAD - String concatenation
const getUser = async (email: string) => {
  return db.query(`SELECT * FROM users WHERE email = '${email}'`)
}
```

### XSS Prevention
```typescript
// ✅ GOOD - Sanitize user input
import DOMPurify from 'dompurify'

const renderUserContent = (html: string) => {
  const clean = DOMPurify.sanitize(html)
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}

// ❌ BAD - Direct HTML injection
const renderUserContent = (html: string) => {
  return <div dangerouslySetInnerHTML={{ __html: html }} />
}
```

---

## 🧪 Testing Standards

### Test Structure
```typescript
// ✅ GOOD - AAA pattern (Arrange, Act, Assert)
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { email: 'test@example.com', password: 'password123' }
      
      // Act
      const user = await userService.createUser(userData)
      
      // Assert
      expect(user.id).toBeDefined()
      expect(user.email).toBe(userData.email)
    })
    
    it('should throw error with invalid email', async () => {
      // Arrange
      const userData = { email: 'invalid', password: 'password123' }
      
      // Act & Assert
      await expect(userService.createUser(userData)).rejects.toThrow()
    })
  })
})
```

### Test Coverage
- **Unit tests**: 80%+ coverage
- **Integration tests**: Critical paths
- **E2E tests**: User flows

---

## 📝 Comments & Documentation

### When to Comment
```typescript
// ✅ GOOD - Explain WHY, not WHAT
// Using exponential backoff to avoid overwhelming the API
// after multiple failed requests
const retryWithBackoff = async (fn: Function, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      await sleep(Math.pow(2, i) * 1000)
    }
  }
}

// ❌ BAD - Obvious comments
// This function adds two numbers
const add = (a: number, b: number) => a + b
```

### JSDoc for Public APIs
```typescript
/**
 * Fetches user profile by ID
 * @param userId - The unique user identifier
 * @returns User profile data
 * @throws {NotFoundError} When user doesn't exist
 */
export const getUserProfile = async (userId: string): Promise<UserProfile> => {
  // Implementation
}
```

---

## 🔍 Code Review Checklist

### Before Submitting PR
- [ ] Code follows project conventions
- [ ] All tests pass
- [ ] No linter errors
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] No hardcoded secrets
- [ ] No console.logs in production code

### Reviewing Code
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Security vulnerabilities checked
- [ ] Performance considerations
- [ ] Code is readable
- [ ] Tests are adequate

---

## 🎨 Formatting Rules

### Prettier Config
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "avoid"
}
```

### ESLint Rules
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "prettier"
  ],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

---

## 🔍 Pattern Sources

**Cursor Agent**:
- Code quality emphasis
- Semantic understanding

**VSCode Agent**:
- Testing patterns
- Documentation standards

**Windsurf**:
- Security best practices
- Code review protocols

**Claude Code**:
- TypeScript patterns
- Error handling

---

## 📋 Implementation Checklist

- [ ] Setup Prettier + ESLint
- [ ] Configure pre-commit hooks (Husky)
- [ ] Define naming conventions
- [ ] Setup testing framework
- [ ] Create code review guidelines
- [ ] Document security practices
- [ ] Setup CI/CD for code quality checks

---

**Related Templates**:
- [Project Structure](./project-structure.md)
- [API Design](./api-design.md)
- [Database Schema](./database-schema.md)
