# Project Overview

> **SiinStore Admin Management System** - Project Overview
> **Last Updated**: 2026-03-11

---

## Project Summary

Full-stack e-commerce admin management system:
- **Frontend**: Next.js 15 + React 19 + TypeScript
- **Backend**: Payload CMS 3.49.1 + MongoDB
- **Theme**: "Pink Petals" - soft, elegant, flower-inspired

---

## Technology Stack

### Core
| Technology | Version |
|------------|---------|
| Next.js | 15.4.4 |
| React | 19.1.0 |
| TypeScript | 5.7.3 |
| PayloadCMS | 3.49.1 |
| TailwindCSS | 4.1.12 |

### UI & Styling
- **Components**: Radix UI (headless)
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod
- **Notifications**: Sonner

### State & Data
- **State**: Redux Toolkit
- **HTTP**: Axios (ApiService)
- **Real-time**: Socket.io

### Development
- **Package Manager**: pnpm 10.12.4
- **Testing**: Vitest + Playwright

---

## Folder Structure

### Nested (Level 1-2) + Flat (Level 3+)

```
src/
├── app/                 # Next.js App Router
├── collections/         # PayloadCMS collections
├── components/         # Design system
│   └── ui/
├── configs/             # App configuration
├── lib/                # Utilities
├── screens/            # Admin screens
├── store/              # Redux store
├── services/           # Business logic
│   ├── order/          # Level 2
│   │   └── service.*.ts    # Level 3 - FLAT
│   └── user/
│       └── service.*.ts    # Level 3 - FLAT
├── hooks/              # Custom hooks
│   ├── use-user/       # Level 2
│   │   └── hook.*.ts       # Level 3 - FLAT
│   └── use-cart/
│       └── hook.*.ts       # Level 3 - FLAT
├── utils/              # Helper functions
│   ├── format/         # Level 2
│   │   └── util.*.ts      # Level 3 - FLAT
│   └── validation/
│       └── util.*.ts       # Level 3 - FLAT
└── types/              # TypeScript definitions
    ├── dto/            # Level 2
    │   └── type.*.ts       # Level 3 - FLAT
    └── entity/
        └── type.*.ts       # Level 3 - FLAT
```

> **Quy tắc**: Level 1-2 = folders, Level 3+ = flat files (KHÔNG subfolders)

---

## Domain-Driven Collections

```
collections/
├── auth/          # Customer, Users
├── commerce/      # Product, Category
├── orders/        # Order, PaymentSession
├── stores/        # Store, StoreWallets
├── marketing/     # Voucher, Campaign
└── system/        # Media, Configs
```

---

## Related Rules

- [core.naming-conventions.md](./core.naming-conventions.md)
- [core.coding-checklist.md](./core.coding-checklist.md)
- [api.patterns.md](./api.patterns.md)
