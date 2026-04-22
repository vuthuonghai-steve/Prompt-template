# Pattern: Todo/Task Management

## Problem
Complex tasks cần tracking progress. Không có todo list → quên steps, user không thấy progress.

## Solution
Sử dụng todo/task management system để plan và track work.

**Core principles:**
- Create todos for complex multi-step tasks
- Mark completed IMMEDIATELY after finishing
- Only ONE task in_progress at a time
- Update in real-time

## Example

### ✅ Good: Multi-Step Feature
```
User: "Add dark mode toggle to settings"

AI Action:
1. Create todo list:
   - Add state management [in_progress]
   - Implement styles [pending]
   - Create toggle component [pending]
   - Update components [pending]

2. Start working on task 1 immediately
3. Mark task 1 completed when done
4. Move to task 2
```

### ✅ Good: Complex Refactoring
```
User: "Refactor authentication to use new useAuth hook"

AI Action:
1. Enter plan mode to explore codebase
2. Create systematic todo list:
   - Update Core Auth Hook
   - Refactor Login Components (5 files)
   - Update Dashboard Components (10 files)
   - Update API Integration
   - Test Auth Flow

3. Work through todos one by one
4. Mark each completed immediately
```

### ❌ Bad: Simple Task
```
User: "Add comment to calculateTotal function"

AI Action:
❌ Don't create todo
✅ Just add the comment directly
```

## When to Use

### Create Todos For:
- Complex multi-step tasks (3+ steps)
- Non-trivial tasks requiring planning
- User provides multiple tasks
- After receiving new instructions
- When starting/completing tasks

### Skip Todos For:
- Single straightforward tasks
- Trivial tasks (< 3 steps)
- Purely conversational requests
- Operational actions (linting, testing, searching)

## Task States

```
pending → in_progress → completed
                     ↘ cancelled
```

## Best Practices

1. **Create early**: After understanding requirements
2. **Update frequently**: Mark in_progress when starting
3. **Complete immediately**: Don't batch completions
4. **One at a time**: Only one task in_progress
5. **Parallel writes**: Batch todo updates with other tool calls

## Anti-patterns
- ❌ Creating todos for simple tasks
- ❌ Batching multiple completions
- ❌ Multiple tasks in_progress
- ❌ Including operational actions (linting, testing)
- ❌ Forgetting to mark completed

## Source
- Cursor Agent Prompt 2.0 - task_management
- Claude Code - Task Management
- Lovable - implicit task tracking
