"use client";
// screens/ProductDetailScreen.jsx
// Shows full product info, artisan section, recommended buyers badge, related products, and add-to-cart.

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { getProductById, getRelatedProducts } from "@/services/productService";
import { useCart } from "@/context/CartContext";
import Toast from "@/components/Toast";
import styles from "./ProductDetailScreen.module.css";

export default function ProductDetailScreen({ productId }) {
  const router = useRouter();
  const { addToCart } = useCart();

  const [product, setProduct] = useState(null);
  const [related, setRelated] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [toastVisible, setToastVisible] = useState(false);
  const [toastKey, setToastKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setQuantity(1);

    getProductById(productId).then(async (prod) => {
      if (cancelled) return;
      setProduct(prod);
      if (prod) {
        const rel = await getRelatedProducts(prod.id, prod.category, prod.tags);
        if (!cancelled) setRelated(rel);
      }
      setLoading(false);
    });

    return () => { cancelled = true; };
  }, [productId]);

  function handleAddToCart() {
    if (!product) return;
    addToCart(product, quantity);
    setToastKey((k) => k + 1);
    setToastVisible(true);
    setTimeout(() => setToastVisible(false), 2500);
  }

  if (loading) {
    return (
      <div className={styles.loadingScreen}>
        <div className={`skeleton ${styles.skeletonHero}`} />
        <div className={styles.skeletonBody}>
          <div className={`skeleton ${styles.skeletonTitle}`} />
          <div className={`skeleton ${styles.skeletonLine}`} />
          <div className={`skeleton ${styles.skeletonLine}`} />
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className={styles.notFound}>
        <p className={styles.notFoundText}>Product not found.</p>
        <button className={styles.backLink} onClick={() => router.push("/")}>← Back to Home</button>
      </div>
    );
  }

  return (
    <div className={styles.screen}>
      <div className={styles.detailGrid}>
        {/* Hero image */}
        <div className={styles.hero}>
          <Image
            src={product.image}
            alt={product.name}
            fill
            sizes="(max-width: 768px) 100vw, 500px"
            className={styles.heroImage}
            priority
            unoptimized
          />
          {/* Back button */}
          <button
            id="product-detail-back"
            className={styles.backBtn}
            onClick={() => router.back()}
            aria-label="Go back"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>
          {/* Top bar title */}
          <div className={styles.heroTitle}>Product Details</div>
        </div>

        <div className={styles.content}>
          {/* Name & price */}
          <div className={styles.nameRow}>
            <div>
              <span className={styles.categoryTag}>{product.category}</span>
              <h1 className={styles.productName}>{product.name}</h1>
            </div>
            <div className={styles.price}>₹{product.price.toLocaleString("en-IN")}</div>
          </div>

          {/* Recommended Buyers Badge — the core feature */}
          {product.recommendedBuyers && product.recommendedBuyers.length > 0 && (
            <div className={styles.buyersBadge} aria-label="Recommended buyers">
              <div className={styles.buyersBadgeHeader}>
                <span className={styles.buyersBadgeIcon}>✨</span>
                <span className={styles.buyersBadgeLabel}>AI-Matched Buyers 🌿</span>
              </div>
              <div className={styles.buyersList}>
                {product.recommendedBuyers.map((buyer) => (
                  <span key={buyer} className={styles.buyerPill}>{buyer}</span>
                ))}
              </div>
            </div>
          )}

          {/* Description */}
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>About this Product</h2>
            <p className={styles.description}>{product.description}</p>
            <div className={styles.metaRow}>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Material</span>
                <span className={styles.metaValue}>{product.material}</span>
              </div>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Category</span>
                <span className={styles.metaValue}>{product.category}</span>
              </div>
            </div>
          </div>

          {/* Meet the Artisan */}
          <div className={styles.artisanCard}>
            <div className={styles.artisanAvatar} aria-hidden="true">
              {product.artisanName ? product.artisanName.charAt(0) : "A"}
            </div>
            <div className={styles.artisanInfo}>
              <div className={styles.artisanHeader}>
                <div>
                  <p className={styles.artisanLabel}>Meet the Artisan</p>
                  <p className={styles.artisanName}>{product.artisanName || "Unknown Artisan"}</p>
                </div>
                {product.artisanRegion && (
                  <span className={styles.regionBadge}>📍 {product.artisanRegion}</span>
                )}
              </div>
              {product.artisanBio && (
                <p className={styles.artisanBio}>{product.artisanBio}</p>
              )}
            </div>
          </div>

          {/* You Might Also Like */}
          {related.length > 0 && (
            <div className={styles.section}>
              <h2 className={styles.sectionTitle}>You Might Also Like</h2>
              <div className={`${styles.relatedRow} hide-scrollbar`}>
                {related.map((rel) => (
                  <Link key={rel.id} href={`/product/${rel.id}`} className={styles.relatedCard}>
                    <div className={styles.relatedImageWrapper}>
                      <Image
                        src={rel.image}
                        alt={rel.name}
                        fill
                        sizes="120px"
                        className={styles.relatedImage}
                        unoptimized
                      />
                    </div>
                    <p className={styles.relatedName}>{rel.name}</p>
                    <p className={styles.relatedPrice}>₹{rel.price.toLocaleString("en-IN")}</p>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Sticky bottom: quantity + add to cart */}
      <div className={styles.stickyBottom}>
        <div className={styles.quantityStepper}>
          <button
            id="qty-decrease"
            className={styles.qtyBtn}
            onClick={() => setQuantity((q) => Math.max(1, q - 1))}
            aria-label="Decrease quantity"
          >
            −
          </button>
          <span className={styles.qtyValue}>{quantity}</span>
          <button
            id="qty-increase"
            className={styles.qtyBtn}
            onClick={() => setQuantity((q) => q + 1)}
            aria-label="Increase quantity"
          >
            +
          </button>
        </div>
        <button
          id="add-to-cart-btn"
          className={styles.addToCartBtn}
          onClick={handleAddToCart}
        >
          Add to Cart · ₹{(product.price * quantity).toLocaleString("en-IN")}
        </button>
      </div>

      <Toast key={toastKey} message="Added to cart 🛒" visible={toastVisible} />
    </div>
  );
}
