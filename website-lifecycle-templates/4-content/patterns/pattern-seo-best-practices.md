# Pattern: SEO Best Practices

## Nguồn
- NotionAI
- Perplexity
- Claude Code

## Mô tả
Optimize content cho search engines: metadata, structured data, semantic HTML, performance. Tăng organic traffic và visibility.

## Khi nào dùng
- Content phase: viết content SEO-friendly
- Development: implement technical SEO
- Testing: validate SEO compliance
- Maintenance: monitor và optimize rankings

## Cách áp dụng

### 1. On-Page SEO
```typescript
interface PageSEO {
  // Meta tags
  title: string              // 50-60 chars
  description: string        // 150-160 chars
  keywords?: string[]
  
  // Open Graph
  ogTitle: string
  ogDescription: string
  ogImage: string
  ogType: 'website' | 'product' | 'article'
  
  // Twitter Card
  twitterCard: 'summary' | 'summary_large_image'
  twitterTitle: string
  twitterDescription: string
  twitterImage: string
  
  // Structured data
  structuredData: object
  
  // Canonical
  canonical: string
}
```

### 2. Structured Data (Schema.org)
```typescript
// Product schema
const productSchema = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: 'Red Rose Bouquet',
  image: 'https://example.com/roses.jpg',
  description: 'Fresh red roses, perfect for romantic occasions',
  brand: {
    '@type': 'Brand',
    name: 'Flower Shop',
  },
  offers: {
    '@type': 'Offer',
    price: '500000',
    priceCurrency: 'VND',
    availability: 'https://schema.org/InStock',
    url: 'https://example.com/products/red-roses',
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.8',
    reviewCount: '127',
  },
}
```

### 3. Technical SEO
```typescript
// Sitemap generation
interface SitemapEntry {
  url: string
  lastmod: string
  changefreq: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly'
  priority: number
}

function generateSitemap(pages: Page[]): string {
  const entries = pages.map((page) => ({
    url: `https://example.com${page.path}`,
    lastmod: page.updatedAt.toISOString(),
    changefreq: page.changefreq,
    priority: page.priority,
  }))
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${entries.map((entry) => `
  <url>
    <loc>${entry.url}</loc>
    <lastmod>${entry.lastmod}</lastmod>
    <changefreq>${entry.changefreq}</changefreq>
    <priority>${entry.priority}</priority>
  </url>
  `).join('')}
</urlset>`
}
```

## Ví dụ thực tế

### E-commerce Product Page SEO

```tsx
// ProductPage.tsx
import { Metadata } from 'next'

export async function generateMetadata({ 
  params 
}: Props): Promise<Metadata> {
  const product = await getProduct(params.slug)
  
  return {
    title: `${product.name} | Flower Shop`,
    description: product.description.slice(0, 160),
    keywords: [
      product.name,
      product.category,
      ...product.tags,
      'fresh flowers',
      'flower delivery',
    ],
    
    // Open Graph
    openGraph: {
      title: product.name,
      description: product.description,
      images: [product.image],
      type: 'product',
      url: `https://flowershop.com/products/${product.slug}`,
    },
    
    // Twitter
    twitter: {
      card: 'summary_large_image',
      title: product.name,
      description: product.description,
      images: [product.image],
    },
    
    // Canonical
    alternates: {
      canonical: `https://flowershop.com/products/${product.slug}`,
    },
  }
}

function ProductPage({ product }: Props) {
  // Structured data
  const productSchema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    description: product.description,
    sku: product.sku,
    brand: {
      '@type': 'Brand',
      name: 'Flower Shop',
    },
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'VND',
      availability: product.inStock 
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
      url: `https://flowershop.com/products/${product.slug}`,
    },
    aggregateRating: product.rating && {
      '@type': 'AggregateRating',
      ratingValue: product.rating.average,
      reviewCount: product.rating.count,
    },
  }
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(productSchema),
        }}
      />
      
      <article itemScope itemType="https://schema.org/Product">
        <h1 itemProp="name">{product.name}</h1>
        <img itemProp="image" src={product.image} alt={product.name} />
        <p itemProp="description">{product.description}</p>
        <span itemProp="offers" itemScope itemType="https://schema.org/Offer">
          <meta itemProp="priceCurrency" content="VND" />
          <span itemProp="price">{product.price}</span>
        </span>
      </article>
    </>
  )
}
```

### Blog Post SEO

```tsx
// BlogPost.tsx
export async function generateMetadata({ 
  params 
}: Props): Promise<Metadata> {
  const post = await getPost(params.slug)
  
  return {
    title: `${post.title} | Flower Care Blog`,
    description: post.excerpt,
    authors: [{ name: post.author.name }],
    
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
    },
  }
}

function BlogPost({ post }: Props) {
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Flower Shop',
      logo: {
        '@type': 'ImageObject',
        url: 'https://flowershop.com/logo.png',
      },
    },
    description: post.excerpt,
  }
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(articleSchema),
        }}
      />
      
      <article>
        <h1>{post.title}</h1>
        <time dateTime={post.publishedAt}>
          {formatDate(post.publishedAt)}
        </time>
        <div dangerouslySetInnerHTML={{ __html: post.content }} />
      </article>
    </>
  )
}
```

### Sitemap Generation

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await getProducts()
  const posts = await getPosts()
  
  const productUrls = products.map((product) => ({
    url: `https://flowershop.com/products/${product.slug}`,
    lastModified: product.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))
  
  const postUrls = posts.map((post) => ({
    url: `https://flowershop.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'monthly' as const,
    priority: 0.6,
  }))
  
  return [
    {
      url: 'https://flowershop.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://flowershop.com/products',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    ...productUrls,
    ...postUrls,
  ]
}
```

## SEO Checklist

### On-Page
- [ ] Title tags (50-60 chars)
- [ ] Meta descriptions (150-160 chars)
- [ ] H1 tag (one per page)
- [ ] Semantic HTML (h2, h3, etc.)
- [ ] Alt text cho images
- [ ] Internal linking
- [ ] URL structure clean

### Technical
- [ ] Sitemap.xml
- [ ] Robots.txt
- [ ] Canonical URLs
- [ ] Structured data (Schema.org)
- [ ] Mobile-friendly
- [ ] Page speed (Core Web Vitals)
- [ ] HTTPS

### Content
- [ ] Keyword research
- [ ] Quality content (> 300 words)
- [ ] Regular updates
- [ ] Unique content (no duplicate)

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Organic traffic | Takes time (3-6 months) |
| Long-term ROI | Requires ongoing effort |
| Brand authority | Algorithm changes |

## Best Practices
1. **Focus on user intent**: Write for humans first
2. **Mobile-first**: Google mobile-first indexing
3. **Page speed**: Core Web Vitals matter
4. **Quality content**: Depth over quantity
5. **Regular updates**: Fresh content ranks better
6. **Internal linking**: Help crawlers discover pages

## Anti-patterns
- ❌ Keyword stuffing
- ❌ Duplicate content
- ❌ Thin content (< 300 words)
- ❌ Slow page speed
- ❌ Broken links
- ❌ Missing alt text

## Related Patterns
- [Content Guidelines](../templates/content-guidelines.md)
- [Metadata Template](../templates/metadata-template.md)
