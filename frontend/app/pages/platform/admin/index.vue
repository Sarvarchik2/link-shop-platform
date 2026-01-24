<template>
  <div class="platform-admin-dashboard">
    <PlatformAdminSidebar :current-route="currentRoute" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <main class="dashboard-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('platformAdmin.dashboard.title') }}</h1>
            <p class="page-subtitle">{{ $t('platformAdmin.dashboard.welcome') }}</p>
          </div>
        </div>

        <div class="nav-right">
          <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
            <iconify-icon icon="lucide:rotate-cw" />
            <span>{{ $t('platformAdmin.dashboard.refresh') }}</span>
          </button>
        </div>
      </header>

      <div class="dashboard-scroll">
        <div v-if="error" class="error-container">
          <iconify-icon icon="lucide:alert-circle" class="error-icon" />
          <h3>{{ $t('platformAdmin.dashboard.errorUnknown') }}</h3>
          <p>{{ error.message }}</p>
          <button @click="refresh" class="retry-btn">{{ $t('platformAdmin.dashboard.retry') }}</button>
        </div>

        <template v-else>
          <!-- Dashboard Period Filter -->
          <div class="filter-bar">
            <div class="period-pills">
              <button v-for="p in periods" :key="p.key" @click="selectedPeriod = p.key"
                :class="['period-pill', { active: selectedPeriod === p.key }]">
                {{ p.label }}
              </button>
            </div>
          </div>

          <!-- KPI Grid -->
          <div class="kpi-grid">
            <div class="kpi-card shops">
              <div class="kpi-content">
                <div class="kpi-label">{{ $t('platformAdmin.dashboard.stats.totalShops') }}</div>
                <div class="kpi-value">{{ subscriptionStats.totalShops }}</div>
                <div class="kpi-meta positive" v-if="shopsRecentlyAdded > 0">
                  <iconify-icon icon="lucide:trending-up" />
                  <span>+{{ shopsRecentlyAdded }} {{ $t('platformAdmin.dashboard.perPeriod') }}</span>
                </div>
              </div>
              <div class="kpi-icon-wrap">
                <iconify-icon icon="lucide:store" />
              </div>
            </div>

            <div class="kpi-card revenue">
              <div class="kpi-content">
                <div class="kpi-label">{{ $t('platformAdmin.dashboard.stats.revenue') }}</div>
                <div class="kpi-value">{{ formatPrice(subscriptionStats.monthlyRevenue) }}</div>
                <div class="kpi-meta">
                  <iconify-icon icon="lucide:calendar" />
                  <span>{{ $t('platformAdmin.dashboard.stats.forecast') }}: {{
                    formatPrice(subscriptionStats.monthlyRevenue * 12) }}{{ $t('platformAdmin.dashboard.perYear')
                    }}</span>
                </div>
              </div>
              <div class="kpi-icon-wrap">
                <iconify-icon icon="lucide:dollar-sign" />
              </div>
            </div>

            <div class="kpi-card active-shops">
              <div class="kpi-content">
                <div class="kpi-label">{{ $t('platformAdmin.dashboard.stats.activeShops') }}</div>
                <div class="kpi-value">{{ subscriptionStats.activeShops }}</div>
                <div class="kpi-progress">
                  <div class="progress-bg">
                    <div class="progress-bar" :style="{ width: activeShopsPercentage + '%' }"></div>
                  </div>
                  <span class="progress-text">{{ activeShopsPercentage }}% {{ $t('platformAdmin.dashboard.ofTotal')
                    }}</span>
                </div>
              </div>
              <div class="kpi-icon-wrap">
                <iconify-icon icon="lucide:check-circle" />
              </div>
            </div>

            <div class="kpi-card users">
              <div class="kpi-content">
                <div class="kpi-label">{{ $t('platformAdmin.dashboard.stats.users') }}</div>
                <div class="kpi-value">{{ periodStats?.users || 0 }}</div>
                <div class="kpi-meta">
                  <iconify-icon icon="lucide:package" />
                  <span>{{ periodStats?.products || 0 }} {{ $t('platformAdmin.dashboard.productsCreated') }}</span>
                </div>
              </div>
              <div class="kpi-icon-wrap">
                <iconify-icon icon="lucide:users" />
              </div>
            </div>
          </div>

          <!-- Charts Row -->
          <div class="charts-row">
            <div class="white-card chart-card wide">
              <div class="card-header">
                <div class="header-main">
                  <h3 class="card-title">{{ $t('platformAdmin.dashboard.salesTrends') }}</h3>
                  <span class="card-badge">{{ $t('platformAdmin.dashboard.last30Days') }}</span>
                </div>
                <div class="chart-summary">
                  <div class="cs-item">
                    <span class="cs-label">{{ $t('platformAdmin.dashboard.total') }}</span>
                    <span class="cs-val">{{ formatPrice(stats?.total_sales || 0) }}</span>
                  </div>
                </div>
              </div>
              <div class="chart-wrapper">
                <ClientOnly>
                  <AdminChart type="line" :data="salesChartData" :options="lineOptions" />
                </ClientOnly>
              </div>
            </div>
            <div class="white-card chart-card">
              <div class="card-header">
                <h3 class="card-title">{{ $t('platformAdmin.dashboard.planDistribution') }}</h3>
              </div>
              <div class="chart-wrapper compact">
                <ClientOnly>
                  <AdminChart type="doughnut" :data="planChartData" :options="donutOptions" />
                </ClientOnly>
              </div>
            </div>
          </div>

          <!-- Top Shops Row -->
          <div class="white-card top-shops-card">
            <div class="card-header">
              <h3 class="card-title">{{ $t('platformAdmin.dashboard.topShops') }}</h3>
              <NuxtLink :to="localePath('/platform/admin/shops')" class="ghost-btn-sm">
                {{ $t('platformAdmin.dashboard.viewAll') }}
              </NuxtLink>
            </div>
            <div class="top-shops-table-wrap">
              <table class="top-shops-table">
                <thead>
                  <tr>
                    <th>{{ $t('platformAdmin.shops.name') }}</th>
                    <th>{{ $t('platformAdmin.dashboard.orders') }}</th>
                    <th class="text-right">{{ $t('platformAdmin.dashboard.revenue') }}</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="shop in stats?.top_shops || []" :key="shop.id">
                    <td>
                      <div class="shop-entry">
                        <div class="se-icon">{{ shop.name.charAt(0) }}</div>
                        <span class="se-name">{{ shop.name }}</span>
                      </div>
                    </td>
                    <td>
                      <div class="order-stat">
                        <span class="os-val">{{ shop.orders_count }}</span>
                        <span class="os-label">{{ $t('platformAdmin.dashboard.ordersShort') }}</span>
                      </div>
                    </td>
                    <td class="text-right">
                      <span class="revenue-val">{{ formatPrice(shop.revenue) }}</span>
                    </td>
                    <td class="text-right">
                      <NuxtLink :to="localePath(`/platform/admin/shops?search=${shop.name}`)" class="action-icon">
                        <iconify-icon icon="lucide:external-link" />
                      </NuxtLink>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-if="!stats?.top_shops?.length" class="empty-table">
                {{ $t('common.noData') }}
              </div>
            </div>
          </div>

          <!-- Secondary Grid -->
          <div class="main-grid">
            <!-- Left: Chart & Breakdown -->
            <div class="grid-col left">
              <div class="white-card">
                <div class="card-header">
                  <h3 class="card-title">{{ $t('platformAdmin.dashboard.subscriptionStats') }}</h3>
                  <div class="card-actions">
                    <button @click="toggleSortExpiry" class="ghost-btn" :class="{ active: sortByExpiry }">
                      <iconify-icon icon="lucide:filter" />
                    </button>
                  </div>
                </div>

                <div class="pie-section">
                  <div class="chart-box">
                    <svg viewBox="0 0 100 100" class="donut">
                      <circle cx="50" cy="50" r="40" class="donut-ring" />
                      <circle cx="50" cy="50" r="40" class="donut-segment trial"
                        :stroke-dasharray="getDonutArray('trial')" stroke-dashoffset="0" />
                      <circle cx="50" cy="50" r="40" class="donut-segment active"
                        :stroke-dasharray="getDonutArray('active')" :stroke-dashoffset="getDonutOffset('active')" />
                      <circle cx="50" cy="50" r="40" class="donut-segment expired"
                        :stroke-dasharray="getDonutArray('expired')" :stroke-dashoffset="getDonutOffset('expired')" />
                    </svg>
                    <div class="chart-center">
                      <div class="total-v">{{ subscriptionStats.totalShops }}</div>
                      <div class="total-l">{{ $t('platformAdmin.dashboard.shopsShort') }}</div>
                    </div>
                  </div>

                  <div class="chart-legend">
                    <div v-for="(val, key) in subscriptionStats.byStatus" :key="key" class="legend-row">
                      <div class="status-dot" :class="key"></div>
                      <span class="status-n">{{ getStatusLabel(key) }}</span>
                      <span class="status-v">{{ val }}</span>
                    </div>
                  </div>
                </div>

                <div class="owners-summary">
                  <div class="summary-item">
                    <div class="si-val">{{ uniqueOwners }}</div>
                    <div class="si-label">{{ $t('platformAdmin.dashboard.uniqueOwners') }}</div>
                  </div>
                  <div class="si-divider"></div>
                  <div class="summary-item">
                    <div class="si-val">{{ shopsWithActiveSubscriptions }}</div>
                    <div class="si-label">{{ $t('platformAdmin.dashboard.activeSubs') }}</div>
                  </div>
                </div>
              </div>

              <div class="white-card danger-zone" v-if="shopsNeedingRenewal > 0">
                <div class="danger-header">
                  <iconify-icon icon="lucide:alert-triangle" />
                  <span>{{ $t('platformAdmin.dashboard.attention') }}</span>
                </div>
                <div class="attention-list">
                  <div v-for="shop in shopsExpiringSoon" :key="shop.id" class="attn-item">
                    <div class="attn-info">
                      <div class="attn-name">{{ shop.name }}</div>
                      <div class="attn-date">{{ $t('platformAdmin.dashboard.expires') }} {{
                        formatDate(shop.subscription_expires_at) }}</div>
                    </div>
                    <div class="attn-badge" :class="getDaysBadgeClass(getDaysUntilExpiry(shop))">
                      {{ getDaysUntilExpiry(shop) }}{{ $t('platformAdmin.plans.days') }}
                    </div>
                  </div>
                </div>
                <NuxtLink :to="localePath('/platform/admin/shops')" class="more-link">
                  {{ $t('platformAdmin.dashboard.allShops') }} <iconify-icon icon="lucide:chevron-right" />
                </NuxtLink>
              </div>
            </div>

            <!-- Right: Recent Activity -->
            <div class="grid-col right">
              <div class="white-card">
                <div class="card-header">
                  <h3 class="card-title">{{ $t('platformAdmin.dashboard.recentShops') }}</h3>
                </div>
                <div class="recent-shops-list">
                  <div v-for="shop in recentShops" :key="shop.id" class="shop-row">
                    <div class="shop-avatar">
                      <img v-if="shop.logo_url" :src="shop.logo_url" />
                      <span v-else>{{ shop.name.charAt(0) }}</span>
                    </div>
                    <div class="shop-details">
                      <div class="shop-n">{{ shop.name }}</div>
                      <div class="shop-o">{{ shop.owner_name || $t('common.create') + ': ' + formatDate(shop.created_at)
                        }}</div>
                    </div>
                    <div class="shop-status-badge" :class="shop.subscription_status">
                      {{ getStatusText(shop.subscription_status) }}
                    </div>
                  </div>
                </div>
                <NuxtLink :to="localePath('/platform/admin/shops')" class="more-link">
                  {{ $t('platformAdmin.dashboard.viewAll') }} <iconify-icon icon="lucide:chevron-right" />
                </NuxtLink>
              </div>

              <!-- Pending Requests Card if any -->
              <div class="white-card" v-if="pendingRequestsCount > 0">
                <div class="card-header highlight">
                  <h3 class="card-title">{{ $t('platformAdmin.dashboard.subRequests') }}</h3>
                  <div class="badge-new">{{ pendingRequestsCount }}</div>
                </div>
                <div class="request-mini-list">
                  <p>{{ $t('platformAdmin.dashboard.newRequestsDesc') }}</p>
                </div>
                <NuxtLink :to="localePath('/platform/admin/subscription-requests')" class="primary-btn-sm">
                  {{ $t('platformAdmin.dashboard.goToRequests') }}
                </NuxtLink>
              </div>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t, locale } = useI18n()
