# Pattern: Immediately Runnable Code

## Problem
Generated code không chạy được ngay → missing imports, dependencies, endpoints.

## Solution
Code MUST be immediately runnable by user. Add ALL necessary dependencies.

**Core principles:**
- Add all import statements
- Include all dependencies
- Add all endpoints
- Create dependency files (package.json, requirements.txt)
- No placeholders or TODOs

## Example

### ❌ Bad: Missing Dependencies
```typescript
// DON'T do this
export function Button() {
  return <button>Click</button>
}
// Missing: React import, types, styles
```

### ✅ Good: Complete Implementation
```typescript
// All imports included
import React from 'react'
import { cn } from '@/lib/utils'
import { ButtonProps } from '@/types'

export function Button({ className, children, ...props }: ButtonProps) {
  return (
    <button 
      className={cn(
        "px-4 py-2 rounded-md bg-primary text-primary-foreground",
        className
      )} 
      {...props}
    >
      {children}
    </button>
  )
}
```

## Checklist for Runnable Code

### 1. Import Statements
```typescript
// ✅ Include ALL imports
import React from 'react'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'
import type { User } from '@/types'
```

### 2. Dependencies
```json
// package.json
{
  "dependencies": {
    "react": "^19.0.0",
    "next": "^15.0.0",
    "lucide-react": "^0.263.1"
  }
}
```

### 3. API Endpoints
```typescript
// ✅ Define all endpoints
const API_BASE = process.env.NEXT_PUBLIC_API_URL

export const endpoints = {
  users: `${API_BASE}/users`,
  products: `${API_BASE}/products`,
  orders: `${API_BASE}/orders`,
}
```

### 4. Types
```typescript
// ✅ Define all types
export interface User {
  id: string
  name: string
  email: string
}

export interface Product {
  id: string
  name: string
  price: number
}
```

### 5. Environment Variables
```bash
# .env.example
NEXT_PUBLIC_API_URL=http://localhost:3000/api
DATABASE_URL=postgresql://...
```

## Creating from Scratch

### New Project Checklist
```
✅ Dependency management file
   - package.json (Node.js)
   - requirements.txt (Python)
   - Cargo.toml (Rust)
   - go.mod (Go)

✅ README.md
   - Setup instructions
   - How to run
   - Environment variables

✅ Configuration files
   - tsconfig.json
   - .eslintrc
   - tailwind.config.ts

✅ Entry point
   - index.ts
   - main.py
   - main.go
```

### Web App Checklist
```
✅ Beautiful, modern UI
✅ Best UX practices
✅ Responsive design
✅ Proper error handling
✅ Loading states
✅ Accessibility (ARIA)
```

## API Integration

### ✅ Complete API Setup
```typescript
// lib/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error)
  }
)

export { api }
```

## Security Best Practices

### ✅ Secure Implementation
```typescript
// ✅ Use environment variables
const apiKey = process.env.API_KEY

// ❌ NEVER hardcode secrets
const apiKey = "sk-1234567890"

// ✅ Validate input
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

// ✅ Sanitize output
const sanitized = DOMPurify.sanitize(userInput)
```

## Anti-patterns
- ❌ Missing imports
- ❌ Undefined dependencies
- ❌ Hardcoded API URLs
- ❌ Missing types
- ❌ No error handling
- ❌ Placeholder comments (// TODO)
- ❌ Incomplete implementations

## Validation

### Before Submitting Code
- [ ] All imports added?
- [ ] Dependencies in package.json?
- [ ] API endpoints defined?
- [ ] Types defined?
- [ ] Error handling included?
- [ ] No TODOs or placeholders?
- [ ] Can run immediately?

## Source
- Windsurf Cascade - "EXTREMELY IMPORTANT: Your generated code must be immediately runnable"
- Cursor Agent Prompt 2.0 - making_code_changes
- Replit - "Focus on user's request, adhere to existing patterns"
