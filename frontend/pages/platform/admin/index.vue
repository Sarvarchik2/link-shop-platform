<template>
  <div class="platform-admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
            <path d="M2 17l10 5 10-5"></path>
            <path d="M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <h2 class="sidebar-title">Панель управления</h2>
      </div>
      
      <nav class="sidebar-nav">
        <NuxtLink to="/platform/admin" class="nav-item" :class="{ active: currentRoute === 'dashboard' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        
        <NuxtLink to="/platform/admin/shops" class="nav-item" :class="{ active: currentRoute === 'shops' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
          </svg>
          <span>Магазины</span>
        </NuxtLink>
        
        <NuxtLink to="/platform/admin/users" class="nav-item" :class="{ active: currentRoute === 'users' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>Пользователи</span>
        </NuxtLink>
        
        <NuxtLink to="/platform/admin/orders" class="nav-item" :class="{ active: currentRoute === 'orders' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Заказы</span>
        </NuxtLink>
      </nav>
      
      <div class="sidebar-footer">
        <NuxtLink to="/" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>На главную</span>
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
      <div class="admin-header">
        <div>
          <h1 class="admin-title">Панель управления платформой</h1>
          <p class="admin-subtitle">Добро пожаловать! Статус вашей платформы.</p>
        </div>
      </div>

      <div class="admin-content">
        <ClientOnly>
          <div v-if="error" class="text-center py-12 text-red-500">
            <p class="mt-4">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
            <button @click="refresh" class="mt-4 px-4 py-2 bg-black text-white rounded-lg">Повторить</button>
          </div>
          <div v-else-if="pending" class="text-center py-12 text-gray-400">
            <div class="loading-spinner"></div>
            <p class="mt-4">Загрузка...</p>
          </div>

          <div v-else>
          <!-- Time Period Selector -->
          <div class="period-selector">
            <button 
              v-for="period in periods" 
              :key="period.key"
              @click="selectedPeriod = period.key"
              :class="['period-btn', { active: selectedPeriod === period.key }]"
            >
              {{ period.label }}
            </button>
          </div>

          <!-- KPI Cards -->
          <div class="stats-grid">
            <div class="stat-card primary">
              <div class="stat-icon">💰</div>
              <div class="stat-info">
                <div class="stat-value">${{ getPeriodSales().toFixed(2) }}</div>
                <div class="stat-label">Общая выручка</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">📦</div>
              <div class="stat-info">
                <div class="stat-value">{{ getPeriodOrders() }}</div>
                <div class="stat-label">Всего заказов</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-info">
                <div class="stat-value">{{ stats?.total_users || 0 }}</div>
                <div class="stat-label">Пользователей</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">🏪</div>
              <div class="stat-info">
                <div class="stat-value">{{ stats?.total_shops || 0 }}</div>
                <div class="stat-label">Магазинов</div>
              </div>
            </div>
          </div>

          <!-- Orders by Status -->
          <div class="section">
            <h2 class="section-title">Заказы по статусу</h2>
            <div class="status-cards">
              <div class="status-card">
                <div class="status-icon">⏰</div>
                <div class="status-value">{{ stats?.orders_by_status?.pending || 0 }}</div>
                <div class="status-label">Ожидают</div>
              </div>
              <div class="status-card">
                <div class="status-icon">⚙️</div>
                <div class="status-value">{{ stats?.orders_by_status?.processing || 0 }}</div>
                <div class="status-label">В обработке</div>
              </div>
              <div class="status-card">
                <div class="status-icon">🚚</div>
                <div class="status-value">{{ stats?.orders_by_status?.shipping || 0 }}</div>
                <div class="status-label">Доставляются</div>
              </div>
              <div class="status-card">
                <div class="status-icon">✅</div>
                <div class="status-value">{{ stats?.orders_by_status?.delivered || 0 }}</div>
                <div class="status-label">Доставлены</div>
              </div>
              <div class="status-card">
                <div class="status-icon">❌</div>
                <div class="status-value">{{ stats?.orders_by_status?.cancelled || 0 }}</div>
                <div class="status-label">Отменены</div>
              </div>
            </div>
          </div>

          <!-- Period Stats -->
          <div class="section">
            <h2 class="section-title">Общие показатели</h2>
            <div class="period-stats-grid">
              <div class="period-stat-card">
                <div class="period-header">
                  <span class="period-name">Сегодня</span>
                  <span class="period-badge live">LIVE</span>
                </div>
                <div class="period-values">
                  <div class="period-value">
                    <span class="value-label">Выручка</span>
                    <span class="value-amount">${{ stats?.today_sales?.toFixed(2) || '0.00' }}</span>
                  </div>
                  <div class="period-value">
                    <span class="value-label">Заказы</span>
                    <span class="value-amount">{{ stats?.today_orders || 0 }}</span>
                  </div>
                </div>
              </div>
              
              <div class="period-stat-card">
                <div class="period-header">
                  <span class="period-name">Эта неделя</span>
                </div>
                <div class="period-values">
                  <div class="period-value">
                    <span class="value-label">Выручка</span>
                    <span class="value-amount">${{ stats?.week_sales?.toFixed(2) || '0.00' }}</span>
                  </div>
                  <div class="period-value">
                    <span class="value-label">Заказы</span>
                    <span class="value-amount">{{ stats?.week_orders || 0 }}</span>
                  </div>
                </div>
              </div>
              
              <div class="period-stat-card">
                <div class="period-header">
                  <span class="period-name">Этот месяц</span>
                </div>
                <div class="period-values">
                  <div class="period-value">
                    <span class="value-label">Выручка</span>
                    <span class="value-amount">${{ stats?.month_sales?.toFixed(2) || '0.00' }}</span>
                  </div>
                  <div class="period-value">
                    <span class="value-label">Заказы</span>
                    <span class="value-amount">{{ stats?.month_orders || 0 }}</span>
                  </div>
                </div>
              </div>
              
              <div class="period-stat-card primary">
                <div class="period-header">
                  <span class="period-name">Все время</span>
                  <span class="period-badge total">ВСЕГО</span>
                </div>
                <div class="period-values">
                  <div class="period-value">
                    <span class="value-label">Выручка</span>
                    <span class="value-amount">${{ stats?.total_sales?.toFixed(2) || '0.00' }}</span>
                  </div>
                  <div class="period-value">
                    <span class="value-label">Заказы</span>
                    <span class="value-amount">{{ stats?.total_orders || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          </div>
        </ClientOnly>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'platform-admin'
})

