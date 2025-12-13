<template>
  <div class="shop-page">
    <AppHeader />
    
    <main class="container py-8">
      <!-- Shop Name -->
      <div v-if="shop" class="shop-header mb-8">
        <h1 class="shop-name">{{ shop.name }}</h1>
        <p v-if="shop.description" class="shop-description">{{ shop.description }}</p>
      </div>
      
      <!-- Hero Section -->
      <div v-if="banner" class="hero-card mb-8">
        <div class="hero-content">
          <div class="badge">{{ banner.badge_text }}</div>
          <h1 class="hero-title" v-html="banner.title.replace(/\\n/g, '<br/>')"></h1>
          <p class="hero-price">{{ banner.subtitle }}</p>
          <NuxtLink :to="`/${shopSlug}/products`" class="hero-btn">{{ banner.button_text }}</NuxtLink>
        </div>
        <div class="hero-image">
          <img :src="banner.image_url" alt="Banner" />
        </div>
      </div>

      <!-- Brand Filters -->
      <section class="mb-8">
        <div class="section-header">
          <h2 class="section-title">Brendlar</h2>
          <NuxtLink :to="`/${shopSlug}/products`" class="view-all-btn">
            Hammasi
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </NuxtLink>
        </div>
        <div class="brand-grid">
          <NuxtLink 
            v-for="brand in brands" 
            :key="brand.id"
            :to="`/${shopSlug}/products?brand=${brand.name}`"
            class="brand-card"
          >
            <div class="brand-logo-wrapper">
              <img :src="brand.logo_url" :alt="brand.name" class="brand-logo-img" />
            </div>
            <span class="brand-name-text">{{ brand.name }}</span>
          </NuxtLink>
        </div>
      </section>

      <!-- Featured Products -->
      <section class="mb-8">
        <div class="section-header">
          <h2 class="section-title">Tavsiya etilgan mahsulotlar</h2>
          <NuxtLink :to="`/${shopSlug}/products`" class="view-all-btn">
            Hammasi
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </NuxtLink>
        </div>
        <div v-if="pending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Mahsulotlar yuklanmoqda...</p>
        </div>
        <div v-else class="products-grid">
          <ProductCard v-for="product in featuredProducts" :key="product.id" :product="product" :shop-slug="shopSlug" />
        </div>
        
        <!-- View All Products Button -->
        <div class="view-all-section">
          <NuxtLink :to="`/${shopSlug}/products`" class="view-all-products-btn">
            <span>Barcha mahsulotlarni ko'rish</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </NuxtLink>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()
const shopSlug = route.params.shop

const { data: shop } = await useFetch(`http://localhost:8000/platform/shops/${shopSlug}`, { server: false })
const { data: banner } = await useFetch(`http://localhost:8000/banner?shop_slug=${shopSlug}`, { server: false })
const { data: brands } = await useFetch(`http://localhost:8000/brands?shop_slug=${shopSlug}`, { server: false })
const { data: products, pending } = await useFetch(`http://localhost:8000/products?shop_slug=${shopSlug}`, {
  server: false
})

// Show only 4 featured products
const featuredProducts = computed(() => {
  if (!products.value) return []
  return products.value.slice(0, 4)
})
</script>

<style scoped>
.shop-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.shop-header {
  text-align: center;
  padding: 32px 20px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.shop-name {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 12px;
  letter-spacing: -0.5px;
}

.shop-description {
  font-size: 1.125rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.6;
}

.hero-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 32px;
  padding: 48px;
  color: white;
  position: relative;
  overflow: hidden;
  min-height: 400px;
  display: flex;
  align-items: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.hero-content {
  z-index: 2;
  max-width: 500px;
}

.badge {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 20px;
  border: 1px solid rgba(255,255,255,0.2);
  letter-spacing: 1px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 16px;
  letter-spacing: -1px;
}

.hero-price {
  font-size: 1.25rem;
  font-weight: 500;
  opacity: 0.9;
  margin-bottom: 32px;
}

.hero-btn {
  display: inline-block;
  background: white;
  color: #111;
  padding: 16px 40px;
  border-radius: 50px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255,255,255,0.2);
  text-decoration: none;
}

.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255,255,255,0.3);
}

.hero-image {
  position: absolute;
  right: -50px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 50%;
  height: 120%;
  opacity: 0.3;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  letter-spacing: -0.5px;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  text-decoration: none;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: #111;
  border-color: #111;
  color: white;
  transform: translateX(4px);
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

.brand-card {
  background: white;
  border: 2px solid #f0f0f0;
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #111;
}

.brand-card:hover {
  border-color: #111;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.brand-logo-wrapper {
  width: 80px;
  height: 80px;
  background: #f9f9f9;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.brand-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-name-text {
  font-weight: 700;
  font-size: 0.95rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.view-all-section {
  margin-top: 32px;
  text-align: center;
}

.view-all-products-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 18px 40px;
  background: #111;
  color: white;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.view-all-products-btn:hover {
  background: #000;
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .shop-header {
    padding: 24px 16px;
    border-radius: 16px;
  }
  
  .shop-name {
    font-size: 1.75rem;
  }
  
  .shop-description {
    font-size: 1rem;
  }
  
  .hero-card {
    padding: 32px 24px;
    min-height: 280px;
    border-radius: 24px;
  }
  
  .hero-title {
    font-size: 1.75rem;
  }
  
  .hero-price {
    font-size: 1rem;
    margin-bottom: 24px;
  }
  
  .hero-btn {
    padding: 14px 28px;
    font-size: 0.875rem;
  }
  
  .hero-image {
    opacity: 0.15;
    width: 70%;
  }
  
  .brand-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .brand-card {
    padding: 16px;
    border-radius: 16px;
  }
  
  .brand-logo-wrapper {
    width: 60px;
    height: 60px;
    padding: 12px;
  }
  
  .brand-name-text {
    font-size: 0.8rem;
  }
  
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .section-header {
    margin-bottom: 16px;
  }
  
  .view-all-btn {
    padding: 8px 14px;
    font-size: 0.75rem;
  }
  
  .view-all-products-btn {
    padding: 16px 32px;
    font-size: 0.875rem;
  }
}

@media (min-width: 1024px) {
  .hero-image {
    opacity: 0.5;
  }
  
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
}
</style>

