<template>
  <div class="platform-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">Панель управления</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar 
      :current-route="currentRoute" 
      :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event"
      @logout="handleLogout" 
    />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div class="header-content">
        <div>
          <h1 class="admin-title">Панель управления платформой</h1>
            <p class="admin-subtitle">Добро пожаловать! Обзор статистики вашей платформы.</p>
          </div>
          <button @click="refresh" class="refresh-btn" :disabled="pending">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ spinning: pending }">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span>Обновить</span>
          </button>
        </div>
      </div>

      <div class="admin-content">
        <ClientOnly>
          <div v-if="error" class="error-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p class="error-message">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
            <button @click="refresh" class="retry-btn">Повторить</button>
          </div>
          
          <div v-else-if="pending" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Загрузка данных...</p>
          </div>

          <div v-else class="dashboard-content">
            <!-- Period Selector -->
          <div class="period-selector">
            <button 
              v-for="period in periods" 
              :key="period.key"
              @click="selectedPeriod = period.key"
              :class="['period-btn', { active: selectedPeriod === period.key }]"
            >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>{{ period.label }}</span>
            </button>
          </div>
            <!-- Main KPI Cards -->
          <div class="stats-grid">
            <div class="stat-card primary">
                <div class="stat-icon-wrapper shop-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
                  </svg>
                </div>
              <div class="stat-info">
                  <div class="stat-value">{{ subscriptionStats.totalShops }}</div>
                  <div class="stat-label">Всего магазинов</div>
                  <div class="stat-change positive" v-if="shopsRecentlyAdded > 0">
                    <span v-if="selectedPeriod === 'today'">+{{ shopsRecentlyAdded }} сегодня</span>
                    <span v-else-if="selectedPeriod === 'week'">+{{ shopsRecentlyAdded }} на неделе</span>
                    <span v-else-if="selectedPeriod === 'month'">+{{ shopsRecentlyAdded }} в месяце</span>
                    <span v-else>+{{ shopsRecentlyAdded }} за месяц</span>
                  </div>
              </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon-wrapper success-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              <div class="stat-info">
                  <div class="stat-value">{{ subscriptionStats.activeShops }}</div>
                  <div class="stat-label">Активных магазинов</div>
                  <div class="stat-percentage">
                    {{ activeShopsPercentage }}% от общего числа
                  </div>
              </div>
            </div>
            
              <div class="stat-card revenue-card">
                <div class="stat-icon-wrapper revenue-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="1" x2="12" y2="23"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                  </svg>
                </div>
              <div class="stat-info">
                  <div class="stat-value">${{ subscriptionStats.monthlyRevenue.toFixed(0) }}</div>
                  <div class="stat-label">
                    <span v-if="selectedPeriod === 'today'">Доход с подписок (сегодня)</span>
                    <span v-else-if="selectedPeriod === 'week'">Доход с подписок (неделя)</span>
                    <span v-else-if="selectedPeriod === 'month'">Доход с подписок (месяц)</span>
                    <span v-else>Доход с подписок/мес</span>
                  </div>
                  <div class="stat-yearly" v-if="selectedPeriod === 'all'">
                    ≈ ${{ (subscriptionStats.monthlyRevenue * 12).toFixed(0) }}/год
                  </div>
                  <div class="stat-yearly" v-else-if="periodStats?.sales">
                    Продажи: ${{ periodStats.sales.toFixed(0) }}
                  </div>
              </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon-wrapper users-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </div>
              <div class="stat-info">
                  <div class="stat-value">{{ periodStats?.users || stats?.total_users || 0 }}</div>
                  <div class="stat-label">Пользователей</div>
                  <div class="stat-products" v-if="periodStats?.products !== null && periodStats?.products !== undefined">
                    {{ periodStats.products }} товаров
                  </div>
                  <div class="stat-products" v-else-if="selectedPeriod === 'all' && stats?.total_products">
                    {{ stats.total_products }} товаров на платформе
                  </div>
              </div>
            </div>
          </div>

            <!-- Two Column Layout -->
            <div class="two-column-grid">
              <!-- Left Column -->
              <div class="left-column">
                <!-- Subscription Statistics -->
          <div class="section">
                  <div class="section-header">
                    <h2 class="section-title">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                      </svg>
                      Статистика подписок
                    </h2>
                    <button @click="toggleSortExpiry" class="sort-btn">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18M7 12h10M11 18h2"></path>
                      </svg>
                      <span>Сортировать по сроку</span>
                    </button>
              </div>
                  
                  <!-- Pie Chart -->
                  <div class="chart-container">
                    <div class="pie-chart-wrapper">
                      <svg viewBox="0 0 200 200" class="pie-chart">
                        <circle cx="100" cy="100" r="80" fill="none" stroke="#F3F4F6" stroke-width="40" />
                        <circle 
                          cx="100" cy="100" r="80" 
                          fill="none" 
                          :stroke="getSubscriptionColor('trial')" 
                          stroke-width="40"
                          :stroke-dasharray="getSubscriptionArc(subscriptionStats.byStatus.trial, subscriptionStats.totalShops)"
                          :stroke-dashoffset="0"
                          transform="rotate(-90 100 100)"
                        />
                        <circle 
                          cx="100" cy="100" r="80" 
                          fill="none" 
                          :stroke="getSubscriptionColor('active')" 
                          stroke-width="40"
                          :stroke-dasharray="getSubscriptionArc(subscriptionStats.byStatus.active, subscriptionStats.totalShops)"
                          :stroke-dashoffset="getSubscriptionOffset('trial', subscriptionStats)"
                          transform="rotate(-90 100 100)"
                        />
                        <circle 
                          cx="100" cy="100" r="80" 
                          fill="none" 
                          :stroke="getSubscriptionColor('expired')" 
                          stroke-width="40"
                          :stroke-dasharray="getSubscriptionArc(subscriptionStats.byStatus.expired, subscriptionStats.totalShops)"
                          :stroke-dashoffset="getSubscriptionOffset('active', subscriptionStats)"
                          transform="rotate(-90 100 100)"
                        />
                        <circle 
                          cx="100" cy="100" r="80" 
                          fill="none" 
                          :stroke="getSubscriptionColor('cancelled')" 
                          stroke-width="40"
                          :stroke-dasharray="getSubscriptionArc(subscriptionStats.byStatus.cancelled, subscriptionStats.totalShops)"
                          :stroke-dashoffset="getSubscriptionOffset('expired', subscriptionStats)"
                          transform="rotate(-90 100 100)"
                        />
                      </svg>
                      <div class="pie-chart-center">
                        <div class="pie-chart-total">{{ subscriptionStats.totalShops }}</div>
                        <div class="pie-chart-label">магазинов</div>
              </div>
              </div>
                    <div class="chart-legend">
                      <div class="legend-item" v-for="(item, key) in subscriptionStats.byStatus" :key="key">
                        <div class="legend-color" :style="{ backgroundColor: getSubscriptionColor(key) }"></div>
                        <div class="legend-label">{{ getStatusLabel(key) }}</div>
                        <div class="legend-value">{{ item }}</div>
              </div>
              </div>
                  </div>
                  
                  <div class="status-cards">
                    <div class="status-card trial">
                      <div class="status-icon-wrapper">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"></circle>
                          <path d="M12 6v6l4 2"></path>
                        </svg>
                      </div>
                      <div class="status-content">
                        <div class="status-value">{{ subscriptionStats.byStatus.trial }}</div>
                        <div class="status-label">Пробный период</div>
            </div>
          </div>

                    <div class="status-card active">
                      <div class="status-icon-wrapper">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </div>
                      <div class="status-content">
                        <div class="status-value">{{ subscriptionStats.byStatus.active }}</div>
                        <div class="status-label">Активные</div>
                      </div>
                    </div>
                    
                    <div class="status-card expired">
                      <div class="status-icon-wrapper">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                      </div>
                      <div class="status-content">
                        <div class="status-value">{{ subscriptionStats.byStatus.expired }}</div>
                        <div class="status-label">Истекшие</div>
                      </div>
                    </div>
                    
                    <div class="status-card cancelled">
                      <div class="status-icon-wrapper">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </div>
                      <div class="status-content">
                        <div class="status-value">{{ subscriptionStats.byStatus.cancelled }}</div>
                        <div class="status-label">Отмененные</div>
                      </div>
                    </div>
                    
                    <div class="status-card payment">
                      <div class="status-icon-wrapper">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <line x1="12" y1="1" x2="12" y2="23"></line>
                          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                        </svg>
                      </div>
                      <div class="status-content">
                        <div class="status-value">{{ subscriptionStats.totalPayments }}</div>
                        <div class="status-label">Оплат получено</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Shop Owners Info -->
          <div class="section">
                  <div class="section-header">
                    <h2 class="section-title">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                      Владельцы магазинов
                    </h2>
                </div>
                  <div class="owners-info-grid">
                    <div class="owner-stat-card">
                      <div class="owner-icon">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                          <circle cx="9" cy="7" r="4"></circle>
                          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                        </svg>
                  </div>
                      <div class="owner-stat-value">{{ uniqueOwners }}</div>
                      <div class="owner-stat-label">Уникальных владельцев</div>
                  </div>
                    
                    <div class="owner-stat-card">
                      <div class="owner-icon">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                </div>
                      <div class="owner-stat-value">{{ shopsWithActiveSubscriptions }}</div>
                      <div class="owner-stat-label">С активными подписками</div>
              </div>
              
                    <div class="owner-stat-card warning" v-if="shopsNeedingRenewal > 0">
                      <div class="owner-icon">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                          <line x1="12" y1="9" x2="12" y2="13"></line>
                          <line x1="12" y1="17" x2="12.01" y2="17"></line>
                        </svg>
                </div>
                      <div class="owner-stat-value">{{ shopsNeedingRenewal }}</div>
                      <div class="owner-stat-label">Требуют продления</div>
                  </div>
                    <div class="owner-stat-card" v-else>
                      <div class="owner-icon">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </div>
                      <div class="owner-stat-value">0</div>
                      <div class="owner-stat-label">Требуют продления</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Right Column -->
              <div class="right-column">
                <!-- Shops Needing Attention -->
                <div class="section" v-if="shopsExpiringSoon.length > 0">
                  <div class="section-header">
                    <h2 class="section-title">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                        <line x1="12" y1="9" x2="12" y2="13"></line>
                        <line x1="12" y1="17" x2="12.01" y2="17"></line>
                      </svg>
                      Требуют внимания
                    </h2>
                  </div>
                  <div class="attention-list">
                    <div v-for="shop in shopsExpiringSoon" :key="shop.id" class="attention-item">
                      <div class="attention-shop-info">
                        <div class="attention-shop-name">{{ shop.name }}</div>
                        <div class="attention-shop-meta">{{ shop.owner_name || 'Владелец не указан' }}</div>
                  </div>
                      <div class="attention-days">
                        <span class="days-badge" :class="getDaysBadgeClass(getDaysUntilExpiry(shop))">
                          {{ getDaysUntilExpiry(shop) }} дн.
                        </span>
                      </div>
                    </div>
                  </div>
                  <NuxtLink to="/platform/admin/shops" class="view-all-link">
                    Посмотреть все магазины →
                  </NuxtLink>
              </div>
              
                <!-- Recent Shops -->
                <div class="section">
                  <div class="section-header">
                    <h2 class="section-title">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                      </svg>
                      Недавно зарегистрированные
                    </h2>
                </div>
                  <div class="recent-list">
                    <div v-for="shop in recentShops" :key="shop.id" class="recent-item">
                      <div class="recent-shop-logo">
                        <span v-if="!shop.logo_url">{{ shop.name.charAt(0).toUpperCase() }}</span>
                        <img v-else :src="shop.logo_url" :alt="shop.name">
                  </div>
                      <div class="recent-shop-info">
                        <div class="recent-shop-name">{{ shop.name }}</div>
                        <div class="recent-shop-date">{{ formatDate(shop.created_at) }}</div>
                  </div>
                      <div class="recent-status" :class="getStatusClass(shop.subscription_status)">
                        {{ getStatusText(shop.subscription_status) }}
                      </div>
                    </div>
                    <NuxtLink to="/platform/admin/shops" class="view-all-link">
                      Посмотреть все магазины →
                    </NuxtLink>
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
const router = useRouter()

