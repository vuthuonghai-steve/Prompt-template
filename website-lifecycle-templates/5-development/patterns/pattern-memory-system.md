# Pattern: Memory System

## Nguồn
- Claude Code
- Cursor

## Mô tả
Persistent file-based memory system for storing user preferences, project context, feedback, and lessons learned across sessions.

## Khi nào dùng
- Long-running projects
- Recurring collaboration patterns
- User preference tracking
- Lessons learned documentation
- Cross-session context preservation

## Cách áp dụng

### 1. Memory Types

```typescript
interface Memory {
  name: string
  description: string
  type: 'user' | 'feedback' | 'project' | 'reference'
  content: string
  createdAt: Date
  updatedAt: Date
}

// user: User profile, preferences, role
// feedback: Guidance on how to work
// project: Ongoing work, goals, deadlines
// reference: External system pointers
```

### 2. Memory Structure

```
.claude/
└── memory/
    ├── MEMORY.md              # Index file
    ├── user-role.md           # User type memory
    ├── feedback-testing.md    # Feedback type memory
    ├── project-launch.md      # Project type memory
    └── reference-linear.md    # Reference type memory
```

### 3. Memory File Format

```markdown
---
name: user-role
description: User is senior frontend developer with React expertise
type: user
---

# User Profile

**Role**: Senior Frontend Developer
**Experience**: 8 years React, 5 years TypeScript
**Current Focus**: E-commerce checkout optimization
**Preferences**:
- Prefers functional components over class components
- Uses Redux Toolkit for state management
- Follows Airbnb style guide
```

### 4. Index File (MEMORY.md)

```markdown
# Memory Index

## User
- [User Role](user-role.md) — Senior frontend dev, React expert
- [Work Style](user-work-style.md) — Prefers TDD, detailed code reviews

## Feedback
- [Testing Approach](feedback-testing.md) — Always write tests first
- [Code Style](feedback-code-style.md) — Use functional components

## Project
- [Launch Timeline](project-launch.md) — Go-live date: 2026-05-01
- [Tech Stack](project-tech-stack.md) — Next.js 15, PayloadCMS 3

## Reference
- [Bug Tracker](reference-linear.md) — Linear project "SHOP"
- [Docs](reference-confluence.md) — Confluence space "Engineering"
```

## Ví dụ thực tế

### E-commerce: User Preference Memory

```markdown
---
name: user-ecommerce-preferences
description: User preferences for e-commerce development
type: user
---

# E-commerce Development Preferences

**Domain**: Flower shop e-commerce
**Tech Stack**: Next.js + PayloadCMS + MongoDB
**Design System**: Pink Petals theme

**Coding Preferences**:
- Comments in Vietnamese
- No semicolons
- Single quotes for frontend
- Double quotes for backend

**Workflow Preferences**:
- Always analyze requirements first
- Propose 2-3 approaches before implementing
- Write tests before code
- Commit after each feature

**Domain Knowledge**:
- Familiar with Vietnamese payment gateways (VNPay, Momo)
- Understands flower seasonality
- Knows Vietnamese address format
```

### E-commerce: Feedback Memory

```markdown
---
name: feedback-api-patterns
description: Guidance on API service layer patterns
type: feedback
---

# API Service Layer Patterns

**Rule**: Always use centralized endpoint configuration

**Why**: Hardcoded URLs caused issues when switching environments. One endpoint was missed during staging deployment, causing checkout failures.

**How to apply**:
- Define all endpoints in `@/api/config/endpoint`
- Import ENDPOINTS constant in services
- Never hardcode API URLs

**Example**:
```typescript
// ❌ Wrong
const response = await fetch('/api/v1/products')

// ✅ Correct
import { ENDPOINTS } from '@/api/config/endpoint'
const response = await fetch(ENDPOINTS.PRODUCTS.LIST)
```

**Related Incident**: 2026-04-15 staging deployment failure
```

### E-commerce: Project Memory

```markdown
---
name: project-checkout-redesign
description: Checkout flow redesign project timeline and goals
type: project
---

# Checkout Flow Redesign

**Goal**: Reduce cart abandonment from 68% to <50%

**Timeline**:
- Design phase: 2026-04-01 to 2026-04-15
- Development: 2026-04-16 to 2026-04-30
- Testing: 2026-05-01 to 2026-05-07
- Launch: 2026-05-08

**Why**: Current checkout has 5 steps, users drop off at payment selection. Analytics show 40% abandon at payment step.

**How to apply**:
- Reduce to 3 steps: Info → Payment → Confirm
- Add guest checkout option
- Pre-fill address from previous orders
- Show trust badges at payment step

**Success Metrics**:
- Cart abandonment <50%
- Checkout completion time <2 minutes
- Mobile conversion rate +20%

**Stakeholders**:
- Product: Sarah (sarah@example.com)
- Design: Mike (mike@example.com)
- Engineering: Steve (steve@example.com)
```

### E-commerce: Reference Memory

```markdown
---
name: reference-payment-gateway
description: VNPay integration documentation location
type: reference
---

# VNPay Payment Gateway

**Documentation**: https://sandbox.vnpayment.vn/apis/docs/

**Credentials Location**: 1Password vault "Engineering" → "VNPay Sandbox"

**Test Cards**:
- Success: 9704 0000 0000 0018
- Insufficient funds: 9704 0000 0000 0026
- Invalid card: 9704 0000 0000 0034

**Webhook Endpoint**: `POST /api/webhooks/vnpay`

**Support Contact**: support@vnpay.vn (response time: 24h)

**Known Issues**:
- Sandbox sometimes returns 504 timeout (retry after 5s)
- Webhook signature verification requires exact header match
```

## Memory Lifecycle

```
1. Capture
   ├── User shares preference
   ├── Feedback given
   ├── Project milestone set
   └── External reference mentioned

2. Store
   ├── Create memory file
   ├── Add to MEMORY.md index
   └── Commit to git

3. Recall
   ├── Load relevant memories at session start
   ├── Reference during work
   └── Update when context changes

4. Update
   ├── Memory becomes outdated
   ├── Update content
   └── Update description if needed

5. Archive
   ├── Memory no longer relevant
   ├── Move to archive/ folder
   └── Remove from MEMORY.md
```

## Best Practices

### Do's
✅ Write memories immediately when learned
✅ Keep descriptions specific and searchable
✅ Update memories when context changes
✅ Use consistent frontmatter format
✅ Commit memory changes to git
✅ Review memories at project milestones

### Don'ts
❌ Store code snippets (use examples instead)
❌ Duplicate information across memories
❌ Write vague descriptions
❌ Let memories become stale
❌ Store sensitive credentials
❌ Create memories for temporary context

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Cross-session continuity | Requires maintenance |
| Personalized collaboration | Can become outdated |
| Lessons learned preserved | Storage overhead |
| Context-aware suggestions | Privacy considerations |

## Related Patterns
- [Spec-Driven Development](./pattern-spec-driven-development.md)
- [Project Documentation](../../2-planning/patterns/pattern-documentation-first.md)
