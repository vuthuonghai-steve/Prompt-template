# Website Lifecycle Templates

> Bộ tài liệu gọn, thực dụng cho toàn bộ vòng đời xây dựng website: discovery → planning → design → content → development → testing → maintenance.
> **Verified**: 2026-04-23
> **Current inventory**: 33 templates · 17 prompts · 20 patterns · 22 examples

---

## Mục đích

Repository này gom các template, prompt, pattern và example để team có thể khởi động, xây dựng, kiểm thử và bảo trì website theo một quy trình nhất quán.

Dùng bộ tài liệu này để:
- chuẩn hóa cách thu thập yêu cầu và lập kế hoạch;
- tạo design/content/development checklist có thể tái sử dụng;
- chuẩn bị testing, security, performance và maintenance artifacts;
- cung cấp prompt mẫu cho các AI coding/design tools.

> Lưu ý nguồn: một phần nội dung được tổng hợp nội bộ từ best practices và system-prompt analysis. Hãy xem đây là pilot/internal guidance cho đến khi từng nguồn được validate bên ngoài.

---

## Cấu trúc chính

```text
website-lifecycle-templates/
├── README.md          # Tổng quan hiện tại
├── QUICK-START.md     # Cách dùng nhanh
├── STRUCTURE.md       # Quy ước thư mục/file
├── STATUS.md          # Inventory đã verify
├── archive/           # Báo cáo lịch sử, iteration notes
├── 1-discovery/
├── 2-planning/
├── 3-design/
├── 4-content/
├── 5-development/
├── 6-testing/
└── 7-maintenance/
```

Mỗi phase giữ cùng một layout:

```text
phase/
├── INDEX.md       # Cổng vào của phase
├── templates/     # Tài liệu/checklist có thể copy dùng ngay
├── prompts/       # Prompt mẫu cho AI tools
├── patterns/      # Best practices/workflows
└── examples/      # Ví dụ thực tế hoặc sample output
```

---

## 7 phases

| Phase | Mục tiêu | Tài liệu chính | Inventory |
|---|---|---|---|
| [1-discovery](./1-discovery/INDEX.md) | Thu thập yêu cầu, người dùng, use cases, rủi ro | Requirements, user stories, use cases, risk analysis | 4 templates · 4 prompts · 3 patterns · 3 examples |
| [2-planning](./2-planning/INDEX.md) | Lập sitemap, kiến trúc, milestone, tech stack | Sitemap, ADR, roadmap, API/integration plan | 5 templates · 2 prompts · 3 patterns · 2 examples |
| [3-design](./3-design/INDEX.md) | Thiết kế UI/UX, design system, responsive, accessibility | Design system, component spec, responsive/accessibility docs | 4 templates · 2 prompts · 4 patterns · 4 examples |
| [4-content](./4-content/INDEX.md) | Content strategy, SEO, metadata, copywriting | Guidelines, SEO checklist, metadata, copy brief | 4 templates · 2 prompts · 1 patterns · 1 examples |
| [5-development](./5-development/INDEX.md) | Chuẩn hóa phát triển frontend/backend, API, DB, deploy | Project structure, coding/API/database/deployment standards | 6 templates · 2 prompts · 4 patterns · 4 examples |
| [6-testing](./6-testing/INDEX.md) | QA, automation, performance, security, launch checks | Test plan, browser automation, performance/security checklists | 5 templates · 4 prompts · 3 patterns · 4 examples |
| [7-maintenance](./7-maintenance/INDEX.md) | Bảo trì, incident, performance baseline/report, feature updates | Maintenance log, incident report, performance baseline/report | 5 templates · 1 prompts · 2 patterns · 4 examples |


---

## Cách dùng nhanh

1. Mở phase phù hợp trong bảng trên.
2. Đọc `INDEX.md` của phase để chọn đúng template/prompt/pattern/example.
3. Copy template vào project thật và thay placeholder bằng dữ liệu thực tế.
4. Dùng prompts để nhờ AI tạo bản nháp, sau đó review bằng checklist.
5. Với Testing/Maintenance, luôn lưu evidence: test output, metrics, owner, sign-off, incident/postmortem links.

---

## Trạng thái chất lượng

- Phase 6 và Phase 7 đã được audit lại về quality/reliability.
- Các link pattern stale đã được sửa.
- `performance-baseline.md` đã được đưa vào Maintenance index.
- Audit chi tiết nằm ở `../reports/quality-reliability-audit-2026-04-23.md`.

Known follow-ups:
- validate external sources cho synthesized material;
- thêm standalone mock strategy;
- thêm monitoring/alerting runbook;
- thêm dependency update runbook;
- mở rộng compliance/i18n nếu project cần.

---

## Archive

Các file báo cáo iteration, multi-agent summary, extraction notes cũ đã được chuyển vào [`archive/`](./archive/README.md) để root project sạch hơn nhưng vẫn giữ provenance.
