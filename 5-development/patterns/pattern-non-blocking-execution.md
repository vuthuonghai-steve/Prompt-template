# Pattern: Non-Blocking Execution

## Problem
Dừng workflow để chờ user response → slow, inefficient.

## Solution
Tiếp tục execution với reasonable assumptions, ask questions non-blocking.

**Core principles:**
- Never stop execution to wait
- Use /btw for short questions (< 10 words)
- Spawn background tasks for complex questions
- Continue with reasonable assumptions

## Example

### ❌ Bad: Blocking Execution
```
User: "Add password validation"

AI: "What is the password policy?"
[STOPS and WAITS for user response]
```

### ✅ Good: Non-Blocking
```
User: "Add password validation"

AI: 
/btw What is the current password policy?

[CONTINUES working with reasonable assumption]
- Minimum 8 characters
- At least 1 uppercase
- At least 1 number
- At least 1 special character

[Implements validation with assumption]
[Will adjust when user responds]
```

### ✅ Good: Background Task
```
User: "Refactor authentication system"

AI:
[Spawns background task: "Research current auth patterns"]
[Continues with main workflow]
[Merges background results when ready]
```

## When to Use

### Use /btw For:
- Short clarifying questions (< 10 words)
- Non-critical information
- Nice-to-have details

### Spawn Background Task For:
- Complex research questions
- Long-running investigations
- Parallel information gathering

### Continue with Assumptions For:
- Standard patterns (password validation)
- Best practices (error handling)
- Common conventions (naming)

## Workflow Pattern

```
[User Request]
    ↓
[Assess Info Completeness]
    ↓
├─ Info Complete → Execute
│
└─ Info Incomplete
    ↓
    ├─ Ask Non-Blocking (/btw or background task)
    ├─ Log assumptions
    ├─ Continue main workflow
    │
    └─ [Merge Response Later]
        ↓
        └─ Adapt if needed
```

## Example Scenarios

### Scenario 1: Password Policy
```typescript
// Assumption logged
// TODO: Verify password policy with user
const passwordSchema = z.string()
  .min(8, "Minimum 8 characters")
  .regex(/[A-Z]/, "At least 1 uppercase")
  .regex(/[0-9]/, "At least 1 number")
  .regex(/[^A-Za-z0-9]/, "At least 1 special character")

/btw What is the current password policy?
```

### Scenario 2: API Endpoint
```typescript
// Assumption: RESTful convention
const endpoint = "/api/users"

/btw Should this be /api/v1/users or /api/users?

// Continue implementing with assumption
```

### Scenario 3: Error Handling
```typescript
// Assumption: Standard error handling
try {
  await saveUser(data)
} catch (error) {
  toast.error("Failed to save user")
  console.error(error)
}

// Background task: Research existing error patterns
```

## Adaptive Response

### If Assumption Correct:
```
User: "Yes, that password policy is correct"

AI: ✅ Confirmed, continuing...
```

### If Assumption Wrong:
```
User: "No, we need minimum 12 characters"

AI: 
[Reverts changes]
[Updates with correct requirement]
[Re-validates]
```

## Anti-patterns
- ❌ Stopping execution to wait
- ❌ Long questions in /btw (> 10 words)
- ❌ Asking for standard best practices
- ❌ Not logging assumptions
- ❌ Not adapting when corrected

## Checklist
- [ ] Can I make reasonable assumption?
- [ ] Is question short enough for /btw?
- [ ] Should I spawn background task?
- [ ] Have I logged my assumptions?
- [ ] Can I continue main workflow?

## Source
- Claude Code - "Adaptive Workflow - Non-Blocking Questions"
- Windsurf Cascade - "keep working until resolved"
