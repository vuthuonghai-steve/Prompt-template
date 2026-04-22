---
name: prompt-improver
description: "Skill cai thien va toi uu hoa prompt cho AI Agent. Phan tich prompt hien tai, xac dinh van de, de xuat cai thien, cung cap templates. Su dung khi: (1) prompt khong ro rang, (2) AI hieu sai yeu cau, (3) can toi uu prompt phuc tap, (4) can tao prompt moi chat luong cao. Trigger: /prompt, improve prompt, fix prompt, optimize prompt, prompt khong hieu qua."
---

# Prompt Improver - AI Prompt Optimization Skill

Skill tu dong phan tich va cai thien prompt de AI Agent hieu va thuc hien dung yeu cau.

---

## Khi Nao Su Dung Skill Nay

### Kich Hoat Khi:
- Nguoi dung noi: "prompt khong hieu qua", "AI khong hieu", "ket qua sai"
- Nguoi dung yeu cau: "cai thien prompt", "optimize prompt", "fix prompt"
- Nguoi dung can: tao prompt moi chat luong cao
- Nguoi dung gap van de: AI lam sai, thieu thong tin, khong dung y

### Khong Can Kich Hoat Khi:
- Prompt don gian, ro rang
- Yeu cau 1-2 buoc don gian
- Nguoi dung da co prompt hieu qua

---

## Workflow Chinh

```
[INPUT: Prompt can cai thien]
         |
         v
[PHASE 1: Phan Tich Prompt]
- Xac dinh cau truc hien tai
- Tim cac van de
- Danh gia muc do ro rang
         |
         v
[PHASE 2: Xac Dinh Van De]
- Problem Categories
- Severity Assessment
- Root Cause Analysis
         |
         v
[PHASE 3: De Xuat Cai Thien]
- Ap dung Prompt Framework
- Them context can thiet
- Cau truc lai noi dung
         |
         v
[PHASE 4: Tao Prompt Moi]
- Viet prompt cai thien
- Them examples neu can
- Validate voi checklist
         |
         v
[OUTPUT: Prompt toi uu — dinh dang XML]
```

---

## PHASE 1: Phan Tich Prompt

### Buoc 1.1: Doc va Hieu Prompt Goc

Khi nhan prompt tu nguoi dung, phan tich theo cac yeu to:

| Yeu To | Cau Hoi | Ghi Chu |
|--------|---------|---------|
| **Muc tieu** | Nguoi dung muon gi? | Xac dinh outcome mong doi |
| **Context** | Thong tin nen la gi? | Project, domain, constraints |
| **Doi tuong** | AI nao se xu ly? | Claude, GPT, Gemini, etc. |
| **Do phuc tap** | Don gian hay phuc tap? | 1 buoc vs nhieu buoc |
| **Output** | Ket qua mong doi dang gi? | Code, text, analysis, etc. |

### Buoc 1.2: Danh Gia Cau Truc Hien Tai

Kiem tra prompt co cac thanh phan:

```
[ ] Identity/Role - Vai tro cua AI
[ ] Context - Thong tin nen
[ ] Task - Nhiem vu cu the
[ ] Instructions - Huong dan thuc hien
[ ] Examples - Vi du input/output
[ ] Output Format - Dinh dang ket qua
[ ] Constraints - Rang buoc/gioi han
```

---

## PHASE 2: Xac Dinh Van De

### 2.1 Problem Categories

| Category | Mo Ta | Vi Du |
|----------|-------|-------|
| **Ambiguity** | Mo ho, khong ro rang | "Fix the bug" (bug nao?) |
| **Missing Context** | Thieu thong tin nen | Khong biet project, tech stack |
| **Overload** | Qua nhieu thong tin | 10 yeu cau trong 1 prompt |
| **No Structure** | Khong co cau truc | Text lien tuc, khong phan chia |
| **Conflicting Requirements** | Mau thuan | "Nhanh" + "Chi tiet" |
| **Implicit Assumptions** | Gia dinh ngam | User biet nhung AI khong |
| **No Examples** | Thieu vi du | AI khong biet output mong doi |
| **Wrong Scope** | Sai pham vi | Qua rong hoac qua hep |

### 2.2 Severity Assessment

| Muc Do | Anh Huong | Hanh Dong |
|--------|-----------|-----------|
| **Critical** | AI khong hieu duoc | Can rewrite hoan toan |
| **Major** | AI hieu sai 1 phan | Can sua doi nhieu |
| **Minor** | AI hieu nhung chua toi uu | Tinh chinh nho |
| **Suggestion** | Co the tot hon | Optional improvements |

### 2.3 Root Cause Analysis

Hoi cac cau hoi:
1. Tai sao AI hieu sai?
2. Thong tin nao bi thieu?
3. Phan nao gay nham lan?
4. Co mau thuan nao khong?

---

## PHASE 3: De Xuat Cai Thien

### 3.1 Prompt Framework (CRISPE)

