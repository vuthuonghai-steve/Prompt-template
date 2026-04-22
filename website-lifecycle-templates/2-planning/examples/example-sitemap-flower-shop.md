# Sitemap - SiinStore Flower Shop

> **Project**: SiinStore E-commerce Website
> **Date**: 2026-04-22
> **Total Pages**: 35+

---

## 1. Site Structure Overview

```
SiinStore
├── Public Pages (No Auth Required)
│   ├── Homepage
│   ├── Product Catalog
│   ├── Product Detail
│   ├── Cart
│   ├── Checkout
│   ├── About Us
│   ├── Contact
│   └── Legal
│
├── Customer Pages (Auth Required)
│   ├── Account Dashboard
│   ├── Order History
│   ├── Wishlist
│   └── Settings
│
└── Admin Pages (Admin Role)
    ├── Dashboard
    ├── Products
    ├── Orders
    ├── Customers
    └── Settings
```

---

## 2. Detailed Sitemap

### 2.1 Public Pages

#### Homepage `/`
```yaml
Purpose: Landing page, showcase featured products
Components:
  - Hero banner (seasonal promotions)
  - Featured products carousel
  - Category cards (Sinh nhật, Cưới hỏi, Khai trương)
  - Testimonials
  - Instagram feed
  - Newsletter signup

SEO:
  Title: "SiinStore - Hoa Tươi Cao Cấp Giao Nhanh TP.HCM"
  Description: "Đặt hoa online giao trong 2h. 200+ mẫu hoa tươi đẹp cho mọi dịp."
  Keywords: "hoa tươi, đặt hoa online, giao hoa nhanh, hoa sinh nhật"
```

#### Product Catalog `/products`
```yaml
Purpose: Browse all products with filters
URL Patterns:
  - /products (all)
  - /products?category=sinh-nhat
  - /products?occasion=wedding
  - /products?price=500000-1000000
  - /products?color=pink

Components:
  - Filter sidebar (Category, Price, Color, Occasion)
  - Sort dropdown (Price, Popularity, Newest)
  - Product grid (24 items/page)
  - Pagination
  - Breadcrumbs

SEO:
  Title: "Hoa Tươi - {Category} | SiinStore"
  Canonical: /products
```

#### Product Detail `/products/[slug]`
```yaml
Purpose: Show product details, add to cart
URL Example: /products/bo-hong-phan-pastel

Components:
  - Image gallery (6-8 images, zoom, 360° view)
  - Product info (Name, Price, SKU, Stock)
  - Description (Rich text)
  - Specifications (Size, Flower types, Care instructions)
  - Quantity selector
  - Add to cart button
  - Related products
  - Reviews & ratings

SEO:
  Title: "{Product Name} - Giá {Price} | SiinStore"
  Description: "{Product Description}"
  Schema: Product (JSON-LD)
```

#### Shopping Cart `/cart`
```yaml
Purpose: Review cart items before checkout
Components:
  - Cart items list (Image, Name, Price, Quantity, Remove)
  - Quantity updater
  - Subtotal calculation
  - Voucher input
  - "Continue Shopping" button
  - "Proceed to Checkout" button

Persistence:
  - localStorage (guest)
  - Database (logged-in users)
```

#### Checkout `/checkout`
```yaml
Purpose: Complete purchase
URL Flow:
  - /checkout/info (Customer info)
  - /checkout/delivery (Date/Time picker)
  - /checkout/payment (Payment method)
  - /checkout/review (Order summary)

Components:
  - Multi-step form (4 steps)
  - Progress indicator
  - Guest checkout option
  - Saved addresses (logged-in)
  - Gift message input
  - Payment method selection
  - Order summary sidebar

Security:
  - HTTPS only
  - CSRF protection
  - Rate limiting
```

#### Order Confirmation `/orders/[orderId]/confirmation`
```yaml
Purpose: Show order success message
URL Example: /orders/ORD-20260423-001234/confirmation

Components:
  - Success message
  - Order details
  - Estimated delivery time
  - Tracking link
  - "Continue Shopping" button
  - Print receipt button
```

#### Order Tracking `/orders/[orderId]/track`
```yaml
Purpose: Track order status
URL Example: /orders/ORD-20260423-001234/track

Components:
  - Order status timeline
  - Delivery person info (when delivering)
  - Estimated arrival time
  - Contact support button

Public Access:
  - Require: Order ID + Phone number (last 4 digits)
```

#### About Us `/about`
```yaml
Purpose: Company story, mission, values
Components:
  - Hero section
  - Our story
  - Team members
  - Values & mission
  - Certifications
  - Press mentions
```

