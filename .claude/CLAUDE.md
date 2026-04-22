# CLAUDE.md — SiinStore API

> **Context nghiệp vụ quan trọng cho mọi Claude Code session**
> **Last Updated**: 2026-04-16

---

## 🚨 CRITICAL LESSON — KHÔNG TẠO COLLECTIONS MỚI KHI TAG ĐÃ COVER

### Sự cố Phase 2 (2026-04-16)

**Lỗi**: Agent tạo 3 collections mới (`StyleTypes`, `ColorTones`, `FlowerTypes`) thay vì dùng Tag collection có sẵn.

**Root cause**: Không research đầy đủ architecture hiện tại, không kiểm tra Tag collection structure trước khi tạo collections mới.

**Hậu quả**: Tạo redundant collections, phá vỡ architecture nhất quán, cần revert và fix.

---

## Tag Collection — Single Source of Truth cho Metadata

### Cấu trúc Tag hiện tại

```typescript
// tag.contants.ts
export const TAG_TYPE = {
  THEME: 'theme',      // Chủ đề
  SEASON: 'season',    // Mùa vụ
  EVENT: 'event',      // Sự kiện
  STYLE: 'style',      // Phong cách
  COLOR: 'color',      // Tone màu (2026-04-16)
  FLOWER: 'flower',    // Loại hoa (2026-04-16)
  MARKETING: 'marketing',
  OTHER: 'other',
}
```

### Nguyên tắc bắt buộc

| Trước khi tạo Collection mới | Action |
|------------------------------|--------|
| Kiểm tra Tag collection | Xem `tag.contants.ts` có type phù hợp chưa? |
| Check existing relationships | Product đã có `tags` relationship chưa? |
| Hỏi Steve | Confirm nếu không chắc chắn |

### Khi nào được tạo Collection mới?

Chỉ tạo khi:
1. ✅ Có yêu cầu nghiệp vụ đặc thù (không thể dùng Tag)
2. ✅ Cần separate admin UI hoặc permissions riêng
3. ✅ Cần fields đặc biệt mà Tag không có (vd: `flowerColor`, `seasonal`, `priceRange`)
4. ✅ Steve confirm explicit yêu cầu

### Khi nào dùng Tag Collection?

| Metadata type | Approach |
|--------------|----------|
| Style/Kiểu cách | Tag với `type: 'style'` |
| Color/Tone màu | Tag với `type: 'color'` |
| Flower/Loại hoa | Tag với `type: 'flower'` |
| Event/Dịp | Tag với `type: 'event'` |
| Theme/Chủ đề | Tag với `type: 'theme'` |
| Season/Mùa | Tag với `type: 'season'` |

---

## 📁 Project Structure

```
siinstore-api/
├── src/
│   ├── collections/
│   │   ├── products/
│   │   │   ├── product/     # Product collection
│   │   │   ├── tag/         # Tag collection (SINGLE SOURCE)
│   │   │   ├── category/    # Category collection
│   │   │   ├── occasion/    # Occasion (standalone)
│   │   │   ├── age-range/   # AgeRange (standalone)
│   │   │   └── ...
│   │   └── ...
│   ├── payload.config.ts
│   └── globals/
│   └── app/
└── .claude/
    ├── rules/               # Project rules
    └── memory/              # Lessons learned
```

---

## 🎯 Development Checklist

### Trước khi thêm field/collection mới:

- [ ] Đọc `tag.contants.ts` — xem có type phù hợp chưa?
- [ ] Kiểm tra Product.ts — xem đã có relationship phù hợp chưa?
- [ ] So sánh với existing patterns (Tag, Occasion, AgeRange)
- [ ] Nếu không chắc → hỏi Steve trước khi code

### Systematic Debugging Rule:

> **KHÔNG BAO GIỜ tạo code mới khi chưa hiểu rõ architecture hiện tại**
>
> 1. Research → 2. Analyze → 3. Verify với Steve → 4. Implement

---

## 📝 Ghi chú khác

- Language: Tiếng Việt (comments, documentation)
- Indentation: 2 spaces
- Quotes: Single quotes `'` (frontend), Double quotes `"` (backend/Payload)
- No semicolons