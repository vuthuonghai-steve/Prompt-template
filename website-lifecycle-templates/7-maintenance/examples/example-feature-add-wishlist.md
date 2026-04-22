# Feature Addition Example: Wishlist

> **Real-world example**: Adding wishlist functionality to e-commerce platform

---

## ✨ Feature Request

**Feature ID**: FEAT-2026-04-05-023  
**Requested**: 2026-04-05 14:20 UTC  
**Priority**: 🟡 Medium  
**Status**: 🟢 Shipped  

### Business Case

**Problem**: Users have no way to save products for later, leading to lost sales opportunities.

**Solution**: Implement wishlist feature allowing users to save products and receive notifications on price drops.

**Expected Impact**:
- Increase user engagement (return visits)
- Reduce cart abandonment
- Enable targeted marketing campaigns
- Increase conversion rate by 15-20%

---

## 📋 Requirements

### Functional Requirements

1. **Add to Wishlist**: Users can add products from listing/detail pages
2. **View Wishlist**: Dedicated page showing all saved products
3. **Remove from Wishlist**: Users can remove items
4. **Move to Cart**: Quick action to move wishlist item to cart
5. **Price Drop Alerts**: Email notification when wishlist item goes on sale
6. **Share Wishlist**: Generate shareable link for gift registries
7. **Guest Wishlist**: Anonymous users can save to local storage

### Non-Functional Requirements

- **Performance**: Add/remove actions < 200ms
- **Scalability**: Support 100+ items per user
- **Mobile-first**: Optimized for mobile experience
- **Accessibility**: WCAG 2.1 AA compliant

---

## 🏗️ Architecture Design

### Database Schema

```typescript
// collections/wishlist/wishlist.ts
export const Wishlist: CollectionConfig = {
  slug: 'wishlists',
  fields: [
    {
      name: 'user',
      type: 'relationship',
      relationTo: 'users',
      required: true,
      index: true,
    },
    {
      name: 'items',
      type: 'array',
      fields: [
        {
          name: 'product',
          type: 'relationship',
          relationTo: 'products',
          required: true,
        },
        {
          name: 'addedAt',
          type: 'date',
          required: true,
          defaultValue: () => new Date().toISOString(),
        },
        {
          name: 'priceWhenAdded',
          type: 'number',
          required: true,
        },
        {
          name: 'notifyOnPriceDrop',
          type: 'checkbox',
          defaultValue: true,
        },
      ],
    },
    {
      name: 'isPublic',
      type: 'checkbox',
      defaultValue: false,
    },
    {
      name: 'shareToken',
      type: 'text',
      unique: true,
      admin: {
        readOnly: true,
      },
    },
  ],
}
```

### API Endpoints

```typescript
// api/config/endpoint.ts
export const ENDPOINTS = {
  WISHLIST: {
    GET: '/api/v1/wishlist',
    ADD: '/api/v1/wishlist/add',
    REMOVE: '/api/v1/wishlist/remove/:itemId',
    MOVE_TO_CART: '/api/v1/wishlist/move-to-cart/:itemId',
    SHARE: '/api/v1/wishlist/share',
    PUBLIC: '/api/v1/wishlist/public/:token',
  },
}
```

### Service Layer

