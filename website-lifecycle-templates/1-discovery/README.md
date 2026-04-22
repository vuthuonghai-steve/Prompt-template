# Discovery Phase - README

> **Phase 1: Discovery & Requirements Gathering**
> Trích xuất patterns từ Claude Code, Cursor, Devin AI, Perplexity

---

## Mục đích

Thu thập requirements, phân tích context, xác định scope, đánh giá risks trước khi bắt đầu thiết kế và development.

---

## Cấu trúc

```
1-discovery/
├── templates/          # Templates thực tế
│   ├── requirements.md
│   ├── user-stories.md
│   ├── use-cases.md
│   └── risk-analysis.md
└── prompts/           # Patterns từ AI tools
    ├── claude-code-discovery.md
    ├── cursor-requirements.md
    ├── devin-discovery.md
    └── perplexity-research.md
```

---

## Templates

### 1. requirements.md
**Mục đích**: Thu thập và cấu trúc hóa requirements

**Sections**:
- Business Context
- User Research
- Functional Requirements (P0/P1/P2)
- Non-Functional Requirements
- Technical Constraints
- Assumptions & Dependencies
- Out of Scope
- Open Questions

**Khi nào dùng**: Bắt đầu mọi project mới

---

### 2. user-stories.md
**Mục đích**: Chuyển requirements thành user stories

**Format**:
```
As a [user type]
I want to [action]
So that [benefit]
```

**Includes**:
- Acceptance Criteria
- Technical Notes
- Dependencies
- Definition of Done

**Khi nào dùng**: Sau khi có requirements, trước planning

---

### 3. use-cases.md
**Mục đích**: Mô tả chi tiết flows và interactions

**Sections**:
- Main Flow
- Alternative Flows
- Exception Flows
- Business Rules
- Data Requirements
- Test Scenarios

**Khi nào dùng**: Features phức tạp cần detailed flows

---

### 4. risk-analysis.md
**Mục đích**: Identify và mitigate risks

**Categories**:
- Technical Risks
- Business Risks
- Resource Risks
- Security Risks
- Dependency Risks

**Includes**:
- Risk Matrix
- Mitigation Strategies
- Action Items

**Khi nào dùng**: Mọi project, update định kỳ

---

## AI Tool Patterns

### Claude Code
**Strengths**:
- 3-Step workflow (Analyze → Research → Implement)
- Non-blocking questions
- Systematic approach
- Memory integration

**Key Patterns**:
- Context gathering before action
- Propose multiple approaches
- Document assumptions
- Validate with user

---

### Cursor Chat
**Strengths**:
- Semantic codebase search
- LSP-driven discovery
- Progressive file reading
- Parallel tool execution

**Key Patterns**:
- Search before proposing
- Understand conventions first
- Verify dependencies
- Concise responses

---

### Devin AI
**Strengths**:
- Planning mode
- Think-first pattern
- Comprehensive analysis
- Risk identification

**Key Patterns**:
- Gather info before concluding
- Use `<think>` for complex decisions
- Multi-source discovery
- Report environment issues

---

### Perplexity
**Strengths**:
- Multi-source research
- Structured synthesis
- Citation discipline
- Comparison tables

**Key Patterns**:
- Combine multiple sources
- Use tables for comparisons
- Cite inline
- Query-type specific formatting

---

## Workflow Tổng Hợp

### Step 1: Initial Discovery
```
1. Đọc user request
2. Clarify ambiguities (non-blocking)
3. Search existing codebase/docs
4. Identify constraints
```

**Tools**: Semantic search, file reading, LSP

---

### Step 2: Research & Analysis
```
1. Gather from multiple sources
2. Understand existing patterns
3. Check dependencies
4. Identify risks
```

**Tools**: Web search, codebase search, browser

---

### Step 3: Requirements Definition
```
1. Document functional requirements
2. Define non-functional requirements
3. Create user stories
4. Map use cases
```

**Output**: requirements.md, user-stories.md

---

### Step 4: Risk Assessment
```
1. Identify technical risks
2. Assess business risks
3. Plan mitigation strategies
4. Document assumptions
```

**Output**: risk-analysis.md

---

### Step 5: Validation
```
1. Review with stakeholders
2. Confirm technical feasibility
3. Validate scope
4. Get approval
```

**Output**: Approved requirements → Ready for Planning phase

---

## Best Practices

### DO
- ✅ Ask clarifying questions early
- ✅ Search codebase before proposing
- ✅ Document assumptions
- ✅ Identify risks proactively
- ✅ Use multiple sources
- ✅ Validate with stakeholders
- ✅ Keep requirements prioritized (P0/P1/P2)

### DON'T
- ❌ Assume requirements without asking
- ❌ Skip existing pattern research
- ❌ Ignore constraints
- ❌ Overlook dependencies
- ❌ Forget to document risks
- ❌ Mix in-scope and out-of-scope

---

## Checklist

### Before Moving to Planning Phase
- [ ] Requirements documented và approved
- [ ] User stories created
- [ ] Use cases mapped (if needed)
- [ ] Risks identified và mitigated
- [ ] Technical feasibility confirmed
- [ ] Dependencies verified
- [ ] Constraints understood
- [ ] Scope clear (in/out)
- [ ] Open questions resolved
- [ ] Stakeholders aligned

---

## Examples

### Example 1: E-commerce Checkout
```
Requirements:
- P0: Guest checkout
- P0: Payment integration (Stripe)
- P1: Save payment methods
- P2: Multiple addresses

Risks:
- High: PCI compliance
- Medium: Payment gateway downtime
- Low: Address validation

User Stories:
- As a guest, I want to checkout without account
- As a user, I want to save my card for future
```

---

### Example 2: User Authentication
```
Requirements:
- P0: Email/password login
- P0: JWT tokens
- P1: Password reset
- P1: 2FA for admin

Risks:
- High: Security vulnerabilities
- Medium: Token management
- Low: Email delivery

Use Cases:
- UC-1: User login
- UC-2: Password reset flow
- UC-3: 2FA setup
```

---

## Next Phase

Sau khi hoàn thành Discovery:
→ **Phase 2: Planning** (architecture, technical design, task breakdown)

---

**Last Updated**: 2026-04-23
**Maintainer**: Discovery Team