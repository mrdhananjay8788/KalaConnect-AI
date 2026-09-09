// app/product/[id]/page.js — Route: /product/:id
// Product Detail screen

import ProductDetailScreen from "@/screens/ProductDetailScreen";

export const metadata = {
  title: "Product Details | Artisan Market",
  description: "View full details, artisan story, and buyer recommendations for this handmade product.",
};

export default async function ProductDetailPage({ params }) {
  const resolvedParams = await params;
  return <ProductDetailScreen productId={resolvedParams.id} />;
}
