# batch-spawner Format Specification

> **Usage**: Đọc khi cần xem lại spec format YAML cho batch-spawner.
> Nguồn: `.claude/agents/batch-spawner.md`

---

## 1. Input Format (YAML)

batch-spawner nhận input là YAML với cấu trúc `tasks`:

```yaml
tasks:
  - id: 1
    description: "Task description"
    target_area: "/path/to/area"
    instructions: "Specific instructions"
  - id: 2
    description: "Task 2 description"
    target_area: "/path/to/area2"
    instructions: "Task 2 instructions"
```

### Required Fields

| Field | Type | Bắt buộc | Mô tả |
|-------|------|-----------|--------|
| `id` | integer | ✅ | Số thứ tự task, bắt đầu từ 1 |
| `description` | string | ✅ | Mô tả ngắn gọn công việc cần làm |
| `target_area` | string | ✅ | Đường dẫn area trong codebase cần thao tác |
| `instructions` | string | ✅ | Hướng dẫn chi tiết cho subagent thực hiện |

### Validation Rules

- Tất cả tasks phải có đủ 4 required fields
- `id` phải là số nguyên, bắt đầu từ 1, không trùng lặp
- `description` phải không rỗng
- `target_area` phải là đường dẫn hợp lệ
- `instructions` phải không rỗng

### Limits

| Limit | Value |
|-------|-------|
| Max tasks per batch | Không giới hạn (Steve tự quản lý việc chia batch nếu cần) |

---

## 2. Output Schema

batch-spawner trả về JSON sau khi hoàn thành:

```json
{
  "metadata": {
    "batchId": "BATCH-{timestamp}",
    "timestamp": "{ISO8601}",
    "totalTasks": 0,
    "completed": 0,
    "failed": 0
  },
  "tasks": [
    {
      "id": 1,
      "status": "COMPLETED|FAILED|PENDING",
      "subagentId": "...",
      "result": { ... }
    }
  ],
  "summary": {
    "successRate": "XX%",
    "totalDuration": "Xs",
    "issues": []
  }
}
```

---

## 3. Error Handling

| Error | Action |
|-------|--------|
| Task missing required field | Skip task, report in summary |
| `id` trùng lặp | Skip task, report |
| Subagent timeout | Mark as FAILED, log error |
