// services/productService.js
// This is the ONLY file permitted to import mockProducts.
// All screens and components must call getProducts() from this file.
// To switch to a real API: replace the body of getProducts() only — no other files need to change.

import mockProducts from "@/data/mockProducts";

/**
 * Returns the full list of products.
 * Simulates an async API call with a small delay.
 * @returns {Promise<Array>}
 */
export async function getProducts() {
  // Simulate network latency (remove this line when wiring up a real API)
  await new Promise((resolve) => setTimeout(resolve, 800));
  return mockProducts;
}

/**
 * Returns a single product by ID, or null if not found.
 * @param {number|string} id
 * @returns {Promise<Object|null>}
 */
export async function getProductById(id) {
  await new Promise((resolve) => setTimeout(resolve, 400));
  const numId = Number(id);
  return mockProducts.find((p) => p.id === numId) ?? null;
}

/**
 * Returns products matching a category string (case-insensitive).
 * @param {string} category
 * @returns {Promise<Array>}
 */
export async function getProductsByCategory(category) {
  await new Promise((resolve) => setTimeout(resolve, 400));
  if (!category || category.toLowerCase() === "all") return mockProducts;
  return mockProducts.filter(
    (p) => p.category.toLowerCase() === category.toLowerCase()
  );
}

/**
 * Returns products that share the same category or have overlapping tags,
 * excluding the product with the given id.
 * @param {number} id - ID of the product to exclude
 * @param {string} category
 * @param {string[]} tags
 * @returns {Promise<Array>}
 */
export async function getRelatedProducts(id, category, tags = []) {
  await new Promise((resolve) => setTimeout(resolve, 200));
  return mockProducts
    .filter((p) => {
      if (p.id === Number(id)) return false;
      const sameCategory = p.category === category;
      const hasOverlapTag = tags.some((t) => p.tags.includes(t));
      return sameCategory || hasOverlapTag;
    })
    .slice(0, 3);
}
