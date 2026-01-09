<template>
  <div class="shop-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">{{ $t('productsPage.title') }}</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" :current-route="currentRoute" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <div class="header-content">
            <div>
              <h1 class="page-title">{{ $t('productsPage.title') }}</h1>
              <p class="page-subtitle">{{ $t('productsPage.subtitle') }}</p>
            </div>

            <div class="header-actions">
              <div class="search-sort-bar">
                <div class="search-input-wrapper">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                    class="search-icon">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                  </svg>
                  <input v-model="searchQuery" type="text" :placeholder="$t('productsPage.searchPlaceholder')"
                    class="search-input" />
                </div>

                <select v-model="sortOption" class="sort-select">
                  <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>

              <NuxtLink :to="`/shop/${shopSlug}/admin/products/new`" class="btn btn-primary">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span class="btn-text">{{ $t('productsPage.titleNew') }}</span>
              </NuxtLink>
            </div>
          </div>
        </div>

        <div class="admin-content">
          <div v-if="!products || products.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
            </div>
            <h3>{{ $t('productsPage.emptyTitle') }}</h3>
            <p>{{ $t('productsPage.emptyDesc') }}</p>
            <NuxtLink :to="`/shop/${shopSlug}/admin/products/new`" class="btn btn-primary">{{
              $t('productsPage.titleNew') }}</NuxtLink>
          </div>

          <div v-else class="products-grid">
            <div v-for="product in products" :key="product.id" class="product-card">
              <div class="product-image">
                <img :src="product.image_url" :alt="product.name" />
                <div class="product-actions">
                  <NuxtLink :to="`/shop/${shopSlug}/admin/products/edit/${product.id}`" class="btn-action btn-edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </NuxtLink>
                  <button @click="deleteProduct(product.id)" class="btn-action btn-delete">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="product-info">
                <div class="product-category">{{ product.category }}</div>
                <h3 class="product-name">{{ getProductName(product) }}</h3>
                <div class="product-brand">{{ product.brand }}</div>
                <div class="product-footer">
                  <div class="product-price">{{ formatPrice(product.price) }}</div>
                  <div class="product-meta">
                    <div class="product-sold" v-if="product.sold_count > 0">
                      🔥 {{ product.sold_count }} {{ $t('productsPage.sold') }}
                    </div>
                    <div class="product-stock" :class="{ 'out-of-stock': product.stock === 0 }">
                      {{ product.stock > 0 ? `${product.stock} ${$t('productsPage.inStock')}` :
                        $t('productsPage.outOfStock') }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useDebounceFn } from '@vueuse/core'

definePageMeta({
  middleware: ['auth', 'shop-owner']
})

const route = useRoute()
const shopSlug = route.params.slug
const { token, logout } = useAuth()
const { t, locale } = useI18n()
const { formatPrice } = useCurrency()

const sidebarOpen = ref(false)
const currentRoute = computed(() => 'products')

// Helper to get localized name
const getProductName = (product) => {
  if (!product) return ''
  const currentLocale = locale.value
  return product[`name_${currentLocale}`] || product.name_en || product.name_ru || product.name_uz || ''
}

// Filters
const searchQuery = ref('')
const debouncedSearch = ref('')
const sortOption = ref('newest')

// Debounce search input to avoid too many API calls
watch(searchQuery, useDebounceFn((newVal) => {
  debouncedSearch.value = newVal
}, 500))

const sortOptions = computed(() => [
  { value: 'newest', label: t('productsPage.sort.newest'), by: 'created_at', order: 'desc' },
  { value: 'oldest', label: t('productsPage.sort.oldest'), by: 'created_at', order: 'asc' },
  { value: 'priceLow', label: t('productsPage.sort.priceLow'), by: 'price', order: 'asc' },
  { value: 'priceHigh', label: t('productsPage.sort.priceHigh'), by: 'price', order: 'desc' },
  { value: 'nameAz', label: t('productsPage.sort.nameAz'), by: 'name', order: 'asc' },
  { value: 'nameZa', label: t('productsPage.sort.nameZa'), by: 'name', order: 'desc' },
  { value: 'soldHigh', label: t('productsPage.sort.soldHigh'), by: 'sold_count', order: 'desc' },
  { value: 'stockLow', label: t('productsPage.sort.stockLow'), by: 'stock', order: 'asc' },
])

const currentSort = computed(() => sortOptions.value.find(o => o.value === sortOption.value) || sortOptions.value[0])

const queryParams = computed(() => {
  return {
    shop_slug: shopSlug,
    q: debouncedSearch.value || undefined,
    sort_by: currentSort.value.by,
    sort_order: currentSort.value.order
  }
})

