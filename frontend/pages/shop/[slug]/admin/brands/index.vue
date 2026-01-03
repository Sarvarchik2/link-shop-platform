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
      <span class="mobile-title">{{ $t('brandsPage.title') }}</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <!-- Sidebar -->
    <ShopAdminSidebar :shop-slug="shopSlug" current-route="brands" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <div>
            <h1 class="page-title">{{ $t('brandsPage.title') }}</h1>
            <p class="page-subtitle">{{ $t('brandsPage.subtitle') }}</p>
          </div>
          <NuxtLink :to="`/shop/${shopSlug}/admin/brands/new`" class="btn btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span class="btn-text">{{ $t('brandsPage.add') }}</span>
          </NuxtLink>
        </div>

        <div class="admin-content">
          <div v-if="isEmpty" class="empty-state">
            <p>{{ $t('brandsPage.empty') }}</p>
          </div>
          <div v-else class="brands-grid">
            <div v-for="brand in brands" :key="brand.id" class="brand-card">
              <div class="brand-logo-wrapper">
                <img :src="brand.logo_url" :alt="brand.name" class="brand-logo" />
              </div>
              <div class="brand-info">
                <h3 class="brand-name">{{ brand.name }}</h3>
                <button @click="deleteBrand(brand.id)" class="btn-delete">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                  {{ $t('common.delete') }}
                </button>
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
const { token } = useAuth()
const sidebarOpen = ref(false)

const { data: brands, error, refresh } = await useFetch(`${useRuntimeConfig().public.apiBase}/brands?shop_slug=${shopSlug}`, {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

const isEmpty = computed(() => !brands.value || brands.value.length === 0)

watch(brands, (newBrands) => {
  if (newBrands) {
    console.log('[Brands List] Бренды загружены:', newBrands.length)
  }
})

watch(error, (newError) => {
  if (newError) {
    console.error('[Brands List] Ошибка загрузки брендов:', newError.message)
    console.error('[Brands List] Детали ошибки:', {
      statusCode: newError.statusCode,
      data: newError.data
    })
  }
})

const deleteBrand = async (id) => {
  if (!confirm(t('brandsPage.deleteConfirm'))) return
  try {
    console.log('[Brands List] Удаление бренда:', id)
    await $fetch(`${useRuntimeConfig().public.apiBase}/brands/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    console.log('[Brands List] Бренд удален успешно')
    refresh()
    useToast().success(t('brandsPage.deleteSuccess'))
  } catch (e) {
    console.error('[Brands List] Ошибка при удалении бренда:', e)
    console.error('[Brands List] Детали ошибки:', {
      message: e.message,
      statusCode: e.statusCode,
      data: e.data
    })
    useToast().error(e.data?.detail || e.message || t('common.error'))
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

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

/* Main Content */
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
  border-radius: 16px;
  color: #9CA3AF;
  font-size: 1.125rem;
}

.brands-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
}

.brand-card {
  background: white;
  border-radius: 24px;
  padding: 32px 24px;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.02);
  border: 1px solid #f1f1f1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.brand-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.brand-logo-wrapper {
  width: 120px;
  height: 120px;
  background: #F9FAFB;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  margin-bottom: 20px;
}

.brand-logo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.brand-info {
  width: 100%;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 16px;
}

.btn-delete {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  background: #FEF2F2;
  color: #EF4444;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-delete:hover {
  background: #EF4444;
  color: white;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 64px 0 0 0;
    width: 100%;
    min-width: 0;
  }

  .container {
    padding: 0;
  }

  .page-header {
    background: white;
    padding: 12px 16px;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
  }

  .page-title,
  .page-subtitle {
    display: none;
  }

  .mobile-header {
    display: flex;
  }
}

@media (max-width: 768px) {
  .page-header>div:first-child {
    display: none;
  }

  .page-header {
    background: white;
    padding: 16px 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
    padding: 14px;
    border-radius: 12px;
  }

  .admin-content {
    padding: 0 20px 40px 20px;
  }

  .brands-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .brand-card {
    padding: 24px 12px;
    border-radius: 20px;
  }

  .brand-logo-wrapper {
    width: 70px;
    height: 70px;
    margin-bottom: 12px;
    padding: 12px;
  }

  .brand-name {
    font-size: 0.9rem;
    margin-bottom: 12px;
  }

  .btn-text {
    font-size: 0.8rem;
  }
}

@media (min-width: 1200px) {
  .brands-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
</style>