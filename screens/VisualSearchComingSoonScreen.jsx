"use client";
// screens/VisualSearchComingSoonScreen.jsx
// Static placeholder screen. No real image upload logic.

import { useRouter } from "next/navigation";
import styles from "./VisualSearchComingSoonScreen.module.css";

export default function VisualSearchComingSoonScreen() {
  const router = useRouter();

  return (
    <div className={styles.screen}>
      {/* Back arrow */}
      <button
        id="visual-search-back"
        className={styles.backBtn}
        onClick={() => router.back()}
        aria-label="Go back"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>

      <div className={styles.centerContent}>
        {/* Camera icon in circular background */}
        <div className={styles.iconCircle} aria-hidden="true">
          <div className={styles.iconInner}>
            <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
          </div>
        </div>

        {/* Decorative orbit ring */}
        <div className={styles.orbitRing} aria-hidden="true" />

        <h1 className={styles.heading}>Visual Search</h1>
        <p className={styles.subheading}>Coming Soon</p>
        <p className={styles.supportText}>
          Soon you&apos;ll be able to upload a photo and find similar handmade products.
        </p>

        {/* Feature pills */}
        <div className={styles.featurePills}>
          <span className={styles.pill}>📸 Upload a photo</span>
          <span className={styles.pill}>🤖 AI matching</span>
          <span className={styles.pill}>🛒 Find & buy</span>
        </div>
      </div>
    </div>
  );
}
