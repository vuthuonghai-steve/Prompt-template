# Refactor Checklist

> Checklist verify sau mỗi bước trong quá trình refactor API directory

---

## Phase 0: DISCOVER

- [ ] Quét tất cả folders trong module
- [ ] Phát hiện folders không chuẩn:
  - [ ] lib/ → cần migrate to utils/
  - [ ] helpers/ → cần migrate to utils/
  - [ ] validators/ → cần migrate to schemas/
  - [ ] models/ → cần migrate to types/
  - [ ] _lib/ → cần migrate

---

## Phase 1: ANALYZE

- [ ] Đọc route.ts trong module gốc
- [ ] Quét tree con (ls src/app/api/v1/{module}/)
- [ ] Đánh giá code trong route.ts:
  - [ ] Có business logic? (>50 lines non-HTTP)
  - [ ] Có validation logic?
  - [ ] Có type definitions?
  - [ ] Có constants/enums?

---

## Phase 2: INIT

- [ ] Tạo services/ folder
- [ ] Tạo schemas/ folder
- [ ] Tạo types/ folder
- [ ] Tạo constants/ folder
- [ ] Tạo utils/ folder

---

## Phase 3: MAP

- [ ] Tạo YAML config
- [ ] Liệt kê tất cả routes trong module
- [ ] Xác định mỗi route thuộc nhóm nào
- [ ] Đánh dấu trạng thái:
  - [ ] pending: chưa refactor
  - [ ] in_progress: đang refactor
  - [ ] completed: đã refactor

---

## Phase 4: REFACTOR

### Trước khi refactor
- [ ] Tạo backup (cp -r module module.bak)
- [ ] Xác nhận với user

### Sau khi refactor
- [ ] Verify imports trong route.ts
- [ ] Verify services/ chứa đúng business logic
- [ ] Verify schemas/ chứa đúng validation
- [ ] Verify types/ chứa đúng DTOs
- [ ] Verify constants/ chứa đúng enums/defaults
- [ ] Xóa backup sau khi user confirm OK

---

## Quality Gates

- [ ] route.ts < 50 lines (chỉ HTTP transport)
- [ ] Business logic trong services/
- [ ] Validation trong schemas/
- [ ] DTOs trong types/
- [ ] Enums trong constants/
- [ ] Helpers trong utils/
- [ ] KHÔNG có: hooks/, model/, validation/, validators/, _lib/
- [ ] File naming đúng pattern: `service.<action>.<entity>.ts`
