# Example: React Component with Hooks

> **Context**: E-commerce flower shop
> **Component**: Shopping cart with state management
> **Stack**: React 19, TypeScript, Context API

---

## 📁 File Structure

```
src/
├── components/
│   └── cart/
│       ├── Cart.tsx                    # Main cart component
│       ├── CartItem.tsx                # Cart item component
│       └── CartSummary.tsx             # Order summary
├── contexts/
│   └── CartContext.tsx                 # Cart context & provider
├── hooks/
│   └── use-cart/
│       └── hook.use-cart.ts            # Cart hook
└── types/
    └── type.cart.ts                    # TypeScript types
```

---

## 💻 Implementation

### 1. TypeScript Types

```typescript
// types/type.cart.ts

export interface CartItem {
  id: string
  productId: string
  name: string
  price: number
  quantity: number
  image: string
  maxQuantity: number
}

export interface Cart {
  items: CartItem[]
  subtotal: number
  shipping: number
  discount: number
  total: number
}

export interface CartContextValue {
  cart: Cart
  addItem: (item: Omit<CartItem, 'quantity'>) => void
  removeItem: (itemId: string) => void
  updateQuantity: (itemId: string, quantity: number) => void
  clearCart: () => void
  applyVoucher: (code: string) => Promise<void>
  isLoading: boolean
}
```

### 2. Cart Context

```typescript
// contexts/CartContext.tsx
import { createContext, useContext, useReducer, useEffect } from 'react'
import type { Cart, CartItem, CartContextValue } from '@/types/type.cart'

// Initial state
const initialCart: Cart = {
  items: [],
  subtotal: 0,
  shipping: 0,
  discount: 0,
  total: 0,
}

// Action types
type CartAction =
  | { type: 'ADD_ITEM'; payload: Omit<CartItem, 'quantity'> }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' }
  | { type: 'APPLY_DISCOUNT'; payload: number }
  | { type: 'LOAD_CART'; payload: Cart }

// Reducer
function cartReducer(state: Cart, action: CartAction): Cart {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingItem = state.items.find(
        (item) => item.productId === action.payload.productId
      )
      
      let newItems: CartItem[]
      
      if (existingItem) {
        // Increment quantity
        newItems = state.items.map((item) =>
          item.productId === action.payload.productId
            ? { ...item, quantity: Math.min(item.quantity + 1, item.maxQuantity) }
            : item
        )
      } else {
        // Add new item
        newItems = [
          ...state.items,
          { ...action.payload, quantity: 1 },
        ]
      }
      
      return calculateTotals({ ...state, items: newItems })
    }
    
    case 'REMOVE_ITEM': {
      const newItems = state.items.filter((item) => item.id !== action.payload)
      return calculateTotals({ ...state, items: newItems })
    }
    
    case 'UPDATE_QUANTITY': {
      const newItems = state.items.map((item) =>
        item.id === action.payload.id
          ? { ...item, quantity: Math.min(action.payload.quantity, item.maxQuantity) }
          : item
      )
      return calculateTotals({ ...state, items: newItems })
    }
    
    case 'CLEAR_CART': {
      return initialCart
    }
    
    case 'APPLY_DISCOUNT': {
      return calculateTotals({ ...state, discount: action.payload })
    }
    
    case 'LOAD_CART': {
      return action.payload
    }
    
    default:
      return state
  }
}

// Calculate totals
function calculateTotals(cart: Cart): Cart {
  const subtotal = cart.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  )
  
  // Free shipping over 500,000 VND
  const shipping = subtotal >= 500000 ? 0 : 30000
  
  const total = subtotal + shipping - cart.discount
  
  return {
    ...cart,
    subtotal,
    shipping,
    total,
  }
}

// Context
const CartContext = createContext<CartContextValue | undefined>(undefined)

// Provider
export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cart, dispatch] = useReducer(cartReducer, initialCart)
  const [isLoading, setIsLoading] = useState(false)
  
  // Load cart from localStorage on mount
  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      try {
        const parsedCart = JSON.parse(savedCart)
        dispatch({ type: 'LOAD_CART', payload: parsedCart })
      } catch (error) {
        console.error('Failed to load cart:', error)
      }
    }
  }, [])
  
  // Save cart to localStorage on change
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart))
  }, [cart])
  
  // Actions
  const addItem = useCallback((item: Omit<CartItem, 'quantity'>) => {
    dispatch({ type: 'ADD_ITEM', payload: item })
  }, [])
  
  const removeItem = useCallback((itemId: string) => {
    dispatch({ type: 'REMOVE_ITEM', payload: itemId })
  }, [])
  
  const updateQuantity = useCallback((itemId: string, quantity: number) => {
    if (quantity <= 0) {
      removeItem(itemId)
    } else {
      dispatch({ type: 'UPDATE_QUANTITY', payload: { id: itemId, quantity } })
    }
  }, [removeItem])
  
  const clearCart = useCallback(() => {
    dispatch({ type: 'CLEAR_CART' })
  }, [])
  
  const applyVoucher = useCallback(async (code: string) => {
    setIsLoading(true)
    try {
      // Call API to validate voucher
      const response = await fetch('/api/vouchers/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, subtotal: cart.subtotal }),
      })
      
      if (!response.ok) {
        throw new Error('Invalid voucher code')
      }
      
      const { discount } = await response.json()
      dispatch({ type: 'APPLY_DISCOUNT', payload: discount })
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [cart.subtotal])
  
  const value: CartContextValue = {
    cart,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    applyVoucher,
    isLoading,
  }
  
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

// Hook
export function useCart() {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within CartProvider')
  }
  return context
}
```

