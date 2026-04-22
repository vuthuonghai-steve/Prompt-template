# State Management with Redux Toolkit Example

> **Context**: E-commerce shopping cart với Redux Toolkit
> **Stack**: React 19 + TypeScript + Redux Toolkit + RTK Query
> **Last Updated**: 2026-04-23

---

## Overview

Complete Redux Toolkit setup cho e-commerce flower shop, bao gồm:
- Shopping cart state management
- Async thunks cho API calls
- RTK Query cho data fetching
- Optimistic updates
- Persistence với localStorage

---

## Store Configuration

```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import cartReducer from './slices/cart.slice'
import userReducer from './slices/user.slice'
import { productsApi } from './api/products.api'
import { ordersApi } from './api/orders.api'

export const store = configureStore({
  reducer: {
    cart: cartReducer,
    user: userReducer,
    [productsApi.reducerPath]: productsApi.reducer,
    [ordersApi.reducerPath]: ordersApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      productsApi.middleware,
      ordersApi.middleware
    ),
})

setupListeners(store.dispatch)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

---

## Cart Slice

```typescript
// store/slices/cart.slice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import type { RootState } from '../index'

// Types
export interface CartItem {
  id: string
  productId: string
  name: string
  price: number
  quantity: number
  image: string
  maxQuantity: number
}

interface CartState {
  items: CartItem[]
  total: number
  itemCount: number
  isLoading: boolean
  error: string | null
  lastUpdated: number | null
}

// Initial state
const initialState: CartState = {
  items: [],
  total: 0,
  itemCount: 0,
  isLoading: false,
  error: null,
  lastUpdated: null,
}

// Async thunks
export const addToCartAsync = createAsyncThunk(
  'cart/addToCartAsync',
  async (
    { productId, quantity }: { productId: string; quantity: number },
    { rejectWithValue }
  ) => {
    try {
      const response = await fetch(`/api/cart/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ productId, quantity }),
      })

      if (!response.ok) {
        throw new Error('Failed to add item to cart')
      }

      const data = await response.json()
      return data.item as CartItem
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Unknown error'
      )
    }
  }
)

export const updateQuantityAsync = createAsyncThunk(
  'cart/updateQuantityAsync',
  async (
    { itemId, quantity }: { itemId: string; quantity: number },
    { rejectWithValue }
  ) => {
    try {
      const response = await fetch(`/api/cart/update`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ itemId, quantity }),
      })

      if (!response.ok) {
        throw new Error('Failed to update quantity')
      }

      return { itemId, quantity }
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Unknown error'
      )
    }
  }
)

export const removeFromCartAsync = createAsyncThunk(
  'cart/removeFromCartAsync',
  async (itemId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/cart/remove`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ itemId }),
      })

      if (!response.ok) {
        throw new Error('Failed to remove item')
      }

      return itemId
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Unknown error'
      )
    }
  }
)

export const syncCartWithServer = createAsyncThunk(
  'cart/syncWithServer',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as RootState
      const response = await fetch('/api/cart/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: state.cart.items }),
      })

      if (!response.ok) {
        throw new Error('Failed to sync cart')
      }

      const data = await response.json()
      return data.items as CartItem[]
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Unknown error'
      )
    }
  }
)

