// app/layout.js
// Root layout: injects CSS variables, wraps the app in CartProvider, renders BottomNav.

import "./globals.css";
import { CartProvider } from "@/context/CartContext";
import BottomNav from "@/components/BottomNav";
import { cssVariables } from "@/styles/theme";

export const metadata = {
  title: "Artisan Market — Customer Dashboard",
  description:
    "Discover and shop authentic handmade products from skilled artisans across India. Bamboo baskets, pottery, paintings, sarees, wooden crafts, and more.",
};

// Convert the cssVariables object to an inline style string for :root injection
function buildCSSVariableString(vars) {
  return Object.entries(vars)
    .map(([key, val]) => `${key}: ${val}`)
    .join("; ");
}

export default function RootLayout({ children }) {
  const cssVarString = buildCSSVariableString(cssVariables);

  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        {/* Inject CSS custom properties at :root */}
        <style>{`:root { ${cssVarString} }`}</style>
      </head>
      <body>
        <CartProvider>
          <main className="page-content">
            {children}
          </main>
          <BottomNav />
        </CartProvider>
      </body>
    </html>
  );
}
