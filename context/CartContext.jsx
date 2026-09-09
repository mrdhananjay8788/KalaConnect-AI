"use client";
// context/CartContext.jsx
// Provides cart state to the entire app via React Context + useReducer.
// Import useCart() in any component/screen to access cart data and actions.

import { createContext, useContext, useReducer, useMemo } from "react";

// ── Reducer ──────────────────────────────────────────────────────────────────

function cartReducer(state, action) {
  switch (action.type) {
    case "ADD_ITEM": {
      const { product, quantity } = action.payload;
      const existing = state.find((item) => item.id === product.id);
      if (existing) {
        return state.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [...state, { ...product, quantity }];
    }

    case "REMOVE_ITEM":
      return state.filter((item) => item.id !== action.payload.id);

    case "UPDATE_QUANTITY": {
      const { id, quantity } = action.payload;
      if (quantity <= 0) return state.filter((item) => item.id !== id);
      return state.map((item) =>
        item.id === id ? { ...item, quantity } : item
      );
    }

    case "CLEAR_CART":
      return [];

    default:
      return state;
  }
}

// ── Context ───────────────────────────────────────────────────────────────────

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [cartItems, dispatch] = useReducer(cartReducer, []);

  const cartCount = useMemo(
    () => cartItems.reduce((sum, item) => sum + item.quantity, 0),
    [cartItems]
  );

  const cartTotal = useMemo(
    () => cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [cartItems]
  );

  function addToCart(product, quantity = 1) {
    dispatch({ type: "ADD_ITEM", payload: { product, quantity } });
  }

  function removeFromCart(id) {
    dispatch({ type: "REMOVE_ITEM", payload: { id } });
  }

  function updateQuantity(id, quantity) {
    dispatch({ type: "UPDATE_QUANTITY", payload: { id, quantity } });
  }

  function clearCart() {
    dispatch({ type: "CLEAR_CART" });
  }

  return (
    <CartContext.Provider
      value={{ cartItems, cartCount, cartTotal, addToCart, removeFromCart, updateQuantity, clearCart }}
    >
      {children}
    </CartContext.Provider>
  );
}

// ── Hook ──────────────────────────────────────────────────────────────────────

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within a <CartProvider>");
  return ctx;
}
