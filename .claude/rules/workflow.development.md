---
trigger: always_on
description: 3-Step development process for all tasks
---

# Development Workflow

> **Last Updated**: 2026-03-05

---

## 3-Step Process

### Step 1: ANALYZE
```
├── Phan tich yeu cau Steve dua ra
├── Trinh bay lai cach hieu
└── CHO Steve xac nhan
```

### Step 2: RESEARCH
```
├── Nghien cuu codebase lien quan
├── De xuat 2-3 approaches
├── Neu trade-offs moi approach
└── CHO Steve chon approach
```

### Step 3: IMPLEMENT
```
├── Chi tao code khi Step 1-2 xong
├── Code theo approach da chon
└── Update docs neu can
```

---

## Skip Conditions

Duoc skip Step 1-2 khi:
- Steve noi "code di" / "lam ngay"
- Task don gian (fix typo, rename, config)
- Steve da cho context day du va explicit

---

## Nghiem Cam

| Action | Reason |
|--------|--------|
| Tao code mau khi chua confirm | Lam loan tam nhin |
| Cai package moi khi chua phep | Co the gay conflict |
| Bo qua CONTEXT.md | Mat context |
| **Tao collection/field moi khi chua check existing** | **Pham architecture, tao redundant** |

## Research Checklist (BAT BUOC)

**Truoc khi tao Collection/Field moi:**
- [ ] Doc `tag.contants.ts` — co TAG_TYPE phu hop chua?
- [ ] Doc `Product.ts` — co relationship phu hop chua?
- [ ] Kiem tra existing collections co can thiet tao moi khong?
- [ ] Hoi Steve neu khong chan chan

> **CRITICAL INCIDENT (2026-04-16)**: Agent tao StyleTypes/ColorTones/FlowerTypes collections sai vi khong check Tag collection truoc. Da tao rule [payload.tag-pattern.md](./payload.tag-pattern.md) de ngan chan lap lai.

---

## Trigger Words

| Steve noi | AI nen lam |
|-----------|-----------|
| "code di" / "lam di" | Tao code ngay |
| "giai thich" / "tai sao" | Giai thich chi tiet |
| "review" | Danh gia solution |
| "so sanh" | Phan tich trade-offs |
| "ok" / "proceed" | Tiep tuc |

---

**Related**:
- [workflow.ai-checklist.md](./workflow.ai-checklist.md)
- [workflow.reflection.md](./workflow.reflection.md)
