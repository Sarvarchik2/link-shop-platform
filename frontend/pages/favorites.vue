<template>
  <div class="favorites-page">
    <AppHeader />
    
    <main class="container py-8">
      <div class="page-header">
        <h1 class="page-title">Sevimlilar</h1>
        <p class="page-subtitle">Sizning sevimli mahsulotlaringiz</p>
      </div>

      <div v-if="pending" class="loading-state">
        <div class="spinner"></div>
        <p>Yuklanmoqda...</p>
      </div>

      <div v-else-if="favoriteProducts.length === 0" class="empty-state">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
        <h2>Sevimlilar ro'yxati bo'sh</h2>
        <p>Yoqtirgan mahsulotlaringizni qo'shing!</p>
        <NuxtLink to="/" class="btn-explore">Mahsulotlarni ko'rish</NuxtLink>
      </div>

      <div v-else class="products-grid">
        <ProductCard 
          v-for="product in favoriteProducts" 
          :key="product.id" 
          :product="product"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { data: products, pending, refresh } = await useFetch('http://localhost:8000/products', {
  server: false
})

const favoriteProducts = computed(() => {
  return products.value?.filter(p => p.is_favorite) || []
})

// Refresh every 2 seconds to update favorites
const refreshInterval = setInterval(() => {
  refresh()
}, 2000)

onUnmounted(() => {
  clearInterval(refreshInterval)
})
</script>

<style scoped>
.favorites-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.page-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
  color: #6B7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  max-width: 400px;
  margin: 0 auto;
}

.empty-state svg {
  color: #E5E7EB;
  margin: 0 auto 24px;
}

.empty-state h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 8px 0;
}

.empty-state p {
  color: #6B7280;
  margin: 0 0 24px 0;
}

.btn-explore {
  display: inline-block;
  padding: 14px 28px;
  background: #111;
  color: white;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-explore:hover {
  background: #000;
  transform: translateY(-2px);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
  }
}
</style>
