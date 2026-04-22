# Prompt Templates

Cac template co san de tao prompt hieu qua cho cac truong hop khac nhau.

---

## 1. BASIC TASK TEMPLATE

Su dung cho: Task don gian, 1-2 buoc

```markdown
## Task
[Mo ta nhiem vu cu the]

## Context
- Project: [ten project]
- File: [file lien quan]

## Requirements
- [Yeu cau 1]
- [Yeu cau 2]

## Expected Output
[Mo ta ket qua mong doi]
```

---

## 2. CODE CHANGE TEMPLATE

Su dung cho: Sua code, them feature, fix bug

```markdown
## Context
- Project: [ten project]
- Tech Stack: [technologies]
- File(s): [files can thay doi]

## Current State
[Mo ta trang thai hien tai]

## Problem/Goal
[Van de can giai quyet HOAC feature can them]

## Task
[Nhiem vu cu the]

## Requirements
- [ ] [Yeu cau 1]
- [ ] [Yeu cau 2]
- [ ] [Yeu cau 3]

## Constraints
- DO: [Nen lam]
- DON'T: [Khong nen lam]

## Success Criteria
- [ ] [Tieu chi kiem tra 1]
- [ ] [Tieu chi kiem tra 2]
```

---

## 3. BUG FIX TEMPLATE

Su dung cho: Fix bugs, errors

```markdown
## Bug Report

### Environment
- OS: [operating system]
- Version: [version]
- File: [file co loi]

### Bug Description
**Expected Behavior:** [Nen xay ra gi]
**Actual Behavior:** [Thuc te xay ra gi]
**Error Message:** [Loi hien thi neu co]

### Steps to Reproduce
1. [Buoc 1]
2. [Buoc 2]
3. [Buoc 3]

### Task
Fix bug sao cho [expected behavior].

### Constraints
- Khong thay doi [phan nay]
- Giu nguyen [logic nay]

### Verification
- [ ] Bug khong con xuat hien
- [ ] Existing functionality van hoat dong
- [ ] No new errors introduced
```

---

## 4. FEATURE IMPLEMENTATION TEMPLATE

Su dung cho: Them feature moi

```markdown
## Feature: [Ten Feature]

### Context
- Project: [ten project]
- Location: [noi dat feature]
- Related Files: [files lien quan]

### User Story
As a [role], I want to [action] so that [benefit].

### Requirements

#### Functional
- [ ] [FR1: Yeu cau chuc nang 1]
- [ ] [FR2: Yeu cau chuc nang 2]

#### Non-Functional
- [ ] [NFR1: Performance, Security, etc.]

### Technical Design
[Mo ta high-level design neu co]

### Implementation Tasks
1. [Task 1]
2. [Task 2]
3. [Task 3]

### Edge Cases
- [Edge case 1]: [Cach xu ly]
- [Edge case 2]: [Cach xu ly]

### Acceptance Criteria
- [ ] [AC1]
- [ ] [AC2]
- [ ] [AC3]
```

---

## 5. CODE REVIEW TEMPLATE

Su dung cho: Review code, PR

```markdown
## Code Review Request

### Context
- PR/Commit: [link hoac description]
- Files Changed: [list files]
- Purpose: [ly do thay doi]

### Review Focus
- [ ] Logic correctness
- [ ] Code style/conventions
- [ ] Error handling
- [ ] Security concerns
- [ ] Performance
- [ ] Test coverage

### Specific Questions
1. [Cau hoi cu the 1]
2. [Cau hoi cu the 2]

### Expected Output
- List of issues found (if any)
- Suggestions for improvement
- Approval recommendation
```

---

## 6. REFACTORING TEMPLATE

Su dung cho: Refactor code

```markdown
## Refactoring: [Ten/Muc tieu]

### Context
- File(s): [files can refactor]
- Current Issue: [van de hien tai - tech debt, complexity, etc.]

### Goal
[Muc tieu cua refactoring]

### Scope
**In Scope:**
- [Phan se thay doi 1]
- [Phan se thay doi 2]

**Out of Scope:**
- [Phan KHONG thay doi]

### Constraints
- [ ] Khong thay doi public API
- [ ] Khong thay doi behavior
- [ ] All tests must pass

### Approach
[Mo ta cach tiep can - extract method, rename, etc.]

### Verification
- [ ] Functionality unchanged
- [ ] Tests pass
- [ ] Code cleaner/more maintainable
```

