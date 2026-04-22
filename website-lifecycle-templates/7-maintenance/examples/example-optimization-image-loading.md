# Performance Optimization Example: Image Loading

> **Real-world example**: Optimizing product image loading for faster page speed

---

## 📊 Performance Issue

**Issue ID**: PERF-2026-04-10-015  
**Reported**: 2026-04-10 11:30 UTC  
**Priority**: 🟡 Medium  
**Status**: 🟢 Optimized  

### Problem Statement

Product listing page loads slowly on mobile devices. Users experience 5-8 second load times, causing high bounce rates (45% on mobile).

### Metrics Before Optimization

| Metric | Desktop | Mobile |
|--------|---------|--------|
| **Page Load Time** | 2.8s | 7.2s |
| **Largest Contentful Paint (LCP)** | 2.1s | 6.8s |
| **First Contentful Paint (FCP)** | 1.2s | 3.5s |
| **Time to Interactive (TTI)** | 3.5s | 9.1s |
| **Lighthouse Score** | 78 | 42 |
| **Bounce Rate** | 28% | 45% |

---

## 🔍 Root Cause Analysis

### Investigation

```bash
# 1. Lighthouse audit
npm run lighthouse -- --url=https://siinstore.com/products

# 2. Network analysis
# Found: 24 product images loaded at full resolution (2000x2000px)
# Each image: 800KB - 1.2MB
# Total: ~20MB of images on initial load

# 3. Chrome DevTools Performance
# Main thread blocked by image decoding
# Layout shifts from images loading
```

### Issues Identified

1. **Full-resolution images**: Loading 2000x2000px images for 300x300px thumbnails
2. **No lazy loading**: All 24 images load immediately
3. **No modern formats**: Using JPEG only (no WebP/AVIF)
4. **No responsive images**: Same image for all screen sizes
5. **No CDN optimization**: Images served from origin server

---

## 🛠️ Optimization Strategy

### 1. Image Resizing & Format Optimization

```typescript
// ❌ BEFORE
<img 
  src={`${API_URL}/products/${product.id}/image.jpg`}
  alt={product.name}
  className="w-[300px] h-[300px]"
/>

// ✅ AFTER
<Image
  src={`${CDN_URL}/products/${product.id}/image.jpg`}
  alt={product.name}
  width={300}
  height={300}
  sizes="(max-width: 768px) 100vw, 300px"
  quality={85}
  placeholder="blur"
  blurDataURL={product.blurDataUrl}
/>
```

### 2. Lazy Loading Implementation

```typescript
// components/ProductCard.tsx
import { LazyLoadImage } from 'react-lazy-load-image-component'

export const ProductCard = ({ product }: Props) => {
  return (
    <div className="product-card">
      <LazyLoadImage
        src={product.imageUrl}
        alt={product.name}
        width={300}
        height={300}
        effect="blur"
        threshold={100}  // Start loading 100px before visible
        placeholderSrc={product.thumbnailUrl}
      />
      {/* ... */}
    </div>
  )
}
```

### 3. Responsive Images with srcset

```typescript
// utils/util.image-srcset.ts
export const generateImageSrcSet = (imageId: string) => {
  const sizes = [300, 600, 900, 1200]
  
  return {
    srcSet: sizes
      .map(size => `${CDN_URL}/products/${imageId}/w_${size}.webp ${size}w`)
      .join(', '),
    sizes: '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 300px',
  }
}

// Usage
<img
  src={`${CDN_URL}/products/${product.id}/w_300.webp`}
  srcSet={generateImageSrcSet(product.imageId).srcSet}
  sizes={generateImageSrcSet(product.imageId).sizes}
  alt={product.name}
  loading="lazy"
/>
```

### 4. CDN Configuration (Cloudflare)

```typescript
// next.config.js
module.exports = {
  images: {
    domains: ['cdn.siinstore.com'],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60 * 60 * 24 * 30,  // 30 days
  },
}
```

### 5. Image Optimization Pipeline

```typescript
// scripts/optimize-images.ts
import sharp from 'sharp'
import { uploadToCDN } from './cdn'

const optimizeProductImage = async (imagePath: string, productId: string) => {
  const sizes = [300, 600, 900, 1200]
  
  for (const size of sizes) {
    // WebP
    await sharp(imagePath)
      .resize(size, size, { fit: 'cover' })
      .webp({ quality: 85 })
      .toFile(`./optimized/${productId}_${size}.webp`)
    
    // AVIF (better compression)
    await sharp(imagePath)
      .resize(size, size, { fit: 'cover' })
      .avif({ quality: 80 })
      .toFile(`./optimized/${productId}_${size}.avif`)
    
    // Fallback JPEG
    await sharp(imagePath)
      .resize(size, size, { fit: 'cover' })
      .jpeg({ quality: 85, progressive: true })
      .toFile(`./optimized/${productId}_${size}.jpg`)
  }
  
  // Generate blur placeholder (20px)
  const blurDataUrl = await sharp(imagePath)
    .resize(20, 20, { fit: 'cover' })
    .blur(10)
    .webp({ quality: 50 })
    .toBuffer()
    .then(buffer => `data:image/webp;base64,${buffer.toString('base64')}`)
  
  // Upload to CDN
  await uploadToCDN(`./optimized/${productId}_*`, `products/${productId}/`)
  
  return { blurDataUrl }
}
```

---

## 📊 Results After Optimization

### Performance Metrics

