<template>
  <div class="products-page">
    <AppHeader />
    
    <main class="products-container">
      <!-- Header with title and filter toggle -->
      <div class="page-header">
        <h1 class="page-title">Barcha mahsulotlar</h1>
        <button class="filter-toggle-btn" @click="showFilters = !showFilters">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="4" y1="21" x2="4" y2="14"></line>
            <line x1="4" y1="10" x2="4" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12" y2="3"></line>
            <line x1="20" y1="21" x2="20" y2="16"></line>
            <line x1="20" y1="12" x2="20" y2="3"></line>
          </svg>
          <span>Filtrlar</span>
          <span v-if="activeFiltersCount > 0" class="filter-count">{{ activeFiltersCount }}</span>
        </button>
      </div>

      <!-- Filters Panel -->
      <Transition name="slide">
        <div v-if="showFilters" class="filters-panel">
          <!-- Brands Filter -->
          <div class="filter-section">
            <h3 class="filter-title">Brendlar</h3>
            <div class="filter-chips">
              <button
                v-for="brand in brands"
                :key="brand.id"
                class="filter-chip"
                :class="{ active: selectedBrands.includes(brand.name) }"
                @click="toggleBrand(brand.name)"
              >
                {{ brand.name }}
              </button>
            </div>
          </div>

          <!-- Categories Filter -->
          <div class="filter-section">
            <h3 class="filter-title">Kategoriyalar</h3>
            <div class="filter-chips">
              <button
                v-for="category in categories"
                :key="category.id"
                class="filter-chip"
                :class="{ active: selectedCategories.includes(category.name) }"
                @click="toggleCategory(category.name)"
              >
                {{ category.name }}
              </button>
            </div>
          </div>

          <!-- Clear Filters -->
          <div class="filter-actions" v-if="activeFiltersCount > 0">
            <button class="clear-filters-btn" @click="clearFilters">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              Barcha filtrlarni tozalash
            </button>
          </div>
        </div>
      </Transition>

      <!-- Active Filters Tags -->
      <div v-if="activeFiltersCount > 0 && !showFilters" class="active-filters">
        <span
          v-for="brand in selectedBrands"
          :key="`brand-${brand}`"
          class="active-filter-tag"
        >
          {{ brand }}
          <button @click="toggleBrand(brand)" class="remove-tag">×</button>
        </span>
        <span
          v-for="category in selectedCategories"
          :key="`cat-${category}`"
          class="active-filter-tag category-tag"
        >
          {{ category }}
          <button @click="toggleCategory(category)" class="remove-tag">×</button>
        </span>
      </div>

      <!-- Products Count -->
      <div class="products-info">
        <span class="products-count">{{ filteredProducts.length }} ta mahsulot</span>
      </div>
      
      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">Mahsulotlar yuklanmoqda...</p>
      </div>
      
      <div v-else-if="filteredProducts.length === 0" class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>Mahsulotlar topilmadi</h3>
        <p>Filtrlarni o'zgartirib ko'ring</p>
        <button class="clear-filters-btn" @click="clearFilters">Filtrlarni tozalash</button>
      </div>
      
      <div v-else class="products-grid">
        <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" />
      </div>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()

const showFilters = ref(false)
const selectedBrands = ref([])
const selectedCategories = ref([])

// Fetch data
const { data: products, pending } = await useFetch('http://localhost:8000/products', {
  server: false
})

const { data: brands } = await useFetch('http://localhost:8000/brands', { server: false })
const { data: categories } = await useFetch('http://localhost:8000/categories', { server: false })

// Check for brand filter in URL query
watch(() => route.query.brand, (newBrand) => {
  if (newBrand) {
    selectedBrands.value = [newBrand]
    showFilters.value = true
  }
}, { immediate: true })

// Filter toggle functions
const toggleBrand = (brand) => {
  const index = selectedBrands.value.indexOf(brand)
  if (index > -1) {
    selectedBrands.value.splice(index, 1)
  } else {
    selectedBrands.value.push(brand)
  }
}

const toggleCategory = (category) => {
  const index = selectedCategories.value.indexOf(category)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(category)
  }
}

const clearFilters = () => {
  selectedBrands.value = []
  selectedCategories.value = []
}

// Computed
const activeFiltersCount = computed(() => {
  return selectedBrands.value.length + selectedCategories.value.length
})

const filteredProducts = computed(() => {
  if (!products.value) return []
  
  let result = [...products.value]
  
  if (selectedBrands.value.length > 0) {
    result = result.filter(p => selectedBrands.value.includes(p.brand))
  }
  
  if (selectedCategories.value.length > 0) {
    result = result.filter(p => selectedCategories.value.includes(p.category))
  }
  
  return result
})
</script>

<style scoped>
.products-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.products-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

@media (max-width: 640px) {
  .products-container {
    padding: 16px;
  }
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
}

.filter-toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-toggle-btn:hover {
  border-color: #111;
  background: #111;
  color: white;
}

.filter-count {
  background: #EF4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  min-width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Filters Panel */
.filters-panel {
  background: white;
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
  border: 1px solid #E5E7EB;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.filter-section {
  margin-bottom: 20px;
}

.filter-section:last-child {
  margin-bottom: 0;
}

.filter-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip {
  padding: 10px 18px;
  border-radius: 50px;
  border: 2px solid #E5E7EB;
  background: white;
  font-size: 0.875rem;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-chip:hover {
  border-color: #111;
}

.filter-chip.active {
  background: #111;
  border-color: #111;
  color: white;
}

.filter-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #E5E7EB;
}

.clear-filters-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: #FEE2E2;
  border: none;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #EF4444;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-filters-btn:hover {
  background: #EF4444;
  color: white;
}

/* Active Filters Tags */
.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.active-filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #111;
  color: white;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
}

.active-filter-tag.category-tag {
  background: #3B82F6;
}

.remove-tag {
  background: none;
  border: none;
  color: white;
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0;
  margin-left: 2px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.remove-tag:hover {
  opacity: 1;
}

/* Products Info */
.products-info {
  margin-bottom: 16px;
}

.products-count {
  font-size: 0.875rem;
  color: #666;
  font-weight: 500;
}

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  border: 1px solid #E5E7EB;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.empty-state p {
  color: #666;
  margin-bottom: 24px;
}

/* Loading */
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

/* Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .filter-toggle-btn {
    width: 100%;
    justify-content: center;
  }
  
  .filters-panel {
    padding: 20px 16px;
  }
  
  .filter-chips {
    gap: 6px;
  }
  
  .filter-chip {
    padding: 8px 14px;
    font-size: 0.8rem;
  }
  
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}

@media (min-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
}

@media (min-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
}
</style>