```typescript
// services/wishlist/service.wishlist.ts
export class WishlistService {
  async addItem(userId: string, productId: string): Promise<WishlistItem> {
    const product = await payload.findByID({
      collection: 'products',
      id: productId,
    })
    
    const wishlist = await this.getOrCreateWishlist(userId)
    
    // Check if already in wishlist
    const exists = wishlist.items.some(item => item.product.id === productId)
    if (exists) {
      throw new Error('Product already in wishlist')
    }
    
    const newItem = {
      product: productId,
      addedAt: new Date().toISOString(),
      priceWhenAdded: product.price,
      notifyOnPriceDrop: true,
    }
    
    await payload.update({
      collection: 'wishlists',
      id: wishlist.id,
      data: {
        items: [...wishlist.items, newItem],
      },
    })
    
    // Track analytics
    analytics.track('Wishlist Item Added', {
      userId,
      productId,
      price: product.price,
    })
    
    return newItem
  }
  
  async removeItem(userId: string, itemId: string): Promise<void> {
    const wishlist = await this.getWishlist(userId)
    
    await payload.update({
      collection: 'wishlists',
      id: wishlist.id,
      data: {
        items: wishlist.items.filter(item => item.id !== itemId),
      },
    })
    
    analytics.track('Wishlist Item Removed', { userId, itemId })
  }
  
  async moveToCart(userId: string, itemId: string): Promise<void> {
    const wishlist = await this.getWishlist(userId)
    const item = wishlist.items.find(i => i.id === itemId)
    
    if (!item) {
      throw new Error('Item not found in wishlist')
    }
    
    // Add to cart
    await CartService.addItem(userId, item.product.id, 1)
    
    // Remove from wishlist
    await this.removeItem(userId, itemId)
    
    analytics.track('Wishlist Item Moved to Cart', { userId, itemId })
  }
  
  async generateShareToken(userId: string): Promise<string> {
    const wishlist = await this.getWishlist(userId)
    const token = crypto.randomBytes(16).toString('hex')
    
    await payload.update({
      collection: 'wishlists',
      id: wishlist.id,
      data: {
        isPublic: true,
        shareToken: token,
      },
    })
    
    return token
  }
}
```

---

## 💻 Frontend Implementation

### Wishlist Button Component

```typescript
// components/wishlist/WishlistButton.tsx
'use client'

import { useState } from 'react'
import { Heart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useWishlist } from '@/hooks/use-wishlist/hook.use-wishlist'
import { cn } from '@/lib/utils'

interface Props {
  productId: string
  variant?: 'icon' | 'button'
  className?: string
}

export const WishlistButton = ({ productId, variant = 'icon', className }: Props) => {
  const { isInWishlist, addItem, removeItem, isLoading } = useWishlist()
  const [isAnimating, setIsAnimating] = useState(false)
  
  const inWishlist = isInWishlist(productId)
  
  const handleClick = async () => {
    setIsAnimating(true)
    
    try {
      if (inWishlist) {
        await removeItem(productId)
      } else {
        await addItem(productId)
      }
    } finally {
      setTimeout(() => setIsAnimating(false), 300)
    }
  }
  
  if (variant === 'icon') {
    return (
      <Button
        variant="ghost"
        size="icon"
        onClick={handleClick}
        disabled={isLoading}
        className={cn(
          'transition-all',
          isAnimating && 'scale-125',
          className
        )}
        aria-label={inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
      >
        <Heart
          className={cn(
            'h-5 w-5 transition-colors',
            inWishlist && 'fill-primary text-primary'
          )}
        />
      </Button>
    )
  }
  
  return (
    <Button
      variant={inWishlist ? 'default' : 'outline'}
      onClick={handleClick}
      disabled={isLoading}
      className={className}
    >
      <Heart className={cn('mr-2 h-4 w-4', inWishlist && 'fill-current')} />
      {inWishlist ? 'In Wishlist' : 'Add to Wishlist'}
    </Button>
  )
}
```

### Wishlist Page

```typescript
// screens/Wishlist/WishlistScreen.tsx
'use client'

import { WishlistItem } from '@/components/wishlist/WishlistItem'
import { Button } from '@/components/ui/button'
import { useWishlist } from '@/hooks/use-wishlist/hook.use-wishlist'
import { Share2, ShoppingCart } from 'lucide-react'

export const WishlistScreen = () => {
  const { items, moveToCart, generateShareLink, isLoading } = useWishlist()
  
  const handleMoveAllToCart = async () => {
    await Promise.all(items.map(item => moveToCart(item.id)))
  }
  
  if (isLoading) {
    return <WishlistSkeleton />
  }
  
  if (items.length === 0) {
    return <EmptyWishlist />
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">My Wishlist ({items.length})</h1>
        
        <div className="flex gap-2">
          <Button variant="outline" onClick={generateShareLink}>
            <Share2 className="mr-2 h-4 w-4" />
            Share
          </Button>
          
          <Button onClick={handleMoveAllToCart}>
            <ShoppingCart className="mr-2 h-4 w-4" />
            Add All to Cart
          </Button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map(item => (
          <WishlistItem key={item.id} item={item} />
        ))}
      </div>
    </div>
  )
}
```

