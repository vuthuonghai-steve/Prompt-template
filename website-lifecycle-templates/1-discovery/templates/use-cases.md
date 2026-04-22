# Use Cases Template

## Use Case: [Tên use case]

**ID**: UC-[Number]
**Priority**: [High/Medium/Low]
**Status**: [Draft/Approved/Implemented]

---

## 1. Overview

**Brief Description**:
[Mô tả ngắn gọn use case]

**Actors**:
- **Primary**: [User type chính]
- **Secondary**: [User type phụ/System]

**Preconditions**:
- [Điều kiện trước khi thực hiện]
- [Trạng thái hệ thống cần có]

**Postconditions**:
- **Success**: [Kết quả khi thành công]
- **Failure**: [Kết quả khi thất bại]

---

## 2. Main Flow

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 1 | [Actor] | [Hành động] | [Phản hồi] |
| 2 | [Actor] | [Hành động] | [Phản hồi] |
| 3 | [Actor] | [Hành động] | [Phản hồi] |

---

## 3. Alternative Flows

### Alt Flow 1: [Tên flow]

**Trigger**: [Điều kiện kích hoạt]

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 3a | [Actor] | [Hành động khác] | [Phản hồi khác] |
| 3b | System | - | [Xử lý đặc biệt] |

**Return to**: Step [X] of Main Flow

---

### Alt Flow 2: [Tên flow]

**Trigger**: [Điều kiện kích hoạt]

| Step | Actor | Action | System Response |
|------|-------|--------|-----------------|
| 2a | [Actor] | [Hành động khác] | [Phản hồi khác] |

**Outcome**: [Kết thúc use case hoặc quay lại Main Flow]

---

## 4. Exception Flows

### Exception 1: [Tên exception]

**Trigger**: [Lỗi/Exception xảy ra]

**Handling**:
1. System displays: [Error message]
2. System logs: [Error details]
3. User can: [Recovery action]

**Recovery**: [Quay lại step X hoặc kết thúc]

---

### Exception 2: [Tên exception]

**Trigger**: [Lỗi/Exception xảy ra]

**Handling**:
1. [Xử lý bước 1]
2. [Xử lý bước 2]

---

## 5. Business Rules

| Rule ID | Description | Impact |
|---------|-------------|--------|
| BR-1 | [Quy tắc nghiệp vụ] | [Ảnh hưởng đến flow] |
| BR-2 | [Quy tắc nghiệp vụ] | [Ảnh hưởng đến flow] |

---

## 6. Data Requirements

### Input Data
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| [Field 1] | [String/Number] | Yes/No | [Rule] |
| [Field 2] | [String/Number] | Yes/No | [Rule] |

### Output Data
| Field | Type | Description |
|-------|------|-------------|
| [Field 1] | [Type] | [Mô tả] |
| [Field 2] | [Type] | [Mô tả] |

---

## 7. UI/UX Notes

**Screens Involved**:
- [Screen 1]: [Purpose]
- [Screen 2]: [Purpose]

**User Interactions**:
- [Interaction 1]: [Behavior]
- [Interaction 2]: [Behavior]

**Wireframe**: [Link hoặc sketch]

---

## 8. Technical Notes

**APIs/Services**:
- [API 1]: [Endpoint, Method]
- [Service 1]: [Purpose]

**Performance Requirements**:
- Response time: [< X seconds]
- Throughput: [X requests/second]

**Security Considerations**:
- [Authentication requirement]
- [Authorization rule]
- [Data sensitivity]

---

## 9. Test Scenarios

### Scenario 1: Happy Path
**Given**: [Initial state]
**When**: [User action]
**Then**: [Expected outcome]

### Scenario 2: [Alternative path]
**Given**: [Initial state]
**When**: [User action]
**Then**: [Expected outcome]

### Scenario 3: [Error case]
**Given**: [Initial state]
**When**: [User action]
**Then**: [Expected error handling]

---

## 10. Related Use Cases

- **Extends**: [UC-X]
- **Includes**: [UC-Y]
- **Depends on**: [UC-Z]