```
C - Capacity/Role: Vai tro AI (You are a senior developer...)
R - Request: Yeu cau cu the (Create a function that...)
I - Instructions: Huong dan chi tiet (Step 1... Step 2...)
S - Style: Phong cach output (Professional, concise...)
P - Persona: Doi tuong (Explain like I'm a beginner...)
E - Examples: Vi du input/output
```

### 3.2 Context Layers

```
Layer 1: Environment
- OS, platform, runtime
- Working directory
- Date/time neu can

Layer 2: Project
- Tech stack
- Architecture
- Conventions

Layer 3: Domain
- Business rules
- Terminology
- Constraints

Layer 4: Task-specific
- Files lien quan
- Previous context
- Related issues
```

### 3.3 Improvement Techniques

| Ky Thuat | Ap Dung Khi | Vi Du |
|----------|-------------|-------|
| **Specificity** | Qua chung chung | "Fix bug" -> "Fix null pointer in auth.ts:42" |
| **Structure** | Text lon, phuc tap | Chia thanh sections voi headers |
| **Examples** | Output khong dung | Them input/output mau |
| **Constraints** | Scope qua rong | Them "Chi thay doi file X" |
| **Step-by-step** | Task phuc tap | Chia thanh cac buoc nho |
| **Negative Examples** | Hay lam sai | Them "KHONG lam..." |

---

## PHASE 4: Tao Prompt Moi

### 4.1 Template Co Ban

```markdown
## Context
[Thong tin ve project, environment, background]

## Task
[Yeu cau cu the, ro rang]

## Requirements
- [Yeu cau 1]
- [Yeu cau 2]
- [Rang buoc]

## Expected Output
[Mo ta ket qua mong doi, format]

## Example (neu can)
Input: [vi du input]
Output: [vi du output]
```

### 4.2 Template Nang Cao

```markdown
## Role
You are [vai tro] with expertise in [chuyen mon].

## Context
### Environment
- Project: [ten project]
- Tech Stack: [technologies]
- Current State: [trang thai hien tai]

### Background
[Thong tin nen can thiet]

## Task
[Nhiem vu chinh]

## Instructions
1. [Buoc 1]
2. [Buoc 2]
3. [Buoc 3]

## Constraints
- DO: [Nen lam]
- DON'T: [Khong nen lam]

## Output Format
[Dinh dang ket qua]

## Examples
<example>
Input: [input mau]
Output: [output mau]
</example>

## Success Criteria
- [ ] [Tieu chi 1]
- [ ] [Tieu chi 2]
```

### 4.3 Định dạng output chuẩn XML (bắt buộc)

Khi xuất **prompt đã nâng cấp**, luôn dùng **định dạng XML** thay vì Markdown. Cấu trúc chuẩn:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<format_prompt_output>
  <summary>
    <analysis>...</analysis>
    <changes_made>...</changes_made>
  </summary>
  <improved_prompt>
    <prompt>
      <role>Vai trò của AI, mô tả ngắn</role>
      <context>
        <environment><item name="...">...</item>...</environment>
        <input description="..."><field name="..." optional="true|false">...</field>...</input>
        <artifacts><artifact path="...">...</artifact>...</artifacts>
      </context>
      <task>
        <step number="1">...</step>
        <step number="2">...</step>
      </task>
      <instructions>
        <step number="1" name="Tên bước"><item>...</item></step>
        ...
      </instructions>
      <constraints>
        <constraint>...</constraint>
      </constraints>
      <expected_output>
        <when name="..."><item>...</item></when>
      </expected_output>
      <example>
        <input>...</input>
        <output><item>...</item></output>
      </example>
    </prompt>
  </improved_prompt>
</format_prompt_output>
```

**Quy tắc:**
- Nội dung prompt cải thiện nằm trong `<prompt>`, cấu trúc con: `<role>`, `<context>`, `<task>`, `<instructions>`, `<constraints>`, `<expected_output>`, `<example>`.
- Dùng thẻ có nghĩa: `<step>`, `<item>`, `<constraint>`, `<field>`, `<artifact>`, `<when>`.
- Tránh CDATA cho nội dung ngắn; nếu có ký tự đặc biệt thì escape XML (vd. `&lt;`, `&gt;`, `&amp;`).
- File output nên có extension `.xml` (vd. `format-prompt-output-*.xml`).

### 4.4 Validation Checklist

Truoc khi finalize prompt, kiem tra:

```
CLARITY (Ro rang)
[ ] Muc tieu duoc neu ro
[ ] Khong co tu mo ho (it, some, maybe)
[ ] Scope duoc gioi han

COMPLETENESS (Day du)
[ ] Co du context
[ ] Co instructions
[ ] Co output format

STRUCTURE (Cau truc)
[ ] Su dung headers/sections
[ ] Co bullet points cho lists
[ ] Logical flow

ACTIONABLE (Thuc hien duoc)
[ ] AI co tools can thiet
[ ] Khong yeu cau bat kha thi
[ ] Co the verify ket qua

