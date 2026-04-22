# Pattern: Mobile-First Design

## Nguồn
- Lovable
- v0 (Vercel)
- Cursor Agent

## Mô tả
Thiết kế cho mobile screen trước, sau đó scale up cho tablet và desktop. Đảm bảo core experience tốt trên mọi devices.

## Khi nào dùng
- Design phase: wireframe, mockup
- Development: CSS, responsive layout
- Testing: mobile testing first
- Optimization: mobile performance priority

## Cách áp dụng

### 1. Design Breakpoints
```css
/* Mobile first - base styles */
.container {
  padding: 1rem;
  font-size: 14px;
}

/* Tablet - 768px+ */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 16px;
  }
}

/* Desktop - 1024px+ */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### 2. Touch-Friendly UI
```typescript
// Minimum touch target: 44x44px (iOS), 48x48px (Android)
const TouchTarget = {
  minWidth: '48px',
  minHeight: '48px',
  padding: '12px',
}

// Spacing for fat fingers
const Spacing = {
  betweenButtons: '8px',
  betweenInputs: '16px',
}
```

### 3. Progressive Enhancement
```tsx
// Base: Mobile experience
function ProductCard({ product }: Props) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p className="price">{product.price}</p>
      <button>Add to Cart</button>
    </div>
  )
}

// Enhanced: Desktop features
function ProductCardDesktop({ product }: Props) {
  return (
    <div className="product-card desktop">
      <img src={product.image} alt={product.name} />
      <div className="details">
        <h3>{product.name}</h3>
        <p className="description">{product.description}</p>
        <div className="meta">
          <span className="rating">⭐ {product.rating}</span>
          <span className="reviews">({product.reviews} reviews)</span>
        </div>
        <p className="price">{product.price}</p>
        <div className="actions">
          <button>Add to Cart</button>
          <button className="wishlist">♥</button>
          <button className="compare">Compare</button>
        </div>
      </div>
    </div>
  )
}
```

## Ví dụ thực tế

### E-commerce Product Listing

```tsx
// Mobile-first product grid
function ProductGrid({ products }: Props) {
  return (
    <div className="grid">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

// CSS: Mobile first
const styles = `
/* Mobile: 1 column */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  padding: 1rem;
}

.product-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.product-card img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    padding: 2rem;
  }
}

/* Desktop: 3-4 columns */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

@media (min-width: 1280px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
`
```

### Mobile Navigation

```tsx
// Mobile: Hamburger menu
function MobileNav() {
  const [isOpen, setIsOpen] = useState(false)
  
  return (
    <>
      <button 
        className="hamburger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
      >
        ☰
      </button>
      
      {isOpen && (
        <nav className="mobile-menu">
          <a href="/products">Products</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </nav>
      )}
    </>
  )
}

// Desktop: Horizontal nav
function DesktopNav() {
  return (
    <nav className="desktop-menu">
      <a href="/products">Products</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </nav>
  )
}

// Responsive wrapper
function Navigation() {
  const isMobile = useMediaQuery('(max-width: 768px)')
  return isMobile ? <MobileNav /> : <DesktopNav />
}
```

## Mobile-First Checklist

### Design
- [ ] Wireframe mobile layout first
- [ ] Touch targets ≥ 48x48px
- [ ] Readable font sizes (≥ 16px body)
- [ ] Adequate spacing between interactive elements
- [ ] Thumb-friendly navigation placement

### Development
- [ ] Base styles for mobile
- [ ] Progressive enhancement với media queries
- [ ] Test on real devices
- [ ] Optimize images for mobile
- [ ] Lazy load below-the-fold content

### Performance
- [ ] First Contentful Paint < 1.8s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Total page size < 1MB
- [ ] Minimize JavaScript bundle
- [ ] Use responsive images

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Better mobile UX | Desktop có thể bị constrained |
| Faster mobile load | Cần test nhiều breakpoints |
| Forces prioritization | Có thể miss desktop opportunities |

## Best Practices
1. **Design constraints first**: Mobile forces focus on essentials
2. **Touch-friendly**: 48x48px minimum, adequate spacing
3. **Performance budget**: < 1MB total, < 1.8s FCP
4. **Test on real devices**: Emulators không đủ
5. **Progressive enhancement**: Add features for larger screens
6. **Thumb zones**: Place key actions in easy-reach areas

## Anti-patterns
- ❌ Desktop design rồi "squeeze" vào mobile
- ❌ Touch targets quá nhỏ (< 44px)
- ❌ Horizontal scrolling
- ❌ Tiny fonts (< 16px)
- ❌ Hover-dependent interactions

## Related Patterns
- [Design System First](./pattern-design-system-first.md)
- [Color System](./pattern-color-system.md)