// Slice
const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addToCart: (state, action: PayloadAction<CartItem>) => {
      const existingItem = state.items.find(
        (item) => item.productId === action.payload.productId
      )

      if (existingItem) {
        const newQuantity = existingItem.quantity + action.payload.quantity
        if (newQuantity <= existingItem.maxQuantity) {
          existingItem.quantity = newQuantity
        } else {
          state.error = `Chỉ còn ${existingItem.maxQuantity} sản phẩm`
          return
        }
      } else {
        state.items.push(action.payload)
      }

      cartSlice.caseReducers.recalculateCart(state)
      state.lastUpdated = Date.now()
    },

    updateQuantity: (
      state,
      action: PayloadAction<{ itemId: string; quantity: number }>
    ) => {
      const item = state.items.find((i) => i.id === action.payload.itemId)
      
      if (item) {
        if (action.payload.quantity <= 0) {
          state.items = state.items.filter((i) => i.id !== action.payload.itemId)
        } else if (action.payload.quantity <= item.maxQuantity) {
          item.quantity = action.payload.quantity
        } else {
          state.error = `Chỉ còn ${item.maxQuantity} sản phẩm`
          return
        }
      }

      cartSlice.caseReducers.recalculateCart(state)
      state.lastUpdated = Date.now()
    },

    removeFromCart: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter((item) => item.id !== action.payload)
      cartSlice.caseReducers.recalculateCart(state)
      state.lastUpdated = Date.now()
    },

    clearCart: (state) => {
      state.items = []
      state.total = 0
      state.itemCount = 0
      state.error = null
      state.lastUpdated = Date.now()
    },

    clearError: (state) => {
      state.error = null
    },

    recalculateCart: (state) => {
      state.total = state.items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
      )
      state.itemCount = state.items.reduce(
        (sum, item) => sum + item.quantity,
        0
      )
    },

    loadCartFromStorage: (state, action: PayloadAction<CartItem[]>) => {
      state.items = action.payload
      cartSlice.caseReducers.recalculateCart(state)
    },
  },
  extraReducers: (builder) => {
    // addToCartAsync
    builder
      .addCase(addToCartAsync.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(addToCartAsync.fulfilled, (state, action) => {
        state.isLoading = false
        cartSlice.caseReducers.addToCart(state, action)
      })
      .addCase(addToCartAsync.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })

    // updateQuantityAsync
    builder
      .addCase(updateQuantityAsync.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(updateQuantityAsync.fulfilled, (state, action) => {
        state.isLoading = false
        cartSlice.caseReducers.updateQuantity(state, action)
      })
      .addCase(updateQuantityAsync.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })

    // removeFromCartAsync
    builder
      .addCase(removeFromCartAsync.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(removeFromCartAsync.fulfilled, (state, action) => {
        state.isLoading = false
        cartSlice.caseReducers.removeFromCart(state, action)
      })
      .addCase(removeFromCartAsync.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })

    // syncCartWithServer
    builder
      .addCase(syncCartWithServer.pending, (state) => {
        state.isLoading = true
      })
      .addCase(syncCartWithServer.fulfilled, (state, action) => {
        state.isLoading = false
        state.items = action.payload
        cartSlice.caseReducers.recalculateCart(state)
        state.lastUpdated = Date.now()
      })
      .addCase(syncCartWithServer.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
  },
})

export const {
  addToCart,
  updateQuantity,
  removeFromCart,
  clearCart,
  clearError,
  loadCartFromStorage,
} = cartSlice.actions

export default cartSlice.reducer

// Selectors
export const selectCartItems = (state: RootState) => state.cart.items
export const selectCartTotal = (state: RootState) => state.cart.total
export const selectCartItemCount = (state: RootState) => state.cart.itemCount
export const selectCartIsLoading = (state: RootState) => state.cart.isLoading
export const selectCartError = (state: RootState) => state.cart.error

export const selectCartItemById = (itemId: string) => (state: RootState) =>
  state.cart.items.find((item) => item.id === itemId)

export const selectIsInCart = (productId: string) => (state: RootState) =>
  state.cart.items.some((item) => item.productId === productId)
```

---

## RTK Query API

```typescript
// store/api/products.api.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export interface Product {
  id: string
  name: string
  description: string
  price: number
  image: string
  category: string
  stock: number
  tags: string[]
}

export interface ProductsResponse {
  products: Product[]
  total: number
  page: number
  limit: number
}

export const productsApi = createApi({
  reducerPath: 'productsApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Product'],
  endpoints: (builder) => ({
    getProducts: builder.query<ProductsResponse, { page?: number; limit?: number; category?: string }>({
      query: ({ page = 1, limit = 12, category }) => ({
        url: '/products',
        params: { page, limit, category },
      }),
      providesTags: (result) =>
        result
          ? [
              ...result.products.map(({ id }) => ({ type: 'Product' as const, id })),
              { type: 'Product', id: 'LIST' },
            ]
          : [{ type: 'Product', id: 'LIST' }],
    }),

    getProductById: builder.query<Product, string>({
      query: (id) => `/products/${id}`,
      providesTags: (result, error, id) => [{ type: 'Product', id }],
    }),

    searchProducts: builder.query<Product[], string>({
      query: (searchTerm) => `/products/search?q=${searchTerm}`,
      providesTags: [{ type: 'Product', id: 'SEARCH' }],
    }),

    getFeaturedProducts: builder.query<Product[], void>({
      query: () => '/products/featured',
      providesTags: [{ type: 'Product', id: 'FEATURED' }],
    }),
  }),
})

