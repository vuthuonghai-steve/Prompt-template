# Understanding AI Agent Processing

Tai lieu giai thich cach AI Agent xu ly prompt de giup viet prompt hieu qua hon.

---

## 1. AI Agent KHONG Phai Vector Search

### Hieu Lam Pho Bien
Nhieu nguoi nghi AI Agent:
- Tim kiem thong tin trong "co so du lieu vector"
- Match keywords voi embeddings
- Tra ve "ket qua gan nhat"

### Thuc Te
AI Agent (nhu Claude, GPT) su dung **Transformer Architecture**:

```
Input (Prompt) → Tokenization → Attention Mechanism → Response Generation
                     ↓               ↓                      ↓
              Chia thanh        Tinh toan          Sinh text
              cac tokens        moi quan he        tu trai → phai
                                giua TAT CA
                                tokens
```

### Attention Mechanism
- Model "nhin" TAT CA tokens cung luc
- Tinh trong so (attention weights) cho moi cap token
- Khong "tim kiem" ma "hieu va suy luan"

**He qua cho prompt writing:**
- Thu tu cac phan trong prompt QUAN TRONG
- Context o gan task description → hieu qua hon
- Khong can "keywords" - can "meaning"

---

## 2. Context Window

### Context Window la gi?
- Gioi han so tokens AI co the "nhin thay" cung luc
- Claude: ~200,000 tokens (~150K words)
- GPT-4: ~128,000 tokens

### Token la gi?
- Khong phai = 1 tu
- Tieng Anh: ~0.75 words/token
- Tieng Viet: ~0.5 words/token (vi diacritics)

**Vi du tokenization:**
```
"Hello world" → ["Hello", " world"] → 2 tokens
"Xin chao" → ["X", "in", " ch", "ao"] → 4 tokens
```

### He qua cho prompt:
- Prompt qua dai → mat thong tin dau (recency bias)
- Context quan trong → dat gan cuoi prompt
- "Trich xuat" thong tin thay vi copy nguyen van

---

## 3. Memory trong AI Agent

### 3.1 Short-term Memory (Conversation)

```
┌─────────────────────────────────┐
│ System Prompt (Instructions)    │ ← Fixed, dau conversation
├─────────────────────────────────┤
│ User Message 1                  │
│ Assistant Response 1            │
│ User Message 2                  │ ← Conversation history
│ Assistant Response 2            │
│ ...                             │
├─────────────────────────────────┤
│ Current User Message            │ ← Prompt hien tai
└─────────────────────────────────┘
```

**Gioi han:** Conversation history bi cat khi qua dai

### 3.2 Long-term Memory (Files)

| Loai | File | Muc dich |
|------|------|----------|
| **Project Memory** | CLAUDE.md | Rules, context cho project |
| **User Memory** | ~/.claude/CLAUDE.md | User preferences |
| **Settings** | .claude/settings.json | Configuration |

**Khac biet:**
- Short-term: Trong 1 session, tu dong
- Long-term: Persist qua sessions, can explicit load

### 3.3 Context Injection

Khi user dung `@file.ts`:
1. Claude Code doc file
2. Inject noi dung vao context
3. AI "thay" file trong conversation

```
User: Fix bug in @src/auth.ts

AI nhan duoc:
┌─────────────────────────────────┐
│ User: Fix bug in src/auth.ts    │
│                                 │
│ <file path="src/auth.ts">       │
│ [Noi dung file duoc inject]     │
│ </file>                         │
└─────────────────────────────────┘
```

---

## 4. Tool Usage Pattern

### Flow xu ly tool

```
User Request
    ↓
AI Analyze → Chon tool phu hop
    ↓
Tool Call (Read, Edit, Bash, etc.)
    ↓
Tool Result → Inject vao context
    ↓
AI Continue → Co the goi them tools
    ↓
Final Response
```

### Parallel vs Sequential Tools

```
Parallel (cung luc):          Sequential (tuan tu):
┌─────────────────┐           ┌─────────────────┐
│ Read file1.ts   │           │ Read file.ts    │
│ Read file2.ts   │ cung luc  │       ↓         │
│ Read file3.ts   │           │ Analyze content │
└─────────────────┘           │       ↓         │
                              │ Edit file.ts    │
                              └─────────────────┘
```

