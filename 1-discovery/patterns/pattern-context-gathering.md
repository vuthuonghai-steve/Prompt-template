# Pattern: Context Gathering

## Problem
Cần hiểu đầy đủ codebase trước khi thực hiện thay đổi. Thiếu context dẫn đến sai lầm.

## Solution
Thu thập context một cách có hệ thống: broad → specific → verify relationships.

**Core principles:**
- Don't stop at the first match
- Examine ALL relevant files
- Understand the full system before making changes

## Example

### Layout Issue Investigation
```
Step 1: Check parents, wrappers, global styles FIRST
Step 2: Check component variants
Step 3: Check theme systems, utility classes
Step 4: Verify relationships

❌ Don't: Jump to editing the component immediately
✅ Do: Understand the layout hierarchy first
```

### Adding New Feature
```
Step 1: Find existing similar implementations
Step 2: Check existing patterns and conventions
Step 3: Look for existing utilities (may already exist)
Step 4: Follow the established pattern

❌ Don't: Create new pattern without checking existing
✅ Do: Follow existing patterns for consistency
```

### State Changes
```
Step 1: Trace where state actually lives
Step 2: Understand state flow
Step 3: Check parent components
Step 4: Verify data dependencies

❌ Don't: Modify state without understanding flow
✅ Do: Trace the complete state lifecycle
```

## When to Use
- Before making ANY code changes
- When encountering unfamiliar code
- When debugging issues
- When adding new features

## Checklist Before Changes
- [ ] Is this the right file among multiple options?
- [ ] Does a parent/wrapper already handle this?
- [ ] Are there existing utilities/patterns I should use?
- [ ] How does this fit into the broader architecture?

## Anti-patterns
- ❌ Stopping at first search result
- ❌ Assuming without verifying
- ❌ Skipping parent component checks
- ❌ Not checking for existing utilities

## Source
- v0 (Vercel) - Context Gathering section
- Lovable - "CHECK USEFUL-CONTEXT FIRST"
- Cursor - "maximize_context_understanding"