### 3. Cart Component

```typescript
// components/cart/Cart.tsx
import { useCart } from '@/contexts/CartContext'
import { CartItem } from './CartItem'
import { CartSummary } from './CartSummary'

export function Cart() {
  const { cart, clearCart } = useCart()
  
  if (cart.items.length === 0) {
    return (
      <div className="cart-empty">
        <p>Your cart is empty</p>
        <a href="/products">Continue Shopping</a>
      </div>
    )
  }
  
  return (
    <div className="cart">
      <div className="cart-header">
        <h2>Shopping Cart ({cart.items.length} items)</h2>
        <button onClick={clearCart} className="btn-clear">
          Clear Cart
        </button>
      </div>
      
      <div className="cart-content">
        <div className="cart-items">
          {cart.items.map((item) => (
            <CartItem key={item.id} item={item} />
          ))}
        </div>
        
        <CartSummary cart={cart} />
      </div>
    </div>
  )
}
```

### 4. Cart Item Component

```typescript
// components/cart/CartItem.tsx
import { useCart } from '@/contexts/CartContext'
import type { CartItem as CartItemType } from '@/types/type.cart'
import { Trash2, Plus, Minus } from 'lucide-react'

interface CartItemProps {
  item: CartItemType
}

export function CartItem({ item }: CartItemProps) {
  const { updateQuantity, removeItem } = useCart()
  
  const handleIncrement = () => {
    updateQuantity(item.id, item.quantity + 1)
  }
  
  const handleDecrement = () => {
    updateQuantity(item.id, item.quantity - 1)
  }
  
  const handleRemove = () => {
    if (confirm('Remove this item from cart?')) {
      removeItem(item.id)
    }
  }
  
  return (
    <div className="cart-item">
      <img src={item.image} alt={item.name} className="cart-item__image" />
      
      <div className="cart-item__details">
        <h3 className="cart-item__name">{item.name}</h3>
        <p className="cart-item__price">{formatPrice(item.price)}</p>
      </div>
      
      <div className="cart-item__quantity">
        <button
          onClick={handleDecrement}
          disabled={item.quantity <= 1}
          className="btn-quantity"
          aria-label="Decrease quantity"
        >
          <Minus size={16} />
        </button>
        
        <span className="quantity-value">{item.quantity}</span>
        
        <button
          onClick={handleIncrement}
          disabled={item.quantity >= item.maxQuantity}
          className="btn-quantity"
          aria-label="Increase quantity"
        >
          <Plus size={16} />
        </button>
      </div>
      
      <div className="cart-item__total">
        {formatPrice(item.price * item.quantity)}
      </div>
      
      <button
        onClick={handleRemove}
        className="btn-remove"
        aria-label="Remove item"
      >
        <Trash2 size={20} />
      </button>
    </div>
  )
}
```

