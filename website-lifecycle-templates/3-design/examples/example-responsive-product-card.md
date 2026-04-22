# Example: Responsive Product Card Design

> **Context**: E-commerce flower shop
> **Component**: Product card with responsive behavior
> **Breakpoints**: Mobile (< 768px), Tablet (768-1024px), Desktop (> 1024px)

---

## 🎨 Design Overview

### Mobile Layout (< 768px)

```
┌─────────────────────────────────────┐
│  ┌───────────────────────────────┐  │
│  │                               │  │
│  │        Product Image          │  │
│  │        (Square 1:1)           │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
│  Rose Bouquet                       │
│  ★★★★★ (127 reviews)               │
│                                     │
│  500,000đ                           │
│                                     │
│  ┌───────────────────────────────┐ │
│  │      Add to Cart              │ │
│  └───────────────────────────────┘ │
│                                     │
│  Width: 100% (full width)           │
│  Padding: 16px                      │
│  Gap: 12px                          │
└─────────────────────────────────────┘
```

### Tablet Layout (768-1024px)

```
┌──────────────────┐  ┌──────────────────┐
│  ┌────────────┐  │  │  ┌────────────┐  │
│  │            │  │  │  │            │  │
│  │   Image    │  │  │  │   Image    │  │
│  │            │  │  │  │            │  │
│  └────────────┘  │  │  └────────────┘  │
│                  │  │                  │
│  Rose Bouquet    │  │  Tulip Mix       │
│  ★★★★★ (127)    │  │  ★★★★☆ (89)     │
│  500,000đ        │  │  350,000đ        │
│  [Add to Cart]   │  │  [Add to Cart]   │
└──────────────────┘  └──────────────────┘

Grid: 2 columns
Gap: 24px
Card width: ~48%
```

### Desktop Layout (> 1024px)

```
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │
│  │Image │  │ │  │Image │  │ │  │Image │  │ │  │Image │  │
│  └──────┘  │ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │
│  Rose      │ │  Tulip     │ │  Orchid    │ │  Lily      │
│  ★★★★★    │ │  ★★★★☆    │ │  ★★★★★    │ │  ★★★★☆    │
│  500,000đ  │ │  350,000đ  │ │  800,000đ  │ │  450,000đ  │
│  [+ Cart]  │ │  [+ Cart]  │ │  [+ Cart]  │ │  [+ Cart]  │
└────────────┘ └────────────┘ └────────────┘ └────────────┘

Grid: 4 columns
Gap: 32px
Card width: ~23%
```

---

## 💻 Implementation

### HTML Structure

```tsx
// ProductCard.tsx
interface ProductCardProps {
  product: {
    id: string
    name: string
    price: number
    image: string
    rating: number
    reviewCount: number
    inStock: boolean
  }
  onAddToCart: (id: string) => void
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <article className="product-card">
      {/* Image */}
      <div className="product-card__image-wrapper">
        <img
          src={product.image}
          alt={product.name}
          className="product-card__image"
          loading="lazy"
        />
        {!product.inStock && (
          <div className="product-card__badge">Out of Stock</div>
        )}
      </div>
      
      {/* Content */}
      <div className="product-card__content">
        <h3 className="product-card__title">{product.name}</h3>
        
        {/* Rating */}
        <div className="product-card__rating">
          <div className="stars" aria-label={`${product.rating} out of 5 stars`}>
            {renderStars(product.rating)}
          </div>
          <span className="review-count">({product.reviewCount})</span>
        </div>
        
        {/* Price */}
        <p className="product-card__price">
          {formatPrice(product.price)}
        </p>
        
        {/* Action */}
        <button
          className="product-card__button"
          onClick={() => onAddToCart(product.id)}
          disabled={!product.inStock}
        >
          {product.inStock ? 'Add to Cart' : 'Out of Stock'}
        </button>
      </div>
    </article>
  )
}
```

### CSS (Mobile-First)