export const {
  useGetProductsQuery,
  useGetProductByIdQuery,
  useSearchProductsQuery,
  useGetFeaturedProductsQuery,
} = productsApi
```

---

## Custom Hooks

```typescript
// hooks/use-cart.ts
import { useDispatch, useSelector } from 'react-redux'
import { useCallback } from 'react'
import type { AppDispatch } from '@/store'
import {
  addToCart,
  updateQuantity,
  removeFromCart,
  clearCart,
  clearError,
  addToCartAsync,
  updateQuantityAsync,
  removeFromCartAsync,
  selectCartItems,
  selectCartTotal,
  selectCartItemCount,
  selectCartIsLoading,
  selectCartError,
  selectIsInCart,
  type CartItem,
} from '@/store/slices/cart.slice'

export function useCart() {
  const dispatch = useDispatch<AppDispatch>()
  
  const items = useSelector(selectCartItems)
  const total = useSelector(selectCartTotal)
  const itemCount = useSelector(selectCartItemCount)
  const isLoading = useSelector(selectCartIsLoading)
  const error = useSelector(selectCartError)

  const addItem = useCallback(
    (item: CartItem) => {
      dispatch(addToCart(item))
    },
    [dispatch]
  )

  const addItemAsync = useCallback(
    (productId: string, quantity: number) => {
      dispatch(addToCartAsync({ productId, quantity }))
    },
    [dispatch]
  )

  const updateItemQuantity = useCallback(
    (itemId: string, quantity: number) => {
      dispatch(updateQuantity({ itemId, quantity }))
    },
    [dispatch]
  )

  const updateItemQuantityAsync = useCallback(
    (itemId: string, quantity: number) => {
      dispatch(updateQuantityAsync({ itemId, quantity }))
    },
    [dispatch]
  )

  const removeItem = useCallback(
    (itemId: string) => {
      dispatch(removeFromCart(itemId))
    },
    [dispatch]
  )

  const removeItemAsync = useCallback(
    (itemId: string) => {
      dispatch(removeFromCartAsync(itemId))
    },
    [dispatch]
  )

  const clear = useCallback(() => {
    dispatch(clearCart())
  }, [dispatch])

  const dismissError = useCallback(() => {
    dispatch(clearError())
  }, [dispatch])

  const isProductInCart = useCallback(
    (productId: string) => {
      return items.some((item) => item.productId === productId)
    },
    [items]
  )

  return {
    items,
    total,
    itemCount,
    isLoading,
    error,
    addItem,
    addItemAsync,
    updateItemQuantity,
    updateItemQuantityAsync,
    removeItem,
    removeItemAsync,
    clear,
    dismissError,
    isProductInCart,
  }
}

// hooks/use-app-selector.ts
import { useSelector, TypedUseSelectorHook } from 'react-redux'
import type { RootState } from '@/store'

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector

// hooks/use-app-dispatch.ts
import { useDispatch } from 'react-redux'
import type { AppDispatch } from '@/store'

export const useAppDispatch = () => useDispatch<AppDispatch>()
```

---

## Component Usage

```tsx
// components/ProductCard.tsx
import React from 'react'
import { useCart } from '@/hooks/use-cart'
import { Button } from '@/components/ui/button'
import { ShoppingCart, Check } from 'lucide-react'
import toast from 'react-hot-toast'

interface ProductCardProps {
  product: {
    id: string
    name: string
    price: number
    image: string
    stock: number
  }
}

export function ProductCard({ product }: ProductCardProps) {
  const { addItemAsync, isProductInCart, isLoading } = useCart()

  const handleAddToCart = () => {
    addItemAsync(product.id, 1)
    toast.success(`Đã thêm ${product.name} vào giỏ hàng`)
  }

  const inCart = isProductInCart(product.id)

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img 
        src={product.image} 
        alt={product.name}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="font-serif text-xl font-semibold mb-2">
          {product.name}
        </h3>
        <p className="text-primary-600 font-semibold text-lg mb-4">
          {product.price.toLocaleString('vi-VN')}đ
        </p>
        
        {product.stock > 0 ? (
          <Button
            onClick={handleAddToCart}
            disabled={isLoading || inCart}
            className="w-full"
          >
            {inCart ? (
              <>
                <Check className="w-4 h-4 mr-2" />
                Đã thêm vào giỏ
              </>
            ) : (
              <>
                <ShoppingCart className="w-4 h-4 mr-2" />
                Thêm vào giỏ
              </>
            )}
          </Button>
        ) : (
          <Button disabled className="w-full">
            Hết hàng
          </Button>
        )}
      </div>
    </div>
  )
}

