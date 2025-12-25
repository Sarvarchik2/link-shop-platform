<template>
    <div class="shop-admin-page">
      <!-- Sidebar -->
      <ShopAdminSidebar :shop-slug="shopSlug" current-route="brands" />
  
      <!-- Main Content -->
      <main class="admin-main">
        <div class="admin-header">
          <div>
            <h1 class="admin-title">Бренды</h1>
            <p class="admin-subtitle">Управление брендами магазина</p>
          </div>
          <NuxtLink :to="`/shop/${shopSlug}/admin/brands/new`" class="btn btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span class="btn-text">Добавить бренд</span>
          </NuxtLink>
        </div>
  
        <div class="admin-content">
          <div v-if="isEmpty" class="empty-state">
            <p>Бренды не найдены</p>
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
                  Удалить
                </button>
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
  
  const handleLogout = () => {
    logout()
    useToast().success('Вы вышли из аккаунта')
  }
  
  const { data: brands, error, refresh } = await useFetch(`http://localhost:8000/brands?shop_slug=${shopSlug}`, {
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
    if (!confirm('Вы уверены, что хотите удалить этот бренд?')) return
    try {
      console.log('[Brands List] Удаление бренда:', id)
      await $fetch(`http://localhost:8000/brands/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token.value}` }
      })
      console.log('[Brands List] Бренд удален успешно')
      refresh()
      useToast().success('Бренд удален')
    } catch (e) {
      console.error('[Brands List] Ошибка при удалении бренда:', e)
      console.error('[Brands List] Детали ошибки:', {
        message: e.message,
        statusCode: e.statusCode,
        data: e.data
      })
      useToast().error(e.data?.detail || e.message || 'Ошибка при удалении бренда')
    }
  }
  </script>
  
  <style scoped>
  .shop-admin-page {
    min-height: 100vh;
    display: flex;
    background: #FAFAFA;
  }
  
  /* Sidebar - same as orders.vue */
  .admin-sidebar {
    width: 280px;
    background: white;
    border-right: 1px solid #E5E7EB;
    display: flex;
    flex-direction: column;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
  }
  
  .sidebar-header {
    padding: 24px 20px;
    border-bottom: 1px solid #E5E7EB;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .sidebar-logo {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .sidebar-title {
    font-size: 1.125rem;
    font-weight: 800;
    color: #111;
    margin: 0;
  }
  
  .sidebar-nav {
    flex: 1;
    padding: 16px 0;
  }
  
  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: #6B7280;
    text-decoration: none;
    transition: all 0.2s;
    font-weight: 500;
  }
  
  .nav-item:hover {
    background: #F9FAFB;
    color: #111;
  }
  
  .nav-item.active {
    background: #111;
    color: white;
  }
  
  .sidebar-footer {
    padding: 16px 20px;
    border-top: 1px solid #E5E7EB;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .back-link {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #6B7280;
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.2s;
  }
  
  .back-link:hover {
    color: #111;
  }
  
  .logout-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #EF4444;
    background: none;
    border: none;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
    padding: 0;
    font-family: inherit;
  }
  
  .logout-btn:hover {
    color: #DC2626;
  }
  
  /* Main Content */
  .admin-main {
    flex: 1;
    margin-left: 280px;
    min-height: 100vh;
  }
  
  .admin-header {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    color: white;
    padding: 48px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 24px;
  }
  
  .admin-title {
    font-size: 2.5rem;
    font-weight: 900;
    margin-bottom: 8px;
  }
  
  .admin-subtitle {
    font-size: 1.125rem;
    opacity: 0.9;
  }
  
  .admin-content {
    padding: 40px;
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
    background: white;
    color: #111;
  }
  
  .btn-primary:hover {
    background: #F3F4F6;
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
    border-radius: 20px;
    padding: 32px 24px;
    transition: all 0.3s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid #f0f0f0;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .brand-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.08);
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
    .admin-sidebar {
      width: 240px;
    }
    
    .admin-main {
      margin-left: 240px;
    }
  }
  
  @media (max-width: 768px) {
    .admin-sidebar {
      transform: translateX(-100%);
      transition: transform 0.3s;
    }
    
    .admin-main {
      margin-left: 0;
    }
    
    .brands-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }
    
    .brand-card {
      padding: 24px 16px;
    }
    
    .brand-logo-wrapper {
      width: 100px;
      height: 100px;
    }
  }
  
  @media (min-width: 1200px) {
    .brands-grid {
      grid-template-columns: repeat(5, 1fr);
    }
  }
  </style>
  
  