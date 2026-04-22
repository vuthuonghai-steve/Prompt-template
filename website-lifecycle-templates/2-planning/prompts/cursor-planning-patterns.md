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

## Planning Workflow

### Step 1: Analyze Request
```
User: Implement user registration, product catalog, shopping cart, checkout flow.