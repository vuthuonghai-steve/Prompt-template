# Performance Checklist

> **Mục đích**: Optimize website performance cho Core Web Vitals & Lighthouse scores

---

## 🎯 Performance Goals

| Metric | Target | Current |
|--------|--------|---------|
| **Lighthouse Performance** | > 90 | ___ |
| **LCP** (Largest Contentful Paint) | < 2.5s | ___ |
| **FID** (First Input Delay) | < 100ms | ___ |
| **CLS** (Cumulative Layout Shift) | < 0.1 | ___ |
| **TTFB** (Time to First Byte) | < 600ms | ___ |
| **FCP** (First Contentful Paint) | < 1.8s | ___ |

---

## 📊 Lighthouse Audit

### Run Lighthouse
```bash
# Chrome DevTools
# 1. Open DevTools (F12)
# 2. Go to Lighthouse tab
# 3. Select categories: Performance, Accessibility, Best Practices, SEO
# 4. Click "Analyze page load"

# CLI
npm install -g lighthouse
lighthouse https://your-site.com --view
```

### Checklist
- [ ] Performance score > 90
- [ ] Accessibility score > 90
- [ ] Best Practices score > 90
- [ ] SEO score > 90
- [ ] No critical issues in report

---

## ⚡ Core Web Vitals Optimization

### LCP (Largest Contentful Paint) < 2.5s
- [ ] Optimize images (WebP, AVIF, lazy loading)
- [ ] Preload critical resources (fonts, hero images)
- [ ] Use CDN for static assets
- [ ] Minimize render-blocking resources
- [ ] Server-side rendering (SSR) for critical content

```html
<!-- Preload hero image -->
<link rel="preload" as="image" href="/hero.webp" />

<!-- Lazy load below-fold images -->
<img src="product.webp" loading="lazy" alt="Product" />
```

### FID (First Input Delay) < 100ms
- [ ] Minimize JavaScript execution time
- [ ] Code splitting & lazy loading
- [ ] Remove unused JavaScript
- [ ] Use web workers for heavy computations
- [ ] Defer non-critical scripts

```javascript
// Code splitting with dynamic import
const HeavyComponent = lazy(() => import('./HeavyComponent'))
```

### CLS (Cumulative Layout Shift) < 0.1
- [ ] Set explicit width/height for images & videos
- [ ] Reserve space for ads & embeds
- [ ] Avoid inserting content above existing content
- [ ] Use CSS aspect-ratio for responsive images
- [ ] Preload fonts to avoid FOIT/FOUT

```css
/* Reserve space for image */
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}
```

---

## 🖼️ Image Optimization

### Format & Compression
- [ ] Use modern formats (WebP, AVIF)
- [ ] Compress images (TinyPNG, Squoosh)
- [ ] Serve responsive images (srcset)
- [ ] Lazy load below-fold images
- [ ] Use image CDN (Cloudinary, Imgix)

```html
<!-- Responsive images -->
<picture>
  <source srcset="hero.avif" type="image/avif" />
  <source srcset="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="Hero" width="1200" height="600" />
</picture>
```

### Image Checklist
- [ ] All images < 200KB
- [ ] Hero images < 500KB
- [ ] Use WebP/AVIF with JPEG fallback
- [ ] Lazy loading enabled
- [ ] Explicit dimensions set

---

## 📦 Bundle Optimization

### JavaScript
- [ ] Code splitting by route
- [ ] Tree shaking enabled
- [ ] Remove unused dependencies
- [ ] Minify & compress (gzip/brotli)
- [ ] Analyze bundle size (webpack-bundle-analyzer)

```bash
# Analyze bundle
npm run build
npx webpack-bundle-analyzer dist/stats.json
```

### CSS
- [ ] Remove unused CSS (PurgeCSS)
- [ ] Critical CSS inlined
- [ ] Minify CSS
- [ ] Use CSS-in-JS with SSR

---

## 🌐 Network Optimization

