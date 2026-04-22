---
trigger: always_on
---

# Reflection Protocol

> Self-review before submitting
> **Last Updated**: 2026-03-05

---

## Overview

AI can dung Producer-Critic model:
```
AI Agent
    ├── PRODUCER (Step 6)
    │   └── Generate output
    └── CRITIC (Step 7-8)
        ├── Self-review
        ├── Identify issues
        └── Refine if needed
```

---

## When to Apply

| Apply | Skip |
|-------|------|
| Code > 20 lines | Config changes |
| Architecture decisions | Typo fixes |
| API design | Simple edits |

---

## Checklist

### Code Quality
- [ ] Logic dung voi requirements?
- [ ] Edge cases da handle?
- [ ] Error handling day du?
- [ ] Naming conventions dung?
- [ ] Barrel pattern compliant?
- [ ] Comments = Tieng Viet?

### Integration
- [ ] Import paths dung?
- [ ] Khong duplicate code?
- [ ] Compatible voi patterns?

---

## Loop

```
Step 6: PRODUCE output
    │
    ▼
Step 7: CRITIQUE (checklist)
    │
    ├─ Pass → Step 9: Submit
    │
    └─ Found issues → Step 8: REFINE
          └─► Loop to Step 7
              (max 2-3 iterations)
```

---

## Max Iterations

| Scenario | Max | Action if exceed |
|----------|-----|-----------------|
| Minor issues | 2 | Submit voi note |
| Major issues | 3 | Request guidance |

---

## Output Format

Khi phat hien issues:

```markdown
## REFLECTION NOTES

**Issues found**:
1. [Issue] → [Fix]

**Refinements made**:
- [Change]

**Remaining concerns**:
- [Need Steve review]
```

---

**Related**:
- [workflow.development.md](./workflow.development.md)
- [workflow.ai-checklist.md](./workflow.ai-checklist.md)
