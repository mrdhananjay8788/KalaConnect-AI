"use client";
// screens/BrowseScreen.jsx
// Home screen: header, search bar with camera icon, category filter chips, 2-col product grid.

import { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import { getProducts } from "@/services/productService";
import ProductGrid from "@/components/ProductGrid";
import styles from "./BrowseScreen.module.css";

const CATEGORIES = ["All", "Home Decor", "Pottery", "Paintings", "Sarees", "Wooden Craft", "Jute Bags"];

export default function BrowseScreen({ customerName = "Guest" }) {
  const router = useRouter();
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    getProducts().then((data) => {
      if (!cancelled) {
        setProducts(data);
        setIsLoading(false);
      }
    });
    return () => { cancelled = true; };
  }, []);

  const filteredProducts = useMemo(() => {
    let result = products;

    if (activeCategory !== "All") {
      result = result.filter(
        (p) => p.category.toLowerCase() === activeCategory.toLowerCase()
      );
    }

    if (searchQuery.trim()) {
      const q = searchQuery.trim().toLowerCase();
      result = result.filter(
        (p) =>
          p.name.toLowerCase().includes(q) ||
          p.category.toLowerCase().includes(q) ||
          (p.tags && p.tags.some((t) => t.toLowerCase().includes(q)))
      );
    }

    return result;
  }, [products, activeCategory, searchQuery]);

  return (
    <div className={styles.screen}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.headerTop}>
          <div>
            <p className={styles.greeting}>Welcome back 👋</p>
            <h1 className={styles.name}>{customerName}</h1>
          </div>
          <div className={styles.avatar} aria-hidden="true">
            {customerName.charAt(0).toUpperCase()}
          </div>
        </div>

        {/* Search bar */}
        <div className={styles.searchBar}>
          <span className={styles.searchIcon} aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
          </span>
          <input
            id="browse-search"
            type="search"
            placeholder="Search handmade products..."
            className={styles.searchInput}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Search products"
          />
          <button
            id="camera-search-btn"
            className={styles.cameraBtn}
            onClick={() => router.push("/visual-search")}
            aria-label="Visual search"
            title="Visual search (coming soon)"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
          </button>
        </div>
      </div>

      {/* Category chips */}
      <div className={styles.chipsWrapper}>
        <div className={`${styles.chips} hide-scrollbar`} role="tablist" aria-label="Filter by category">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              id={`chip-${cat.replace(/\s+/g, "-").toLowerCase()}`}
              role="tab"
              aria-selected={activeCategory === cat}
              className={`${styles.chip} ${activeCategory === cat ? styles.chipActive : ""}`}
              onClick={() => setActiveCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Section heading */}
      <div className={styles.sectionHeading}>
        <h2 className={styles.sectionTitle}>
          {activeCategory === "All" ? "All Products" : activeCategory}
        </h2>
        {!isLoading && (
          <span className={styles.productCount}>{filteredProducts.length} items</span>
        )}
      </div>

      {/* Product grid */}
      <ProductGrid products={filteredProducts} isLoading={isLoading} />
    </div>
  );
}