### Custom Hook

```typescript
// hooks/use-wishlist/hook.use-wishlist.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { WishlistService } from '@/services/wishlist/service.wishlist'
import { toast } from 'sonner'

export const useWishlist = () => {
  const queryClient = useQueryClient()
  
  const { data: wishlist, isLoading } = useQuery({
    queryKey: ['wishlist'],
    queryFn: () => WishlistService.getWishlist(),
  })
  
  const addMutation = useMutation({
    mutationFn: (productId: string) => WishlistService.addItem(productId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wishlist'] })
      toast.success('Added to wishlist')
    },
    onError: (error) => {
      toast.error(error.message || 'Failed to add to wishlist')
    },
  })
  
  const removeMutation = useMutation({
    mutationFn: (itemId: string) => WishlistService.removeItem(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wishlist'] })
      toast.success('Removed from wishlist')
    },
  })
  
  const moveToCartMutation = useMutation({
    mutationFn: (itemId: string) => WishlistService.moveToCart(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wishlist'] })
      queryClient.invalidateQueries({ queryKey: ['cart'] })
      toast.success('Moved to cart')
    },
  })
  
  return {
    items: wishlist?.items || [],
    isLoading,
    addItem: addMutation.mutate,
    removeItem: removeMutation.mutate,
    moveToCart: moveToCartMutation.mutate,
    isInWishlist: (productId: string) => 
      wishlist?.items.some(item => item.product.id === productId) || false,
    generateShareLink: async () => {
      const token = await WishlistService.generateShareToken()
      const url = `${window.location.origin}/wishlist/shared/${token}`
      await navigator.clipboard.writeText(url)
      toast.success('Share link copied to clipboard')
    },
  }
}
```

---

## 🔔 Price Drop Notifications

### Background Job

```typescript
// jobs/check-wishlist-price-drops.ts
import { payload } from 'payload'
import { sendEmail } from '@/lib/email'

export const checkWishlistPriceDrops = async () => {
  const wishlists = await payload.find({
    collection: 'wishlists',
    limit: 1000,
  })
  
  for (const wishlist of wishlists.docs) {
    for (const item of wishlist.items) {
      if (!item.notifyOnPriceDrop) continue
      
      const product = await payload.findByID({
        collection: 'products',
        id: item.product.id,
      })
      
      const priceDrop = item.priceWhenAdded - product.price
      const percentDrop = (priceDrop / item.priceWhenAdded) * 100
      
      // Notify if price dropped by 10% or more
      if (percentDrop >= 10) {
        await sendEmail({
          to: wishlist.user.email,
          template: 'price-drop-alert',
          data: {
            productName: product.name,
            productImage: product.image.url,
            oldPrice: item.priceWhenAdded,
            newPrice: product.price,
            savings: priceDrop,
            percentDrop: percentDrop.toFixed(0),
            productUrl: `${process.env.SITE_URL}/products/${product.slug}`,
          },
        })
        
        // Update price to avoid duplicate notifications
        await payload.update({
          collection: 'wishlists',
          id: wishlist.id,
          data: {
            items: wishlist.items.map(i => 
              i.id === item.id 
                ? { ...i, priceWhenAdded: product.price }
                : i
            ),
          },
        })
      }
    }
  }
}

// Schedule: Run daily at 9 AM
// Cron: 0 9 * * *
```

---

## 📊 Testing

### Unit Tests

