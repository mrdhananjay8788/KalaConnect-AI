// app/cart/page.js — Route: /cart

import CartScreen from "@/screens/CartScreen";

export const metadata = {
  title: "Your Cart | Artisan Market",
  description: "Review your selected handmade products and proceed to checkout.",
};

export default function CartPage() {
  return <CartScreen />;
}
