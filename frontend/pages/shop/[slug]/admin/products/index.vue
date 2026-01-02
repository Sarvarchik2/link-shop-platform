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
          <div>
            <h1 class="page-title">{{ $t('productsPage.title') }}</h1>
            <p class="page-subtitle">{{ $t('productsPage.subtitle') }}</p>
          </div>
          <NuxtLink :to="`/shop/${shopSlug}/admin/products/new`" class="btn btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span class="btn-text">{{ $t('productsPage.titleNew') }}</span>
          </NuxtLink>
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
                <h3 class="product-name">{{ product.name }}</h3>
                <div class="product-brand">{{ product.brand }}</div>
                <div class="product-footer">
                  <div class="product-price">${{ product.price.toFixed(2) }}</div>
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
definePageMeta({
  middleware: ['auth', 'shop-owner']
})

const route = useRoute()
const shopSlug = route.params.slug
const { token, logout } = useAuth()
const { t } = useI18n()

const sidebarOpen = ref(false)

const currentRoute = computed(() => 'products')

const { data: products, error, refresh } = await useFetch(`http://localhost:8000/products?shop_slug=${shopSlug}`, {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

watch(error, (newError) => {
  if (newError) {
    console.error('[Products List] Ошибка загрузки товаров:', newError)
  }
})

const deleteProduct = async (id) => {
  if (!confirm(t('productsPage.deleteConfirm'))) return
  try {
    await $fetch(`http://localhost:8000/products/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    refresh()
    useToast().success(t('alerts.shop.productDeleted'))
  } catch (e) {
    console.error('[Products List] Ошибка при удалении товара:', e)
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
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
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
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
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  border: 1px solid #E5E7EB;
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
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.02);
  border: 1px solid #f1f1f1;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.product-image {
  position: relative;
  background: #F9FAFB;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
  border-radius: 10px;
}

.product-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.2s;
}

.product-card:hover .product-actions {
  opacity: 1;
}

.btn-action {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-edit {
  background: white;
  color: #3B82F6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-edit:hover {
  background: #3B82F6;
  color: white;
}

.btn-delete {
  background: white;
  color: #EF4444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-delete:hover {
  background: #EF4444;
  color: white;
}

.product-info {
  padding: 16px;
}

.product-category {
  font-size: 0.65rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.product-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 2px;
  line-height: 1.3;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-brand {
  font-size: 0.8rem;
  color: #6B7280;
  margin-bottom: 12px;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.product-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.product-sold {
  font-size: 0.65rem;
  font-weight: 700;
  color: #F59E0B;
  background: #FFFBEB;
  padding: 2px 6px;
  border-radius: 4px;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 800;
  color: #111;
}

.product-stock {
  font-size: 0.7rem;
  font-weight: 600;
  color: #10B981;
  background: #ECFDF5;
  padding: 4px 8px;
  border-radius: 6px;
}

.product-stock.out-of-stock {
  color: #EF4444;
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
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
    padding: 14px;
    border-radius: 12px;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .product-actions {
    opacity: 1;
  }
}
</style>
