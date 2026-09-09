// data/mockProducts.js
// ⚠️  DO NOT import this file from any screen or component.
// All product data must be accessed ONLY via getProducts() in services/productService.js

const mockProducts = [
  {
    id: 1,
    name: "Handwoven Bamboo Basket",
    category: "Home Decor",
    material: "Bamboo",
    description:
      "A hand-woven bamboo basket crafted using centuries-old weaving techniques. Eco-friendly, sturdy, and perfect for storage or display. Each basket is unique — no two are exactly alike.",
    price: 450,
    image: "/product_basket.jpg",
    tags: ["eco-friendly", "handmade", "storage", "natural"],
    recommendedBuyers: ["Home Decor Stores", "Eco-friendly Retailers", "Gift Shops"],
    artisanName: "Ramesh Patil",
    artisanRegion: "Maharashtra",
    artisanBio:
      "Weaving bamboo baskets for over 15 years using traditional techniques passed down through his family. Ramesh sources all bamboo locally from the forests near his village.",
  },
  {
    id: 2,
    name: "Blue Pottery Vase",
    category: "Pottery",
    material: "Clay",
    description:
      "An exquisite blue pottery vase hand-painted with traditional Rajasthani floral motifs. Fired using a centuries-old low-temperature process that preserves the vibrant blue glaze.",
    price: 780,
    image: "/product_vase.jpg",
    tags: ["ceramic", "handmade", "decorative", "traditional"],
    recommendedBuyers: ["Handicraft Boutiques", "Interior Designers", "Museum Gift Shops"],
    artisanName: "Fatima Begum",
    artisanRegion: "Rajasthan",
    artisanBio:
      "Fatima is a third-generation blue pottery artisan from Jaipur. She learned the craft from her mother at age 10 and now trains young women in her community.",
  },
  {
    id: 3,
    name: "Madhubani Painting",
    category: "Paintings",
    material: "Handmade Paper",
    description:
      "A vibrant Madhubani painting depicting scenes from Indian mythology. Drawn with natural pigments and fine bamboo sticks. Comes mounted on archival handmade paper.",
    price: 1200,
    image: "/product_madhubani.jpg",
    tags: ["art", "folk", "mythological", "wall-art"],
    recommendedBuyers: ["Art Galleries", "Corporate Gift Buyers", "Cultural Centers"],
    artisanName: "Sushma Devi",
    artisanRegion: "Bihar",
    artisanBio:
      "Sushma has been painting Madhubani art for 20 years. Her work has been exhibited in Delhi, Mumbai, and at the Crafts Museum. She teaches the art form to girls in her village.",
  },
  {
    id: 4,
    name: "Banarasi Silk Saree",
    category: "Sarees",
    material: "Silk",
    description:
      "An elegant Banarasi silk saree with intricate gold zari work woven directly into the fabric. Each saree takes 15–20 days to complete on a traditional handloom.",
    price: 4500,
    image: "/product_saree.jpg",
    tags: ["silk", "handloom", "bridal", "luxury"],
    recommendedBuyers: ["Ethnic Wear Retailers", "Bridal Boutiques", "Fashion Exporters"],
    artisanName: "Mohammad Salim",
    artisanRegion: "Uttar Pradesh",
    artisanBio:
      "A master weaver from Varanasi with 25 years of experience. Mohammad's family has been weaving Banarasi silk for four generations. He employs six weavers from his neighbourhood.",
  },
  {
    id: 5,
    name: "Carved Sandalwood Box",
    category: "Wooden Craft",
    material: "Sandalwood",
    description:
      "A beautifully hand-carved sandalwood jewellery box with floral and peacock motifs. Retains its natural fragrance for years. Perfect as a keepsake or gift.",
    price: 1850,
    image: "/product_wooden_box.jpg",
    tags: ["wooden", "handcarved", "fragrant", "gift"],
    recommendedBuyers: ["Luxury Gift Shops", "Jewellery Stores", "Souvenir Retailers"],
    artisanName: "Gopalaiah",
    artisanRegion: "Karnataka",
    artisanBio:
      "Gopalaiah is a sandalwood carving master from Mysore with 30 years of experience. He carves each box entirely by hand using traditional chisels.",
  },
  {
    id: 6,
    name: "Handcrafted Jute Tote Bag",
    category: "Jute Bags",
    material: "Jute",
    description:
      "A sturdy, eco-friendly jute tote bag with hand-embroidered traditional motifs. Spacious, durable, and biodegradable — the sustainable alternative to plastic bags.",
    price: 320,
    image: "/product_jute_bag.jpg",
    tags: ["eco-friendly", "jute", "embroidered", "sustainable"],
    recommendedBuyers: ["Eco-friendly Retailers", "Grocery Chains", "Corporate Gifting"],
    artisanName: "Anita Mondal",
    artisanRegion: "West Bengal",
    artisanBio:
      "Anita runs a small self-help group of 12 women artisans who hand-embroider jute bags. Her group has won two state-level awards for promoting sustainable craftsmanship.",
  },
];

export default mockProducts;
