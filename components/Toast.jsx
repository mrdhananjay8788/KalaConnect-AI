"use client";
// components/Toast.jsx
// Simple auto-dismiss snackbar notification.
// Usage: pass `message` prop and `visible` boolean.

import { useEffect, useState } from "react";
import styles from "./Toast.module.css";

export default function Toast({ message, visible }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (visible) {
      setShow(true);
      const t = setTimeout(() => setShow(false), 2200);
      return () => clearTimeout(t);
    }
  }, [visible]);

  if (!show) return null;

  return (
    <div className={styles.toast} role="status" aria-live="polite">
      <span className={styles.icon}>✓</span>
      <span className={styles.text}>{message}</span>
    </div>
  );
}
