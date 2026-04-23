# Pattern: Responsive Design Mobile-First

## Nguồn
- Claude Code
- Cursor
- Windsurf

## Mô tả
Design and develop for mobile screens first, then progressively enhance for larger screens. Start with constraints, add features as space allows.

## Khi nào dùng
- All modern web development
- E-commerce websites
- Content-heavy sites
- Progressive web apps
- Mobile-first products

## Cách áp dụng

### 1. Mobile-First Breakpoints

```css
/* Base styles: Mobile (320px+) */
.container {
  padding: 1rem;
  font-size: 14px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 16px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Large Desktop (1440px+) */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
}
```

### 2. Tailwind CSS Mobile-First

```tsx
// Base: Mobile
// md: Tablet (768px+)
// lg: Desktop (1024px+)
// xl: Large Desktop (1280px+)

<div className="
  p-4           /* Mobile: 1rem padding */
  md:p-6        /* Tablet: 1.5rem padding */
  lg:p-8        /* Desktop: 2rem padding */
  
  grid
  grid-cols-1   /* Mobile: 1 column */
  md:grid-cols-2 /* Tablet: 2 columns */
  lg:grid-cols-3 /* Desktop: 3 columns */
  
  gap-4         /* Mobile: 1rem gap */
  md:gap-6      /* Tablet: 1.5rem gap */
  lg:gap-8      /* Desktop: 2rem gap */
">
  {products.map(product => (
    <ProductCard key={product.id} product={product} />
  ))}
</div>
```

### 3. Component Adaptation

```tsx
// Mobile-first component structure
export function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="
      /* Mobile: Stack vertically */
      flex flex-col
      
      /* Tablet: Horizontal layout */
      md:flex-row md:items-center
      
      /* Desktop: Card layout */
      lg:flex-col
      
      bg-white rounded-lg shadow-sm
      p-4 md:p-6
    ">
      {/* Image */}
      <img 
        src={product.image}
        alt={product.name}
        className="
          w-full h-48        /* Mobile: Full width */
          md:w-32 md:h-32    /* Tablet: Fixed size */
          lg:w-full lg:h-64  /* Desktop: Full width again */
          object-cover rounded
        "
      />
      
      {/* Content */}
      <div className="
        mt-4 md:mt-0 md:ml-4 lg:mt-4 lg:ml-0
      ">
        <h3 className="
          text-lg md:text-xl lg:text-2xl
          font-semibold
        ">
          {product.name}
        </h3>
        
        <p className="
          text-sm md:text-base
          text-gray-600 mt-2
          line-clamp-2 md:line-clamp-3
        ">
          {product.description}
        </p>
        
        <div className="
          flex items-center justify-between
          mt-4
        ">
          <span className="
            text-xl md:text-2xl
            font-bold text-primary
          ">
            {formatCurrency(product.price)}
          </span>
          
          <Button 
            size="sm"
            className="md:size-default"
          >
            Add to Cart
          </Button>
        </div>
      </div>
    </div>
  )
}
```

## Ví dụ thực tế

### E-commerce: Product Grid

```tsx
// src/screens/Products/ProductGrid.tsx

export function ProductGrid({ products }: ProductGridProps) {
  return (
    <div className="container mx-auto px-4 py-6">
      {/* Header */}
      <div className="
        flex flex-col gap-4
        md:flex-row md:items-center md:justify-between
        mb-6
      ">
        <h1 className="
          text-2xl md:text-3xl lg:text-4xl
          font-bold
        ">
          Products
        </h1>
        
        {/* Filters - Mobile: Drawer, Desktop: Inline */}
        <div className="
          flex items-center gap-2
        ">
          {/* Mobile: Filter button */}
          <Button 
            variant="outline"
            className="md:hidden"
            onClick={() => setShowFilters(true)}
          >
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </Button>
          
          {/* Desktop: Inline filters */}
          <div className="
            hidden md:flex
            items-center gap-4
          ">
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="roses">Roses</SelectItem>
                <SelectItem value="tulips">Tulips</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="newest">Newest</SelectItem>
                <SelectItem value="price-asc">Price: Low to High</SelectItem>
                <SelectItem value="price-desc">Price: High to Low</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
      
      {/* Product Grid */}
      <div className="
        grid
        grid-cols-1        /* Mobile: 1 column */
        sm:grid-cols-2     /* Small: 2 columns */
        lg:grid-cols-3     /* Desktop: 3 columns */
        xl:grid-cols-4     /* Large: 4 columns */
        gap-4 md:gap-6
      ">
        {products.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
      
      {/* Mobile Filter Drawer */}
      <Sheet open={showFilters} onOpenChange={setShowFilters}>
        <SheetContent side="bottom" className="h-[80vh]">
          <SheetHeader>
            <SheetTitle>Filters</SheetTitle>
          </SheetHeader>
          <div className="py-4 space-y-4">
            {/* Filter options */}
          </div>
        </SheetContent>
      </Sheet>
    </div>
  )
}
```

