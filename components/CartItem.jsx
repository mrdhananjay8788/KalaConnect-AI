"use client";
// components/CartItem.jsx
// A single row in the cart: image, name, price, quantity stepper, remove button.
// Reads from and writes to CartContext directly.

import Image from "next/image";
import { useCart } from "@/context/CartContext";
import styles from "./CartItem.module.css";

export default function CartItem({ item }) {
  const { updateQuantity, removeFromCart } = useCart();
  const { id, name, price, image, quantity } = item;

  return (
    <div className={styles.row}>
      <div className={styles.imageWrapper}>
        <Image
          src={image}
          alt={name}
          fill
          sizes="72px"
          className={styles.image}
          unoptimized
        />
      </div>

      <div className={styles.details}>
        <p className={styles.name}>{name}</p>
        <p className={styles.price}>₹{price.toLocaleString("en-IN")}</p>

        <div className={styles.actions}>
          <div className={styles.stepper}>
            <button
              className={styles.stepBtn}
              onClick={() => updateQuantity(id, quantity - 1)}
              aria-label="Decrease quantity"
            >
              −
            </button>
            <span className={styles.qty}>{quantity}</span>
            <button
              className={styles.stepBtn}
              onClick={() => updateQuantity(id, quantity + 1)}
              aria-label="Increase quantity"
            >
              +
            </button>
          </div>

          <button
            className={styles.removeBtn}
            onClick={() => removeFromCart(id)}
            aria-label="Remove item"
          >
            Remove
          </button>
        </div>
      </div>

      <p className={styles.subtotal}>
        ₹{(price * quantity).toLocaleString("en-IN")}
      </p>
    </div>
  );
}
