<template>
  <div class="shop-admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
          </svg>
        </div>
        <h2 class="sidebar-title">Панель управления</h2>
      </div>
      
      <nav class="sidebar-nav">
        <NuxtLink :to="`/shop/${shopSlug}/admin`" class="nav-item" :class="{ active: currentRoute === 'dashboard' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="nav-item" :class="{ active: currentRoute === 'products' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>Товары</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/orders`" class="nav-item" :class="{ active: currentRoute === 'orders' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Заказы</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="nav-item" :class="{ active: currentRoute === 'categories' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
          <span>Категории</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="nav-item" :class="{ active: currentRoute === 'brands' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <line x1="7" y1="7" x2="7.01" y2="7"></line>
          </svg>
          <span>Бренды</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/banner`" class="nav-item" :class="{ active: currentRoute === 'banner' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span>Баннер</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/subscription`" class="nav-item" :class="{ active: currentRoute === 'subscription' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <span>Подписка</span>
        </NuxtLink>
      </nav>
      
      <div class="sidebar-footer">
        <NuxtLink :to="`/${shopSlug}`" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>В магазин</span>
        </NuxtLink>
        <button @click="handleLogout" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Выйти</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="admin-main">
      <div class="dashboard-page">
        <ClientOnly>
          <div class="dashboard-header">
            <div class="header-left">
              <h1 class="page-title">{{ shop?.name || 'Загрузка...' }} - Админка</h1>
              <p class="page-subtitle">Добро пожаловать! Статус вашего магазина.</p>
            </div>
            <div class="header-right">
              <span v-if="shop" :class="['status-badge', getStatusClass(shop?.subscription_status)]">
                {{ getStatusText(shop?.subscription_status) }}
              </span>
              <NuxtLink v-if="shop && (shop?.subscription_status === 'trial' || shop?.subscription_status === 'expired')" :to="`/shop/${shopSlug}/subscription`" class="upgrade-btn">
                Выбрать подписку
              </NuxtLink>
            </div>
          </div>

          <div v-if="pending" class="loading-state">
            <div class="spinner"></div>
            <p>Загрузка...</p>
          </div>

          <div v-else class="dashboard-content">
      <!-- Period Selector -->
      <div class="period-selector">
        <button 
          v-for="period in periods" 
          :key="period.key"
          @click="selectedPeriod = period.key"
          class="period-btn"
          :class="{ active: selectedPeriod === period.key }"
        >
          {{ period.label }}
        </button>
      </div>

      <!-- Main Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card revenue-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <div class="stat-comparison" v-if="getPeriodOrders() > 0">
              <span class="comparison-value">{{ getPeriodOrders() }} заказов</span>
            </div>
          </div>
          <div class="stat-value">${{ getPeriodSales().toFixed(2) }}</div>
          <div class="stat-label">{{ periodLabel }} выручка</div>
          <div class="stat-note" v-if="stats?.orders_by_status?.cancelled > 0">
            {{ stats.orders_by_status.cancelled }} отмененных не учтено
          </div>
        </div>

        <div class="stat-card orders-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats?.total_orders || 0 }}</div>
          <div class="stat-label">Всего заказов</div>
          <div class="stat-breakdown">
            <span class="breakdown-item pending" v-if="stats?.orders_by_status?.pending">
              {{ stats.orders_by_status.pending }} ожидают
            </span>
          </div>
        </div>

        <div class="stat-card users-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats?.total_users || 0 }}</div>
          <div class="stat-label">Клиентов</div>
        </div>

        <div class="stat-card products-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats?.total_products || 0 }}</div>
          <div class="stat-label">Товаров</div>
        </div>
      </div>

      <!-- Orders by Status -->
      <div class="section orders-section">
        <h2 class="section-title">Заказы по статусу</h2>
        <div class="status-grid">
          <div class="status-card pending">
            <div class="status-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="status-info">
              <span class="status-count">{{ stats?.orders_by_status?.pending || 0 }}</span>
              <span class="status-label">Ожидают</span>
            </div>
            <div class="status-bar">
              <div class="status-fill" :style="{ width: getStatusPercent('pending') + '%' }"></div>
            </div>
          </div>

          <div class="status-card processing">
            <div class="status-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24"></path>
              </svg>
            </div>
            <div class="status-info">
              <span class="status-count">{{ stats?.orders_by_status?.processing || 0 }}</span>
              <span class="status-label">В обработке</span>
            </div>
            <div class="status-bar">
              <div class="status-fill" :style="{ width: getStatusPercent('processing') + '%' }"></div>
            </div>
          </div>

          <div class="status-card shipping">
            <div class="status-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="1" y="3" width="15" height="13"></rect>
                <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                <circle cx="5.5" cy="18.5" r="2.5"></circle>
                <circle cx="18.5" cy="18.5" r="2.5"></circle>
              </svg>
            </div>
            <div class="status-info">
              <span class="status-count">{{ stats?.orders_by_status?.shipping || 0 }}</span>
              <span class="status-label">Доставляются</span>
            </div>
            <div class="status-bar">
              <div class="status-fill" :style="{ width: getStatusPercent('shipping') + '%' }"></div>
            </div>
          </div>

          <div class="status-card delivered">
            <div class="status-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="status-info">
              <span class="status-count">{{ stats?.orders_by_status?.delivered || 0 }}</span>
              <span class="status-label">Доставлены</span>
            </div>
            <div class="status-bar">
              <div class="status-fill" :style="{ width: getStatusPercent('delivered') + '%' }"></div>
            </div>
          </div>

          <div class="status-card cancelled">
            <div class="status-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
            </div>
            <div class="status-info">
              <span class="status-count">{{ stats?.orders_by_status?.cancelled || 0 }}</span>
              <span class="status-label">Отменены</span>
            </div>
            <div class="status-bar">
              <div class="status-fill" :style="{ width: getStatusPercent('cancelled') + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Period Comparison -->
      <div class="section comparison-section">
        <h2 class="section-title">Общие показатели</h2>
        <div class="comparison-grid">
          <div class="comparison-card">
            <div class="comparison-header">
              <span class="comparison-title">Сегодня</span>
              <span class="comparison-badge today">LIVE</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.today_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Выручка</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.today_orders || 0 }}</span>
                <span class="comp-label">Заказы</span>
              </div>
            </div>
          </div>

          <div class="comparison-card">
            <div class="comparison-header">
              <span class="comparison-title">Эта неделя</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.week_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Выручка</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.week_orders || 0 }}</span>
                <span class="comp-label">Заказы</span>
              </div>
            </div>
          </div>

          <div class="comparison-card">
            <div class="comparison-header">
              <span class="comparison-title">Этот месяц</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.month_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Выручка</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.month_orders || 0 }}</span>
                <span class="comp-label">Заказы</span>
              </div>
            </div>
          </div>

          <div class="comparison-card total-card">
            <div class="comparison-header">
              <span class="comparison-title">Все время</span>
              <span class="comparison-badge total">ВСЕГО</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.total_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Выручка</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.total_orders || 0 }}</span>
                <span class="comp-label">Заказы</span>
              </div>
            </div>
          </div>
          </div>
        </div>
      </div>
          <template #fallback>
            <div class="loading-state">
              <div class="spinner"></div>
              <p>Загрузка...</p>
            </div>
          </template>
        </ClientOnly>
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

const currentRoute = computed(() => {
  const path = route.path
  if (path.includes('/products')) return 'products'
  if (path.includes('/orders')) return 'orders'
  if (path.includes('/categories')) return 'categories'
  if (path.includes('/brands')) return 'brands'
  if (path.includes('/banner')) return 'banner'
  if (path.includes('/subscription')) return 'subscription'
  return 'dashboard'
})

const selectedPeriod = ref('all')
const periods = [
  { key: 'today', label: 'Сегодня' },
  { key: 'week', label: 'Эта неделя' },
  { key: 'month', label: 'Этот месяц' },
  { key: 'all', label: 'Все время' }
]

const { data: shop } = await useFetch(`http://localhost:8000/platform/shops/${shopSlug}`, {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

const { data: stats, pending, refresh, error } = await useFetch(`http://localhost:8000/shop/${shopSlug}/admin/stats`, {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  })),
  watch: [token]
})

