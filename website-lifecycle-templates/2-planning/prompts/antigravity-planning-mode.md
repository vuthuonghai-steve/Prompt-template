# Antigravity - Planning Mode

> **Trích xuất từ Google Antigravity Planning Mode**
> **Focus**: Structured planning with artifacts, mode-based workflow

---

## Planning Mode Overview

### Three Modes
```
PLANNING → EXECUTION → VERIFICATION
```

### Mode Descriptions

#### PLANNING Mode
```
Research the codebase, understand requirements, and design your approach. 
Always create implementation_plan.md to document your proposed changes 
and get user approval.

If user requests changes to your plan, stay in PLANNING mode, update 
the same implementation_plan.md, and request review again via notify_user 
until approved.
```

#### EXECUTION Mode
```
Write code, make changes, implement your design. 
Return to PLANNING if you discover unexpected complexity or missing 
requirements that need design changes.
```

#### VERIFICATION Mode
```
Test your changes, run verification steps, validate correctness. 
Create walkthrough.md after completing verification to show proof of work.
```

---

## Planning Artifacts

### 1. task.md - Detailed Checklist

**Purpose**: Break down complex tasks into component-level items and track progress.

**Format**:
```markdown
## Authentication System

- [ ] Database schema
  - [ ] Users table
  - [ ] Sessions table
- [/] API endpoints (in progress)
  - [x] POST /auth/register
  - [/] POST /auth/login
  - [ ] POST /auth/logout
- [ ] Frontend components
  - [ ] Login form
  - [ ] Register form
```

**Notation**:
- `[ ]` = Uncompleted
- `[/]` = In progress
- `[x]` = Completed

---

### 2. implementation_plan.md - Technical Plan

**Purpose**: Document technical plan during PLANNING mode for user review.

**Structure**:
```markdown
# [Goal Description]

Brief description of the problem, background context, and what the change accomplishes.

## User Review Required

> [!IMPORTANT]
> Breaking change: Authentication tokens will expire after 24 hours instead of 7 days.

> [!WARNING]
> This requires database migration that will take ~5 minutes of downtime.

## Proposed Changes

### Authentication Module

#### [MODIFY] [auth.service.ts](file:///path/to/auth.service.ts)
- Add JWT token generation
- Implement refresh token logic
- Add password hashing with bcrypt

#### [NEW] [auth.middleware.ts](file:///path/to/auth.middleware.ts)
- Create authentication middleware
- Add role-based access control

#### [DELETE] [old-auth.js](file:///path/to/old-auth.js)
- Remove deprecated authentication logic

---

### Database Layer

#### [MODIFY] [schema.prisma](file:///path/to/schema.prisma)
- Add User model
- Add Session model
- Add refresh token fields

## Verification Plan

### Automated Tests
- Run `npm test` to verify all auth tests pass
- Run `npm run test:e2e` for end-to-end auth flow

### Manual Verification
- Test login flow in browser
- Verify token refresh works
- Test logout functionality
```

---

### 3. walkthrough.md - Post-Completion Summary

**Purpose**: After completing work, summarize what was accomplished.

**Structure**:
```markdown
# Authentication System Implementation

## Changes Made

### Backend
- Implemented JWT-based authentication
- Added refresh token mechanism
- Created role-based access control middleware

### Database
- Added Users and Sessions tables
- Implemented migration scripts

### Frontend
- Created login and register forms
- Added authentication state management
- Implemented protected routes

## What Was Tested

### Automated Tests
- ✅ All unit tests passing (45/45)
- ✅ Integration tests passing (12/12)
- ✅ E2E tests passing (8/8)

### Manual Verification
- ✅ User can register with email/password
- ✅ User can login and receive JWT token
- ✅ Token refresh works correctly
- ✅ Protected routes redirect to login
- ✅ Logout clears session

## Validation Results

- Performance: Login response time < 200ms ✅
- Security: Passwords hashed with bcrypt ✅
- UX: Error messages clear and helpful ✅

![Login Flow Demo](./screenshots/login-demo.gif)
```

---

## Task Boundary Tool

### Purpose
```
Communicate progress through a structured task UI.
Enter task view mode to give users clear visibility into progress 
without overwhelming them with every detail.
```