const { data: products, error, refresh } = await useFetch(useRuntimeConfig().public.apiBase + '/products', {
  server: false,
  lazy: true,
  query: queryParams,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

watch(error, (newError) => {
  if (newError) {
    console.error('[Products List] Error loading products:', newError)
  }
})

const deleteProduct = async (id) => {
  if (!confirm(t('productsPage.deleteConfirm'))) return
  try {
    await $fetch(`${useRuntimeConfig().public.apiBase}/products/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    refresh()
    useToast().success(t('alerts.shop.productDeleted'))
  } catch (e) {
    console.error('[Products List] Error deleting:', e)
    useToast().error(e.data?.detail || e.message || t('alerts.shop.deleteError'))
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

/* Sidebar styles handled by ShopAdminSidebar component */

/* Mobile Header */
.mobile-header {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
  z-index: 1000;
}

.menu-btn,
.home-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  color: #111;
  transition: all 0.2s;
}

.menu-btn:hover,
.home-btn:hover {
  background: #111;
  color: white;
}

.mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
  padding: 40px;
  background: #fafafa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  /* Align bottom to match buttons */
  gap: 24px;
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-sort-bar {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input-wrapper {
  position: relative;
  width: 320px;
  /* Slightly wider */
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9CA3AF;
  width: 18px;
  height: 18px;
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 48px;
  /* Taller inputs */
  padding: 0 16px 0 42px;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.2s;
  background: white;
  color: #111;
}

.search-input:focus {
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.search-input::placeholder {
  color: #9CA3AF;
}

.sort-select {
  height: 48px;
  /* Match height */
  padding: 0 40px 0 16px;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.95rem;
  /* Match font size */
  font-weight: 500;
  outline: none;
  cursor: pointer;
  background-color: white;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 12 12' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M2.5 4.5L6 8L9.5 4.5' stroke='%23111111' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  color: #111;
  min-width: 200px;
  /* Wider select */
  transition: all 0.2s;
}

.sort-select:hover {
  border-color: #D1D5DB;
}

.sort-select:focus {
  border-color: #111;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.95rem;
  color: #6B7280;
  margin: 0;
}

.admin-content {
  padding: 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 24px;
  height: 48px;
  /* Match height */
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #000;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  border: 1px dashed #E5E7EB;
}

.empty-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  color: #D1D5DB;
}

.empty-icon svg {
  width: 64px;
  height: 64px;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.empty-state p {
  color: #6B7280;
  margin-bottom: 24px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  /* Wider cards */
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  border: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06);
  border-color: #e5e7eb;
}

.product-image {
  position: relative;
  background: #F8F9FA;
  aspect-ratio: 4/3;
  /* Better aspect ratio */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transform: translateY(-5px);
  transition: all 0.2s ease;
}

.product-card:hover .product-actions {
  opacity: 1;
  transform: translateY(0);
}

.btn-action {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn-edit {
  color: #3B82F6;
}

.btn-edit:hover {
  background: #3B82F6;
  color: white;
}

.btn-delete {
  color: #EF4444;
}

.btn-delete:hover {
  background: #EF4444;
  color: white;
}

.product-info {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-category {
  font-size: 0.7rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 4px;
  line-height: 1.35;

  /* Truncate nicely */
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-brand {
  font-size: 0.85rem;
  color: #6B7280;
  margin-bottom: 16px;
}

.product-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 16px;
  border-top: 1px solid #F3F4F6;
}

.product-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.product-sold {
  font-size: 0.7rem;
  font-weight: 700;
  color: #D97706;
  background: #FFFBEB;
  padding: 3px 8px;
  border-radius: 6px;
}

.product-price {
  font-size: 1.25rem;
  /* Larger price */
  font-weight: 800;
  color: #111;
  letter-spacing: -0.02em;
}

.product-stock {
  font-size: 0.75rem;
  font-weight: 600;
  color: #059669;
  background: #ECFDF5;
  padding: 4px 8px;
  border-radius: 6px;
}

.product-stock.out-of-stock {
  color: #DC2626;
  background: #FEF2F2;
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }

  /* Hide large title/subtitle on mobile since we have the Mobile Header */
  .page-title,
  .page-subtitle {
    display: none;
  }

  .admin-main {
    margin-left: 0;
    padding: 60px 0 0 0;
    width: 100%;
    min-width: 0;
  }

  .container {
    padding: 0;
  }

  .page-header {
    padding: 16px 20px;
    margin-bottom: 20px;
    background: white;
    border-bottom: 1px solid #eee;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .header-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .search-sort-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input-wrapper,
  .sort-select {
    width: 100%;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    padding: 0 16px 20px 16px;
  }

  .product-image {
    padding: 12px;
  }

  .product-actions {
    opacity: 1;
    transform: none;
    top: 8px;
    right: 8px;
  }

  .btn-action {
    width: 32px;
    height: 32px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .product-info {
    padding: 12px;
  }

  .product-name {
    font-size: 0.95rem;
  }

  .product-price {
    font-size: 1rem;
  }
}
</style>