const { formatPrice } = useCurrency()
const { token, logout } = useAuth()
const config = useRuntimeConfig()
const localePath = useLocalePath()
const route = useRoute()

// Use internal URL for SSR, public URL for client
const apiBase = process.server ? config.apiBaseInternal : config.public.apiBase

definePageMeta({ middleware: 'platform-admin' })

const sidebarOpen = ref(false)
const selectedPeriod = ref('all')
const sortByExpiry = ref(false)

// Chart Computeds
const salesChartData = computed(() => {
  const history = stats.value?.history || []
  return {
    labels: history.map(h => formatDate(h.date)),
    datasets: [
      {
        label: t('platformAdmin.dashboard.stats.revenue'),
        data: history.map(h => h.sales),
        borderColor: '#db2777',
        backgroundColor: 'rgba(219, 39, 119, 0.05)',
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 5
      },
      {
        label: t('platformAdmin.dashboard.orders'),
        data: history.map(h => h.orders),
        borderColor: '#0284c7',
        backgroundColor: 'transparent',
        fill: false,
        tension: 0.4,
        pointRadius: 0,
        borderDash: [5, 5]
      }
    ]
  }
})

const planChartData = computed(() => {
  const plans = stats.value?.plan_distribution || []
  return {
    labels: plans.map(p => p.name),
    datasets: [
      {
        data: plans.map(p => p.count),
        backgroundColor: ['#10b981', '#3b82f6', '#fbbf24', '#f472b6', '#8b5cf6', '#64748b'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }
    ]
  }
})

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: '#111',
      padding: 12,
      cornerRadius: 12
    }
  },
  hover: { mode: 'index', intersect: false },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(0,0,0,0.03)', drawBorder: false },
      ticks: { font: { size: 10, weight: '700' }, color: '#94a3b8' }
    },
    x: {
      grid: { display: false },
      ticks: { font: { size: 10, weight: '700' }, color: '#94a3b8', maxRotation: 0 }
    }
  }
}

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: { size: 11, weight: '700' }
      }
    }
  }
}

