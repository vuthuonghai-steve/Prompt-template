# Cursor Agent - Coding Prompt

> Source: Cursor Agent Prompt 2.0
> Phase: Development
> Use Case: Code implementation with semantic understanding

---

## 🎯 Prompt Purpose

Leverage Cursor's semantic search and codebase understanding for intelligent code implementation.

---

## 📋 Prompt Template

```
I need to implement [FEATURE/FIX] in my codebase.

Context:
- Project type: [React/Node.js/Full-stack/etc.]
- Tech stack: [TypeScript, Next.js, Prisma, etc.]
- Current state: [Brief description of existing code]

Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

Please:
1. Search the codebase to understand existing patterns
2. Identify relevant files and functions
3. Propose implementation following project conventions
4. Ensure code is immediately runnable
5. Add necessary imports and dependencies

Constraints:
- Follow existing naming conventions
- Match current code style
- Maintain type safety
- Add appropriate error handling
```

---

## 💡 Example Usage

### Example 1: Add Authentication
```
I need to implement JWT authentication in my Express API.

Context:
- Project: Node.js + Express + TypeScript
- Database: PostgreSQL with Prisma
- Current state: Basic user CRUD exists

Requirements:
1. Login endpoint with email/password
2. JWT token generation
3. Auth middleware for protected routes
4. Token refresh mechanism

Please:
1. Search for existing user model and routes
2. Identify where to add auth logic
3. Implement following REST conventions
4. Add proper error handling
5. Include validation

Constraints:
- Use bcrypt for password hashing
- JWT secret from environment variable
- Token expiry: 1 hour
- Refresh token expiry: 7 days
```

### Example 2: Refactor Component
```
I need to refactor the UserProfile component to use React Query.

Context:
- Project: Next.js 14 + TypeScript
- Current state: Using useEffect + fetch
- API: RESTful endpoints at /api/users

Requirements:
1. Replace useEffect with useQuery
2. Add loading and error states
3. Implement optimistic updates
4. Add mutation for profile updates

Please:
1. Search for similar React Query usage in codebase
2. Identify the UserProfile component
3. Refactor following existing patterns
4. Maintain current UI/UX
5. Add proper TypeScript types

Constraints:
- Keep component structure similar
- Don't break existing tests
- Follow project's React Query config
```

---

## 🔧 Key Features

### 1. Semantic Search
Cursor understands code meaning, not just text matching:
```
"Where is user authentication handled?"
→ Finds auth middleware, login routes, JWT logic

"How do we handle errors in API calls?"
→ Finds error handling patterns across services
```

### 2. Context-Aware Suggestions
Cursor analyzes existing code to suggest consistent patterns:
- Naming conventions
- Import styles
- Error handling patterns
- Testing approaches

### 3. Multi-File Edits
Cursor can propose changes across multiple files:
```
"Add a new Product model with CRUD operations"
→ Creates:
  - models/product.model.ts
  - services/product.service.ts
  - routes/product.routes.ts
  - controllers/product.controller.ts
```

---

## 📝 Best Practices

### DO ✅
- Provide clear context about project structure
- Specify tech stack and frameworks
- Mention existing patterns to follow
- Ask Cursor to search codebase first
- Request type-safe implementations

### DON'T ❌
- Give vague requirements
- Skip context about existing code
- Ask for code without understanding current patterns
- Request changes without specifying constraints

---

## 🎨 Advanced Patterns

### Pattern 1: Explore Then Implement
```
Step 1: "Search the codebase for how we handle API errors"
Step 2: "Now implement error handling for the new payment service following the same pattern"
```

### Pattern 2: Understand Then Refactor
```
Step 1: "Explain how the current authentication flow works"
Step 2: "Refactor it to use refresh tokens while maintaining the same API"
```

### Pattern 3: Find Similar Then Create
```
Step 1: "Find examples of React components using form validation"
Step 2: "Create a new UserRegistration component following the same validation pattern"
```

---

## 🔍 When to Use This Prompt

✅ **Use when**:
- Implementing new features
- Refactoring existing code
- Need to follow existing patterns
- Working with unfamiliar codebase
- Want consistent code style

❌ **Don't use when**:
- Simple text search is enough
- Creating new project from scratch
- No existing patterns to follow

---

## 📊 Expected Output

Cursor will:
1. Search codebase for relevant patterns
2. Identify files to modify/create
3. Propose implementation with:
   - Proper imports
   - Type definitions
   - Error handling
   - Following project conventions
4. Explain changes made

---

**Related Prompts**:
- [Windsurf Refactor Prompt](./windsurf-refactor-prompt.md)
- [VSCode Agent Debug Prompt](./vscode-debug-prompt.md)
