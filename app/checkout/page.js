// app/checkout/page.js — Route: /checkout

import CheckoutScreen from "@/screens/CheckoutScreen";

export const metadata = {
  title: "Checkout | Artisan Market",
  description: "Complete your order and support skilled artisans across India.",
};

export default function CheckoutPage() {
  // customerName defaults to "Guest" — replace with session data when login module is integrated
  return <CheckoutScreen customerName="Guest" />;
}