### E-commerce: Checkout Form

```tsx
// src/screens/Checkout/CheckoutForm.tsx

export function CheckoutForm() {
  return (
    <form className="
      max-w-4xl mx-auto
      px-4 py-6
    ">
      <div className="
        grid
        grid-cols-1      /* Mobile: Single column */
        lg:grid-cols-2   /* Desktop: Two columns */
        gap-6 lg:gap-8
      ">
        {/* Left Column: Shipping Info */}
        <div className="space-y-6">
          <h2 className="
            text-xl md:text-2xl
            font-bold
          ">
            Shipping Information
          </h2>
          
          {/* Full Name */}
          <div>
            <Label htmlFor="name">Full Name</Label>
            <Input
              id="name"
              className="
                h-12 md:h-14    /* Larger touch targets on mobile */
                text-base md:text-lg
              "
              placeholder="John Doe"
            />
          </div>
          
          {/* Phone & Email - Stack on mobile, side-by-side on desktop */}
          <div className="
            grid
            grid-cols-1
            md:grid-cols-2
            gap-4
          ">
            <div>
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                type="tel"
                className="h-12 md:h-14"
                placeholder="0901234567"
              />
            </div>
            
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                className="h-12 md:h-14"
                placeholder="john@example.com"
              />
            </div>
          </div>
          
          {/* Address */}
          <div>
            <Label htmlFor="address">Address</Label>
            <Textarea
              id="address"
              className="
                min-h-24 md:min-h-32
                text-base md:text-lg
              "
              placeholder="123 Main St, District 1"
            />
          </div>
          
          {/* Payment Method - Radio buttons with larger touch targets */}
          <div>
            <Label>Payment Method</Label>
            <RadioGroup defaultValue="vnpay" className="mt-2 space-y-3">
              <div className="
                flex items-center
                p-4 rounded-lg border
                cursor-pointer
                hover:bg-gray-50
              ">
                <RadioGroupItem value="vnpay" id="vnpay" />
                <Label 
                  htmlFor="vnpay"
                  className="
                    ml-3 flex-1
                    cursor-pointer
                    text-base md:text-lg
                  "
                >
                  VNPay
                </Label>
              </div>
              
              <div className="
                flex items-center
                p-4 rounded-lg border
                cursor-pointer
                hover:bg-gray-50
              ">
                <RadioGroupItem value="cod" id="cod" />
                <Label 
                  htmlFor="cod"
                  className="
                    ml-3 flex-1
                    cursor-pointer
                    text-base md:text-lg
                  "
                >
                  Cash on Delivery
                </Label>
              </div>
            </RadioGroup>
          </div>
        </div>
        
        {/* Right Column: Order Summary */}
        <div className="
          /* Mobile: Below form */
          order-first lg:order-last
          
          /* Desktop: Sticky sidebar */
          lg:sticky lg:top-4 lg:h-fit
        ">
          <div className="
            bg-gray-50 rounded-lg
            p-4 md:p-6
          ">
            <h2 className="
              text-xl md:text-2xl
              font-bold mb-4
            ">
              Order Summary
            </h2>
            
            {/* Cart Items */}
            <div className="space-y-3 mb-4">
              {cart.items.map(item => (
                <div key={item.id} className="
                  flex items-center gap-3
                ">
                  <img 
                    src={item.image}
                    alt={item.name}
                    className="
                      w-16 h-16 md:w-20 md:h-20
                      object-cover rounded
                    "
                  />
                  <div className="flex-1 min-w-0">
                    <p className="
                      font-medium truncate
                      text-sm md:text-base
                    ">
                      {item.name}
                    </p>
                    <p className="
                      text-sm text-gray-600
                    ">
                      Qty: {item.quantity}
                    </p>
                  </div>
                  <p className="
                    font-semibold
                    text-sm md:text-base
                  ">
                    {formatCurrency(item.price * item.quantity)}
                  </p>
                </div>
              ))}
            </div>
            
            {/* Totals */}
            <div className="
              border-t pt-4 space-y-2
              text-sm md:text-base
            ">
              <div className="flex justify-between">
                <span>Subtotal</span>
                <span>{formatCurrency(subtotal)}</span>
              </div>
              <div className="flex justify-between">
                <span>Shipping</span>
                <span>{formatCurrency(shipping)}</span>
              </div>
              <div className="
                flex justify-between
                text-lg md:text-xl
                font-bold
                border-t pt-2
              ">
                <span>Total</span>
                <span className="text-primary">
                  {formatCurrency(total)}
                </span>
              </div>
            </div>
            
            {/* Submit Button - Full width on mobile */}
            <Button 
              type="submit"
              size="lg"
              className="
                w-full mt-6
                h-12 md:h-14
                text-base md:text-lg
              "
            >
              Place Order
            </Button>
          </div>
        </div>
      </div>
    </form>
  )
}
```

