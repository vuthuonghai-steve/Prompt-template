# Pattern: Test-Driven Validation

## Problem
Code changes không được test → regressions, broken features.

## Solution
Validate changes bằng tests. Run lint/typecheck commands sau khi implement.

**Core principles:**
- NEVER assume test framework
- Check README or search codebase for test commands
- Run lint + typecheck after changes
- Fix errors before claiming complete
- Suggest adding to CLAUDE.md if commands not found

## Example

### ✅ Good: Complete Validation
```
Step 1: Implement feature
[Make code changes]

Step 2: Find test commands
[Check package.json scripts]
Found:
- npm run lint
- npm run typecheck
- npm test

Step 3: Run validation
npm run lint
npm run typecheck
npm test

Step 4: Fix errors if any
[Fix linting errors]
[Fix type errors]
[Fix failing tests]

Step 5: Re-run validation
[Confirm all pass]
```

### ❌ Bad: No Validation
```
Step 1: Implement feature
[Make code changes]

Step 2: Done
[No testing, may have broken things]
```

## Finding Test Commands

### 1. Check package.json
```json
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit"
  }
}
```

### 2. Search README
```bash
# Look for test instructions
grep -i "test" README.md
grep -i "lint" README.md
```

### 3. Search Codebase
```bash
# Find test files
find . -name "*.test.ts"
find . -name "*.spec.ts"

# Find config files
find . -name "vitest.config.ts"
find . -name "jest.config.js"
```

## Validation Workflow

```
Code Changes Complete
    ↓
Find Test Commands
    ↓
├─ Commands Found
│   ↓
│   Run: lint + typecheck + test
│   ↓
│   ├─ All Pass → Done ✅
│   │
│   └─ Errors Found
│       ↓
│       Fix Errors
│       ↓
│       Re-run Tests
│       ↓
│       Confirm Pass ✅
│
└─ Commands Not Found
    ↓
    Ask User for Commands
    ↓
    Suggest Adding to CLAUDE.md
```

## Common Test Commands

| Framework | Commands |
|-----------|----------|
| Vitest | `npm run test`, `vitest --run` |
| Jest | `npm test`, `jest` |
| Playwright | `npx playwright test` |
| Cypress | `npm run cypress` |
| ESLint | `npm run lint`, `eslint .` |
| TypeScript | `tsc --noEmit`, `npm run typecheck` |
| Python | `pytest`, `python -m pytest` |
| Go | `go test ./...` |
| Rust | `cargo test` |

## What to Validate

### 1. Linting
```bash
# JavaScript/TypeScript
npm run lint
eslint .

# Python
ruff check .
flake8 .

# Go
golint ./...
```

### 2. Type Checking
```bash
# TypeScript
tsc --noEmit
npm run typecheck

# Python
mypy .

# Go
go build ./...
```

### 3. Unit Tests
```bash
# JavaScript/TypeScript
npm test
vitest --run

# Python
pytest

# Go
go test ./...
```

### 4. Integration Tests
```bash
# E2E tests
npx playwright test
npm run test:e2e
```

## Error Handling

### Fix Relevant Errors
```
Error: Unused variable 'oldFunction'
Action: Remove unused variable

Error: Type 'string' not assignable to 'number'
Action: Fix type mismatch

Error: Test failed: expected 200, got 404
Action: Fix API endpoint or test
```

### Ignore Unrelated Errors
```
Error: Linting error in unrelated file
Action: Note it, but don't fix (out of scope)
```

## Best Practices

### 1. Run All Validations
```bash
# Don't skip any
npm run lint && npm run typecheck && npm test
```

### 2. Fix Before Claiming Complete
```
❌ "Feature complete" (but tests failing)
✅ "Feature complete, all tests passing"
```

### 3. Document Commands
```markdown
# CLAUDE.md
## Testing
- Lint: `npm run lint`
- Typecheck: `npm run typecheck`
- Test: `npm test`
```

### 4. Use Fast Mode for Quick Checks
```bash
# Use --run flag for single execution
vitest --run  # Not vitest --watch
```

## When Commands Not Found

### Ask User
```
I've implemented the feature. What commands should I run to validate?
- Lint command?
- Typecheck command?
- Test command?
```

### Suggest Documentation
```
Would you like me to add these commands to CLAUDE.md 
so I'll know to run them next time?
```

## Anti-patterns
- ❌ Assuming test framework (jest vs vitest)
- ❌ Not running tests after changes
- ❌ Claiming complete with failing tests
- ❌ Using watch mode (--watch) in validation
- ❌ Skipping typecheck

## Checklist
- [ ] Found test commands?
- [ ] Ran lint?
- [ ] Ran typecheck?
- [ ] Ran tests?
- [ ] All passing?
- [ ] Fixed relevant errors?
- [ ] Documented commands if needed?

## Source
- Claude Code - "VERY IMPORTANT: run lint and typecheck commands"
- Cursor Agent Prompt 2.0 - "After editing, MUST call get_errors"
- VSCode Agent - "After editing, use get_errors to validate"
