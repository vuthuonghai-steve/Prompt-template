# Pattern: Context Gathering

## Nguồn
- Claude Code
- Windsurf Cascade
- Cursor Agent

## Mô tả
Thu thập context đầy đủ trước khi đưa ra quyết định hoặc implement. Tránh assumptions sai, giảm rework.

## Khi nào dùng
- Discovery phase: hiểu business requirements
- Planning: xác định tech stack, architecture
- Development: trước khi code feature mới
- Debugging: tìm root cause

## Cách áp dụng

### 1. Structured Questions
```markdown
## Business Context
- Mục tiêu business?
- Target audience?
- Success metrics?

## Technical Context
- Existing systems?
- Constraints (budget, timeline, tech)?
- Integration requirements?

## User Context
- User pain points?
- Current workflow?
- Expected behavior?
```

### 2. Multi-source Gathering
- Stakeholder interviews
- User research
- Competitor analysis
- Technical documentation
- Analytics data

### 3. Context Validation
- Confirm understanding với stakeholders
- Cross-check thông tin từ nhiều nguồn
- Document assumptions rõ ràng

## Ví dụ thực tế

### E-commerce Flower Shop Discovery

**Business Context:**
```yaml
Goal: Tăng conversion rate 20% trong Q2
Target: Khách hàng 25-45 tuổi, urban, middle-income
Pain points:
  - Khó chọn hoa phù hợp với dịp
  - Không biết hoa nào tươi lâu
  - Lo lắng về delivery time
```

**Technical Context:**
```yaml
Current stack:
  - Frontend: React (legacy)
  - Backend: Node.js + MongoDB
  - Payment: VNPay, Momo
  - Delivery: Giao Hàng Nhanh API

Constraints:
  - Budget: 200M VND
  - Timeline: 3 months
  - Team: 2 FE, 2 BE, 1 Designer
```

**User Context:**
```yaml
User journey:
  1. Browse by occasion (birthday, wedding, etc.)
  2. Filter by price, style
  3. View product details + care instructions
  4. Add to cart
  5. Checkout with delivery scheduling
  6. Track order

Pain points:
  - Quá nhiều options → overwhelmed
  - Không rõ hoa có tươi không
  - Delivery time không flexible
```

## Context Gathering Checklist

### Discovery Phase
- [ ] Business goals documented?
- [ ] Target audience defined?
- [ ] Success metrics agreed?
- [ ] Budget & timeline confirmed?
- [ ] Technical constraints identified?
- [ ] User pain points validated?
- [ ] Competitor analysis done?
- [ ] Stakeholder alignment achieved?

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Giảm rework | Tốn thời gian upfront |
| Quyết định đúng hơn | Có thể over-analyze |
| Alignment tốt hơn | Cần skill hỏi đúng câu |

## Best Practices
1. **Start broad, then narrow**: Hiểu big picture trước khi dive vào details
2. **Document everything**: Context sẽ bị quên nếu không ghi lại
3. **Validate assumptions**: Đừng assume, hãy confirm
4. **Iterate**: Context gathering là continuous process
5. **Share context**: Đảm bảo team cùng hiểu

## Anti-patterns
- ❌ Assume based on past projects
- ❌ Skip stakeholder validation
- ❌ Gather context nhưng không document
- ❌ Gather quá nhiều context không cần thiết

## Related Patterns
- [Semantic Search](./pattern-semantic-search.md)
- [Parallel Tool Calls](./pattern-parallel-tool-calls.md)