// components/CartDrawer.tsx
import React from 'react'
import { useCart } from '@/hooks/use-cart'
import { Button } from '@/components/ui/button'
import { Trash2, Plus, Minus } from 'lucide-react'
import { useRouter } from 'next/navigation'

export function CartDrawer() {
  const router = useRouter()
  const { 
    items, 
    total, 
    itemCount, 
    updateItemQuantity, 
    removeItem 
  } = useCart()

  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Giỏ hàng trống</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {items.map((item) => (
          <div key={item.id} className="flex gap-4 bg-white rounded-lg p-4 shadow">
            <img 
              src={item.image} 
              alt={item.name}
              className="w-20 h-20 object-cover rounded"
            />
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900">{item.name}</h4>
              <p className="text-primary-600 font-medium">
                {item.price.toLocaleString('vi-VN')}đ
              </p>
              
              <div className="flex items-center gap-2 mt-2">
                <button
                  onClick={() => updateItemQuantity(item.id, item.quantity - 1)}
                  className="p-1 rounded hover:bg-gray-100"
                  disabled={item.quantity <= 1}
                >
                  <Minus className="w-4 h-4" />
                </button>
                
                <span className="w-8 text-center font-medium">
                  {item.quantity}
                </span>
                
                <button
                  onClick={() => updateItemQuantity(item.id, item.quantity + 1)}
                  className="p-1 rounded hover:bg-gray-100"
                  disabled={item.quantity >= item.maxQuantity}
                >
                  <Plus className="w-4 h-4" />
                </button>
                
                <button
                  onClick={() => removeItem(item.id)}
                  className="ml-auto p-1 text-red-600 hover:bg-red-50 rounded"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="border-t p-4 space-y-4">
        <div className="flex justify-between text-lg font-semibold">
          <span>Tổng cộng ({itemCount} sản phẩm)</span>
          <span className="text-primary-600">
            {total.toLocaleString('vi-VN')}đ
          </span>
        </div>
        
        <Button 
          onClick={() => router.push('/checkout')}
          className="w-full"
          size="lg"
        >
          Thanh toán
        </Button>
      </div>
    </div>
  )
}
```

---

## LocalStorage Persistence

```typescript
// lib/cart-persistence.ts
import { store } from '@/store'
import { loadCartFromStorage } from '@/store/slices/cart.slice'

const CART_STORAGE_KEY = 'siinstore_cart'

export function saveCartToStorage() {
  try {
    const state = store.getState()
    const cartData = JSON.stringify(state.cart.items)
    localStorage.setItem(CART_STORAGE_KEY, cartData)
  } catch (error) {
    console.error('Failed to save cart to storage:', error)
  }
}

export function loadCartFromStorageOnInit() {
  try {
    const cartData = localStorage.getItem(CART_STORAGE_KEY)
    if (cartData) {
      const items = JSON.parse(cartData)
      store.dispatch(loadCartFromStorage(items))
    }
  } catch (error) {
    console.error('Failed to load cart from storage:', error)
  }
}

// Subscribe to store changes
store.subscribe(() => {
  saveCartToStorage()
})
```

---

## Provider Setup

```tsx
// app/providers.tsx
'use client'

import React, { useEffect } from 'react'
import { Provider } from 'react-redux'
import { store } from '@/store'
import { loadCartFromStorageOnInit } from '@/lib/cart-persistence'

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    loadCartFromStorageOnInit()
  }, [])

  return <Provider store={store}>{children}</Provider>
}
```

---

## Benefits

| Feature | Implementation |
|---------|----------------|
| **Type Safety** | Full TypeScript support |
| **Async Operations** | createAsyncThunk cho API calls |
| **Optimistic Updates** | Local updates trước, sync sau |
| **Caching** | RTK Query auto-caching |
| **Persistence** | localStorage integration |
| **DevTools** | Redux DevTools support |

---

## Related

- [template-state-management.md](../templates/template-state-management.md)
- [example-form-validation.md](./example-form-validation.md)