```css
/* Base styles (Mobile) */
.product-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.product-card__image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 100%; /* 1:1 aspect ratio */
  overflow: hidden;
  background: #f3f4f6;
}

.product-card__image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-card__image {
  transform: scale(1.05);
}

.product-card__badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
}

.product-card__content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-card__title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  line-height: 1.4;
  /* Truncate to 2 lines */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-card__rating {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.stars {
  color: #f59e0b;
  display: flex;
  gap: 2px;
}

.review-count {
  color: #6b7280;
  font-size: 13px;
}

.product-card__price {
  font-size: 20px;
  font-weight: 700;
  color: #ec4899;
  margin: 4px 0;
}

.product-card__button {
  width: 100%;
  padding: 12px;
  background: #ec4899;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.product-card__button:hover:not(:disabled) {
  background: #db2777;
}

.product-card__button:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .product-card__content {
    padding: 20px;
    gap: 10px;
  }
  
  .product-card__title {
    font-size: 18px;
  }
  
  .product-card__price {
    font-size: 22px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .product-card__content {
    padding: 24px;
  }
  
  .product-card__button {
    padding: 14px;
  }
}
```

### Grid Layout

```css
/* Product grid container */
.product-grid {
  display: grid;
  gap: 16px;
  padding: 16px;
}

/* Mobile: 1 column */
@media (max-width: 767px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}

/* Tablet: 2 columns */
@media (min-width: 768px) and (max-width: 1023px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    padding: 24px;
  }
}

/* Desktop: 4 columns */
@media (min-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 32px;
    padding: 32px;
    max-width: 1400px;
    margin: 0 auto;
  }
}

/* Large desktop: 4-5 columns */
@media (min-width: 1440px) {
  .product-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
```

---

## 📱 Responsive Behavior Details

### Image Aspect Ratio

```css
/* Mobile: Square (1:1) */
@media (max-width: 767px) {
  .product-card__image-wrapper {
    padding-top: 100%; /* 1:1 */
  }
}

/* Tablet+: Slightly taller (4:5) */
@media (min-width: 768px) {
  .product-card__image-wrapper {
    padding-top: 125%; /* 4:5 */
  }
}
```

### Typography Scaling

```css
/* Mobile */
.product-card__title {
  font-size: 16px;
  line-height: 1.4;
}

.product-card__price {
  font-size: 20px;
}

/* Tablet */
@media (min-width: 768px) {
  .product-card__title {
    font-size: 18px;
  }
  
  .product-card__price {
    font-size: 22px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .product-card__title {
    font-size: 18px;
  }
  
  .product-card__price {
    font-size: 24px;
  }
}
```

### Touch Targets

```css
/* Mobile: Larger touch targets */
@media (max-width: 767px) {
  .product-card__button {
    min-height: 48px; /* WCAG 2.1 minimum */
    font-size: 16px;
  }
}

/* Desktop: Standard size */
@media (min-width: 768px) {
  .product-card__button {
    min-height: 44px;
    font-size: 15px;
  }
}
```

---

## ✅ Responsive Checklist

### Mobile (< 768px)
- [x] Full-width cards
- [x] Square images (1:1)
- [x] Touch-friendly buttons (≥ 48px)
- [x] Readable text (≥ 16px)
- [x] Adequate spacing (16px padding)

### Tablet (768-1024px)
- [x] 2-column grid
- [x] Balanced card proportions
- [x] Hover states work
- [x] Comfortable spacing (24px gap)

### Desktop (> 1024px)
- [x] 4-column grid
- [x] Hover effects smooth
- [x] Max-width container (1400px)
- [x] Generous spacing (32px gap)

---

## 🧪 Testing Scenarios

### Visual Testing
- [ ] Cards render correctly at all breakpoints
- [ ] Images maintain aspect ratio
- [ ] Text doesn't overflow
- [ ] Hover states work on desktop
- [ ] Touch states work on mobile

### Performance Testing
- [ ] Images lazy load
- [ ] Smooth transitions
- [ ] No layout shift (CLS)
- [ ] Fast paint times

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Screen reader announces product info
- [ ] Color contrast passes WCAG AA
- [ ] Touch targets ≥ 44x44px
