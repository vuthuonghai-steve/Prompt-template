# Pattern: Plan Mode

## Problem
Large/complex tasks cần detailed planning trước khi implement. Jumping straight to code → mistakes.

## Solution
Enter "plan mode" để explore, analyze, và create comprehensive plan for user approval.

**Core principles:**
- Use for significant refactoring or large features
- Explore codebase thoroughly during planning
- Get user approval before implementation
- Create actionable, specific plans

## Example

### ✅ Good: Authentication Refactoring
```
User: "Refactor our authentication system to use the new useAuth hook"

AI Action:
Step 1: Enter Plan Mode
- Explore codebase
- Find all AuthContext usage (15+ components)
- Analyze dependencies
- Identify risks

Step 2: Create Plan
1. Update Core Auth Hook
2. Refactor Login Components (5 files)
3. Update Dashboard Components (10 files)
4. Update API Integration
5. Test Auth Flow

Step 3: Get User Approval
[Present plan, wait for approval]

Step 4: Implementation
- Create todo list from plan
- Execute step by step
```

### ✅ Good: Full-Stack App
```
User: "Build me a full-stack app for managing my business"

AI Action:
Step 1: Enter Plan Mode
- Ask clarifying questions:
  - What type of business?
  - Required features?
  - Authentication needs?

Step 2: Create Detailed Plan
[Based on user answers]

Step 3: Get Approval
[Iterate on plan if needed]

Step 4: Implementation
[Follow approved plan]
```

### ❌ Bad: Simple Task
```
User: "Update button color to blue"

AI Action:
❌ Don't enter plan mode
✅ Just update the color directly
```

## When to Use

### Enter Plan Mode For:
- Large features (full-stack apps)
- Significant refactoring (15+ files)
- Complex system changes
- Unclear requirements
- Multiple possible approaches

### Skip Plan Mode For:
- Simple changes
- Clear, straightforward tasks
- Single file edits
- Bug fixes (unless complex)

## Plan Structure

```markdown
## Goal
[What we're trying to achieve]

## Current State Analysis
[What exists now]

## Proposed Approach
1. [Step 1 with details]
2. [Step 2 with details]
3. [Step 3 with details]

## Files to Change
- file1.ts: [what changes]
- file2.ts: [what changes]

## Risks/Considerations
- [Risk 1]
- [Risk 2]

## Testing Strategy
[How to verify]
```

## Best Practices

1. **Explore first**: Use search tools during planning
2. **Be specific**: List exact files and changes
3. **Ask questions**: Clarify unclear requirements
4. **Get approval**: Wait for user confirmation
5. **Create todos**: Convert plan to actionable tasks

## Anti-patterns
- ❌ Planning without exploration
- ❌ Vague plans ("update auth system")
- ❌ Starting implementation before approval
- ❌ Using plan mode for simple tasks

## Source
- v0 (Vercel) - EnterPlanMode examples
- Windsurf Cascade - planning section
- Lovable - "THINK & PLAN" workflow
