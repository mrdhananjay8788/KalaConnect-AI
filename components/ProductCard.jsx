"use client";
// components/ProductCard.jsx
// Fixed-height card for a single product. Navigates to Product Detail on click.

import Link from "next/link";
import Image from "next/image";
import styles from "./ProductCard.module.css";

export default function ProductCard({ product }) {
  const { id, name, category, price, image } = product;

  return (
    <Link href={`/product/${id}`} className={styles.card}>
      <div className={styles.imageWrapper}>
        <Image
          src={image}
          alt={name}
          fill
          sizes="(max-width: 430px) 45vw, 200px"
          className={styles.image}
          unoptimized
        />
        <span className={styles.categoryChip}>{category}</span>
      </div>
      <div className={styles.body}>
        <p className={styles.name}>{name}</p>
        <p className={styles.price}>₹{price.toLocaleString("en-IN")}</p>
      </div>
    </Link>
  );
}
