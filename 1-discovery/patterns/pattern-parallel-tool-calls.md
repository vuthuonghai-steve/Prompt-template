# Pattern: Parallel Tool Calls

## Problem
Sequential tool calls làm chậm workflow. Nhiều operations có thể chạy đồng thời.

## Solution
Gọi multiple tools cùng lúc khi chúng independent (không phụ thuộc lẫn nhau).

**Core principles:**
- Maximize parallel execution
- Only sequential when dependencies exist
- Never use placeholders for missing parameters

## Example

### ✅ Good: Parallel Reads
```typescript
// Reading 3 independent files
Parallel:
- Read("src/components/Button.tsx")
- Read("src/utils/helpers.ts")
- Read("src/types/index.ts")

Reason: No dependencies between reads
```

### ❌ Bad: Sequential When Could Be Parallel
```typescript
// DON'T do this
Step 1: Read("Button.tsx")
Wait for result...
Step 2: Read("helpers.ts")
Wait for result...
Step 3: Read("types/index.ts")

Reason: Wasting time, should run in parallel
```

### ✅ Good: Sequential When Dependencies Exist
```typescript
Step 1: Search for "AuthService"
Wait for result → found in "auth/service.ts"

Step 2: Read("auth/service.ts")
Wait for content...

Step 3: Edit based on content

Reason: Each step depends on previous result
```

## When to Use
- Reading multiple files
- Multiple independent searches
- Gathering context from different sources
- Running multiple git commands (git status + git diff)

## When NOT to Use
- Tool calls with dependencies
- When parameters depend on previous results
- Semantic search (should not run in parallel per Cursor docs)

## Decision Matrix

| Scenario | Approach |
|----------|----------|
| Read 3 unrelated files | ✅ Parallel |
| Search + Read result | ❌ Sequential |
| git status + git diff | ✅ Parallel |
| Search → Narrow search | ❌ Sequential |
| Multiple grep patterns | ✅ Parallel |

## Anti-patterns
- ❌ Using placeholders for missing params
- ❌ Running semantic_search in parallel
- ❌ Parallel when dependencies exist

## Source
- Cursor Agent Prompt 2.0
- v0 (Vercel) - "Use Parallel Tool Calls Where Possible"
- Lovable - "MAXIMIZE EFFICIENCY"