### Caching Strategy
- [ ] Set cache headers (max-age, immutable)
- [ ] Use service worker for offline support
- [ ] Cache static assets (images, fonts, CSS, JS)
- [ ] Implement stale-while-revalidate

```javascript
// Service worker caching
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request)
    })
  )
})
```

### CDN & Compression
- [ ] Use CDN for static assets
- [ ] Enable gzip/brotli compression
- [ ] Minimize DNS lookups
- [ ] Use HTTP/2 or HTTP/3
- [ ] Preconnect to third-party domains

```html
<!-- Preconnect to CDN -->
<link rel="preconnect" href="https://cdn.example.com" />
<link rel="dns-prefetch" href="https://analytics.example.com" />
```

---

## 🔤 Font Optimization

- [ ] Use system fonts or web fonts sparingly
- [ ] Preload critical fonts
- [ ] Use font-display: swap
- [ ] Subset fonts (only needed characters)
- [ ] Self-host fonts (avoid Google Fonts latency)

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
}
```

---

## 🧪 Load Testing

### Tools
- **k6**: Modern load testing tool
- **Artillery**: Easy-to-use load testing
- **Apache JMeter**: Enterprise load testing

### Test Scenarios
```javascript
// k6 load test
import http from 'k6/http'
import { check, sleep } from 'k6'

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
}

export default function () {
  let res = http.get('https://your-site.com')
  check(res, { 'status is 200': (r) => r.status === 200 })
  sleep(1)
}
```

### Load Test Checklist
- [ ] Test with 100 concurrent users
- [ ] Test with 500 concurrent users
- [ ] Test with 1000 concurrent users
- [ ] Response time < 500ms (p95)
- [ ] Error rate < 1%
- [ ] Server CPU < 70%
- [ ] Server memory < 80%

---

## 📱 Mobile Performance

### Mobile-Specific Optimization
- [ ] Reduce JavaScript for mobile
- [ ] Use smaller images for mobile
- [ ] Test on real devices (not just emulators)
- [ ] Optimize for 3G/4G networks
- [ ] Use adaptive loading

```javascript
// Adaptive loading based on network
if (navigator.connection.effectiveType === '4g') {
  // Load high-quality images
} else {
  // Load low-quality images
}
```

### Mobile Testing
- [ ] iPhone 12/13/14 (Safari)
- [ ] Samsung Galaxy S21 (Chrome)
- [ ] iPad Pro (Safari)
- [ ] Test on slow 3G network
- [ ] Test on throttled CPU

---

## 🔍 Monitoring & Analytics

### Real User Monitoring (RUM)
- [ ] Set up Google Analytics 4
- [ ] Track Core Web Vitals
- [ ] Monitor page load times
- [ ] Track error rates
- [ ] Set up alerts for performance degradation

```javascript
// Track Core Web Vitals
import { getCLS, getFID, getLCP } from 'web-vitals'

getCLS(console.log)
getFID(console.log)
getLCP(console.log)
```

### Performance Budget
- [ ] Set performance budget (Lighthouse CI)
- [ ] Fail CI if budget exceeded
- [ ] Monitor bundle size over time

```json
// lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }]
      }
    }
  }
}
```

---

## ✅ Final Checklist

### Before Launch
- [ ] Lighthouse Performance > 90
- [ ] Core Web Vitals pass (LCP, FID, CLS)
- [ ] Load test passed (1000 concurrent users)
- [ ] Mobile performance optimized
- [ ] CDN configured
- [ ] Caching strategy implemented
- [ ] Monitoring & alerts set up
- [ ] Performance budget enforced in CI

### Post-Launch
- [ ] Monitor Core Web Vitals daily
- [ ] Review performance reports weekly
- [ ] Optimize based on real user data
- [ ] A/B test performance improvements

---

## 🔗 Resources

- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [k6 Load Testing](https://k6.io/)
- [WebPageTest](https://www.webpagetest.org/)