**Parallel tot khi:** Doc nhieu files doc lap
**Sequential tot khi:** Buoc sau phu thuoc buoc truoc

---

## 5. Instruction Following

### Priority cua Instructions

```
1. System Prompt (cao nhat)
   - Rules bat buoc
   - Dinh nghia behavior

2. CLAUDE.md / Project Files
   - Project-specific rules
   - Conventions

3. Conversation History
   - Previous context
   - User preferences da noi

4. Current User Message (thap nhat)
   - Co the bi override boi rules tren
```

### Tai sao AI "khong nghe"?

| Nguyen nhan | Vi du | Giai phap |
|-------------|-------|-----------|
| Conflict voi system prompt | Yeu cau lam dieu bi cam | Khong the - do thiet ke |
| Khong du ro rang | "Make it better" | Be specific |
| Context qua xa | Yeu cau o dau, task o cuoi | Đưa context gan task |
| Overridden by rules | Custom format bi CLAUDE.md override | Update CLAUDE.md |

---

## 6. Generation Pattern

### Auto-regressive Generation

AI sinh text **tung token mot**, tu trai sang phai:

```
"The" → "The answer" → "The answer is" → "The answer is 42"
  1        2               3                    4
```

**He qua:**
- Khong the "quay lai" sua
- Token truoc anh huong token sau
- Dai hon ≠ tot hon

### Khi nao AI "bi lac"?

1. **Context qua dai** → Quen phan dau
2. **Task khong ro** → Chon huong sai tu dau
3. **Nhieu yeu cau** → Mix up giua cac tasks

---

## 7. Best Practices Tu Hieu Biet Nay

### 7.1 Structure for Attention
```
❌ Kem:
"I need you to do X and also Y and then Z and make sure you..."

✅ Tot:
## Task 1: X
[Details]

## Task 2: Y
[Details]

## Task 3: Z
[Details]
```

### 7.2 Context Placement
```
❌ Kem:
"Fix the bug. By the way, the project uses React and TypeScript..."

✅ Tot:
## Context
- Framework: React 18
- Language: TypeScript 5.0

## Task
Fix the bug in...
```

### 7.3 Explicit > Implicit
```
❌ Kem:
"Do it like we discussed" (AI khong nho)

✅ Tot:
"Create the function with:
- Input: string array
- Output: filtered array
- Filter: remove empty strings"
```

### 7.4 One Thing at a Time
```
❌ Kem:
"Build the entire checkout flow with all features"

✅ Tot:
"Phase 1: Cart validation
[Details]

We'll do payment in the next conversation"
```

### 7.5 Examples > Descriptions
```
❌ Kem:
"Format the output nicely"

✅ Tot:
"Format output like:
```json
{
  "name": "John",
  "age": 30
}
```"
```

---

## 8. Debug Khi AI Lam Sai

### Checklist Debug

- [ ] **Context missing?** → Them thong tin nen
- [ ] **Instruction unclear?** → Viet lai cu the hon
- [ ] **Conflict?** → Check CLAUDE.md va system rules
- [ ] **Too complex?** → Chia nho task
- [ ] **No examples?** → Them input/output mau
- [ ] **Wrong assumption?** → Explicit hoa gia dinh

### Ask AI to Explain
```
"Truoc khi thuc hien, hay giai thich ban hieu task nay the nao
va cac buoc ban se lam."
```

Neu AI hieu sai → Fix prompt truoc khi cho thuc hien.

---

## Summary: Key Takeaways

| Insight | Implication for Prompts |
|---------|------------------------|
| Attention-based, not search | Meaning matters, not keywords |
| Context window limited | Be concise, put important info near task |
| Sequential token generation | Clear structure prevents "going off track" |
| Tools extend capabilities | Leverage tools, don't ask AI to "imagine" |
| Instructions have priority | Know what can/cannot be overridden |
| Memory is limited | Explicit > assuming AI remembers |