### E-commerce: Navigation

```tsx
// src/components/Navigation/Navigation.tsx

export function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  return (
    <nav className="
      bg-white border-b
      sticky top-0 z-50
    ">
      <div className="
        container mx-auto
        px-4 py-3 md:py-4
      ">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="
            text-xl md:text-2xl
            font-bold text-primary
          ">
            FlowerShop
          </Link>
          
          {/* Desktop Navigation */}
          <div className="
            hidden md:flex
            items-center gap-6
          ">
            <Link href="/products" className="hover:text-primary">
              Products
            </Link>
            <Link href="/about" className="hover:text-primary">
              About
            </Link>
            <Link href="/contact" className="hover:text-primary">
              Contact
            </Link>
          </div>
          
          {/* Actions */}
          <div className="flex items-center gap-2 md:gap-4">
            {/* Search - Hidden on mobile, shown on tablet+ */}
            <Button
              variant="ghost"
              size="icon"
              className="hidden sm:flex"
            >
              <Search className="w-5 h-5" />
            </Button>
            
            {/* Cart */}
            <Button
              variant="ghost"
              size="icon"
              className="relative"
            >
              <ShoppingCart className="w-5 h-5" />
              {cartCount > 0 && (
                <span className="
                  absolute -top-1 -right-1
                  bg-primary text-white
                  text-xs font-bold
                  w-5 h-5 rounded-full
                  flex items-center justify-center
                ">
                  {cartCount}
                </span>
              )}
            </Button>
            
            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(true)}
            >
              <Menu className="w-6 h-6" />
            </Button>
          </div>
        </div>
      </div>
      
      {/* Mobile Menu Drawer */}
      <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
        <SheetContent side="right" className="w-[80vw] sm:w-[350px]">
          <SheetHeader>
            <SheetTitle>Menu</SheetTitle>
          </SheetHeader>
          <nav className="flex flex-col gap-4 mt-6">
            <Link 
              href="/products"
              className="
                text-lg py-3 px-4
                hover:bg-gray-100 rounded
              "
              onClick={() => setMobileMenuOpen(false)}
            >
              Products
            </Link>
            <Link 
              href="/about"
              className="
                text-lg py-3 px-4
                hover:bg-gray-100 rounded
              "
              onClick={() => setMobileMenuOpen(false)}
            >
              About
            </Link>
            <Link 
              href="/contact"
              className="
                text-lg py-3 px-4
                hover:bg-gray-100 rounded
              "
              onClick={() => setMobileMenuOpen(false)}
            >
              Contact
            </Link>
          </nav>
        </SheetContent>
      </Sheet>
    </nav>
  )
}
```

## Touch Target Guidelines

```tsx
// Minimum touch target: 44x44px (iOS) / 48x48px (Android)

// ❌ WRONG: Too small for mobile
<button className="w-8 h-8">
  <X className="w-4 h-4" />
</button>

// ✅ CORRECT: Adequate touch target
<button className="
  w-12 h-12        /* 48px minimum */
  flex items-center justify-center
">
  <X className="w-5 h-5" />
</button>

// ✅ CORRECT: Responsive touch targets
<button className="
  w-10 h-10       /* Mobile: 40px */
  md:w-12 md:h-12 /* Desktop: 48px */
  flex items-center justify-center
">
  <X className="w-5 h-5" />
</button>
```

## Typography Scale

```css
/* Mobile-first typography */
.heading-1 {
  font-size: 1.75rem;  /* 28px mobile */
  line-height: 1.2;
}

@media (min-width: 768px) {
  .heading-1 {
    font-size: 2.25rem;  /* 36px tablet */
  }
}

@media (min-width: 1024px) {
  .heading-1 {
    font-size: 3rem;  /* 48px desktop */
  }
}
```

## Best Practices

### Do's
✅ Start with mobile layout
✅ Use min-width media queries
✅ Test on real devices
✅ Optimize images for mobile
✅ Use touch-friendly targets (44px+)
✅ Progressive enhancement

### Don'ts
❌ Design desktop-first
❌ Use max-width media queries
❌ Test only in browser DevTools
❌ Serve desktop images to mobile
❌ Use small touch targets
❌ Hide content on mobile

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Better mobile UX | More planning needed |
| Faster mobile load | Desktop may feel constrained |
| Forces prioritization | More CSS to write |
| Future-proof | Team mindset shift |

## Related Patterns
- [Performance Baseline](../../7-maintenance/templates/performance-baseline.md)
- [Browser Automation Testing](../../6-testing/patterns/pattern-browser-automation-testing.md)
