<template>
  <div class="products-page">
    <AppHeader />

    <main class="container py-8">
      <div class="page-header">
        <h1 class="page-title">{{ $t('store.productsTitle') }}</h1>
        <div class="filters">
          <!-- Custom Category Dropdown -->
          <div class="custom-dropdown" v-click-outside="() => showCategoryDropdown = false">
            <button class="dropdown-trigger" @click="showCategoryDropdown = !showCategoryDropdown"
              :class="{ 'active': showCategoryDropdown, 'has-selection': selectedCategory }">
              <span class="selected-value">{{ selectedCategory || $t('store.allCategories') }}</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                class="chevron">
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>
            <Transition name="dropdown">
              <div v-if="showCategoryDropdown" class="dropdown-menu">
                <div class="dropdown-item" :class="{ 'active': !selectedCategory }" @click="selectCategory('')">
                  <span class="item-text">{{ $t('store.allCategories') }}</span>
                  <svg v-if="!selectedCategory" width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="3">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
                <div v-for="cat in categories" :key="cat.id" class="dropdown-item"
                  :class="{ 'active': selectedCategory === getField(cat, 'name') }"
                  @click="selectCategory(getField(cat, 'name'))">
                  <span class="item-text">{{ getField(cat, 'name') }}</span>
                  <svg v-if="selectedCategory === getField(cat, 'name')" width="18" height="18" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="3">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              </div>
            </Transition>
          </div>

          <!-- Custom Brand Dropdown -->
          <div class="custom-dropdown" v-click-outside="() => showBrandDropdown = false">
            <button class="dropdown-trigger" @click="showBrandDropdown = !showBrandDropdown"
              :class="{ 'active': showBrandDropdown, 'has-selection': selectedBrand }">
              <span class="selected-value">{{ selectedBrand || $t('store.allBrands') }}</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                class="chevron">
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>
            <Transition name="dropdown">
              <div v-if="showBrandDropdown" class="dropdown-menu">
                <div class="dropdown-item" :class="{ 'active': !selectedBrand }" @click="selectBrand('')">
                  <span class="item-text">{{ $t('store.allBrands') }}</span>
                  <svg v-if="!selectedBrand" width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="3">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
                <div v-for="brand in brands" :key="brand.id" class="dropdown-item"
                  :class="{ 'active': selectedBrand === getField(brand, 'name') }"
                  @click="selectBrand(getField(brand, 'name'))">
                  <span class="item-text">{{ getField(brand, 'name') }}</span>
                  <svg v-if="selectedBrand === getField(brand, 'name')" width="18" height="18" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="3">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>

      <div v-if="pending" class="text-center py-12 text-gray-400">
        <div class="loading-spinner"></div>
        <p class="mt-4">{{ $t('store.loadingProducts') }}</p>
      </div>

      <div v-else-if="filteredProducts.length > 0" class="products-grid">
        <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" :shop-slug="shopSlug" />
      </div>

      <div v-else class="text-center py-12 text-gray-400">
        <p>{{ $t('store.noProducts') }}</p>
      </div>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()
const shopSlug = route.params.shop
const config = useRuntimeConfig()
const { t } = useI18n()
const { getField } = useMultilingual()

const selectedCategory = ref('')
const selectedBrand = ref('')
const showCategoryDropdown = ref(false)
const showBrandDropdown = ref(false)

const selectCategory = (cat) => {
  selectedCategory.value = cat
  showCategoryDropdown.value = false
}

const selectBrand = (brand) => {
  selectedBrand.value = brand
  showBrandDropdown.value = false
}

// SEO
useHead({
  title: t('store.productsTitle'),
})

const { data: categories } = await useFetch(`${config.public.apiBase}/categories?shop_slug=${shopSlug}`)
const { data: brands } = await useFetch(`${config.public.apiBase}/brands?shop_slug=${shopSlug}`)
const { data: products, pending } = await useFetch(`${config.public.apiBase}/products?shop_slug=${shopSlug}`)

// Directive to close dropdown when clicking outside
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
}

const filteredProducts = computed(() => {
  if (!products.value) return []
  let filtered = products.value

  if (selectedCategory.value) {
    filtered = filtered.filter(p => {
      const productCategory = getField(p, 'category')
      return productCategory === selectedCategory.value
    })
  }

  if (selectedBrand.value) {
    filtered = filtered.filter(p => {
      const productBrand = getField(p, 'brand')
      return productBrand === selectedBrand.value
    })
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
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 32px;
  color: #111;
  letter-spacing: -0.02em;
}

.filters {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

/* Custom Dropdown Styles */
.custom-dropdown {
  position: relative;
  min-width: 220px;
}

.dropdown-trigger {
  width: 100%;
  height: 52px;
  padding: 0 20px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  color: #6B7280;
  font-size: 0.9375rem;
}

.dropdown-trigger:hover {
  border-color: #111;
  color: #111;
}

.dropdown-trigger.active {
  border-color: #111;
  color: #111;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

.dropdown-trigger.has-selection {
  border-color: #111;
  color: #111;
}

.selected-value {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 12px;
}

.chevron {
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.dropdown-trigger.active .chevron {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(229, 231, 235, 0.5);
  border-radius: 18px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -6px rgba(0, 0, 0, 0.04);
  padding: 8px;
  z-index: 100;
  max-height: 300px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.dropdown-item {
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9375rem;
  color: #4B5563;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.dropdown-item:hover {
  background: #F3F4F6;
  color: #111;
}

.dropdown-item.active {
  background: #111;
  color: white;
}

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease-out;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
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
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .custom-dropdown {
    min-width: 100%;
  }

  .page-title {
    font-size: 1.75rem;
  }
}

@media (min-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
}
</style>
