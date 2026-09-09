"use client";
// components/ProductGrid.jsx
// 2-column product grid with skeleton loading state.
// Shows SkeletonCards for `SKELETON_DURATION_MS` ms, then renders real ProductCards.

import { useState, useEffect } from "react";
import ProductCard from "./ProductCard";
import SkeletonCard from "./SkeletonCard";
import styles from "./ProductGrid.module.css";

const SKELETON_COUNT = 6;
const SKELETON_DURATION_MS = 900;

export default function ProductGrid({ products, isLoading }) {
  const [showSkeleton, setShowSkeleton] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => setShowSkeleton(false), SKELETON_DURATION_MS);
    return () => clearTimeout(t);
  }, []);

  if (isLoading || showSkeleton) {
    return (
      <div className={styles.grid}>
        {Array.from({ length: SKELETON_COUNT }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  if (!products || products.length === 0) {
    return (
      <div className={styles.empty}>
        <span className={styles.emptyIcon}>🔍</span>
        <p className={styles.emptyTitle}>No products found</p>
        <p className={styles.emptySubtitle}>Try a different search or category</p>
      </div>
    );
  }

  return (
    <div className={styles.grid}>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
