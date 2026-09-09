// styles/theme.js
// Central design tokens. All CSS custom properties are defined here.
// Reference these variable names in your components; never hardcode hex values.

const theme = {
  colors: {
    bg: "var(--color-bg)",
    surface: "var(--color-surface)",
    surfaceElevated: "var(--color-surface-elevated)",
    textPrimary: "var(--color-text-primary)",
    textSecondary: "var(--color-text-secondary)",
    textMuted: "var(--color-text-muted)",
    accent: "var(--color-accent)",
    accentDark: "var(--color-accent-dark)",
    accentLight: "var(--color-accent-light)",
    accentText: "var(--color-accent-text)",
    border: "var(--color-border)",
    skeleton: "var(--color-skeleton)",
    skeletonHighlight: "var(--color-skeleton-highlight)",
    success: "var(--color-success)",
    error: "var(--color-error)",
    navBg: "var(--color-nav-bg)",
    navActive: "var(--color-nav-active)",
    navInactive: "var(--color-nav-inactive)",
    badgeBg: "var(--color-badge-bg)",
    badgeText: "var(--color-badge-text)",
    chipBg: "var(--color-chip-bg)",
    chipActive: "var(--color-chip-active)",
    chipActiveBg: "var(--color-chip-active-bg)",
  },
  fonts: {
    body: "var(--font-body)",
    heading: "var(--font-heading)",
  },
  radii: {
    sm: "var(--radius-sm)",
    md: "var(--radius-md)",
    lg: "var(--radius-lg)",
    xl: "var(--radius-xl)",
    full: "var(--radius-full)",
  },
  shadows: {
    card: "var(--shadow-card)",
    nav: "var(--shadow-nav)",
    button: "var(--shadow-button)",
  },
  spacing: {
    xs: "var(--space-xs)",
    sm: "var(--space-sm)",
    md: "var(--space-md)",
    lg: "var(--space-lg)",
    xl: "var(--space-xl)",
  },
};

// CSS custom property values injected at :root
// Palette is tuned to the Indian watercolor peacock art background.
export const cssVariables = {
  // ── Backgrounds (glass / transparent for art-bg blending) ──
  "--color-bg": "rgba(250,245,236,0.0)",
  "--color-bg-gradient": "transparent",
  "--color-surface": "rgba(255,251,244,0.75)",
  "--color-surface-elevated": "rgba(255,253,248,0.85)",

  // ── Text ──
  "--color-text-primary": "#22140a",
  "--color-text-secondary": "#5c3d2a",
  "--color-text-muted": "#8a6a54",

  // ── Accent — deep saffron-crimson from the peacock art ──
  "--color-accent": "#c0501a",
  "--color-accent-dark": "#943c12",
  "--color-accent-light": "rgba(240,180,140,0.35)",
  "--color-accent-text": "#ffffff",

  // ── Borders & Skeletons ──
  "--color-border": "rgba(196,142,84,0.32)",
  "--color-skeleton": "rgba(220,196,168,0.55)",
  "--color-skeleton-highlight": "rgba(245,235,218,0.70)",

  // ── Semantic ──
  "--color-success": "#3d7a52",
  "--color-error": "#b03535",

  // ── Nav (glass) ──
  "--color-nav-bg": "rgba(255,251,244,0.82)",
  "--color-nav-active": "#c0501a",
  "--color-nav-inactive": "#8a6a54",

  // ── Badges & Chips ──
  "--color-badge-bg": "#c0501a",
  "--color-badge-text": "#ffffff",
  "--color-chip-bg": "rgba(240,220,196,0.60)",
  "--color-chip-active": "#ffffff",
  "--color-chip-active-bg": "#c0501a",
  "--color-chip-active-gradient":
    "linear-gradient(135deg, #b8400e 0%, #d4743a 55%, #c0501a 100%)",

  // ── Brand accents ──
  "--color-gold": "#c9920a",
  "--color-teal": "#1e6b5f",
  "--color-peacock-blue": "#1a4d6e",

  // ── Typography — font families ──
  "--font-body": "'Poppins', sans-serif",
  "--font-display": "'Yatra One', 'Poppins', sans-serif",
  "--font-heading": "'Yatra One', 'Poppins', sans-serif", /* alias for compat */
  "--font-ui": "'Poppins', sans-serif",

  // ── Typography — size scale (standard, comfortable sizes) ──
  "--text-xs":   "0.85rem",    /*  ~13.6px — labels, badges, chips   */
  "--text-sm":   "0.95rem",    /*  ~15.2px — secondary text           */
  "--text-base": "1rem",       /*   16px   — body copy (browser std)  */
  "--text-md":   "1.125rem",   /*  ~18px   — card titles, subtitles  */
  "--text-lg":   "1.35rem",    /*  ~21.6px — section headings         */
  "--text-xl":   "1.75rem",    /*   28px   — page headings            */

  // ── Typography — line heights ──
  "--leading-tight":   "1.2",
  "--leading-snug":    "1.35",
  "--leading-normal":  "1.6",
  "--leading-relaxed": "1.75",

  // ── Radii ──
  "--radius-sm": "6px",
  "--radius-md": "12px",
  "--radius-lg": "18px",
  "--radius-xl": "26px",
  "--radius-full": "9999px",

  // ── Shadows (glass-friendly) ──
  "--shadow-card":
    "0 4px 20px rgba(44,20,10,0.14), 0 0 0 1px rgba(196,142,84,0.22), 0 1px 0 rgba(255,255,255,0.50) inset",
  "--shadow-card-hover":
    "0 10px 36px rgba(192,80,26,0.22), 0 0 0 1px rgba(196,142,84,0.35)",
  "--shadow-nav":
    "0 -4px 24px rgba(44,20,10,0.15), 0 0 0 1px rgba(196,142,84,0.18)",
  "--shadow-button": "0 4px 18px rgba(192,80,26,0.38)",

  // ── Spacing ──
  "--space-xs": "4px",
  "--space-sm": "8px",
  "--space-md": "16px",
  "--space-lg": "24px",
  "--space-xl": "32px",
};

export default theme;
