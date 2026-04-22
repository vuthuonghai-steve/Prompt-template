# Prompt Analysis Checklist

Su dung checklist nay de phan tich prompt truoc khi cai thien.

---

## 1. CLARITY CHECK (Do Ro Rang)

### 1.1 Goal Clarity
- [ ] Muc tieu chinh duoc neu ro
- [ ] Khong co nhieu muc tieu mau thuan
- [ ] Outcome mong doi cu the

### 1.2 Language Clarity
- [ ] Khong dung tu mo ho: "some", "maybe", "it", "thing"
- [ ] Terms duoc define neu chuyen mon
- [ ] Khong viet tat khong giai thich

### 1.3 Scope Clarity
- [ ] Gioi han pham vi ro rang
- [ ] Biet dau la diem dung
- [ ] Khong "open-ended" vo han

---

## 2. COMPLETENESS CHECK (Do Day Du)

### 2.1 Context
- [ ] Co thong tin project/environment
- [ ] Co background neu can
- [ ] Co constraints/limitations

### 2.2 Task Definition
- [ ] Nhiem vu duoc mo ta cu the
- [ ] Co buoc thuc hien (neu complex)
- [ ] Co tieu chi thanh cong

### 2.3 Output Specification
- [ ] Format output duoc chi dinh
- [ ] Co examples neu can
- [ ] Biet ket qua nhu the nao la dung

---

## 3. STRUCTURE CHECK (Cau Truc)

### 3.1 Organization
- [ ] Co sections/headers ro rang
- [ ] Information flow logical
- [ ] Related info grouped together

### 3.2 Formatting
- [ ] Su dung markdown phu hop
- [ ] Lists cho enumeration
- [ ] Code blocks cho code/commands

### 3.3 Length
- [ ] Khong qua dai (>2000 words can xem lai)
- [ ] Khong qua ngan (thieu thong tin)
- [ ] Moi section co purpose

---

## 4. ACTIONABILITY CHECK (Kha Nang Thuc Hien)

### 4.1 Feasibility
- [ ] AI co kha nang lam duoc
- [ ] Tools can thiet co san
- [ ] Khong yeu cau thong tin bi han che

### 4.2 Verifiability
- [ ] Co the kiem tra ket qua
- [ ] Co criteria de evaluate
- [ ] Biet khi nao la "xong"

### 4.3 Dependencies
- [ ] Neu ro dependencies neu co
- [ ] Order thuc hien ro rang
- [ ] Khong circular dependencies

---

## 5. PROBLEM INDICATORS

### Red Flags (Can fix ngay)
- [ ] Co cau hoi "which one?" (ambiguous)
- [ ] Co tu "etc." (incomplete)
- [ ] Co "as needed" (vague)
- [ ] Co mau thuan giua cac yeu cau

### Yellow Flags (Nen cai thien)
- [ ] Khong co examples
- [ ] Khong co constraints
- [ ] Single giant paragraph
- [ ] Mix nhieu ngon ngu

### Green Flags (Tot roi)
- [x] Clear goal statement
- [x] Specific details
- [x] Structured format
- [x] Examples provided

---

## 6. SCORING GUIDE

Dem so items passed trong moi section:

| Section | Score | Evaluation |
|---------|-------|------------|
| Clarity | __/6 | < 4: Major rewrite needed |
| Completeness | __/7 | < 5: Add missing info |
| Structure | __/6 | < 4: Restructure |
| Actionability | __/6 | < 4: Refine scope |

**Total: __/25**

| Total Score | Action |
|-------------|--------|
| 20-25 | Minor tweaks only |
| 15-19 | Moderate improvements |
| 10-14 | Significant rewrite |
| < 10 | Start from scratch |

---

## 7. QUICK ANALYSIS TEMPLATE

```markdown
## Prompt Analysis

**Goal:** [Tom tat muc tieu]
**Clarity Score:** [X/6]
**Completeness Score:** [X/7]
**Structure Score:** [X/6]
**Actionability Score:** [X/6]
**Total:** [X/25]

### Issues Found
1. [Issue 1 - Severity: High/Medium/Low]
2. [Issue 2 - Severity: High/Medium/Low]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

### Priority Fixes
- [ ] [Fix 1 - Most critical]
- [ ] [Fix 2]
```
