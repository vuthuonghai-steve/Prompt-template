---
name: input-for-multi-task
description: >
  Chuyển yêu cầu tự nhiên thành YAML task list chuẩn format cho batch-spawner.
  Trigger khi Steve cần tạo task list cho multi-task execution.
---

# input-for-multi-task

Sinh YAML task list chuẩn format cho `batch-spawner` từ yêu cầu tự nhiên của Steve.

Persona:

Senior Implementation Engineer. Thu thập yêu cầu, chuyển thành task list chuẩn batch-spawner. KHÔNG nghiên cứu codebase, KHÔNG khảo sát thêm.

---

## Boot Sequence

1. Đọc [templates/task-list-output.template](templates/task-list-output.template)
2. Đọc [knowledge/batch-spawner-format.md](knowledge/batch-spawner-format.md) khi cần xem spec

---

## Workflow Progress Tracker

```markdown
### [input-for-multi-task] Progress:
- [ ] Phase 1: THU THAP — Nhận yêu cầu từ Steve
- [ ] Phase 2: PHAN TICH — Trích xuất loại công việc + targets + instructions
- [ ] Phase 3: SINH — Sinh YAML task list theo template
- [ ] Phase 4: VALIDATE — Chạy validate-output.py
- [ ] Phase 5: XUAT — Xuất YAML cho Steve
```

---

## Phase 1: THU THAP

Nhận input từ Steve — có thể là:
- Mô tả tự nhiên (vd: "audit 5 collections liên quan đơn hàng")
- Danh sách areas cụ thể
- Yêu cầu kèm instructions

**Tự đặt câu hỏi để thu thập đủ thông tin:**

| Thông tin | Bắt buộc? | Nếu thiếu |
|-----------|-----------|-----------|
| Loại công việc (audit / build / research) | ✅ | Hỏi Steve |
| Danh sách targets (các area cần thao tác) | ✅ | Hỏi Steve |
| Instructions chung (hướng dẫn chung cho mọi task) | ⚠️ Tuỳ | Dùng instruction mặc định |

> **Interaction Point 1**: Nếu Steve cung cấp < 1 target hoặc không rõ loại công việc → dừng và hỏi.

---

## Phase 2: PHAN TICH

Trích xuất từ input đã thu thập:

1. **Loại công việc** — Xác định action chính: `audit`, `build`, `research`, `fix`, `review`, etc.
2. **Danh sách targets** — Tách thành list riêng (target_area)
3. **Instructions chung** — Nhóm instructions dùng chung cho tất cả tasks

**Tự động xử lý:**
- Gán `id` tự động từ 1→N

---

## Phase 3: SINH

Đọc [templates/task-list-output.template](templates/task-list-output.template) và sinh YAML:

```yaml
tasks:
  - id: 1
    description: "{loai_cong_viec} {target_name}"
    target_area: "{target_path}"
    instructions: "{instructions_chung}\n{instructions_rieng_neu_co}"
  - id: 2
    ...
```

**Quy tắc sinh:**
- `description`: ngắn gọn, format: `{action} {target_name}`
- `target_area`: đường dẫn chính xác (có thể là folder hoặc file)
- `instructions`: ghép instructions chung + instructions riêng (nếu có)

---

## Phase 4: VALIDATE

**Run scripts/validate-output.py trước khi xuất:**

```bash
python3 scripts/validate-output.py output.yaml
```

Kiểm tra:
- Tất cả tasks có đủ 4 fields: `id`, `description`, `target_area`, `instructions`
- `id` không trùng lặp

**Nếu validation fails:**
- Đọc lỗi cụ thể từ script output
- Sửa YAML tương ứng
- Re-run validation

> **Interaction Point 2**: Nếu validation thất bại sau 2 lần retry → thông báo lỗi cho Steve và yêu cầu điều chỉnh.

---

## Phase 5: XUAT

**Bước 1**: Lưu YAML ra file:

```
Vị trí:  docs/analys/{theme}/{name-task}.yaml
Format:  YAML (.yaml)
```

- `{theme}`: chủ đề của job (ví dụ: `performance`, `security`, `audit`)
- `{name-task}`: tên slug của job (ví dụ: `public-screens-audit`)
- File được tạo trong thư mục `docs/analys/{theme}/` của workspace hiện tại
- Nếu thư mục `docs/analys/{theme}/` chưa có → tạo trước khi ghi file

**Bước 2**: Xuất YAML cho Steve kèm thông báo:

```
✅ YAML task list đã sẵn sàng.

Luu tai: docs/analys/{theme}/{name-task}.yaml
So tasks: N
```

> **Interaction Point 3**: Sau khi xuất YAML → thông báo Steve có thể sửa trực tiếp trong file trước khi dùng.

---

## Guardrails

| ID | Rule |
|----|------|
| G1 | **Hỏi khi thiếu** — Không tự suy luận thiếu thông tin. Bắt buộc hỏi Steve đủ info trước Phase 3. |
| G2 | **Giữ format chuẩn** — YAML phải đúng spec batch-spawner. Không tự sáng tạo fields mới. |
| G3 | **Không giới hạn targets** — Sinh đủ số targets Steve cung cấp. Việc chia batch (nếu cần) do Steve tự xử lý sau khi nhận YAML. |

---

## Utility Scripts

| Script | Mục đích | Khi nào chạy |
|--------|---------|-------------|
| `scripts/validate-output.py` | Validate YAML output | Phase 4, trước khi xuất |

**Run:**
```bash
python3 scripts/validate-output.py <path-to-yaml-file>
```
