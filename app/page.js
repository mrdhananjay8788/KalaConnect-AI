// app/page.js — Route: /
// Browse / Home screen

import BrowseScreen from "@/screens/BrowseScreen";

export const metadata = {
  title: "Browse Products | Artisan Market",
  description:
    "Explore handmade bamboo baskets, pottery, paintings, silk sarees, wooden crafts and more from skilled artisans across India.",
};

export default function HomePage() {
  // customerName defaults to "Guest". Replace with session/prop from login when integrated.
  return <BrowseScreen customerName="Guest" />;
}