```typescript
// services/wishlist/test.wishlist.test.ts
describe('WishlistService', () => {
  it('should add item to wishlist', async () => {
    const userId = 'user-123'
    const productId = 'product-456'
    
    const item = await WishlistService.addItem(userId, productId)
    
    expect(item.product).toBe(productId)
    expect(item.priceWhenAdded).toBeGreaterThan(0)
  })
  
  it('should not add duplicate items', async () => {
    const userId = 'user-123'
    const productId = 'product-456'
    
    await WishlistService.addItem(userId, productId)
    
    await expect(
      WishlistService.addItem(userId, productId)
    ).rejects.toThrow('Product already in wishlist')
  })
  
  it('should move item to cart', async () => {
    const userId = 'user-123'
    const item = await WishlistService.addItem(userId, 'product-456')
    
    await WishlistService.moveToCart(userId, item.id)
    
    const wishlist = await WishlistService.getWishlist(userId)
    const cart = await CartService.getCart(userId)
    
    expect(wishlist.items).not.toContainEqual(item)
    expect(cart.items).toContainEqual(
      expect.objectContaining({ product: 'product-456' })
    )
  })
})
```

### E2E Tests

```typescript
// e2e/wishlist.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Wishlist', () => {
  test('should add product to wishlist', async ({ page }) => {
    await page.goto('/products/rose-bouquet')
    
    await page.click('[aria-label="Add to wishlist"]')
    
    await expect(page.locator('text=Added to wishlist')).toBeVisible()
    await expect(page.locator('[aria-label="Remove from wishlist"]')).toBeVisible()
  })
  
  test('should view wishlist page', async ({ page }) => {
    await page.goto('/wishlist')
    
    await expect(page.locator('h1:has-text("My Wishlist")')).toBeVisible()
    await expect(page.locator('.wishlist-item')).toHaveCount(3)
  })
  
  test('should move item to cart', async ({ page }) => {
    await page.goto('/wishlist')
    
    await page.click('.wishlist-item:first-child button:has-text("Add to Cart")')
    
    await expect(page.locator('text=Moved to cart')).toBeVisible()
    await page.goto('/cart')
    await expect(page.locator('.cart-item')).toHaveCount(1)
  })
})
```

---

## 🚀 Deployment

### Rollout Plan

**Phase 1: Beta (Week 1)**
- Deploy to 10% of users
- Monitor performance and errors
- Collect user feedback

**Phase 2: Gradual Rollout (Week 2)**
- 25% → 50% → 75% → 100%
- Monitor metrics at each stage

**Phase 3: Full Launch (Week 3)**
- 100% rollout
- Marketing campaign
- Email announcement

### Migration

```typescript
// migrations/create-wishlists.ts
export const createWishlists = async () => {
  const users = await payload.find({
    collection: 'users',
    limit: 10000,
  })
  
  for (const user of users.docs) {
    await payload.create({
      collection: 'wishlists',
      data: {
        user: user.id,
        items: [],
        isPublic: false,
      },
    })
  }
}
```

---

## 📈 Results (4 weeks post-launch)

### Adoption Metrics

| Metric | Value |
|--------|-------|
| **Users with wishlists** | 12,450 (45% of active users) |
| **Avg items per wishlist** | 6.8 |
| **Total wishlist items** | 84,660 |
| **Wishlist → Cart conversion** | 28% |
| **Shared wishlists** | 1,240 |

### Business Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Return visit rate** | 32% | 48% | +50% |
| **Avg session duration** | 3.2min | 4.9min | +53% |
| **Conversion rate** | 2.8% | 3.4% | +21% |
| **Revenue per user** | $45 | $58 | +29% |

### User Feedback

- **Satisfaction**: 4.6/5 stars (890 reviews)
- **Most requested**: Mobile app support (coming Q3)
- **Top use case**: Gift registries (35% of shared wishlists)

---

## 🔗 References

- **Feature Request**: #FEAT-2026-04-05-023
- **PRs**: #1301, #1305, #1312
- **Design**: [Figma](https://figma.com/wishlist-design)
- **Analytics**: [Dashboard](https://analytics.siinstore.com/wishlist)

---

## 👥 Team

- **Product Manager**: Carol Lee
- **Backend**: John Doe
- **Frontend**: Alice Johnson
- **Designer**: Emma Wilson
- **QA**: Bob Chen

---

**Feature Type**: User Engagement  
**Development Time**: 3 weeks  
**Impact**: High (+21% conversion rate)