EXAMPLES (Vi du)
[ ] Co examples neu task phuc tap
[ ] Examples representative
[ ] Edge cases duoc cover
```

---

## Vi Du Su Dung

### Vi Du 1: Prompt Mo Ho -> Cai Thien

**Prompt goc:**
```
Fix the authentication bug
```

**Van de:**
- Khong biet bug nao
- Khong biet file nao
- Khong biet expected behavior

**Prompt cai thien:**
```markdown
## Context
- Project: SiinStore API (Next.js 15 + PayloadCMS)
- File: src/app/api/v1/auth/login/route.ts

## Problem
Login endpoint returns 500 error when user enters wrong password.
Expected: Return 401 with message "Sai mat khau"
Actual: Server crash with "Cannot read property 'id' of null"

## Task
Fix the authentication bug so that wrong password returns proper 401 error.

## Constraints
- DO NOT change the response format
- Keep existing validation logic
- Use `errorResponse` helper from @/lib/api-response

## Success Criteria
- [ ] Wrong password returns 401
- [ ] Correct password still works
- [ ] No server crash
```

### Vi Du 2: Prompt Overload -> Restructure

**Prompt goc:**
```
I need you to create a new product page with a gallery, reviews section,
add to cart button, related products, and make sure it's responsive and
has good SEO and loads fast and follows our design system and handles
errors properly and has loading states
```

**Van de:**
- Qua nhieu yeu cau trong 1 prompt
- Khong co priority
- Khong co chi tiet

**Prompt cai thien:**
```markdown
## Context
- Project: SiinStore Frontend (Next.js 15 + React 19)
- Design System: @siinstore-web/src/components/ui/
- Location: Create at src/screens/product/ProductDetailScreen.tsx

## Task
Create Product Detail Page with the following sections:

## Requirements (Priority Order)

### P0 - Must Have
1. **Product Gallery** - Image carousel with zoom
2. **Product Info** - Name, price, description
3. **Add to Cart** - Button with quantity selector
4. **Responsive** - Mobile-first design

### P1 - Should Have
5. **Reviews Section** - List of reviews with ratings
6. **Related Products** - Grid of 4 similar products
7. **Loading States** - Skeleton components

### P2 - Nice to Have
8. **SEO Optimization** - Meta tags, structured data
9. **Error Boundaries** - Graceful error handling

## Technical Constraints
- Use existing UI components from src/components/ui/
- Follow screen pattern: business logic in Screen, thin wrapper in app/
- Use SWR for data fetching

## Output
- ProductDetailScreen.tsx with all P0 requirements
- List of follow-up tasks for P1, P2
```

---

## Tips Su Dung Skill

### 1. Bat Dau Tu Van De
- Hoi nguoi dung: "AI dang hieu sai gi?"
- Xac dinh gap between expected vs actual

### 2. Iterative Improvement
- Khong can perfect ngay lan dau
- Cai thien dan qua feedback

### 3. Context is King
- Them context > them instructions
- AI can thong tin de suy luan

### 4. Less is More
- Prompt ngan hon thuong tot hon
- Chi giu thong tin can thiet

### 5. Test va Validate
- Thu prompt voi AI
- Kiem tra output co dung khong

---

## Quick Reference

### Common Fixes

| Van De | Fix |
|--------|-----|
| "AI lam qua nhieu" | Them constraint: "CHI lam X" |
| "AI bo sot" | Them checklist: "Dam bao cover: A, B, C" |
| "Output sai format" | Them template: "Tra ve theo format sau: ..." |
| "AI hoi lai qua nhieu" | Them: "Gia dinh X neu khong chac chan" |
| "Qua chung chung" | Them specific: files, line numbers, names |

### Format Tags Hieu Qua / Output chuẩn XML

**Prompt đã nâng cấp phải xuất theo định dạng XML** (xem mục 4.3). Các thẻ gợi ý khi viết prompt (có thể nhúng trong XML):

```xml
<context>...</context>      <!-- Thong tin nen -->
<task>...</task>            <!-- Nhiem vu chinh -->
<constraints>...</constraints>  <!-- Rang buoc -->
<example>...</example>      <!-- Vi du -->
<output>...</output>        <!-- Dinh dang output -->
```

---

## Trigger Phrases

Skill nay duoc kich hoat khi nguoi dung:

### Phan Tich Prompt
- "prompt nay co van de gi"
- "tai sao AI khong hieu"
- "phan tich prompt"
- "review prompt"

### Cai Thien Prompt
- "cai thien prompt"
- "optimize prompt"
- "fix prompt"
- "lam prompt tot hon"
- "prompt hieu qua hon"

### Tao Prompt Moi
- "tao prompt cho..."
- "viet prompt de..."
- "can prompt"
- "giup tao prompt"

### Debug Prompt
- "AI lam sai"
- "ket qua khong dung"
- "AI khong lam theo yeu cau"
- "output sai"
