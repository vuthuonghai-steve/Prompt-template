# Pattern: Memory System

## Problem
AI cần nhớ context, preferences, và decisions qua nhiều conversations. Không có memory → lặp lại mistakes.

## Solution
Persistent memory system để lưu trữ important context cho future reference.

**Core principles:**
- Proactively save important information
- Don't wait for user permission
- Save from both failure AND success
- Update or remove stale memories

## Example

### ✅ Good: Proactive Memory Creation
```
User: "I've been writing Go for ten years but this is my first time touching the React side"

AI Action:
- Save memory: "User has deep Go expertise, new to React"
- Type: user
- Use: Frame frontend explanations in terms of backend analogues
```

### ✅ Good: Learning from Corrections
```
User: "Don't mock the database in these tests — we got burned last quarter"

AI Action:
- Save memory: "Integration tests must hit real database, not mocks"
- Type: feedback
- Why: Prior incident where mock/prod divergence masked broken migration
```

### ✅ Good: Learning from Success
```
User: "Yeah the single bundled PR was the right call here"

AI Action:
- Save memory: "For refactors in this area, user prefers one bundled PR"
- Type: feedback
- Why: Validated judgment call, not a correction
```

## Memory Types

| Type | When to Save | Example |
|------|-------------|---------|
| **user** | User's role, preferences, knowledge | "User is data scientist, focused on logging" |
| **feedback** | Corrections OR confirmations | "Don't use mocks for DB tests" |
| **project** | Ongoing work, goals, deadlines | "Merge freeze begins 2026-03-05" |
| **reference** | External system pointers | "Bugs tracked in Linear project INGEST" |

## When to Save

### Save Immediately When:
- User corrects your approach
- User confirms non-obvious approach worked
- Learn about user's role/expertise
- Discover project constraints/deadlines
- Find external system references

### Don't Save:
- Code patterns (derive from current state)
- Git history (use git log)
- Debugging solutions (in the code)
- Ephemeral task details
- Anything in CLAUDE.md

## Memory Structure

```markdown
---
name: feedback_testing
description: Integration tests must use real database
type: feedback
---

Integration tests must hit a real database, not mocks.

**Why:** Prior incident where mock/prod divergence masked a broken migration.

**How to apply:** When writing tests for database operations, always use real DB connection.
```

## Anti-patterns
- ❌ Only saving corrections (miss validated approaches)
- ❌ Waiting until end of conversation
- ❌ Saving code snippets (should be in codebase)
- ❌ Creating duplicate memories

## Source
- Windsurf Cascade - memory_system section
- Claude Code - auto memory system
