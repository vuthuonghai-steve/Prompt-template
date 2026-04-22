# Windsurf - Refactor Prompt

> Source: Windsurf Cascade Prompt (Wave 11)
> Phase: Development
> Use Case: Code refactoring with AI Flow paradigm

---

## 🎯 Prompt Purpose

Leverage Windsurf's agentic capabilities for autonomous code refactoring and optimization.

---

## 📋 Prompt Template

```
I need to refactor [COMPONENT/MODULE/FEATURE] in my codebase.

Current Issues:
- [Issue 1: e.g., Performance bottleneck]
- [Issue 2: e.g., Code duplication]
- [Issue 3: e.g., Poor maintainability]

Goals:
1. [Goal 1: e.g., Improve performance by 50%]
2. [Goal 2: e.g., Reduce code duplication]
3. [Goal 3: e.g., Better type safety]

Context:
- Tech stack: [React, TypeScript, etc.]
- Current architecture: [Brief description]
- Constraints: [Any limitations]

Please:
1. Analyze the current implementation
2. Identify refactoring opportunities
3. Propose a refactoring plan
4. Implement changes autonomously
5. Ensure all tests pass
6. Update documentation

Requirements:
- Maintain backward compatibility
- Keep existing API contracts
- Add tests for new code
- Follow project conventions
```

---

## 💡 Example Usage

### Example 1: Performance Optimization
```
I need to refactor the ProductList component - it's rendering slowly with 1000+ items.

Current Issues:
- Re-renders entire list on any state change
- No virtualization for long lists
- Expensive calculations in render
- Fetching all data at once

Goals:
1. Reduce initial render time by 70%
2. Implement virtual scrolling
3. Add pagination or infinite scroll
4. Optimize data fetching

Context:
- Tech stack: React 18, TypeScript, React Query
- Current: Fetches all products, renders in single list
- Constraints: Must maintain current UI/UX

Please:
1. Analyze current ProductList implementation
2. Identify performance bottlenecks
3. Propose optimization strategy
4. Implement:
   - React.memo for list items
   - Virtual scrolling (react-window)
   - Pagination with React Query
   - Memoized calculations
5. Run performance tests
6. Update component documentation

Requirements:
- Keep current props API
- Maintain accessibility
- Add loading states
- Test with 10,000 items
```

### Example 2: Architecture Refactor
```
I need to refactor our authentication system - it's scattered across multiple files with duplicated logic.

Current Issues:
- Auth logic duplicated in 5+ components
- No centralized token management
- Inconsistent error handling
- Hard to test

Goals:
1. Centralize auth logic in a service
2. Create reusable auth hooks
3. Standardize error handling
4. Improve testability

Context:
- Tech stack: Next.js 14, TypeScript, JWT
- Current: Auth logic in components, localStorage for tokens
- Constraints: Can't change API endpoints

Please:
1. Search codebase for all auth-related code
2. Design new auth architecture:
   - AuthService for API calls
   - useAuth hook for components
   - AuthContext for global state
   - Token refresh mechanism
3. Implement refactored system
4. Migrate existing components
5. Add comprehensive tests
6. Update documentation

Requirements:
- Zero downtime migration
- Backward compatible during transition
- 90%+ test coverage
- Type-safe throughout
```

---

## 🔧 Key Features

### 1. Autonomous Execution
Windsurf works independently until task completion:
```
"Refactor the user service to use dependency injection"
→ Windsurf:
  1. Analyzes current implementation
  2. Designs DI pattern
  3. Refactors code
  4. Updates tests
  5. Runs test suite
  6. Reports completion
```

### 2. Memory System
Windsurf remembers project context:
```
First session: "We use Zod for validation"
Later session: "Add validation to the new endpoint"
→ Windsurf automatically uses Zod (remembers preference)
```

### 3. Multi-Step Planning
Windsurf creates and executes plans:
```
Task: "Migrate from REST to GraphQL"
→ Plan:
  1. Setup Apollo Server
  2. Define GraphQL schema
  3. Create resolvers
  4. Update frontend queries
  5. Add error handling
  6. Write tests
  7. Update docs
→ Executes each step autonomously
```

---

## 📝 Best Practices

### DO ✅
- Provide clear refactoring goals
- Specify performance targets
- Mention constraints upfront
- Let Windsurf work autonomously
- Review changes after completion

### DON'T ❌
- Micromanage each step
- Interrupt during execution
- Give conflicting requirements
- Skip context about current state

---

## 🎨 Advanced Patterns

### Pattern 1: Incremental Refactor
```
Phase 1: "Refactor UserService to use async/await instead of callbacks"
Phase 2: "Now add error handling with custom error classes"
Phase 3: "Add retry logic with exponential backoff"
```

### Pattern 2: Test-Driven Refactor
```
Step 1: "Write comprehensive tests for current UserService behavior"
Step 2: "Refactor UserService to use dependency injection while keeping tests green"
Step 3: "Add new features now that we have good test coverage"
```

### Pattern 3: Safe Migration
```
Step 1: "Create new AuthServiceV2 alongside existing AuthService"
Step 2: "Migrate components one by one to use AuthServiceV2"
Step 3: "Once all migrated, remove old AuthService"
```

---

## 🔍 When to Use This Prompt

✅ **Use when**:
- Large-scale refactoring needed
- Performance optimization required
- Architecture changes
- Code quality improvements
- Technical debt reduction

❌ **Don't use when**:
- Simple one-line changes
- Just need code explanation
- Exploring options (use planning mode)

---

## 📊 Expected Output

Windsurf will:
1. Analyze current codebase
2. Create refactoring plan
3. Execute changes autonomously
4. Run tests to verify
5. Update documentation
6. Provide summary of changes

---

## 🎯 Refactoring Checklist

After Windsurf completes refactoring:
- [ ] All tests pass
- [ ] No linter errors
- [ ] Performance improved (if applicable)
- [ ] Documentation updated
- [ ] No breaking changes (unless intended)
- [ ] Code follows project conventions
- [ ] Git history is clean

---

**Related Prompts**:
- [Cursor Coding Prompt](./cursor-coding-prompt.md)
- [VSCode Debug Prompt](./vscode-debug-prompt.md)
