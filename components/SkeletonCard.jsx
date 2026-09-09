"use client";
// components/SkeletonCard.jsx
// Placeholder card shown during product loading. Mimics ProductCard dimensions.

import styles from "./SkeletonCard.module.css";

export default function SkeletonCard() {
  return (
    <div className={styles.card}>
      <div className={`skeleton ${styles.image}`} />
      <div className={styles.body}>
        <div className={`skeleton ${styles.chip}`} />
        <div className={`skeleton ${styles.title}`} />
        <div className={`skeleton ${styles.titleShort}`} />
        <div className={`skeleton ${styles.price}`} />
      </div>
    </div>
  );
}