### 5. Cart Summary Component

```typescript
// components/cart/CartSummary.tsx
import { useState } from 'react'
import { useCart } from '@/contexts/CartContext'
import type { Cart } from '@/types/type.cart'

interface CartSummaryProps {
  cart: Cart
}

export function CartSummary({ cart }: CartSummaryProps) {
  const { applyVoucher, isLoading } = useCart()
  const [voucherCode, setVoucherCode] = useState('')
  const [voucherError, setVoucherError] = useState('')
  
  const handleApplyVoucher = async () => {
    if (!voucherCode.trim()) return
    
    setVoucherError('')
    try {
      await applyVoucher(voucherCode)
      setVoucherCode('')
    } catch (error) {
      setVoucherError(error.message)
    }
  }
  
  return (
    <div className="cart-summary">
      <h3>Order Summary</h3>
      
      <div className="summary-row">
        <span>Subtotal</span>
        <span>{formatPrice(cart.subtotal)}</span>
      </div>
      
      <div className="summary-row">
        <span>Shipping</span>
        <span>
          {cart.shipping === 0 ? (
            <span className="text-success">Free</span>
          ) : (
            formatPrice(cart.shipping)
          )}
        </span>
      </div>
      
      {cart.discount > 0 && (
        <div className="summary-row text-success">
          <span>Discount</span>
          <span>-{formatPrice(cart.discount)}</span>
        </div>
      )}
      
      <div className="summary-divider" />
      
      <div className="summary-row summary-total">
        <span>Total</span>
        <span>{formatPrice(cart.total)}</span>
      </div>
      
      {/* Voucher input */}
      <div className="voucher-section">
        <input
          type="text"
          placeholder="Voucher code"
          value={voucherCode}
          onChange={(e) => setVoucherCode(e.target.value)}
          className="voucher-input"
        />
        <button
          onClick={handleApplyVoucher}
          disabled={isLoading || !voucherCode.trim()}
          className="btn-apply"
        >
          {isLoading ? 'Applying...' : 'Apply'}
        </button>
      </div>
      
      {voucherError && (
        <p className="voucher-error">{voucherError}</p>
      )}
      
      {/* Free shipping notice */}
      {cart.subtotal < 500000 && (
        <p className="shipping-notice">
          Add {formatPrice(500000 - cart.subtotal)} more for free shipping
        </p>
      )}
      
      <button className="btn-checkout">
        Proceed to Checkout
      </button>
    </div>
  )
}
```

### 6. Usage in App

```typescript
// app/layout.tsx
import { CartProvider } from '@/contexts/CartContext'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <CartProvider>
          {children}
        </CartProvider>
      </body>
    </html>
  )
}

// components/ProductCard.tsx
import { useCart } from '@/contexts/CartContext'

export function ProductCard({ product }) {
  const { addItem } = useCart()
  
  const handleAddToCart = () => {
    addItem({
      id: `cart-${product.id}`,
      productId: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      maxQuantity: product.quantity,
    })
  }
  
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{formatPrice(product.price)}</p>
      <button onClick={handleAddToCart}>Add to Cart</button>
    </div>
  )
}
```

---

## 🎯 Key Features Demonstrated

### 1. State Management
- Context API for global state
- useReducer for complex state logic
- localStorage persistence
- Optimistic updates

### 2. React Hooks
- useState for local state
- useEffect for side effects
- useCallback for memoization
- useContext for consuming context
- Custom hooks (useCart)

### 3. TypeScript
- Full type safety
- Interface definitions
- Type guards
- Generic types

### 4. Performance
- Memoized callbacks
- Efficient re-renders
- Lazy loading

### 5. User Experience
- Loading states
- Error handling
- Confirmation dialogs
- Accessibility (ARIA labels)

---

## ✅ Best Practices

### Component Structure
- Single responsibility
- Props interface
- Clear naming
- Proper exports

### State Management
- Immutable updates
- Centralized logic
- Predictable state changes

### Error Handling
- Try-catch blocks
- User-friendly messages
- Graceful degradation

### Accessibility
- ARIA labels
- Keyboard navigation
- Screen reader support

### Performance
- Memoization
- Efficient updates
- Minimal re-renders
