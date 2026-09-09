"use client";
// screens/CartScreen.jsx
// Displays all cart items, live total, empty state, and Proceed to Checkout button.

import Link from "next/link";
import { useCart } from "@/context/CartContext";
import CartItem from "@/components/CartItem";
import styles from "./CartScreen.module.css";

export default function CartScreen() {
  const { cartItems, cartTotal } = useCart();
  const isEmpty = cartItems.length === 0;

  return (
    <div className={styles.screen}>
      {/* Top bar */}
      <div className={styles.topBar}>
        <h1 className={styles.title}>Your Cart</h1>
        {!isEmpty && (
          <span className={styles.count}>{cartItems.length} item{cartItems.length !== 1 ? "s" : ""}</span>
        )}
      </div>

      {isEmpty ? (
        /* Empty state */
        <div className={styles.emptyState} aria-label="Cart is empty">
          <div className={styles.emptyIconWrapper} aria-hidden="true">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="9" cy="21" r="1" />
              <circle cx="20" cy="21" r="1" />
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
            </svg>
          </div>
          <h2 className={styles.emptyTitle}>Your cart is empty</h2>
          <p className={styles.emptySubtitle}>
            Discover beautiful handmade artisan products and add them to your cart.
          </p>
          <Link href="/" id="empty-cart-browse-btn" className={styles.browseBtn}>
            Browse Products
          </Link>
        </div>
      ) : (
        <div className={styles.cartGrid}>
          {/* Cart items list */}
          <div className={styles.itemsList}>
            {cartItems.map((item) => (
              <CartItem key={item.id} item={item} />
            ))}
          </div>

          {/* Sidebar: Order summary + checkout */}
          <div className={styles.summarySidebar}>
            <div className={styles.summary}>
              <div className={styles.summaryRow}>
                <span className={styles.summaryLabel}>Subtotal</span>
                <span className={styles.summaryValue}>₹{cartTotal.toLocaleString("en-IN")}</span>
              </div>
              <div className={styles.summaryRow}>
                <span className={styles.summaryLabel}>Delivery</span>
                <span className={styles.summaryFree}>FREE</span>
              </div>
              <div className={styles.divider} />
              <div className={styles.summaryRow}>
                <span className={styles.totalLabel}>Total</span>
                <span className={styles.totalValue}>₹{cartTotal.toLocaleString("en-IN")}</span>
              </div>
            </div>

            <div className={styles.checkoutBar}>
              <Link
                href="/checkout"
                id="proceed-to-checkout-btn"
                className={styles.checkoutBtn}
              >
                Proceed to Checkout →
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
