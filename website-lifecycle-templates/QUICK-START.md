# Quick Start

> Dùng trong 5 phút để chọn đúng tài liệu cho giai đoạn xây dựng website hiện tại.

---

## 1. Chọn phase

```text
1 Discovery → 2 Planning → 3 Design → 4 Content → 5 Development → 6 Testing → 7 Maintenance
```

| Nếu bạn đang... | Vào thư mục |
|---|---|
| Làm rõ ý tưởng, yêu cầu, user story, rủi ro | [`1-discovery/`](./1-discovery/INDEX.md) |
| Chọn kiến trúc, sitemap, milestone, API/integration | [`2-planning/`](./2-planning/INDEX.md) |
| Thiết kế UI/UX, responsive, accessibility | [`3-design/`](./3-design/INDEX.md) |
| Viết nội dung, SEO, metadata, copy brief | [`4-content/`](./4-content/INDEX.md) |
| Code frontend/backend, DB, deploy, git workflow | [`5-development/`](./5-development/INDEX.md) |
| Test, security, performance, browser automation | [`6-testing/`](./6-testing/INDEX.md) |
| Bảo trì, incident, performance baseline/report | [`7-maintenance/`](./7-maintenance/INDEX.md) |

---

## 2. Chọn loại tài liệu

```text
templates/  copy và điền cho project thật
prompts/    dùng với AI tool để tạo bản nháp
patterns/   đọc trước khi thiết kế workflow/cách làm
examples/   tham khảo output thực tế
```

---

## 3. Workflow đề xuất

### Website nhỏ / MVP
1. `1-discovery/templates/requirements.md`
2. `2-planning/templates/sitemap-structure.md`
3. `3-design/templates/design-system.md`
4. `4-content/templates/seo-checklist.md`
5. `5-development/templates/project-structure.md`
6. `6-testing/templates/test-plan.md`
7. `7-maintenance/templates/maintenance-log.md`

### Website production/e-commerce
Thêm các artifact reliability:
- `6-testing/templates/security-checklist.md`
- `6-testing/templates/performance-checklist.md`
- `6-testing/templates/browser-automation-test-plan.md`
- `7-maintenance/templates/performance-baseline.md`
- `7-maintenance/templates/incident-report.md`

---

## 4. Nguyên tắc dùng tài liệu

- Không cần dùng 100%; chọn artifact phù hợp với rủi ro và quy mô project.
- Luôn thay placeholder bằng dữ liệu thật: owner, deadline, metric, evidence, link.
- Với nội dung synthesized/internal, dùng như starting point và validate lại trước khi coi là production standard.
- Giữ output cuối cùng trong repo/project thật, không chỉ trong chat AI.
