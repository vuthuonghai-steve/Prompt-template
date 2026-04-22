# PayloadCMS — Tag Collection Pattern

> **CRITICAL**: Tag = Single Source of Truth cho Metadata
> **Last Updated**: 2026-04-16 (lessons from Phase 2 incident)

---

## Nguyên tắc VÀNG

```
⚠️  TRƯỚC KHI tạo collection mới cho metadata
✅  KIỂM TRA Tag collection trước
```

---

## Tag Collection Structure

### `tag.contants.ts` — TAG_TYPE enum

```typescript
export const TAG_TYPE = {
  THEME: 'theme',      // Chủ đề (Theme)
  SEASON: 'season',    // Mùa vụ (Season)
  EVENT: 'event',      // Sự kiện (Event)
  STYLE: 'style',       // Phong cách (Style)
  COLOR: 'color',       // Tone màu (Color) — THÊM 2026-04-16
  FLOWER: 'flower',    // Loại hoa (Flower) — THÊM 2026-04-16
  MARKETING: 'marketing',
  OTHER: 'other',
}
```

### Product.ts — Tags Relationship

```typescript
{
  name: 'tags',
  type: 'relationship',
  relationTo: 'tags',
  hasMany: true,
  label: 'Tags',
  admin: {
    description: 'Tags phân loại (Dịp, Phong cách, Màu sắc)',
  },
}
```

---

## Decision Matrix

| Metadata cần tạo | Action |
|-----------------|--------|
| Style/Kiểu cách | Dùng Tag + `type: 'style'` |
| Color/Tone màu | Dùng Tag + `type: 'color'` |
| Flower/Loại hoa | Dùng Tag + `type: 'flower'` |
| Event/Dịp | Dùng Tag + `type: 'event'` |
| Theme/Chủ đề | Dùng Tag + `type: 'theme'` |
| Season/Mùa vụ | Dùng Tag + `type: 'season'` |
| Metadata đặc thù khác | **Hỏi Steve** trước |

---

## Khi nào TẠO Collection riêng (mới)?

Chỉ khi CÓ ÍT NHẤT 1 trong:

1. ✅ Cần fields đặc biệt mà Tag không có
   - Ví dụ: `flower-types` cần `flowerColor`, `seasonal`, `wateringInfo`
   - Ví dụ: `color-tones` cần `hexCode`, `colorFamily`, `brightness`

2. ✅ Cần separate admin UI / permissions
   - Team A quản lý flower-types
   - Team B quản lý style-types

3. ✅ Cần independent CRUD logic/hooks
   - Auto-sync với external API
   - Complex validation

4. ✅ Steve explicit yêu cầu

---

## Checklist TRƯỚC KHI tạo Collection mới

```yaml
---
paths:
  - "src/collections/**/*.ts"
---
# Applies khi làm việc với collections
```

- [ ] Đọc `tag.contants.ts` — có TAG_TYPE phù hợp chưa?
- [ ] Đọc `Product.ts` — có `tags` relationship chưa?
- [ ] So sánh với Tag pattern — đồng nhất không?
- [ ] **Nếu không chắc** → Hỏi Steve trước khi code

---

## Sự cố đã xảy ra (2026-04-16)

| Sai | Đúng |
|-----|------|
| Tạo `StyleTypes` collection | Dùng Tag + `type: 'style'` |
| Tạo `ColorTones` collection | Dùng Tag + `type: 'color'` |
| Tạo `FlowerTypes` collection | Dùng Tag + `type: 'flower'` |

**Root cause**: Không đọc `tag.contants.ts` trước khi tạo collections mới

---

## Related Rules

- [payload.collections.md](./payload.collections.md) — Collection definitions
- [workflow.development.md](./workflow.development.md) — 3-Step process
