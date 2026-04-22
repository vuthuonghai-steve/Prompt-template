# Cursor Agent - Planning Patterns

> **Trích xuất từ Cursor Agent Prompt 2.0**
> **Focus**: Task breakdown, todo management, systematic planning

---

## Core Planning Philosophy

### Task Management Tool
```
You have access to the todo_write tool to help you manage and plan tasks.
Use these tools VERY frequently to ensure that you are tracking your tasks 
and giving the user visibility into your progress.

These tools are also EXTREMELY helpful for planning tasks, and for breaking 
down larger complex tasks into smaller steps. If you do not use this tool 
when planning, you may forget to do important tasks - and that is unacceptable.
```

### When to Use Todo List

**USE for**:
- Complex multi-step tasks (3+ distinct steps)
- Non-trivial tasks requiring careful planning
- User explicitly requests todo list
- User provides multiple tasks (numbered/comma-separated)
- After receiving new instructions - capture requirements as todos

**SKIP for**:
- Single, straightforward tasks
- Trivial tasks with no organizational benefit
- Tasks completable in < 3 trivial steps
- Purely conversational/informational requests

---

## Planning Workflow Example

### User Request
```
Implement user registration, product catalog, shopping cart, checkout flow.
```

### AI Response - Create Todo List
```
I'll help you implement a complete e-commerce system. Let me break this down:

1. User Registration [pending]
2. Product Catalog [pending]
3. Shopping Cart [pending]
4. Checkout Flow [pending]

Starting with User Registration...
```

### Task Breakdown Pattern
```
Complex features → Multiple smaller tasks
- User Registration
  → Database schema
  → API endpoints
  → Frontend forms
  → Validation
  → Email verification
```

---

## Task States

| State | When to Use |
|-------|-------------|
| `pending` | Not yet started |
| `in_progress` | Currently working on (ONLY ONE at a time) |
| `completed` | Finished successfully |
| `cancelled` | No longer needed |

---

## Best Practices

### 1. Immediate Task Creation
```
✅ GOOD:
User: Add dark mode
AI: [Creates todo list immediately]
    1. Add state management [in_progress]
    2. Implement styles [pending]
    3. Create toggle component [pending]
    [Starts working on task 1]

❌ BAD:
User: Add dark mode
AI: I'll add dark mode for you.
    [No todo list, starts coding]
```

### 2. Mark Complete Immediately
```
✅ GOOD:
[Completes task 1]
[Marks task 1 as completed]
[Marks task 2 as in_progress]
[Starts task 2]

❌ BAD:
[Completes tasks 1, 2, 3]
[Marks all as completed at once]
```

### 3. One Task In Progress
```
✅ GOOD:
1. Add state management [in_progress]
2. Implement styles [pending]
3. Create toggle [pending]

❌ BAD:
1. Add state management [in_progress]
2. Implement styles [in_progress]
3. Create toggle [in_progress]
```

---

## Planning Prompts

### Prompt 1: Break Down Complex Task
```
I need to [complex task]. Can you break this down into smaller, 
manageable steps with a clear implementation order?
```

### Prompt 2: Create Implementation Plan
```
Create a detailed implementation plan for [feature] including:
- Task breakdown
- Dependencies
- Estimated complexity
- Testing requirements
```

### Prompt 3: Prioritize Features
```
I have these features to implement: [list]. Help me prioritize them 
based on dependencies, complexity, and user value.
```

---

## Anti-Patterns to Avoid

### ❌ No Planning for Complex Tasks
```
User: Build a full authentication system
AI: [Starts coding immediately without planning]
```

### ❌ Vague Task Descriptions
```
❌ BAD: "Fix the app"
✅ GOOD: "Fix login form validation error on empty email"
```

### ❌ Too Many Tasks In Progress
```
❌ BAD: 5 tasks marked as in_progress
✅ GOOD: 1 task in_progress, others pending
```

---

## Integration with Development

### Planning → Implementation Flow
```
1. User Request
   ↓
2. Create Todo List (planning)
   ↓
3. Mark first task as in_progress
   ↓
4. Research/Gather context
   ↓
5. Implement task
   ↓
6. Mark complete
   ↓
7. Move to next task
```

---

**Key Takeaway**: Planning with todo lists prevents forgotten tasks and gives users visibility into progress.