const handleLogout = () => {
  logout()
  useToast().success(t('auth.loggedOut'))
}

const toggleSortExpiry = () => { sortByExpiry.value = !sortByExpiry.value }

const periods = computed(() => [
  { key: 'today', label: t('platformAdmin.dashboard.periods.today') },
  { key: 'week', label: t('platformAdmin.dashboard.periods.week') },
  { key: 'month', label: t('platformAdmin.dashboard.periods.month') },
  { key: 'all', label: t('platformAdmin.dashboard.periods.all') }
])

const currentRoute = computed(() => {
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

// Statistics API
const { data: stats, pending, refresh, error } = useFetch(apiBase + '/platform/admin/stats', {
  lazy: true,
  watch: [token],
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

// Shops Data API
const { data: shops } = useFetch(apiBase + '/platform/shops', {
  lazy: true,
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

// Request Data (for badge)
const { data: requests } = useFetch(apiBase + '/platform/admin/subscription-requests', {
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` })),
  server: false
})
const pendingRequestsCount = computed(() => requests.value?.filter(r => r.status === 'pending').length || 0)


const getPeriodRange = () => {
  const now = new Date()
  let startDate = null
  switch (selectedPeriod.value) {
    case 'today':
      startDate = new Date(now).setHours(0, 0, 0, 0); break
    case 'week':
      const diff = now.getDate() - now.getDay() + (now.getDay() === 0 ? -6 : 1)
      startDate = new Date(now.setDate(diff)).setHours(0, 0, 0, 0); break
    case 'month':
      startDate = new Date(now.getFullYear(), now.getMonth(), 1).setHours(0, 0, 0, 0); break
    default: startDate = null
  }
  return { startDate }
}

const filteredShops = computed(() => {
  if (!shops.value) return []
  if (selectedPeriod.value === 'all') return shops.value
  const { startDate } = getPeriodRange()
  if (!startDate) return shops.value
  return shops.value.filter(s => new Date(s.created_at) >= startDate)
})

const subscriptionStats = computed(() => {
  const list = filteredShops.value
  if (selectedPeriod.value === 'all' && stats.value?.subscriptions_mrr !== undefined) {
    return {
      totalShops: stats.value.total_shops || 0,
      activeShops: stats.value.active_shops || 0,
      monthlyRevenue: stats.value.subscriptions_mrr || 0,
      byStatus: {
        trial: stats.value.subscriptions_trial || 0,
        active: stats.value.subscriptions_active || 0,
        expired: stats.value.subscriptions_expired || 0,
        cancelled: 0
      }
    }
  }

  const active = list.filter(s => s.is_active && (s.subscription_status === 'active' || s.subscription_status === 'trial'))
  const statusCounts = {
    trial: list.filter(s => s.subscription_status === 'trial').length,
    active: list.filter(s => s.subscription_status === 'active').length,
    expired: list.filter(s => s.subscription_status === 'expired').length,
    cancelled: list.filter(s => s.subscription_status === 'cancelled').length
  }

  return {
    totalShops: list.length,
    activeShops: active.length,
    monthlyRevenue: statusCounts.active * 29,
    byStatus: statusCounts
  }
})

const periodStats = computed(() => {
  if (!stats.value) return null
  if (selectedPeriod.value === 'all') return {
    users: stats.value.total_users || 0,
    products: stats.value.total_products || 0,
    sales: stats.value.total_sales || 0
  }
  return {
    users: stats.value[`${selectedPeriod.value}_orders`] || 0,
    sales: stats.value[`${selectedPeriod.value}_sales`] || 0
  }
})

const activeShopsPercentage = computed(() =>
  subscriptionStats.value.totalShops ? Math.round((subscriptionStats.value.activeShops / subscriptionStats.value.totalShops) * 100) : 0
)

const uniqueOwners = computed(() => new Set(filteredShops.value.map(s => s.owner_id)).size)
const shopsWithActiveSubscriptions = computed(() => filteredShops.value.filter(s => s.subscription_status === 'active').length)

const shopsExpiringSoon = computed(() => {
  const now = new Date()
  return (shops.value || [])
    .filter(s => {
      if (!s.subscription_expires_at || s.subscription_status !== 'active') return false
      const days = Math.ceil((new Date(s.subscription_expires_at) - now) / (1000 * 60 * 60 * 24))
      return days <= 7 && days > 0
    })
    .sort((a, b) => new Date(a.subscription_expires_at) - new Date(b.subscription_expires_at))
    .slice(0, 5)
})

const shopsNeedingRenewal = computed(() => shopsExpiringSoon.value.length)

const recentShops = computed(() =>
  [...(filteredShops.value || [])].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 7)
)

const shopsRecentlyAdded = computed(() => {
  if (selectedPeriod.value !== 'all') return filteredShops.value.length
  const monthAgo = new Date().setMonth(new Date().getMonth() - 1)
  return filteredShops.value.filter(s => new Date(s.created_at) >= monthAgo).length
})

// Helpers
const getDaysUntilExpiry = (shop) => {
  if (!shop.subscription_expires_at) return 0
  return Math.ceil((new Date(shop.subscription_expires_at) - new Date()) / (1000 * 60 * 60 * 24))
}
const getDaysBadgeClass = (d) => d <= 3 ? 'critical' : (d <= 7 ? 'warning' : 'normal')
const getStatusText = (s) => t(`platformAdmin.dashboard.status.${s}`) || s
const formatDate = (ds) => ds ? new Date(ds).toLocaleDateString(locale.value, { day: 'numeric', month: 'short' }) : '-'

// Simple Donut Chart Calculation
const getDonutArray = (key) => {
  const total = subscriptionStats.value.totalShops || 1
  const val = subscriptionStats.value.byStatus[key] || 0
  const circ = 2 * Math.PI * 40
  const segment = (val / total) * circ
  return `${segment} ${circ}`
}

const getDonutOffset = (key) => {
  const total = subscriptionStats.value.totalShops || 1
  const order = ['trial', 'active', 'expired', 'cancelled']
  let cumulative = 0
  for (const k of order) {
    if (k === key) break
    cumulative += subscriptionStats.value.byStatus[k] || 0
  }
  const circ = 2 * Math.PI * 40
  return - (cumulative / total) * circ
}

const getStatusLabel = (s) => t(`platformAdmin.dashboard.status.${s}`) || s
</script>

<style scoped>
.platform-admin-dashboard {
  background: #f8fafc;
  min-height: 100vh;
  display: flex;
}

.dashboard-main {
  flex: 1;
  margin-left: 280px;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.top-nav {
  padding: 24px 32px;
  background: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mobile-menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  border: none;
  background: #f1f5f9;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 950;
  margin: 0;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 4px 0 0;
}

.refresh-btn {
  padding: 10px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.refresh-btn.loading iconify-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.dashboard-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.filter-bar {
  margin-bottom: 32px;
  display: flex;
  gap: 16px;
}

.period-pills {
  display: flex;
  background: #fff;
  padding: 4px;
  border-radius: 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
}

.period-pill {
  padding: 8px 16px;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.85rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.period-pill.active {
  background: #111;
  color: #fff;
}

/* KPI Cards */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.kpi-card {
  background: white;
  padding: 24px;
  border-radius: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  position: relative;
  overflow: hidden;
}

.kpi-label {
  font-size: 0.8rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.kpi-value {
  font-size: 1.85rem;
  font-weight: 950;
  color: #111;
  letter-spacing: -1px;
}

.kpi-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  margin-top: 10px;
  color: #64748b;
}

.kpi-meta.positive {
  color: #10b981;
}

.kpi-icon-wrap {
  width: 56px;
  height: 56px;
  background: #f8fafc;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #111;
}

.kpi-card.shops .kpi-icon-wrap {
  background: #f0fdf4;
  color: #16a34a;
}

.kpi-card.revenue .kpi-icon-wrap {
  background: #fdf2f8;
  color: #db2777;
}

.kpi-card.active-shops .kpi-icon-wrap {
  background: #f0f9ff;
  color: #0284c7;
}

.kpi-card.users .kpi-icon-wrap {
  background: #fffbeb;
  color: #d97706;
}

.kpi-progress {
  margin-top: 12px;
  width: 140px;
}

.progress-bg {
  height: 6px;
  background: #f1f5f9;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #111;
  border-radius: 10px;
  transition: width 1s ease;
}

.progress-text {
  font-size: 0.65rem;
  font-weight: 800;
  color: #94a3b8;
  margin-top: 4px;
  display: block;
}

/* Main Grid Layout */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.grid-col {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.white-card {
  background: white;
  padding: 32px;
  border-radius: 28px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 900;
  color: #111;
  margin: 0;
}

.ghost-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: #f8fafc;
  border-radius: 12px;
  cursor: pointer;
  color: #64748b;
}

.ghost-btn.active {
  background: #111;
  color: white;
}

/* Pie / Donut */
.pie-section {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 10px 0;
}

.chart-box {
  position: relative;
  width: 140px;
  height: 140px;
}

.donut {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-ring {
  fill: none;
  stroke: #f1f5f9;
  stroke-width: 12;
}

.donut-segment {
  fill: none;
  stroke-width: 12;
  stroke-linecap: round;
  transition: all 1s;
}

.donut-segment.trial {
  stroke: #fbbf24;
}

.donut-segment.active {
  stroke: #10b981;
}

.donut-segment.expired {
  stroke: #ef4444;
}

.chart-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.total-v {
  font-size: 1.5rem;
  font-weight: 950;
  color: #111;
  line-height: 1;
}

.total-l {
  font-size: 0.7rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
}

.chart-legend {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 0.9rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-dot.trial {
  background: #fbbf24;
}

.status-dot.active {
  background: #10b981;
}

.status-dot.expired {
  background: #ef4444;
}

.status-dot.cancelled {
  background: #94a3b8;
}

.status-v {
  margin-left: auto;
  color: #94a3b8;
}

.owners-summary {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-around;
  text-align: center;
}

.si-val {
  font-size: 1.25rem;
  font-weight: 900;
}

.si-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 700;
}

.si-divider {
  width: 1px;
  background: #f1f5f9;
}

/* Recent Activity */
.recent-shops-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.shop-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.shop-avatar {
  width: 44px;
  height: 44px;
  background: #f1f5f9;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  border: 1.5px solid #e2e8f0;
}

.shop-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 14px;
  object-fit: cover;
}

.shop-details {
  flex: 1;
}

.shop-n {
  font-weight: 800;
  color: #111;
  font-size: 0.95rem;
}

.shop-o {
  font-size: 0.8rem;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 2px;
}

.shop-status-badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
}

.shop-status-badge.active {
  background: #dcfce7;
  color: #166534;
}

.shop-status-badge.trial {
  background: #fef3c7;
  color: #92400e;
}

.shop-status-badge.expired {
  background: #fee2e2;
  color: #991b1b;
}

.more-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  font-weight: 800;
  color: #111;
  text-decoration: none;
  margin-top: 12px;
}

/* Danger Zone */
.danger-zone {
  background: #fff5f5;
  border: 1.5px solid #fee2e2;
}

.danger-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 900;
  color: #ef4444;
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.attn-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 14px 18px;
  border-radius: 16px;
  margin-bottom: 10px;
  border: 1px solid #fee2e2;
}

.attn-name {
  font-weight: 800;
  font-size: 0.9rem;
}

.attn-date {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 700;
  margin-top: 2px;
}

.attn-badge {
  font-size: 0.7rem;
  font-weight: 950;
  padding: 2px 8px;
  border-radius: 20px;
}

.attn-badge.critical {
  background: #ef4444;
  color: white;
}

.attn-badge.warning {
  background: #fbbf24;
  color: white;
}

/* Requests highlight */
.card-header.highlight .card-title {
  color: #2563eb;
}

.badge-new {
  background: #2563eb;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 900;
}

.primary-btn-sm {
  display: block;
  text-align: center;
  padding: 12px;
  background: #111;
  color: white;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.85rem;
  text-decoration: none;
  margin-top: 16px;
}

@media (max-width: 1024px) {
  .dashboard-main {
    margin-left: 0;
  }

  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .top-nav {
    gap: 16px;
  }

  .nav-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .main-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .dashboard-scroll {
    padding: 20px;
  }

  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .pie-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 24px;
  }
}

/* New Metrics CSS */
.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}

.chart-card.wide {
  grid-column: span 1;
}

.chart-wrapper {
  height: 300px;
  position: relative;
}

.chart-wrapper.compact {
  height: 250px;
}

.header-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-badge {
  font-size: 0.65rem;
  font-weight: 800;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 6px;
  width: fit-content;
}

.chart-summary {
  display: flex;
  gap: 24px;
}

.cs-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.cs-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
}

.cs-val {
  font-size: 1.1rem;
  font-weight: 900;
  color: #111;
}

/* Top Shops Table */
.top-shops-card {
  margin-bottom: 32px;
}

.top-shops-table-wrap {
  overflow-x: auto;
}

.top-shops-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}

.top-shops-table th {
  text-align: left;
  padding: 0 12px 12px;
  font-size: 0.75rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.top-shops-table td {
  padding: 16px 12px;
  background: #f8fafc;
  border-top: 1px solid transparent;
  border-bottom: 1px solid transparent;
}

.top-shops-table tr td:first-child {
  border-left: 1px solid transparent;
  border-radius: 16px 0 0 16px;
}

.top-shops-table tr td:last-child {
  border-right: 1px solid transparent;
  border-radius: 0 16px 16px 0;
}

.shop-entry {
  display: flex;
  align-items: center;
  gap: 12px;
}

.se-icon {
  width: 36px;
  height: 36px;
  background: #111;
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 950;
  font-size: 0.9rem;
}

.se-name {
  font-weight: 800;
  color: #111;
}

.order-stat {
  display: flex;
  flex-direction: column;
}

.os-val {
  font-weight: 900;
  color: #111;
  font-size: 1rem;
}

.os-label {
  font-size: 0.65rem;
  color: #64748b;
  font-weight: 700;
}

.revenue-val {
  font-weight: 950;
  color: #111;
  font-size: 1.1rem;
}

.action-icon {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s;
  border: 1px solid #e2e8f0;
}

.action-icon:hover {
  background: #111;
  color: white;
  border-color: #111;
}

.ghost-btn-sm {
  padding: 8px 12px;
  font-size: 0.75rem;
  font-weight: 800;
  color: #64748b;
  background: #f8fafc;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.ghost-btn-sm:hover {
  background: #f1f5f9;
  color: #111;
}

@media (max-width: 1024px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