const route = useRoute()
const { token, logout } = useAuth()

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const currentRoute = computed(() => {
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  if (route.path.includes('/orders')) return 'orders'
  return 'dashboard'
})

const selectedPeriod = ref('all')
const periods = [
  { key: 'today', label: 'Сегодня' },
  { key: 'week', label: 'Эта неделя' },
  { key: 'month', label: 'Этот месяц' },
  { key: 'all', label: 'Все время' }
]

const { data: stats, pending, refresh, error } = await useFetch('http://localhost:8000/platform/admin/stats', {
  server: false,
  lazy: true,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Watch for errors and log them
watch(error, (newError) => {
  if (newError) {
    console.error('[Admin Dashboard] Ошибка загрузки статистики:', newError)
    console.error('[Admin Dashboard] Детали ошибки:', {
      message: newError.message,
      statusCode: newError.statusCode,
      statusMessage: newError.statusMessage,
      data: newError.data
    })
  }
}, { immediate: true })

// Watch for token changes and refresh data
watch(token, () => {
  if (token.value) {
    console.log('[Admin Dashboard] Токен обновлен, обновляю данные...')
    refresh()
  }
}, { immediate: true })

// Log when data is loaded
watch(stats, (newStats) => {
  if (newStats) {
    console.log('[Admin Dashboard] Данные загружены:', newStats)
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
</script>

<style scoped>
.platform-admin-page {
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

.nav-item svg {
  flex-shrink: 0;
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

/* Period Selector */
.period-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}

.period-btn {
  padding: 10px 20px;
  border: 2px solid #E5E7EB;
  background: white;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn:hover {
  border-color: #111;
}

.period-btn.active {
  background: #111;
  color: white;
  border-color: #111;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.stat-card.primary {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  border: none;
}

.stat-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 900;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.8;
}

.stat-card.primary .stat-label {
  opacity: 0.9;
}

/* Section */
.section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 20px;
  color: #111;
}

/* Status Cards */
.status-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid #E5E7EB;
}

.status-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.status-value {
  font-size: 1.5rem;
  font-weight: 900;
  margin-bottom: 4px;
  color: #111;
}

.status-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 600;
}

/* Period Stats */
.period-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.period-stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #E5E7EB;
}

.period-stat-card.primary {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  border: none;
}

.period-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.period-name {
  font-weight: 700;
  font-size: 0.875rem;
}

.period-badge {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
}

.period-badge.live {
  background: #10B981;
  color: white;
}

.period-badge.total {
  background: rgba(255,255,255,0.2);
  color: white;
}

.period-values {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.period-value {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.value-label {
  font-size: 0.75rem;
  opacity: 0.7;
}

.value-amount {
  font-size: 1.125rem;
  font-weight: 800;
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

@media (max-width: 1024px) {
  .admin-sidebar {
    width: 240px;
  }
  
  .admin-main {
    margin-left: 240px;
  }
  
  .stats-grid,
  .period-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .status-cards {
    grid-template-columns: repeat(3, 1fr);
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
  
  .stats-grid,
  .period-stats-grid,
  .status-cards {
    grid-template-columns: 1fr;
  }
}
</style>
