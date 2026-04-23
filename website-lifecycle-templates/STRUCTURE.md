# Structure Guide

> Quy ước tổ chức tài liệu hiện tại cho `website-lifecycle-templates/`.

---

## Main surface

Root chỉ nên giữ thông tin chính:

```text
README.md       # Tổng quan
QUICK-START.md  # Hướng dẫn dùng nhanh
STRUCTURE.md    # Quy ước tổ chức
STATUS.md       # Inventory verified
archive/        # Lịch sử/iteration reports
1-discovery/ ... 7-maintenance/
```

Các báo cáo quá trình, iteration notes và extraction summaries nên để trong `archive/`, không để lẫn với tài liệu sử dụng hằng ngày.

---

## Phase layout

Mỗi phase nên có đúng các phần chính:

```text
{phase}/
├── INDEX.md
├── templates/
├── prompts/
├── patterns/
└── examples/
```

### `INDEX.md`
Cổng vào của phase. Phải liệt kê link tới templates/prompts/patterns/examples hiện có, không để `Coming soon` nếu file đã tồn tại.

### `templates/`
Tài liệu có thể copy vào project thật: checklist, report, plan, spec, log.

### `prompts/`
Prompt dùng với Claude Code, Cursor, Windsurf, Devin, Lovable, v0 hoặc AI tool khác.

### `patterns/`
Best practices, workflow, decision framework, cách làm có thể tái sử dụng.

### `examples/`
Sample output hoặc case study giúp người dùng hiểu cách điền/áp dụng template.

---

## Naming convention thực tế

Repo hiện dùng kebab-case, không bắt buộc prefix dạng `template.`:

```text
templates/test-plan.md
prompts/prompt-cursor-testing.md
patterns/pattern-test-driven-validation.md
examples/example-performance-report.md
```

Quy tắc:
- lowercase;
- kebab-case;
- tên mô tả rõ mục đích;
- với prompts nên có tool hoặc task trong tên nếu hữu ích;
- với patterns/examples nên dùng prefix `pattern-` / `example-` khi tạo file mới để dễ scan.

---

## Khi thêm tài liệu mới

1. Chọn đúng phase.
2. Chọn đúng thư mục: `templates`, `prompts`, `patterns`, hoặc `examples`.
3. Tạo file kebab-case.
4. Cập nhật `INDEX.md` của phase.
5. Nếu tài liệu liên quan reliability/security/performance, thêm owner/evidence/verification/sign-off fields.
6. Chạy link check hoặc kiểm tra thủ công các link Markdown mới.

---

## Current inventory

Xem [`STATUS.md`](./STATUS.md) để biết số lượng verified mới nhất.
