<template>
  <div class="products-page">
    <AppHeader />
    
    <main class="container py-8">
      <div class="page-header">
        <h1 class="page-title">Mahsulotlar</h1>
        <div class="filters">
          <select v-model="selectedCategory" class="filter-select">
            <option value="">Barcha kategoriyalar</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.name">{{ cat.name }}</option>
          </select>
          <select v-model="selectedBrand" class="filter-select">
            <option value="">Barcha brendlar</option>
            <option v-for="brand in brands" :key="brand.id" :value="brand.name">{{ brand.name }}</option>
          </select>
        </div>
      </div>

      <div v-if="pending" class="text-center py-12 text-gray-400">
        <div class="loading-spinner"></div>
        <p class="mt-4">Mahsulotlar yuklanmoqda...</p>
      </div>
      
      <div v-else-if="filteredProducts.length > 0" class="products-grid">
        <ProductCard 
          v-for="product in filteredProducts" 
          :key="product.id" 
          :product="product"
          :shop-slug="shopSlug"
        />
      </div>
      
      <div v-else class="text-center py-12 text-gray-400">
        <p>Mahsulotlar topilmadi</p>
      </div>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()
const shopSlug = route.params.shop

const selectedCategory = ref('')
const selectedBrand = ref('')

const { data: categories } = await useFetch(`http://localhost:8000/categories?shop_slug=${shopSlug}`, { server: false })
const { data: brands } = await useFetch(`http://localhost:8000/brands?shop_slug=${shopSlug}`, { server: false })
const { data: products, pending } = await useFetch(`http://localhost:8000/products?shop_slug=${shopSlug}`, {
  server: false
})

const filteredProducts = computed(() => {
  if (!products.value) return []
  let filtered = products.value
  
  if (selectedCategory.value) {
    filtered = filtered.filter(p => p.category === selectedCategory.value)
  }
  
  if (selectedBrand.value) {
    filtered = filtered.filter(p => p.brand === selectedBrand.value)
  }
  
  return filtered
})
</script>

<style scoped>
.products-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 24px;
  color: #111;
}

.filters {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #111;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
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

@media (min-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
}
</style>

