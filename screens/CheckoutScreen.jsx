"use client";
// screens/CheckoutScreen.jsx
// Read-only order summary, delivery address input, place order → confirmation view.

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useCart } from "@/context/CartContext";
import styles from "./CheckoutScreen.module.css";

function generateOrderId() {
  return `#${Math.floor(Math.random() * 900) + 100}`;
}

export default function CheckoutScreen({ customerName = "Guest" }) {
  const router = useRouter();
  const { cartItems, cartTotal, clearCart } = useCart();

  const [address, setAddress] = useState("");
  const [name, setName] = useState(customerName);
  const [confirmed, setConfirmed] = useState(false);
  const [orderId, setOrderId] = useState("");

  function handlePlaceOrder() {
    const id = generateOrderId();
    setOrderId(id);
    clearCart();
    setConfirmed(true);
  }

  /* Confirmation view */
  if (confirmed) {
    return (
      <div className={styles.screen}>
        <div className={styles.confirmationView}>
          <div className={styles.successIcon} aria-hidden="true">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <h1 className={styles.confirmTitle}>Order Placed!</h1>
          <p className={styles.confirmSubtitle}>
            Thank you for supporting handmade artisans. 🙏
          </p>
          <div className={styles.orderIdCard}>
            <p className={styles.orderIdLabel}>Your Order ID</p>
            <p className={styles.orderIdValue}>Order {orderId}</p>
          </div>
          <p className={styles.deliveryNote}>
            Your handcrafted items will be delivered within 5–7 business days.
          </p>
          <button
            id="back-to-home-btn"
            className={styles.homeBtn}
            onClick={() => router.push("/")}
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.screen}>
      {/* Top bar */}
      <div className={styles.topBar}>
        <button
          className={styles.backBtn}
          onClick={() => router.back()}
          aria-label="Go back"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <h1 className={styles.title}>Checkout</h1>
        <div style={{ width: 36 }} />
      </div>

      <div className={styles.content}>
        {/* Delivery details column */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Delivery Details</h2>

          <div className={styles.fieldGroup}>
            <label htmlFor="checkout-name" className={styles.fieldLabel}>Full Name</label>
            <input
              id="checkout-name"
              type="text"
              className={styles.input}
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your full name"
            />
          </div>

          <div className={styles.fieldGroup}>
            <label htmlFor="checkout-address" className={styles.fieldLabel}>Delivery Address</label>
            <textarea
              id="checkout-address"
              className={`${styles.input} ${styles.textarea}`}
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="House / flat no., street, city, state, PIN code"
              rows={3}
            />
          </div>
        </section>

        {/* Order summary sidebar column */}
        <div className={styles.summarySidebar}>
          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Order Summary</h2>
            <div className={styles.orderItems}>
              {cartItems.map((item) => (
                <div key={item.id} className={styles.orderRow}>
                  <div className={styles.orderImageWrapper}>
                    <Image
                      src={item.image}
                      alt={item.name}
                      fill
                      sizes="52px"
                      className={styles.orderImage}
                      unoptimized
                    />
                  </div>
                  <div className={styles.orderDetails}>
                    <p className={styles.orderName}>{item.name}</p>
                    <p className={styles.orderQty}>Qty: {item.quantity}</p>
                  </div>
                  <p className={styles.orderSubtotal}>
                    ₹{(item.price * item.quantity).toLocaleString("en-IN")}
                  </p>
                </div>
              ))}
            </div>
            <div className={styles.totalRow}>
              <span className={styles.totalLabel}>Total</span>
              <span className={styles.totalValue}>₹{cartTotal.toLocaleString("en-IN")}</span>
            </div>
          </section>

          {/* Place Order button */}
          <div className={styles.footer}>
            <button
              id="place-order-btn"
              className={styles.placeOrderBtn}
              onClick={handlePlaceOrder}
            >
              Place Order · ₹{cartTotal.toLocaleString("en-IN")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
