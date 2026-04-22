# Claude Code - Discovery Phase Patterns

> Trích xuất từ: Claude Code Prompt (Anthropic)
> Focus: Context gathering, systematic analysis, planning

---

## 1. Context Gathering Pattern

### Approach
```
Step 1: ANALYZE
├── Phân tích yêu cầu user
├── Trình bày lại cách hiểu
└── CHỜ user xác nhận

Step 2: RESEARCH
├── Nghiên cứu codebase liên quan
├── Đề xuất 2-3 approaches
├── Nêu trade-offs mỗi approach
└── CHỜ user chọn approach
```

### Key Principles
- **Non-blocking questions**: Dùng `/btw` cho câu hỏi ngắn
- **Continuous context collection**: Cache state, ghi assumptions
- **Dynamic adjustment**: Adapt khi có thông tin mới

---

## 2. Information Handling

**From Devin AI**:
- Don't assume content of links without visiting them
- Use browsing capabilities to inspect web pages when needed
- Gather information before concluding root cause

**Pattern**:
```
When encountering difficulties:
1. Take time to gather information
2. Analyze before acting
3. Consider multiple sources
```

---

## 3. Requirement Analysis Pattern

### Questions to Ask

**Business Context**:
- What problem are we solving?
- Why now? (Urgency/Priority)
- What are success metrics?

**Technical Context**:
- What exists already?
- What constraints do we have?
- What dependencies exist?

**User Context**:
- Who are the users?
- What are their pain points?
- What's the user journey?

---

## 4. Planning Pattern

**From Devin AI Planning Mode**:
```
While in "planning" mode:
1. Gather all information needed
2. Search and understand codebase
3. Use LSP to inspect code
4. Use browser for online sources
5. Ask user if missing crucial context
6. Create confident plan with all edit locations
```

**Output**: `<suggest_plan />` when ready

---

## 5. Systematic Approach

### Before Starting
- [ ] Đọc CLAUDE.md / project docs
- [ ] Check existing patterns
- [ ] Understand conventions
- [ ] Identify constraints

### During Discovery
- [ ] Use search tools extensively (parallel + sequential)
- [ ] Read relevant files
- [ ] Check dependencies
- [ ] Validate assumptions

### Before Proposing
- [ ] Have complete context
- [ ] Know all locations to edit
- [ ] Understand references
- [ ] Verify technical feasibility

---

## 6. Risk Identification

**From Devin AI**:
```
Think about:
1. Environment issues
2. Missing dependencies
3. Integration challenges
4. Security considerations
```

**Pattern**:
- Identify risks early
- Report to user
- Find workarounds
- Don't try to fix environment alone

---

## 7. Competitive Analysis Pattern

**From Perplexity**:
```
When researching:
1. Gather from multiple sources
2. Compare different perspectives
3. Prioritize trustworthy sources
4. Combine related information
5. Cite all sources
```

**Output Format**:
- Summary first
- Structured sections (##)
- Tables for comparisons
- Citations inline

---

## 8. Discovery Checklist

### Information Completeness
- [ ] Business requirements clear?
- [ ] Technical constraints identified?
- [ ] User needs understood?
- [ ] Dependencies mapped?
- [ ] Risks identified?

### Validation
- [ ] Assumptions documented?
- [ ] Open questions listed?
- [ ] Stakeholders aligned?
- [ ] Feasibility confirmed?

---

## 9. Communication Pattern

**Concise Updates**:
```
Before first tool call: State what you're doing (1 sentence)
While working: Short updates at key moments
End of turn: 1-2 sentences (what changed, what's next)
```

**Avoid**:
- Verbose explanations
- Unnecessary preamble
- Repeating obvious information

---

## 10. Example Discovery Flow

```
User: "Build a user authentication system"

AI: ✅ Đã hiểu: Xây dựng hệ thống authentication

📋 Approach:
1. Research existing auth patterns in codebase
2. Identify requirements (OAuth/JWT/Session?)
3. Check security constraints
4. Propose architecture options

Bắt đầu research...

[Uses search tools to find existing auth code]
[Reads relevant files]
[Checks dependencies]

Found: Project uses JWT, has User model, no auth yet

Options:
A. JWT + Refresh Token (Secure, scalable)
B. Session-based (Simple, server state)
C. OAuth2 + JWT (Enterprise, complex)

Trade-offs:
- A: Best security, needs Redis
- B: Easiest, not scalable
- C: Most flexible, high complexity

Recommend: Option A
Reason: Matches existing JWT usage, scalable

Confirm approach?
```

---

## 11. Memory Integration

**Save to Memory**:
- User preferences discovered
- Project-specific patterns
- Decisions made and why
- Constraints identified

**Example**:
```yaml
type: project
name: auth-requirements
description: Authentication requirements for project X
---
- Must use JWT (existing pattern)
- Redis available for refresh tokens
- OAuth not needed (internal users only)
- 2FA required for admin roles
```