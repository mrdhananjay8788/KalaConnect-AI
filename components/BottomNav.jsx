"use client";
// components/BottomNav.jsx
// Fixed bottom navigation bar — Home, Categories, Cart (with badge), Profile.

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCart } from "@/context/CartContext";
import styles from "./BottomNav.module.css";

const NAV_ITEMS = [
  {
    id: "home",
    label: "Home",
    href: "/",
    icon: (active) => (
      <svg width="22" height="22" viewBox="0 0 24 24" fill={active ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z" />
        <polyline points="9 21 9 12 15 12 15 21" />
      </svg>
    ),
  },
  {
    id: "categories",
    label: "Categories",
    href: "/categories",
    icon: (active) => (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1" fill={active ? "currentColor" : "none"} />
        <rect x="14" y="3" width="7" height="7" rx="1" fill={active ? "currentColor" : "none"} />
        <rect x="3" y="14" width="7" height="7" rx="1" fill={active ? "currentColor" : "none"} />
        <rect x="14" y="14" width="7" height="7" rx="1" fill={active ? "currentColor" : "none"} />
      </svg>
    ),
  },
  {
    id: "cart",
    label: "Cart",
    href: "/cart",
    icon: (active) => (
      <svg width="22" height="22" viewBox="0 0 24 24" fill={active ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="9" cy="21" r="1" />
        <circle cx="20" cy="21" r="1" />
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
      </svg>
    ),
  },
  {
    id: "profile",
    label: "Profile",
    href: "/profile",
    icon: (active) => (
      <svg width="22" height="22" viewBox="0 0 24 24" fill={active ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
    ),
  },
];

export default function BottomNav() {
  const pathname = usePathname();
  const { cartCount } = useCart();

  function isActive(href) {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  }

  return (
    <nav className={styles.nav} role="navigation" aria-label="Main navigation">
      {NAV_ITEMS.map(({ id, label, href, icon }) => {
        const active = isActive(href);
        return (
          <Link
            key={id}
            href={href}
            id={`nav-${id}`}
            className={`${styles.tab} ${active ? styles.active : ""}`}
            aria-current={active ? "page" : undefined}
          >
            <span className={styles.iconWrapper}>
              {icon(active)}
              {id === "cart" && cartCount > 0 && (
                <span className={styles.badge} aria-label={`${cartCount} items in cart`}>
                  {cartCount > 9 ? "9+" : cartCount}
                </span>
              )}
            </span>
            <span className={styles.label}>{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