const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

// Period selection
const selectedPeriod = ref('all')
const periods = [
  { key: 'today', label: 'Сегодня' },
  { key: 'week', label: 'Эта неделя' },
  { key: 'month', label: 'Этот месяц' },
  { key: 'all', label: 'Все время' }
]

const currentRoute = computed(() => {
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

const { data: stats, pending, refresh, error } = await useFetch('http://localhost:8000/platform/admin/stats', {
  server: false,
  lazy: true,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

const { data: shops } = await useFetch('http://localhost:8000/platform/admin/shops', {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Get date range for selected period
const getPeriodRange = () => {
  const now = new Date()
  let startDate = null

  switch (selectedPeriod.value) {
    case 'today':
      startDate = new Date(now)
      startDate.setHours(0, 0, 0, 0)
      break
    case 'week':
      startDate = new Date(now)
      const dayOfWeek = startDate.getDay()
      const diff = startDate.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1)
      startDate.setDate(diff)
      startDate.setHours(0, 0, 0, 0)
      break
    case 'month':
      startDate = new Date(now.getFullYear(), now.getMonth(), 1)
      startDate.setHours(0, 0, 0, 0)
      break
    case 'all':
    default:
      startDate = null
  }

  return { startDate, endDate: now }
}

// Filter shops by period
const filteredShops = computed(() => {
  if (!shops.value || shops.value.length === 0) return []
  if (selectedPeriod.value === 'all') return shops.value

  const { startDate } = getPeriodRange()
  if (!startDate) return shops.value

  return shops.value.filter(shop => {
    const shopDate = new Date(shop.created_at)
    return shopDate >= startDate
  })
})

// Subscription statistics computed from filtered shops data
const subscriptionStats = computed(() => {
  const shopsToUse = filteredShops.value

  if (!shopsToUse || shopsToUse.length === 0) {
    return {
      totalShops: 0,
      activeShops: 0,
      monthlyRevenue: 0,
      byStatus: {
        trial: 0,
        active: 0,
        expired: 0,
        cancelled: 0
      },
      totalPayments: 0
    }
  }

  const now = new Date()
  const activeShops = shopsToUse.filter(s => s.is_active && 
    (s.subscription_status === 'active' || s.subscription_status === 'trial'))
  
  const byStatus = {
    trial: shopsToUse.filter(s => s.subscription_status === 'trial').length,
    active: shopsToUse.filter(s => s.subscription_status === 'active').length,
    expired: shopsToUse.filter(s => s.subscription_status === 'expired').length,
    cancelled: shopsToUse.filter(s => s.subscription_status === 'cancelled').length
  }

  const monthlyRevenue = byStatus.active * 29
  const totalPayments = byStatus.active

  return {
    totalShops: shopsToUse.length,
    activeShops: activeShops.length,
    monthlyRevenue,
    byStatus,
    totalPayments
  }
})

// Get period-specific stats from API
const periodStats = computed(() => {
  if (!stats.value) return null

  switch (selectedPeriod.value) {
    case 'today':
      return {
        users: stats.value.today_orders || 0, // This would need to be filtered differently
        products: null, // Would need API support
        sales: stats.value.today_sales || 0,
        orders: stats.value.today_orders || 0
      }
    case 'week':
      return {
        users: stats.value.week_orders || 0,
        products: null,
        sales: stats.value.week_sales || 0,
        orders: stats.value.week_orders || 0
      }
    case 'month':
      return {
        users: stats.value.month_orders || 0,
        products: null,
        sales: stats.value.month_sales || 0,
        orders: stats.value.month_orders || 0
      }
    case 'all':
    default:
      return {
        users: stats.value.total_users || 0,
        products: stats.value.total_products || 0,
        sales: stats.value.total_sales || 0,
        orders: stats.value.total_orders || 0
      }
  }
})

const activeShopsPercentage = computed(() => {
  if (subscriptionStats.value.totalShops === 0) return 0
  return Math.round((subscriptionStats.value.activeShops / subscriptionStats.value.totalShops) * 100)
})

const uniqueOwners = computed(() => {
  const shopsToUse = filteredShops.value
  if (!shopsToUse) return 0
  const ownerIds = new Set(shopsToUse.map(s => s.owner_id))
  return ownerIds.size
})

const shopsWithActiveSubscriptions = computed(() => {
  const shopsToUse = filteredShops.value
  if (!shopsToUse) return 0
  return shopsToUse.filter(s => s.subscription_status === 'active').length
})

const shopsNeedingRenewal = computed(() => {
  const shopsToUse = filteredShops.value
  if (!shopsToUse) return 0
  const now = new Date()
  return shopsToUse.filter(s => {
    if (!s.subscription_expires_at) return false
    const expiresAt = new Date(s.subscription_expires_at)
    const daysLeft = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
    return daysLeft <= 7 && daysLeft > 0 && s.subscription_status === 'active'
  }).length
})

const shopsExpiringSoon = computed(() => {
  const shopsToUse = shops.value // Always show all shops that need renewal
  if (!shopsToUse) return []
  const now = new Date()
  return shopsToUse
    .filter(s => {
      if (!s.subscription_expires_at || s.subscription_status !== 'active') return false
      const expiresAt = new Date(s.subscription_expires_at)
      const daysLeft = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
      return daysLeft <= 7 && daysLeft > 0
    })
    .sort((a, b) => {
      const daysA = Math.ceil((new Date(a.subscription_expires_at) - now) / (1000 * 60 * 60 * 24))
      const daysB = Math.ceil((new Date(b.subscription_expires_at) - now) / (1000 * 60 * 60 * 24))
      return daysA - daysB
    })
    .slice(0, 5)
})

const recentShops = computed(() => {
  const shopsToUse = filteredShops.value
  if (!shopsToUse) return []
  return [...shopsToUse]
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 5)
})

const shopsRecentlyAdded = computed(() => {
  const shopsToUse = filteredShops.value
  if (!shopsToUse) return 0
  
  const { startDate } = getPeriodRange()
  if (!startDate) {
    // For "all time", show last month
    const monthAgo = new Date()
    monthAgo.setMonth(monthAgo.getMonth() - 1)
    return shopsToUse.filter(s => new Date(s.created_at) >= monthAgo).length
  }
  
  return shopsToUse.length
})

const getDaysUntilExpiry = (shop) => {
  if (!shop.subscription_expires_at) return 0
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  return Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
}

const getDaysBadgeClass = (days) => {
  if (days <= 3) return 'critical'
  if (days <= 7) return 'warning'
  return 'normal'
}

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
    'trial': 'Пробный',
    'active': 'Активна',
    'expired': 'Истекла',
    'cancelled': 'Отменена'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

// Sort subscriptions by expiry date
const sortByExpiry = ref(false)

const toggleSortExpiry = () => {
  sortByExpiry.value = !sortByExpiry.value
}

// Sort shops by expiry date
const sortedShopsByExpiry = computed(() => {
  if (!shops.value || !sortByExpiry.value) return filteredShops.value
  
  const now = new Date()
  return [...filteredShops.value].sort((a, b) => {
    const expiryA = a.subscription_expires_at ? new Date(a.subscription_expires_at) : null
    const expiryB = b.subscription_expires_at ? new Date(b.subscription_expires_at) : null
    
    if (!expiryA && !expiryB) return 0
    if (!expiryA) return 1
    if (!expiryB) return -1
    
    return expiryA.getTime() - expiryB.getTime()
  })
})

// Chart functions
const getSubscriptionColor = (status) => {
  const colors = {
    'trial': '#FCD34D',
    'active': '#10B981',
    'expired': '#EF4444',
    'cancelled': '#9CA3AF'
  }
  return colors[status] || '#9CA3AF'
}

const getStatusLabel = (status) => {
  const labels = {
    'trial': 'Пробный период',
    'active': 'Активные',
    'expired': 'Истекшие',
    'cancelled': 'Отмененные'
  }
  return labels[status] || status
}

const getSubscriptionArc = (value, total) => {
  if (total === 0) return '0 502.65'
  const percentage = value / total
  const circumference = 2 * Math.PI * 80
  const arcLength = percentage * circumference
  return `${arcLength} ${circumference}`
}

const getSubscriptionOffset = (status, stats) => {
  if (stats.totalShops === 0) return 0
  const order = ['trial', 'active', 'expired', 'cancelled']
  const currentIndex = order.indexOf(status)
  if (currentIndex === 0) return 0
  
  const circumference = 2 * Math.PI * 80
  let offset = 0
  
  for (let i = 0; i < currentIndex; i++) {
    const prevStatus = order[i]
    const prevValue = stats.byStatus[prevStatus] || 0
    const prevPercentage = prevValue / stats.totalShops
    offset += prevPercentage * circumference
  }
  
  return -offset
}
</script>

<style scoped>
.platform-admin-page {
  min-height: 100vh;
  display: flex;
  background: #F5F7FA;
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
}

.admin-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 40px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.admin-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.admin-subtitle {
  font-size: 1rem;
  opacity: 0.85;
  font-weight: 400;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-btn svg {
  transition: transform 0.3s;
}

.refresh-btn svg.spinning {
  animation: spin 1s linear infinite;
}

.admin-content {
  padding: 32px;
}

/* Period Selector */
.period-selector {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
  background: white;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
  width: fit-content;
}

.period-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #6B7280;
}

.period-btn:hover {
  background: #F9FAFB;
  color: #111;
}

.period-btn.active {
  background: #111;
  color: white;
}

.period-btn svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* Loading & Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  color: #6B7280;
}

.error-state {
  color: #EF4444;
}

.error-state svg {
  margin-bottom: 16px;
  color: #EF4444;
}

.error-message {
  margin: 16px 0;
  font-size: 1rem;
}

.retry-btn {
  margin-top: 16px;
  padding: 10px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #2d2d2d;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 28px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
  transition: all 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.stat-card.primary {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  border: none;
}

.stat-card.revenue-card {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-color: #FCD34D;
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.shop-icon {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.success-icon {
  background: #D1FAE5;
  color: #065F46;
}

.revenue-icon {
  background: rgba(255, 255, 255, 0.8);
  color: #92400E;
}

.users-icon {
  background: #DBEAFE;
  color: #1E40AF;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 6px;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.75;
  font-weight: 500;
  margin-bottom: 4px;
}

.stat-change,
.stat-percentage,
.stat-yearly,
.stat-products {
  font-size: 0.75rem;
  opacity: 0.7;
  font-weight: 500;
}

.stat-change.positive {
  color: #10B981;
}

.stat-card.primary .stat-change.positive {
  color: #34D399;
}

/* Two Column Layout */
.two-column-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Section */
.section {
  background: white;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
}

.section-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-btn:hover {
  background: #F3F4F6;
  border-color: #D1D5DB;
}

.sort-btn svg {
  width: 16px;
  height: 16px;
}

.chart-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 32px;
  margin-bottom: 24px;
  padding: 24px;
  background: #F9FAFB;
  border-radius: 16px;
}

.pie-chart-wrapper {
  position: relative;
  width: 300px;
  height: 300px;
}

.pie-chart {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.pie-chart-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.pie-chart-total {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  line-height: 1.2;
}

.pie-chart-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 16px;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  flex-shrink: 0;
}

.legend-label {
  flex: 1;
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.legend-value {
  font-size: 1rem;
  font-weight: 700;
  color: #111;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.section-title svg {
  color: #6B7280;
}

/* Status Cards */
.status-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}

.status-card {
  background: #F9FAFB;
  border-radius: 14px;
  padding: 20px;
  text-align: center;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.status-card:hover {
  border-color: #E5E7EB;
  transform: translateY(-2px);
}

.status-card.trial {
  background: #FEF3C7;
  border-color: #FCD34D;
}

.status-card.active {
  background: #D1FAE5;
  border-color: #34D399;
}

.status-card.expired {
  background: #FEE2E2;
  border-color: #FCA5A5;
}

.status-card.cancelled {
  background: #F3F4F6;
  border-color: #D1D5DB;
}

.status-card.payment {
  background: #DBEAFE;
  border-color: #93C5FD;
}

.status-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  background: rgba(255, 255, 255, 0.6);
}

.status-card.trial .status-icon-wrapper {
  color: #92400E;
}

.status-card.active .status-icon-wrapper {
  color: #065F46;
}

.status-card.expired .status-icon-wrapper {
  color: #991B1B;
}

.status-card.cancelled .status-icon-wrapper {
  color: #4B5563;
}

.status-card.payment .status-icon-wrapper {
  color: #1E40AF;
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-value {
  font-size: 1.5rem;
  font-weight: 900;
  color: #111;
  line-height: 1.2;
}

.status-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Owners Info */
.owners-info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.owner-stat-card {
  background: #F9FAFB;
  border-radius: 14px;
  padding: 24px;
  text-align: center;
  border: 2px solid #E5E7EB;
  transition: all 0.2s;
}

.owner-stat-card:hover {
  border-color: #D1D5DB;
  transform: translateY(-2px);
}

.owner-stat-card.warning {
  background: #FEF3C7;
  border-color: #FCD34D;
}

.owner-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: #6B7280;
}

.owner-stat-card.warning .owner-icon {
  background: rgba(255, 255, 255, 0.6);
  color: #92400E;
}

.owner-stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 6px;
  line-height: 1.2;
}

.owner-stat-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 500;
  line-height: 1.3;
}

/* Attention List */
.attention-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.attention-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #FEF3C7;
  border-radius: 12px;
  border: 1px solid #FCD34D;
  transition: all 0.2s;
}

.attention-item:hover {
  background: #FDE68A;
  transform: translateX(4px);
}

.attention-shop-info {
  flex: 1;
}

.attention-shop-name {
  font-weight: 700;
  color: #111;
  margin-bottom: 4px;
  font-size: 0.9375rem;
}

.attention-shop-meta {
  font-size: 0.8125rem;
  color: #6B7280;
}

.attention-days {
  margin-left: 16px;
}

.days-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 700;
  white-space: nowrap;
}

.days-badge.critical {
  background: #FEE2E2;
  color: #991B1B;
}

.days-badge.warning {
  background: #FEF3C7;
  color: #92400E;
}

.days-badge.normal {
  background: #D1FAE5;
  color: #065F46;
}

/* Recent List */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #F9FAFB;
  border-radius: 12px;
  transition: all 0.2s;
}

.recent-item:hover {
  background: #F3F4F6;
  transform: translateX(4px);
}

.recent-shop-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.recent-shop-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.recent-shop-info {
  flex: 1;
  min-width: 0;
}

.recent-shop-name {
  font-weight: 600;
  color: #111;
  margin-bottom: 2px;
  font-size: 0.9375rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-shop-date {
  font-size: 0.75rem;
  color: #6B7280;
}

.recent-status {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
}

.recent-status.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.recent-status.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.recent-status.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.recent-status.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  margin-top: 12px;
  color: #111;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.view-all-link:hover {
  color: #6B7280;
}

/* Responsive */
@media (max-width: 1400px) {
  .two-column-grid {
    grid-template-columns: 1fr 350px;
  }
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }
  
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
  
  .chart-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .pie-chart-wrapper {
    margin: 0 auto;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .two-column-grid {
    grid-template-columns: 1fr;
  }
  
  .status-cards {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .owners-info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
  
  .stats-grid,
  .status-cards,
  .owners-info-grid {
    grid-template-columns: 1fr;
  }
  
  .admin-header {
    padding: 24px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
  }
  
  .admin-title {
    font-size: 2rem;
  }
  
  .admin-content {
    padding: 20px;
  }
}
</style>