#### Contact `/contact`
```yaml
Purpose: Contact form, store locations
Components:
  - Contact form (Name, Email, Phone, Message)
  - Store locations (Google Maps)
  - Business hours
  - Social media links
  - FAQ section
```

#### Blog `/blog`
```yaml
Purpose: Content marketing, SEO
URL Patterns:
  - /blog (list)
  - /blog/[slug] (detail)
  - /blog/category/[category]

Components:
  - Blog post list
  - Featured posts
  - Categories sidebar
  - Search
  - Related posts

SEO:
  - Rich snippets (Article schema)
  - Open Graph tags
```

#### Legal Pages
```yaml
Pages:
  - /terms-of-service
  - /privacy-policy
  - /return-policy
  - /shipping-policy

Components:
  - Rich text content
  - Last updated date
  - Table of contents
```

---

### 2.2 Customer Pages (Auth Required)

#### Account Dashboard `/account`
```yaml
Purpose: Customer account overview
Components:
  - Welcome message
  - Recent orders (last 5)
  - Loyalty points balance
  - Quick actions (Reorder, Track, Wishlist)
  - Account settings link
```

#### Order History `/account/orders`
```yaml
Purpose: View all past orders
URL Patterns:
  - /account/orders (list)
  - /account/orders/[orderId] (detail)

Components:
  - Orders table (Date, Order ID, Total, Status)
  - Filter (Status, Date range)
  - Search by Order ID
  - Pagination
  - "Reorder" button
  - "Track" button
  - "Download Invoice" button
```

#### Wishlist `/account/wishlist`
```yaml
Purpose: Save products for later
Components:
  - Wishlist items grid
  - "Add to Cart" button
  - "Remove" button
  - Share wishlist link
```

#### Saved Addresses `/account/addresses`
```yaml
Purpose: Manage delivery addresses
Components:
  - Addresses list
  - "Add New Address" button
  - "Edit" button
  - "Delete" button
  - "Set as Default" button
```

#### Account Settings `/account/settings`
```yaml
Purpose: Update profile, password, preferences
Tabs:
  - Profile (Name, Email, Phone, Avatar)
  - Password (Change password)
  - Notifications (Email, SMS preferences)
  - Privacy (Data export, Delete account)
```

---

### 2.3 Admin Pages (Admin Role)

#### Admin Dashboard `/admin`
```yaml
Purpose: Overview of store metrics
Components:
  - Revenue chart (daily, weekly, monthly)
  - Orders summary (Pending, Processing, Delivered)
  - Top products
  - Recent orders
  - Low stock alerts
  - Customer stats
```

#### Products Management `/admin/products`
```yaml
Purpose: CRUD products
URL Patterns:
  - /admin/products (list)
  - /admin/products/create (create)
  - /admin/products/[id]/edit (edit)

Components:
  - Products table (Image, Name, Price, Stock, Status)
  - Search & filters
  - Bulk actions (Delete, Update status)
  - "Add Product" button
  - Export CSV
```

#### Orders Management `/admin/orders`
```yaml
Purpose: Manage orders
URL Patterns:
  - /admin/orders (list)
  - /admin/orders/[id] (detail)

Components:
  - Orders table (Order ID, Customer, Total, Status, Date)
  - Filter (Status, Date range, Payment method)
  - Search by Order ID / Customer
  - Status update dropdown
  - Print invoice
  - Assign delivery person
```

#### Customers Management `/admin/customers`
```yaml
Purpose: View customer data
Components:
  - Customers table (Name, Email, Orders, Total Spent)
  - Search
  - Customer detail view
  - Order history per customer
  - Export CSV
```

#### Vouchers Management `/admin/vouchers`
```yaml
Purpose: Create/manage discount codes
Components:
  - Vouchers table (Code, Discount, Valid Until, Usage)
  - "Create Voucher" button
  - Edit/Delete actions
  - Usage analytics
```

#### Settings `/admin/settings`
```yaml
Purpose: Store configuration
Tabs:
  - General (Store name, Logo, Contact)
  - Shipping (Zones, Rates, Partners)
  - Payment (Gateway credentials)
  - Email (Templates, SMTP settings)
  - SEO (Meta tags, Analytics)
```

---

## 3. URL Structure & Naming Conventions

### 3.1 URL Patterns

