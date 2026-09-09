// app/categories/page.js — Route: /categories
// Redirects to Browse screen. The BottomNav "Categories" tab lands here.
// Reuses BrowseScreen — category chips are the primary filter UI.

import BrowseScreen from "@/screens/BrowseScreen";

export const metadata = {
  title: "Categories | Artisan Market",
  description: "Browse all product categories — pottery, paintings, sarees, wooden crafts, and more.",
};

export default function CategoriesPage() {
  return <BrowseScreen customerName="Guest" />;
}