---

## 7. RESEARCH/EXPLORATION TEMPLATE

Su dung cho: Tim hieu codebase, nghien cuu

```markdown
## Research: [Chu de]

### Context
- Project: [ten project]
- Area of Interest: [phan can tim hieu]

### Questions
1. [Cau hoi 1]
2. [Cau hoi 2]
3. [Cau hoi 3]

### Scope
- Focus on: [gioi han pham vi]
- Ignore: [khong can xem]

### Expected Output
- Summary of findings
- Key files/functions identified
- Recommendations (if applicable)

### Output Format
[Mo ta format mong doi - bullet points, diagram, etc.]
```

---

## 8. API DEVELOPMENT TEMPLATE

Su dung cho: Tao API endpoints

```markdown
## API Endpoint: [Method] [Path]

### Context
- Project: [ten project]
- Base URL: [base url]
- Authentication: [auth method]

### Endpoint Specification

**Method:** [GET/POST/PUT/DELETE]
**Path:** [/api/v1/...]
**Description:** [Mo ta endpoint]

### Request
```json
{
  "param1": "type - description",
  "param2": "type - description"
}
```

### Response
**Success (200):**
```json
{
  "success": true,
  "data": {},
  "message": "string"
}
```

**Error (4xx/5xx):**
```json
{
  "success": false,
  "error": "string",
  "message": "string"
}
```

### Validation Rules
- param1: [validation rules]
- param2: [validation rules]

### Business Logic
1. [Buoc xu ly 1]
2. [Buoc xu ly 2]

### Error Cases
| Case | Status | Message |
|------|--------|---------|
| [Case 1] | 400 | [Message] |
| [Case 2] | 401 | [Message] |
```

---

## 9. TESTING TEMPLATE

Su dung cho: Viet tests

```markdown
## Test: [Ten test suite]

### Context
- File to Test: [file can test]
- Test Framework: [Jest, Vitest, etc.]
- Test Location: [noi dat test file]

### Test Scenarios

#### Happy Path
1. [Scenario 1]: [Expected result]
2. [Scenario 2]: [Expected result]

#### Edge Cases
1. [Edge case 1]: [Expected result]
2. [Edge case 2]: [Expected result]

#### Error Cases
1. [Error case 1]: [Expected error]
2. [Error case 2]: [Expected error]

### Mock Requirements
- [Dependency 1]: [Mock behavior]
- [Dependency 2]: [Mock behavior]

### Coverage Goals
- [ ] Line coverage: [X]%
- [ ] Branch coverage: [X]%
```

---

## 10. SYSTEM PROMPT TEMPLATE

Su dung cho: Tao system prompt cho AI Agent

```markdown
## Role
You are [vai tro] with expertise in [chuyen mon].

## Context
[Thong tin ve environment, project, constraints]

## Capabilities
You have access to:
- [Tool 1]: [Mo ta]
- [Tool 2]: [Mo ta]

## Instructions

### General Guidelines
- [Guideline 1]
- [Guideline 2]

### Workflow
1. [Buoc 1]
2. [Buoc 2]
3. [Buoc 3]

### Rules
- DO: [Nen lam]
- DON'T: [Khong nen lam]

## Output Format
[Mo ta format output mong doi]

## Examples
<example>
User: [input mau]
Assistant: [output mau]
</example>
```

---

## USAGE GUIDE

### Chon Template Phu Hop

| Situation | Template |
|-----------|----------|
| Viet code don gian | Basic Task |
| Fix bug | Bug Fix |
| Them feature | Feature Implementation |
| Review code | Code Review |
| Refactor | Refactoring |
| Tim hieu codebase | Research |
| Tao API | API Development |
| Viet test | Testing |
| Tao AI prompt | System Prompt |

### Customization Tips

1. **Khong can dung het** - Chi dung phan can thiet
2. **Them context** - Cang nhieu context cang tot
3. **Specific > Generic** - Cu the hon la chung chung
4. **Examples help** - Them vi du khi co the