```yaml
Products:
  - /products (list)
  - /products/[slug] (detail)
  - /products?category=sinh-nhat (filter)

Categories:
  - /categories/[slug] (category page)

Collections:
  - /collections/[slug] (curated collections)

Pages:
  - /about
  - /contact
  - /blog
  - /blog/[slug]

Account:
  - /account (dashboard)
  - /account/orders
  - /account/wishlist
  - /account/settings

Checkout:
  - /cart
  - /checkout
  - /checkout/info
  - /checkout/delivery
  - /checkout/payment
  - /checkout/review

Admin:
  - /admin (dashboard)
  - /admin/products
  - /admin/orders
  - /admin/customers
```

### 3.2 Slug Format

```yaml
Products: kebab-case
  Example: bo-hong-phan-pastel

Categories: kebab-case
  Example: hoa-sinh-nhat

Blog: kebab-case + date
  Example: cach-cham-soc-hoa-tuoi-2026-04-22
```

---

## 4. Navigation Structure

### 4.1 Main Navigation (Header)

```yaml
Desktop:
  - Logo (left)
  - Menu:
    - Sản phẩm (dropdown)
      - Hoa Sinh Nhật
      - Hoa Cưới Hỏi
      - Hoa Khai Trương
      - Hoa Chia Buồn
      - Hoa Tình Yêu
    - Dịp đặc biệt (dropdown)
      - Tết
      - Valentine
      - 8/3
      - 20/10
      - Giáng Sinh
    - Blog
    - Về chúng tôi
    - Liên hệ
  - Search bar (center)
  - Icons (right):
    - Account
    - Wishlist (badge)
    - Cart (badge)

Mobile:
  - Hamburger menu (left)
  - Logo (center)
  - Cart icon (right)
```

### 4.2 Footer Navigation

```yaml
Columns:
  - Về SiinStore:
    - Giới thiệu
    - Tuyển dụng
    - Liên hệ
  
  - Chính sách:
    - Chính sách đổi trả
    - Chính sách giao hàng
    - Chính sách bảo mật
    - Điều khoản sử dụng
  
  - Hỗ trợ:
    - Hướng dẫn đặt hàng
    - Câu hỏi thường gặp
    - Chăm sóc hoa
    - Liên hệ hỗ trợ
  
  - Kết nối:
    - Facebook
    - Instagram
    - Zalo
    - Email

Bottom:
  - Copyright © 2026 SiinStore
  - Payment methods icons
  - Certifications
```

---

## 5. Breadcrumbs

```yaml
Homepage:
  - Trang chủ

Product Catalog:
  - Trang chủ > Sản phẩm

Product Detail:
  - Trang chủ > Sản phẩm > {Category} > {Product Name}

Cart:
  - Trang chủ > Giỏ hàng

Checkout:
  - Trang chủ > Giỏ hàng > Thanh toán

Account:
  - Trang chủ > Tài khoản > {Page}

Admin:
  - Admin > {Section} > {Page}
```

---

## 6. Redirects & Error Pages

### 6.1 Redirects

```yaml
Old URL → New URL:
  - /shop → /products
  - /product/[id] → /products/[slug]
  - /my-account → /account
```

### 6.2 Error Pages

```yaml
404 Not Found:
  - Custom design
  - Search bar
  - Popular products
  - "Back to Home" button

500 Server Error:
  - Error message
  - "Try again" button
  - Contact support link

403 Forbidden:
  - "Access Denied" message
  - "Login" button (if not authenticated)
```

---

## 7. SEO & Meta Tags

### 7.1 Homepage

```html
<title>SiinStore - Hoa Tươi Cao Cấp Giao Nhanh TP.HCM</title>
<meta name="description" content="Đặt hoa online giao trong 2h. 200+ mẫu hoa tươi đẹp cho mọi dịp. Miễn phí giao hàng nội thành TP.HCM." />
<meta name="keywords" content="hoa tươi, đặt hoa online, giao hoa nhanh, hoa sinh nhật, hoa cưới" />
<link rel="canonical" href="https://siinstore.com" />
```

### 7.2 Product Page

```html
<title>{Product Name} - Giá {Price} | SiinStore</title>
<meta name="description" content="{Product Description}" />
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{Product Name}",
  "image": "{Product Image}",
  "description": "{Product Description}",
  "sku": "{SKU}",
  "offers": {
    "@type": "Offer",
    "price": "{Price}",
    "priceCurrency": "VND",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

---

## 8. Related Documents

- **Requirements**: `1-discovery/examples/example-requirements-flower-shop.md`
- **Tech Stack**: [example-tech-stack-ecommerce.md](./example-tech-stack-ecommerce.md)
- **Architecture**: [example-architecture-microservices.md](./example-architecture-microservices.md)
- **Design System**: `3-design/examples/example-design-system-siinstore.md`
