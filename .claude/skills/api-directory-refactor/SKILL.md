---
name: api-directory-refactor
description: Refactors API directory structure to follow module-first pattern. Use when need to organize API endpoints with support folders (services/, schemas/, types/, constants/, utils/) at module root level.
---

# API Directory Refactor Skill

> **Persona**: Senior Refactor Engineer
> **Purpose**: Refactor API directories to follow standardized module-first pattern

---

## Progressive Disclosure

### Tier 1: Always Load
- SKILL.md (this file)
- knowledge/api-pattern.md — Pattern definitions and rules
- templates/yaml-config.template.yaml — Output format

### Tier 2: Load When Needed
- loop/refactor-checklist.md — After each phase
- templates/service.template.ts — When creating new service
- templates/route-thin.template.ts — When refactoring route

---

## Workflow Progress Tracker

```
### [api-directory-refactor] Progress:
- [ ] Phase 0: DISCOVER
- [ ] Phase 1: ANALYZE
- [ ] Phase 2: INIT
- [ ] Phase 3: MAP
- [ ] Phase 4: REFACTOR → [⏸️ Gate: User confirm]
```

---

## Phase 0: DISCOVER

Quet tat ca folders trong module, phat hien folders khong chuan.

**Steps**:
1. Load knowledge/api-pattern.md
2. Use Glob/ls to scan: `ls src/app/api/v1/{module}/`
3. Identify non-standard folders:
   - lib/ → migrate to utils/
   - helpers/ → migrate to utils/
   - validators/ → migrate to schemas/
   - models/ → migrate to types/
   - _lib/ → migrate

**Interaction**: If found non-standard folders → AskUserQuestion: "Phat hien folders khong chuan. Co muon migrate khong?"

---

## Phase 1: ANALYZE

Doc route.ts va danh gia code ben trong.

**Steps**:
1. Read `src/app/api/v1/{module}/route.ts`
2. Scan tree: `ls -la src/app/api/v1/{module}/`
3. Analyze code:
   - Business logic lines (>50 lines non-HTTP)?
   - Validation logic?
   - Type definitions?
   - Constants/enums?

---

## Phase 2: INIT

Tao support folders tai module root.

**Steps**:
1. Create folders:
   - `src/app/api/v1/{module}/services/`
   - `src/app/api/v1/{module}/schemas/`
   - `src/app/api/v1/{module}/types/`
   - `src/app/api/v1/{module}/constants/`
   - `src/app/api/v1/{module}/utils/`

**Rule**: Only create support folders at level directly under v{version}. NOT at sub-levels like [slug]/, create/, etc.

---

## Phase 3: MAP

Tao YAML config de track cac nhom API con.

**Steps**:
1. Scan all routes in module
2. Group by path (create, [id], [slug], etc.)
3. Generate YAML config:
   - Current structure
   - Target structure for each route
   - Files to create/move

**Output**: `{module}/.api-map.yaml`

---

## Phase 4: REFACTOR

Di chuyen code theo pattern. CHI CHAY KHI USER CONFIRM.

**Steps**:
1. Create backup: `cp -r {module} {module}.bak`
2. Show YAML config to user
3. Wait for user confirmation
4. If confirmed:
   - Extract business logic → services/
   - Extract validation → schemas/
   - Extract types → types/
   - Extract constants → constants/
   - Extract helpers → utils/
   - Simplify route.ts (thin transport only)
5. Verify imports
6. Delete backup after user OK

---

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | Trace from YAML | AI phai trace tu YAML config, khong duoc bia file path |
| G2 | One module at a time | Moi lan chi refactor MOT module goc |
| G3 | AskUserQuestion | Dung khi gap ambiguous cases |
| G4 | Backup first | Tao backup truoc khi refactor |
| G5 | Native tools | Su dung Glob, Grep, Read, Write, Bash |
| G6 | Thin route | route.ts chi chua HTTP transport |

---

## Non-Standard Folder Migrations

| From | To | Notes |
|------|-----|-------|
| lib/ | utils/ | Helpers, utilities |
| helpers/ | utils/ | Helper functions |
| validators/ | schemas/ | Zod validations |
| models/ | types/ | Interfaces, types |
| _lib/ | utils/ | Private helpers |

---

## Interaction Points

| # | When | Action |
|---|------|--------|
| 1 | Start | User doesn't provide module name → AskUserQuestion |
| 2 | After DISCOVER | Found non-standard folders → AskUserQuestion |
| 3 | After MAP | Show YAML config → Wait confirm before REFACTOR |
| 4 | Ambiguous | Can't determine where code belongs → AskUserQuestion |

---

## Error Handling

If error occurs:
1. Log error to console
2. AskUserQuestion: "Co loi xay ra. Tiep tuc hay rollback?"
3. If rollback → restore from backup

---

## Examples

### Example 1: Initial Trigger

```
User: /api-directory-refactor products
AI: Loading pattern...
AI: Available modules: products, orders, auth, customers, stores
Which module to refactor?
```

### Example 2: After MAP

```
AI: Da phan tich xong. Day la YAML config:

api_groups:
  - name: create
    path: create
    status: pending
    target:
      service: service.create.product.ts
      schema: schema.create.product.ts

Tiep tuc refactor? (Confirm de bat dau)
```
