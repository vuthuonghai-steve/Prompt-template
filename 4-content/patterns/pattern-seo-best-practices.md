# Pattern: SEO Best Practices

## Problem
Poor SEO → low visibility, không crawlable, slow performance.

## Solution
Implement SEO best practices AUTOMATICALLY cho mọi page/component.

**Core principles:**
- Always implement SEO by default
- Semantic HTML structure
- Optimized meta tags
- Performance optimization
- Mobile-first

## Example

### ✅ Good: Complete SEO Implementation
```tsx
// app/page.tsx
export const metadata = {
  title: "E-commerce Store - Buy Quality Products Online",
  description: "Shop the best products with fast shipping and great prices. Free returns on all orders.",
  keywords: ["e-commerce", "online shopping", "quality products"],
  openGraph: {
    title: "E-commerce Store",
    description: "Shop quality products online",
    images: ["/og-image.jpg"],
  },
}

export default function Page() {
  return (
    <>
      {/* Semantic HTML */}
      <header>
        <nav aria-label="Main navigation">...</nav>
      </header>
      
      <main>
        {/* Single H1 with main keyword */}
        <h1>Buy Quality Products Online</h1>
        
        <article>
          <h2>Featured Products</h2>
          {/* Optimized images */}
          <img 
            src="/product.jpg" 
            alt="Premium leather wallet with card slots"
            loading="lazy"
          />
        </article>
      </main>
      
      <footer>...</footer>
    </>
  )
}
```

### ❌ Bad: No SEO
```tsx
// DON'T do this
export default function Page() {
  return (
    <div>
      <div>Navigation</div>
      <div>
        <div>Title</div>
        <img src="/product.jpg" /> {/* No alt text */}
      </div>
    </div>
  )
}
```

## SEO Checklist

### 1. Meta Tags
```tsx
export const metadata = {
  // Title: < 60 characters, include main keyword
  title: "Main Keyword - Brand Name",
  
  // Description: < 160 characters, natural keyword integration
  description: "Compelling description with target keyword naturally integrated.",
  
  // Keywords
  keywords: ["keyword1", "keyword2", "keyword3"],
  
  // Open Graph
  openGraph: {
    title: "...",
    description: "...",
    images: ["/og-image.jpg"],
  },
  
  // Canonical URL
  alternates: {
    canonical: "https://example.com/page",
  },
}
```

### 2. Semantic HTML
```tsx
<header>
  <nav aria-label="Main navigation">...</nav>
</header>

<main>
  {/* Single H1 per page */}
  <h1>Main Page Title</h1>
  
  <article>
    <h2>Section Title</h2>
    <p>Content...</p>
  </article>
  
  <aside>
    <h2>Related Content</h2>
  </aside>
</main>

<footer>
  <nav aria-label="Footer navigation">...</nav>
</footer>
```

### 3. Image Optimization
```tsx
<img 
  src="/product.jpg"
  alt="Descriptive alt text with relevant keywords"
  loading="lazy"
  width={800}
  height={600}
/>
```

### 4. Structured Data (JSON-LD)
```tsx
// For products
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "image": "https://example.com/product.jpg",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD"
  }
}
</script>
```

### 5. Performance
```tsx
// Lazy loading
<img loading="lazy" />

// Defer non-critical scripts
<script src="analytics.js" defer />

// Viewport meta tag
export const viewport = {
  width: "device-width",
  initialScale: 1,
}
```

### 6. Mobile Optimization
```tsx
// Responsive design
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  ...
</div>

// Touch-friendly
<button className="min-h-[44px] min-w-[44px]">
  Click
</button>
```

### 7. Clean URLs
```tsx
// Good: /products/leather-wallet
// Bad: /products?id=123&cat=wallets
```

## Structured Data Types

### Product
```json
{
  "@type": "Product",
  "name": "...",
  "description": "...",
  "image": "...",
  "offers": { ... }
}
```

### Article
```json
{
  "@type": "Article",
  "headline": "...",
  "author": { ... },
  "datePublished": "..."
}
```

### FAQ
```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "...",
      "acceptedAnswer": { ... }
    }
  ]
}
```

## ARIA Attributes

```tsx
// Navigation
<nav aria-label="Main navigation">...</nav>

// Screen reader only text
<span className="sr-only">Skip to main content</span>

// Buttons
<button aria-label="Close dialog">×</button>

// Images (decorative)
<img src="decoration.jpg" alt="" aria-hidden="true" />
```

## Anti-patterns
- ❌ No meta description
- ❌ Multiple H1 tags
- ❌ Missing alt text
- ❌ Non-semantic HTML (all divs)
- ❌ No structured data
- ❌ Slow loading images
- ❌ No mobile optimization

## Checklist
- [ ] Title tag < 60 chars with keyword?
- [ ] Meta description < 160 chars?
- [ ] Single H1 with main keyword?
- [ ] Semantic HTML (header, main, footer)?
- [ ] All images have alt text?
- [ ] Structured data added?
- [ ] Lazy loading for images?
- [ ] Canonical tag set?
- [ ] Mobile responsive?
- [ ] Clean, crawlable URLs?

## Source
- Lovable - "SEO Requirements: ALWAYS implement SEO best practices"
- v0 (Vercel) - layout.tsx metadata guidelines
