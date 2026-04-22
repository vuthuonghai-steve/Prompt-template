# Pattern: File Edit with Validation

## Problem
Edit files mà không validate → syntax errors, type errors, broken code.

## Solution
ALWAYS validate changes sau khi edit bằng get_errors/linter.

**Core principles:**
- Read file before editing
- Use minimal edit hints (comments for unchanged code)
- Validate immediately after edit
- Fix errors if relevant
- Maximum 3 iterations per file

## Example

### ✅ Good: Edit with Validation
```
Step 1: Read file
[Read Button.tsx to understand current structure]

Step 2: Edit with minimal hints
// ...existing imports...
import { Loader } from 'lucide-react'

export function Button({ loading, children, ...props }) {
  // ...existing code...
  return (
    <button {...props}>
      {loading && <Loader className="animate-spin" />}
      {children}
    </button>
  )
}

Step 3: Validate
[Call get_errors on Button.tsx]

Step 4: Fix if needed
[If errors found, fix them]

Step 5: Re-validate
[Confirm errors fixed]
```

### ❌ Bad: No Validation
```
Step 1: Edit file
[Make changes]

Step 2: Done
[No validation, may have broken code]
```

## Edit Format

### Use Comments for Unchanged Code
```typescript
// ❌ DON'T repeat entire file
import React from 'react'
import { cn } from '@/lib/utils'

export function Button({ className, children, ...props }) {
  return (
    <button className={cn("btn", className)} {...props}>
      {children}
    </button>
  )
}

// ✅ DO use comments
// ...existing imports...

export function Button({ className, loading, children, ...props }) {
  // ...existing code...
  return (
    <button className={cn("btn", className)} {...props}>
      {loading && <Loader />}
      {children}
    </button>
  )
}
```

## Validation Workflow

```
Edit File
    ↓
Call get_errors
    ↓
├─ No errors → Done ✅
│
└─ Has errors
    ↓
    ├─ Relevant to change? → Fix
    │   ↓
    │   Re-validate
    │   ↓
    │   Iteration count++
    │   ↓
    │   ├─ Fixed → Done ✅
    │   └─ Still errors
    │       ↓
    │       ├─ Iteration < 3 → Fix again
    │       └─ Iteration = 3 → Stop, ask user
    │
    └─ Not relevant → Done ✅
```

## Error Handling

### Relevant Errors (Fix)
```
Error: 'Loader' is not defined
Action: Add import statement
```

### Irrelevant Errors (Ignore)
```
Error: Unused variable 'oldFunction' in different file
Action: Ignore, not related to current change
```

## Best Practices

### 1. Read Before Edit
```typescript
// ALWAYS read file first to understand structure
[Read file]
[Understand current code]
[Make informed changes]
```

### 2. Group Changes by File
```typescript
// Edit all changes for one file at once
File: Button.tsx
- Add loading prop
- Add Loader icon
- Update styles
```

### 3. Use External Libraries
```typescript
// If popular library exists, use it
import { Loader } from 'lucide-react'  // ✅
// Don't create custom loader           // ❌
```

### 4. Follow Best Practices
```typescript
// Use proper package installation
npm install lucide-react

// Use TypeScript properly
interface ButtonProps {
  loading?: boolean
  children: React.ReactNode
}
```

## Maximum Iterations Rule

```
Iteration 1: Fix errors
    ↓
Iteration 2: Fix remaining errors
    ↓
Iteration 3: Final attempt
    ↓
If still errors → STOP and ask user
```

**Reason:** Prevent infinite loops, get user guidance.

## Tools by Language

| Language | Validation Tool |
|----------|----------------|
| TypeScript/JavaScript | get_errors, tsc, eslint |
| Python | get_errors, mypy, ruff |
| Go | go build, golint |
| Rust | cargo check |

## Anti-patterns
- ❌ Editing without reading first
- ❌ No validation after edit
- ❌ Repeating entire file content
- ❌ Looping > 3 times on same file
- ❌ Ignoring relevant errors

## Checklist
- [ ] Read file before editing?
- [ ] Used minimal edit hints?
- [ ] Called get_errors after edit?
- [ ] Fixed relevant errors?
- [ ] Re-validated after fix?
- [ ] Stopped at 3 iterations?

## Source
- Cursor Agent Prompt 2.0 - editFileInstructions
- VSCode Agent - "After editing, MUST call get_errors"
- Windsurf Cascade - making_code_changes