### When to Use
```
✅ USE: Complex work requiring multiple steps
❌ SKIP: Simple work (answering questions, quick refactors, single-file edits)
```

### Task Boundary Parameters

| Parameter | Description |
|-----------|-------------|
| **TaskName** | Header of UI block (e.g., "Planning Authentication") |
| **TaskSummary** | Description of goal and progress |
| **TaskStatus** | Current activity (what you're about to do) |
| **Mode** | PLANNING / EXECUTION / VERIFICATION |

### TaskName Granularity
```
Change TaskName when:
- Moving between major modes (Planning → Implementing → Verifying)
- Switching to fundamentally different component
- Starting new major activity

Keep same TaskName when:
- Backtracking mid-task
- Adjusting approach within same task
```

---

## Planning Workflow

### Step 1: Enter Planning Mode
```
task_boundary(
  TaskName="Planning Authentication System",
  TaskSummary="Designing JWT-based authentication with refresh tokens",
  TaskStatus="Researching existing auth patterns in codebase",
  Mode="PLANNING"
)
```

### Step 2: Research & Design
```
- Search codebase for existing auth code
- Review database schema
- Check third-party dependencies
- Design architecture
```

### Step 3: Create Implementation Plan
```
- Write implementation_plan.md
- Document proposed changes
- List all files to modify/create/delete
- Define verification plan
```

### Step 4: Request User Review
```
notify_user(
  Message="I've created an implementation plan for the authentication system. 
          Please review the proposed changes.",
  PathsToReview=["/path/to/implementation_plan.md"],
  ConfidenceScore=8,
  ConfidenceJustification="Plan follows best practices, but needs user approval 
                          for breaking changes",
  BlockedOnUser=true
)
```

### Step 5: Iterate if Needed
```
If user requests changes:
- Stay in PLANNING mode
- Update implementation_plan.md
- Request review again
- Repeat until approved
```

### Step 6: Move to Execution
```
Once approved:
task_boundary(
  TaskName="Implementing Authentication System",
  TaskSummary="Building JWT auth based on approved plan",
  TaskStatus="Setting up database schema",
  Mode="EXECUTION"
)
```

---

## Planning Prompts

### Prompt 1: Create Implementation Plan
```
I need to implement [feature]. Please:
1. Research the existing codebase
2. Design the architecture
3. Create a detailed implementation plan
4. List all files that need to be modified/created
5. Define how we'll verify the implementation
```

### Prompt 2: Review and Refine Plan
```
Here's my initial plan for [feature]. Please review and:
- Identify potential issues
- Suggest improvements
- Highlight risks
- Estimate complexity
```

### Prompt 3: Break Down into Phases
```
This feature is complex. Break it down into phases where:
- Each phase delivers value
- Phases can be tested independently
- Later phases build on earlier ones
```

---

## Best Practices

### 1. Always Create implementation_plan.md
```
✅ GOOD: Create plan → Get approval → Implement
❌ BAD: Start coding immediately
```

### 2. Use GitHub Alerts for Important Items
```markdown
> [!IMPORTANT]
> This change requires database migration

> [!WARNING]
> Breaking change: API response format will change

> [!CAUTION]
> This operation will delete user data
```

### 3. Link to Specific Files and Lines
```markdown
#### [MODIFY] [auth.service.ts](file:///absolute/path/to/auth.service.ts)
- Update [login function](file:///path/to/auth.service.ts#L45-L67)
```

### 4. Group Changes by Component
```markdown
## Proposed Changes

### Authentication Module
[Changes here]

---

### Database Layer
[Changes here]

---

### Frontend Components
[Changes here]
```

---

## Anti-Patterns

### ❌ Skipping Planning for Complex Tasks
```
User: Implement authentication system
AI: [Starts coding immediately]
```

### ❌ Not Getting User Approval
```
AI: [Creates plan but doesn't request review]
AI: [Proceeds to implementation]
```

### ❌ Vague Implementation Plans
```
❌ BAD: "Update auth files"
✅ GOOD: "Modify auth.service.ts to add JWT generation (lines 45-67)"
```

---

**Key Takeaway**: Structured planning with artifacts ensures alignment before implementation and provides clear documentation.
