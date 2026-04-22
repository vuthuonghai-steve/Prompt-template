# Pattern: Debug Logging

## Problem
Không biết code đang chạy như thế nào, khó debug issues.

## Solution
Sử dụng debug logs để trace execution, inspect variables, identify issues.

**Core principles:**
- Use descriptive messages
- Include relevant context
- Log both success and errors
- Remove after issue resolved

## Example

### ✅ Good: Descriptive Debug Logs
```typescript
console.log("[v0] User data received:", userData)
console.log("[v0] API call starting with params:", params)
console.log("[v0] Component rendered with props:", props)
console.log("[v0] Error occurred in function:", error.message)
console.log("[v0] State updated:", newState)
```

### ❌ Bad: Vague Logs
```typescript
console.log("data")
console.log("error")
console.log("done")
```

## Debug Log Format

### Prefix Pattern
```typescript
// Use consistent prefix for easy filtering
console.log("[v0] ...")
console.log("[debug] ...")
console.log("[AI] ...")
```

### Include Context
```typescript
// ✅ Good: Context included
console.log("[v0] Fetching user:", { userId, endpoint })

// ❌ Bad: No context
console.log("fetching")
```

## When to Use

### Use Debug Logs For:
- Tracing execution flow
- Inspecting variable values
- Identifying issues
- Understanding state changes
- Debugging API calls

### Log These Events:
```typescript
// Data received
console.log("[v0] User data received:", userData)

// Operations starting
console.log("[v0] API call starting with params:", params)

// Component lifecycle
console.log("[v0] Component rendered with props:", props)

// Errors
console.log("[v0] Error occurred:", error.message)

// State changes
console.log("[v0] State updated:", newState)
```

## Best Practices

### 1. Descriptive Messages
```typescript
// ✅ Clear what you're checking
console.log("[v0] Checking authentication status:", isAuthenticated)

// ❌ Unclear
console.log("auth:", isAuthenticated)
```

### 2. Include Variable Values
```typescript
// ✅ Show actual values
console.log("[v0] User ID:", userId, "Role:", userRole)

// ❌ Just variable names
console.log("userId, userRole")
```

### 3. Log Object States
```typescript
// ✅ Full object for inspection
console.log("[v0] Current state:", {
  user: currentUser,
  isLoading,
  error,
})

// ❌ Partial info
console.log("state updated")
```

### 4. Error Context
```typescript
// ✅ Full error context
console.log("[v0] API Error:", {
  endpoint: "/api/users",
  status: error.status,
  message: error.message,
  data: error.response?.data,
})

// ❌ Just error message
console.log("error:", error.message)
```

## Cleanup

### Remove After Resolved
```typescript
// During debugging
console.log("[v0] Checking user data:", userData)

// After issue fixed
// [Remove the debug log]
```

### When to Keep
```typescript
// Keep for important events
console.error("Authentication failed:", error)
console.warn("Deprecated API used:", endpoint)
```

## Debug Workflow

```
Issue Detected
    ↓
Add Debug Logs
    ↓
Run Code
    ↓
Inspect Logs
    ↓
Identify Issue
    ↓
Fix Issue
    ↓
Verify Fix
    ↓
Remove Debug Logs
```

## Example Scenarios

### Scenario 1: API Call
```typescript
console.log("[v0] Starting API call:", {
  endpoint: "/api/users",
  method: "POST",
  data: requestData,
})

const response = await api.post("/api/users", requestData)

console.log("[v0] API response received:", {
  status: response.status,
  data: response.data,
})
```

### Scenario 2: State Update
```typescript
console.log("[v0] Before state update:", currentState)

setState(newState)

console.log("[v0] After state update:", newState)
```

### Scenario 3: Component Render
```typescript
function MyComponent({ userId, data }) {
  console.log("[v0] Component rendering with:", {
    userId,
    dataLength: data?.length,
    timestamp: Date.now(),
  })
  
  // ...component logic
}
```

## Anti-patterns
- ❌ Vague messages: "data", "error", "done"
- ❌ No context: console.log(value)
- ❌ Leaving debug logs after fix
- ❌ Logging sensitive data (passwords, tokens)

## Checklist
- [ ] Descriptive message?
- [ ] Relevant context included?
- [ ] Variable values shown?
- [ ] Clear what you're debugging?
- [ ] Will remove after fix?
- [ ] No sensitive data logged?

## Source
- v0 (Vercel) - "Debugging" section
- Windsurf Cascade - debugging best practices