| Metric | Desktop | Mobile | Improvement |
|--------|---------|--------|-------------|
| **Page Load Time** | 1.2s ⬇️ | 2.8s ⬇️ | 58% faster (mobile) |
| **LCP** | 0.9s ⬇️ | 2.1s ⬇️ | 69% faster (mobile) |
| **FCP** | 0.6s ⬇️ | 1.4s ⬇️ | 60% faster (mobile) |
| **TTI** | 1.8s ⬇️ | 3.5s ⬇️ | 62% faster (mobile) |
| **Lighthouse Score** | 95 ⬆️ | 88 ⬆️ | +46 points (mobile) |
| **Bounce Rate** | 22% ⬇️ | 28% ⬇️ | 38% reduction (mobile) |

### Image Size Reduction

| Format | Before | After | Savings |
|--------|--------|-------|---------|
| **JPEG (full)** | 1.2MB | - | - |
| **JPEG (optimized)** | - | 85KB | 93% |
| **WebP** | - | 42KB | 96.5% |
| **AVIF** | - | 28KB | 97.7% |

### Network Impact

```
Before: 24 images × 1.2MB = 28.8MB total
After:  24 images × 42KB (WebP) = 1.01MB total
Savings: 96.5% reduction in image payload
```

---

## 🔧 Implementation Details

### Files Changed

| File | Changes | Purpose |
|------|---------|---------|
| `components/ProductCard.tsx` | Lazy loading | Defer offscreen images |
| `utils/util.image-srcset.ts` | Responsive images | Serve correct size |
| `next.config.js` | CDN config | Enable modern formats |
| `scripts/optimize-images.ts` | Image pipeline | Batch optimization |
| `services/service.product.ts` | Add blurDataUrl | Placeholder support |

### Deployment Steps

```bash
# 1. Optimize existing images
npm run optimize:images -- --batch=all

# 2. Upload to CDN
npm run cdn:upload -- --source=./optimized --dest=products/

# 3. Update database with blur placeholders
npm run db:migrate -- --migration=add-blur-data-urls

# 4. Deploy code changes
npm run deploy:production

# 5. Verify
npm run lighthouse -- --url=https://siinstore.com/products
```

---

## 📈 Business Impact

### User Experience

- **Mobile bounce rate**: 45% → 28% (38% reduction)
- **Avg session duration**: 2.3min → 3.8min (65% increase)
- **Pages per session**: 3.2 → 4.7 (47% increase)

### SEO Impact

- **Google PageSpeed Score**: 42 → 88 (mobile)
- **Core Web Vitals**: Failed → Passed
- **Search ranking**: Position 8 → Position 4 (product category)

### Revenue Impact

- **Conversion rate**: 2.1% → 2.8% (33% increase)
- **Revenue lift**: +$12,000/month (estimated)
- **ROI**: 15x (optimization cost: $800, monthly gain: $12K)

---

## 🔄 Ongoing Optimization

### Automated Pipeline

```yaml
# .github/workflows/optimize-images.yml
name: Optimize Product Images

on:
  push:
    paths:
      - 'public/products/**/*.jpg'
      - 'public/products/**/*.png'

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Optimize images
        run: npm run optimize:images -- --changed-only
      
      - name: Upload to CDN
        run: npm run cdn:upload
      
      - name: Update database
        run: npm run db:update-image-urls
```

### Monitoring

```typescript
// monitoring/image-performance.ts
export const trackImagePerformance = () => {
  // Track LCP for product images
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.entryType === 'largest-contentful-paint') {
        analytics.track('LCP', {
          value: entry.renderTime,
          element: entry.element?.tagName,
          url: entry.url,
        })
      }
    }
  }).observe({ entryTypes: ['largest-contentful-paint'] })
  
  // Track image load times
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.initiatorType === 'img') {
        analytics.track('Image Load', {
          duration: entry.duration,
          size: entry.transferSize,
          url: entry.name,
        })
      }
    }
  }).observe({ entryTypes: ['resource'] })
}
```

---

## 📚 Lessons Learned

### What Went Well

1. **Significant impact**: 96.5% reduction in image payload
2. **User experience**: Bounce rate reduced by 38%
3. **SEO boost**: Core Web Vitals passed, ranking improved
4. **Automated pipeline**: Future images auto-optimized

### What Could Be Improved

1. **Earlier detection**: Should have monitored LCP from launch
2. **Testing**: Should have tested on real mobile devices earlier
3. **Documentation**: Image optimization guidelines not documented

### Best Practices Established

1. **Image guidelines**:
   - Max upload size: 2MB
   - Recommended: 1200x1200px for product images
   - Auto-generate: 300px, 600px, 900px, 1200px variants
   - Formats: AVIF (primary), WebP (fallback), JPEG (legacy)

2. **Performance budget**:
   - LCP < 2.5s (mobile)
   - Total image payload < 2MB per page
   - Lighthouse score > 85 (mobile)

3. **Monitoring**:
   - Weekly Lighthouse audits
   - Real User Monitoring (RUM) for LCP
   - Alert if mobile LCP > 3s

---

## 🔗 References

- **Issue**: #PERF-2026-04-10-015
- **PR**: #1289 (Image optimization)
- **Lighthouse Report**: [Before](https://lighthouse-report.com/before) | [After](https://lighthouse-report.com/after)
- **CDN Dashboard**: https://dash.cloudflare.com/siinstore
- **Performance Dashboard**: https://analytics.siinstore.com/performance

---

## 👥 Team

- **Developer**: Alice Johnson
- **DevOps**: Bob Wilson (CDN setup)
- **Designer**: Carol Lee (image quality review)
- **Product**: David Chen (business impact analysis)

---

**Optimization Type**: Image Loading  
**Impact**: High (96.5% payload reduction)  
**Effort**: Medium (2 days)  
**ROI**: 15x
