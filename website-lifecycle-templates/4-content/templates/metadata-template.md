# Metadata Template

> **Mục đích**: Chuẩn hóa meta tags cho SEO và social sharing

---

## 📄 Basic Meta Tags

```html
<!-- Primary Meta Tags -->
<title>[Page Title - Max 60 chars] | [Brand Name]</title>
<meta name="title" content="[Page Title - Max 60 chars]">
<meta name="description" content="[Compelling description 150-160 chars]">
<meta name="keywords" content="[keyword1, keyword2, keyword3]">
<meta name="author" content="[Company Name]">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<link rel="canonical" href="[https://example.com/page-url]">
```

---

## 🌐 Open Graph (Facebook, LinkedIn)

```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="[https://example.com/page-url]">
<meta property="og:title" content="[Page Title - Max 60 chars]">
<meta property="og:description" content="[Description 150-160 chars]">
<meta property="og:image" content="[https://example.com/og-image.jpg]">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="[Brand Name]">
<meta property="og:locale" content="vi_VN">
```

**OG Image Requirements**:
- Kích thước: 1200x630px (tỷ lệ 1.91:1)
- Format: JPG hoặc PNG
- Dung lượng: < 300KB
- Nội dung: Logo + headline + visual

---

## 🐦 Twitter Card

```html
<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="[https://example.com/page-url]">
<meta property="twitter:title" content="[Page Title - Max 60 chars]">
<meta property="twitter:description" content="[Description 150-160 chars]">
<meta property="twitter:image" content="[https://example.com/twitter-image.jpg]">
<meta name="twitter:site" content="@[twitter_handle]">
<meta name="twitter:creator" content="@[author_handle]">
```

**Twitter Image Requirements**:
- Kích thước: 1200x675px (tỷ lệ 16:9)
- Format: JPG, PNG, WEBP, GIF
- Dung lượng: < 5MB

---

## 🔍 Schema.org Structured Data

### Website Schema
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[Brand Name]",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

### Organization Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://facebook.com/[page]",
    "https://twitter.com/[handle]",
    "https://instagram.com/[handle]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+84-xxx-xxx-xxx",
    "contactType": "Customer Service",
    "areaServed": "VN",
    "availableLanguage": "Vietnamese"
  }
}
```

### Product Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product Name]",
  "image": "[Product Image URL]",
  "description": "[Product Description]",
  "brand": {
    "@type": "Brand",
    "name": "[Brand Name]"
  },
  "offers": {
    "@type": "Offer",
    "url": "[Product URL]",
    "priceCurrency": "VND",
    "price": "[Price]",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2026-12-31"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "89"
  }
}
```

### Article Schema (Blog Posts)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Article Title]",
  "image": "[Article Image URL]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Company Name]",
    "logo": {
      "@type": "ImageObject",
      "url": "[Logo URL]"
    }
  },
  "datePublished": "2026-04-23",
  "dateModified": "2026-04-23",
  "description": "[Article Description]"
}
```

### Breadcrumb Schema
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[Category]",
      "item": "https://example.com/[category]"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[Current Page]",
      "item": "https://example.com/[category]/[page]"
    }
  ]
}
```

---

## 📱 Mobile App Meta Tags

```html
<!-- iOS -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="[App Name]">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<!-- Android -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#[hex-color]">
<link rel="manifest" href="/manifest.json">
```

---

## 🎯 Page-Specific Templates

### Homepage
```yaml
title: "[Brand Name] - [Tagline/Value Proposition]"
description: "[What you do] + [Key benefit] + [CTA hint]"
keywords: "primary keyword, secondary keyword, brand name"
og:type: "website"
schema: ["Organization", "WebSite"]
```

### Product Page
```yaml
title: "[Product Name] - [Key Feature] | [Brand]"
description: "[Product benefit] + [Price/Offer] + [CTA]"
keywords: "product name, category, feature keywords"
og:type: "product"
schema: ["Product", "Breadcrumb"]
```

### Blog Post
```yaml
title: "[Article Title - Max 60 chars]"
description: "[Article summary with hook]"
keywords: "topic keywords, related terms"
og:type: "article"
schema: ["Article", "Breadcrumb"]
```

### Category Page
```yaml
title: "[Category Name] - [Product Count] Products | [Brand]"
description: "Browse [number] [category] products. [Key benefits]"
keywords: "category name, product types, related terms"
og:type: "website"
schema: ["CollectionPage", "Breadcrumb"]
```

---

## ✅ Metadata Checklist

### Before Publishing
- [ ] Title tag: 50-60 characters, includes primary keyword
- [ ] Meta description: 150-160 characters, compelling copy
- [ ] OG image: 1200x630px, < 300KB
- [ ] Twitter image: 1200x675px, < 5MB
- [ ] Canonical URL: Set correctly
- [ ] Schema markup: Validated with Google Rich Results Test
- [ ] Keywords: 3-5 relevant keywords
- [ ] Robots meta: Set correctly (index/noindex)

### Testing Tools
- [ ] [Google Rich Results Test](https://search.google.com/test/rich-results)
- [ ] [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [ ] [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [ ] [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

---

## 🚨 Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Title > 60 chars (bị cắt) | Keep under 60 chars |
| Description < 120 chars (quá ngắn) | 150-160 chars optimal |
| Missing OG image | Always include OG image |
| Duplicate meta descriptions | Unique per page |
| No schema markup | Add relevant schema |
| Wrong canonical URL | Point to correct URL |

---

## 📊 Priority by Page Type

| Page Type | Must Have | Nice to Have |
|-----------|-----------|--------------|
| Homepage | Title, Description, OG, Schema (Org + Website) | Twitter Card |
| Product | Title, Description, OG, Schema (Product) | Reviews Schema |
| Blog | Title, Description, OG, Schema (Article) | Author Schema |
| Category | Title, Description, OG, Schema (Collection) | Breadcrumb |

---

## 🔗 Resources

- [Open Graph Protocol](https://ogp.me/)
- [Twitter Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- [Schema.org Documentation](https://schema.org/)
- [Google Search Central](https://developers.google.com/search/docs)
