---
trigger: always_on
priority: 0
---

# AI Checklist

> **MANDATORY - Verify before any code change**
> **Last Updated**: 2026-03-05

---

## Before Starting Task

### Context Loading
- [ ] Doc INDEX.md
- [ ] Doc project-specific CONTEXT.md
- [ ] Check exports-inventory de tranh duplicate
- [ ] Hieu Workflow Protocol

### Requirements Understanding
- [ ] Phan tich yeu cau va trinh bay cach hieu
- [ ] Nhan duoc XAC NHAN tu Steve
- [ ] Xac dinh rõ scope

---

## Before Creating Files

### Naming
- [ ] Ten < 50 ky tu
- [ ] Ten mo ta ro chuc nang
- [ ] Dung case convention
- [ ] Khong dung generic names

### Barrel Pattern
- [ ] Folder co index.ts chua?
- [ ] Tao file implement truoc
- [ ] Export trong index.ts
- [ ] Verify import path

### Location
- [ ] Collections → `collections/`
- [ ] API routes → `app/api/v1/{feature}/`
- [ ] Services → `services/`

---

## Before Importing

### Import Path
- [ ] Import tu folder (Barrel Pattern)?
- [ ] Import order dung?
  1. React/Next
  2. Third-party
  3. Internal components
  4. Internal services/hooks
  5. Types/constants

### Dependencies
- [ ] Package da co trong package.json?
- [ ] KHONG tu y cai package moi?

---

## Before Writing Code

### Code Style
- [ ] Comments/Logs = Tieng Viet
- [ ] Indentation = 2 spaces
- [ ] KHONG dung semicolons
- [ ] Quotes:
  - Frontend: Single `'`
  - Backend: Double `"`

### Architecture
- [ ] `/app/` routes thin wrappers (5-10 lines)?
- [ ] Business logic trong `/screens/`?
- [ ] API flow: Component → Hook → Service → API?

### Security
- [ ] KHONG hardcode secrets
- [ ] KHONG co fallback cho secrets
- [ ] Sensitive endpoints co rate limiting?

---

## Before Creating Sample Code

### Permission
- [ ] Steve CO YEU CAU tao code?
- [ ] Neu KHONG → NGHIEM CAM tao code mau

---

## Before Submitting

### Quality
- [ ] Naming convention?
- [ ] Barrel Pattern?
- [ ] Tieng Viet comments?
- [ ] KHONG generic names?
- [ ] KHONG hardcoded secrets?

### Documentation
- [ ] Can update exports-inventory?
- [ ] Can update CONTEXT.md?

### Testing
- [ ] Syntax OK?
- [ ] Import paths work?
- [ ] Type errors resolved?

---

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Import tu file | Import tu folder |
| Tao code mau khi chua yeu cau | Chi mo ta, CHO xac nhan |
| Dung generic names | Dung descriptive names |
| Bo qua workflow | Tuân thu 3-Step |
| Tu y cai package | Xin phep truoc |
| Hardcode secrets | Require tu env |

---

**Related**:
- [workflow.development.md](./workflow.development.md)
- [workflow.reflection.md](./workflow.reflection.md)