watch(stats, (newStats) => {
  if (newStats) {
    console.log('[Shop Admin Dashboard] Статистика загружена:', newStats)
  }
})

watch(error, (newError) => {
  if (newError) {
    console.error('[Shop Admin Dashboard] Ошибка загрузки статистики:', newError.message)
    console.error('[Shop Admin Dashboard] Детали ошибки:', {
      statusCode: newError.statusCode,
      data: newError.data
    })
  }
})

const getStatusClass = (status) => {
  const statusMap = {
    'trial': 'status-trial',
    'active': 'status-active',
    'expired': 'status-expired',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || 'status-trial'
}

const getStatusText = (status) => {
  const statusMap = {
    'trial': 'Пробный период',
    'active': 'Активна',
    'expired': 'Истекла',
    'cancelled': 'Отменена'
  }
  return statusMap[status] || status
}

const periodLabel = computed(() => {
  switch (selectedPeriod.value) {
    case 'today': return "Сегодняшняя"
    case 'week': return "Недельная"
    case 'month': return "Месячная"
    default: return 'Общая'
  }
})

const getPeriodSales = () => {
  if (selectedPeriod.value === 'today') return stats.value?.today_sales || 0
  if (selectedPeriod.value === 'week') return stats.value?.week_sales || 0
  if (selectedPeriod.value === 'month') return stats.value?.month_sales || 0
  return stats.value?.total_sales || 0
}

const getPeriodOrders = () => {
  if (selectedPeriod.value === 'today') return stats.value?.today_orders || 0
  if (selectedPeriod.value === 'week') return stats.value?.week_orders || 0
  if (selectedPeriod.value === 'month') return stats.value?.month_orders || 0
  return stats.value?.total_orders || 0
}

const getStatusPercent = (status) => {
  if (!stats.value?.total_orders || stats.value.total_orders === 0) return 0
  const count = stats.value.orders_by_status?.[status] || 0
  return Math.round((count / stats.value.total_orders) * 100)
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

/* Sidebar */
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
  padding: 40px;
}

.dashboard-page {
  width: 100%;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-badge {
  display: inline-block;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 700;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.status-active {
  background: #D1FAE5;
  color: #059669;
}

.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.status-cancelled {
  background: #F3F4F6;
  color: #374151;
}

.upgrade-btn {
  padding: 12px 24px;
  background: #111;
  color: white;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.upgrade-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  background: #000;
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

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.period-selector {
  display: flex;
  gap: 8px;
  background: #F3F4F6;
  padding: 6px;
  border-radius: 12px;
  width: fit-content;
}

.period-btn {
  padding: 10px 20px;
  border: none;
  background: transparent;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.period-btn:hover { color: #111; }

.period-btn.active {
  background: white;
  color: #111;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.revenue-card {
  background: linear-gradient(135deg, #111 0%, #374151 100%);
  color: white;
}

.revenue-card .stat-icon { background: rgba(255,255,255,0.2); }

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
}

.comparison-value {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.7);
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 4px;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
}

.revenue-card .stat-label { color: rgba(255,255,255,0.8); }

.stat-note {
  margin-top: 12px;
  font-size: 0.7rem;
  color: rgba(255,255,255,0.5);
}

.stat-breakdown {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.breakdown-item {
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 600;
}

.breakdown-item.pending {
  background: #FEF3C7;
  color: #92400E;
}

.section {
  background: white;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 20px 0;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.status-card {
  background: #F9FAFB;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-icon svg {
  width: 24px;
  height: 24px;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.status-count {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
}

.status-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 600;
}

.status-bar {
  height: 4px;
  background: #E5E7EB;
  border-radius: 2px;
  overflow: hidden;
}

.status-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease-out;
}

.status-card.pending .status-fill { background: #F59E0B; }
.status-card.processing .status-fill { background: #3B82F6; }
.status-card.shipping .status-fill { background: #6366F1; }
.status-card.delivered .status-fill { background: #10B981; }
.status-card.cancelled .status-fill { background: #EF4444; }

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.comparison-card {
  background: #F9FAFB;
  border-radius: 16px;
  padding: 20px;
}

.total-card {
  background: linear-gradient(135deg, #111 0%, #374151 100%);
  color: white;
}

.comparison-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.comparison-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #6B7280;
}

.total-card .comparison-title { color: rgba(255,255,255,0.8); }

.comparison-badge {
  font-size: 0.625rem;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 700;
  text-transform: uppercase;
}

.comparison-badge.today {
  background: #D1FAE5;
  color: #059669;
}

.comparison-badge.total {
  background: rgba(255,255,255,0.2);
  color: white;
}

.comparison-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comparison-stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.comp-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
}

.total-card .comp-value { color: white; }

.comp-label {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.total-card .comp-label { color: rgba(255,255,255,0.6); }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .status-grid { grid-template-columns: repeat(3, 1fr); }
  .comparison-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .dashboard-header { flex-direction: column; gap: 12px; }
  .page-title { font-size: 1.75rem; }
  .header-right { align-self: flex-start; flex-direction: column; align-items: flex-start; }
  
  .period-selector {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .period-btn {
    padding: 8px 16px;
    white-space: nowrap;
  }
  
  .stats-grid { grid-template-columns: 1fr; gap: 12px; }
  .stat-card { padding: 20px; }
  .section { padding: 20px; border-radius: 16px; }
  .section-title { font-size: 1.1rem; margin-bottom: 16px; }
  .status-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .status-card:last-child { grid-column: span 2; }
  .status-card { padding: 16px; }
  .status-count { font-size: 1.25rem; }
  .comparison-grid { grid-template-columns: 1fr; gap: 12px; }
  .comparison-card { padding: 16px; }
}
</style>
