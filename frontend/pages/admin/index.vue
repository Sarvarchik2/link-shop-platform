<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <div class="header-left">
      <h1 class="page-title">Boshqaruv paneli</h1>
      <p class="page-subtitle">Xush kelibsiz! Do'koningiz holati.</p>
      </div>
      <div class="header-right">
        <span class="current-date">{{ formatDate(new Date()) }}</span>
      </div>
    </div>

    <div v-if="pending" class="loading-state">
      <div class="spinner"></div>
      <p>Yuklanmoqda...</p>
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
            <div class="stat-comparison" v-if="periodStats.orders > 0">
              <span class="comparison-value">{{ periodStats.orders }} ta buyurtma</span>
            </div>
          </div>
          <div class="stat-value">${{ periodStats.sales.toFixed(2) }}</div>
          <div class="stat-label">{{ periodLabel }} daromad</div>
          <div class="stat-note" v-if="stats?.orders_by_status?.cancelled > 0">
            {{ stats.orders_by_status.cancelled }} ta bekor qilingan hisobga olinmagan
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
          <div class="stat-label">Jami buyurtmalar</div>
          <div class="stat-breakdown">
            <span class="breakdown-item pending" v-if="stats?.orders_by_status?.pending">
              {{ stats.orders_by_status.pending }} ta kutilmoqda
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
          <div class="stat-label">Jami foydalanuvchilar</div>
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
          <div class="stat-label">Jami mahsulotlar</div>
        </div>
      </div>

      <!-- Orders by Status -->
      <div class="section orders-section">
        <h2 class="section-title">Status bo'yicha buyurtmalar</h2>
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
              <span class="status-label">Kutilmoqda</span>
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
              <span class="status-label">Jarayonda</span>
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
              <span class="status-label">Yetkazilmoqda</span>
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
              <span class="status-label">Yetkazildi</span>
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
              <span class="status-label">Bekor qilindi</span>
            </div>
            <div class="status-bar">
              <div class="status-fill" :style="{ width: getStatusPercent('cancelled') + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Period Comparison -->
      <div class="section comparison-section">
        <h2 class="section-title">Umumiy ko'rsatkichlar</h2>
        <div class="comparison-grid">
          <div class="comparison-card">
            <div class="comparison-header">
              <span class="comparison-title">Bugun</span>
              <span class="comparison-badge today">Jonli</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.today_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Daromad</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.today_orders || 0 }}</span>
                <span class="comp-label">Buyurtmalar</span>
              </div>
            </div>
          </div>

          <div class="comparison-card">
            <div class="comparison-header">
              <span class="comparison-title">Bu hafta</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.week_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Daromad</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.week_orders || 0 }}</span>
                <span class="comp-label">Buyurtmalar</span>
              </div>
            </div>
          </div>

          <div class="comparison-card">
            <div class="comparison-header">
              <span class="comparison-title">Bu oy</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.month_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Daromad</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.month_orders || 0 }}</span>
                <span class="comp-label">Buyurtmalar</span>
              </div>
            </div>
          </div>

          <div class="comparison-card total-card">
            <div class="comparison-header">
              <span class="comparison-title">Barcha vaqt</span>
              <span class="comparison-badge total">Jami</span>
            </div>
            <div class="comparison-stats">
              <div class="comparison-stat">
                <span class="comp-value">${{ stats?.total_sales?.toFixed(2) || '0.00' }}</span>
                <span class="comp-label">Daromad</span>
              </div>
              <div class="comparison-stat">
                <span class="comp-value">{{ stats?.total_orders || 0 }}</span>
                <span class="comp-label">Buyurtmalar</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="section quick-actions">
        <h2 class="section-title">Tezkor amallar</h2>
        <div class="actions-grid">
          <NuxtLink to="/admin/products/new" class="action-card">
            <div class="action-icon add">➕</div>
            <div class="action-text">
              <div class="action-title">Mahsulot qo'shish</div>
              <div class="action-subtitle">Yangi mahsulot yaratish</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/orders" class="action-card" :class="{ highlight: (stats?.orders_by_status?.pending || 0) > 0 }">
            <div class="action-icon orders">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
            </div>
            <div class="action-text">
              <div class="action-title">
                Buyurtmalarni boshqarish
                <span v-if="stats?.orders_by_status?.pending" class="action-badge">{{ stats.orders_by_status.pending }}</span>
              </div>
              <div class="action-subtitle">Buyurtmalarni ko'rish va qayta ishlash</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/users" class="action-card">
            <div class="action-icon users">👥</div>
            <div class="action-text">
              <div class="action-title">Foydalanuvchilar</div>
              <div class="action-subtitle">{{ stats?.total_users || 0 }} ta mijoz</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/categories" class="action-card">
            <div class="action-icon">📁</div>
            <div class="action-text">
              <div class="action-title">Kategoriyalar</div>
              <div class="action-subtitle">Kategoriyalarni boshqarish</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/brands" class="action-card">
            <div class="action-icon">🏷️</div>
            <div class="action-text">
              <div class="action-title">Brendlar</div>
              <div class="action-subtitle">Brendlarni boshqarish</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/products" class="action-card">
            <div class="action-icon">🛍️</div>
            <div class="action-text">
              <div class="action-title">Barcha mahsulotlar</div>
              <div class="action-subtitle">{{ stats?.total_products || 0 }} ta mahsulot</div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { token } = useAuth()
const { data: stats, pending } = await useFetch('http://localhost:8000/admin/stats', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const selectedPeriod = ref('all')

const periods = [
  { key: 'today', label: 'Bugun' },
  { key: 'week', label: 'Bu hafta' },
  { key: 'month', label: 'Bu oy' },
  { key: 'all', label: 'Barcha vaqt' }
]

const periodLabel = computed(() => {
  switch (selectedPeriod.value) {
    case 'today': return "Bugungi"
    case 'week': return "Bu haftaning"
    case 'month': return "Bu oyning"
    default: return 'Jami'
  }
})

const periodStats = computed(() => {
  if (!stats.value) return { sales: 0, orders: 0 }
  
  switch (selectedPeriod.value) {
    case 'today':
      return { sales: stats.value.today_sales || 0, orders: stats.value.today_orders || 0 }
    case 'week':
      return { sales: stats.value.week_sales || 0, orders: stats.value.week_orders || 0 }
    case 'month':
      return { sales: stats.value.month_sales || 0, orders: stats.value.month_orders || 0 }
    default:
      return { sales: stats.value.total_sales || 0, orders: stats.value.total_orders || 0 }
  }
})

const getStatusPercent = (status) => {
  if (!stats.value?.total_orders || stats.value.total_orders === 0) return 0
  const count = stats.value.orders_by_status?.[status] || 0
  return Math.round((count / stats.value.total_orders) * 100)
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }).format(date)
}
</script>

<style scoped>
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

.current-date {
  font-size: 0.875rem;
  color: #6B7280;
  background: #F3F4F6;
  padding: 8px 16px;
  border-radius: 8px;
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

.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.action-card {
  background: #F9FAFB;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.action-card:hover {
  background: white;
  border-color: #E5E7EB;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.08);
}

.action-card.highlight {
  background: #FEF3C7;
  border-color: #F59E0B;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-icon svg {
  width: 24px;
  height: 24px;
}

.action-text { flex: 1; }

.action-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-badge {
  font-size: 0.625rem;
  padding: 3px 8px;
  border-radius: 10px;
  background: #EF4444;
  color: white;
  font-weight: 700;
}

.action-subtitle {
  font-size: 0.8rem;
  color: #6B7280;
}

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .status-grid { grid-template-columns: repeat(3, 1fr); }
  .comparison-grid { grid-template-columns: repeat(2, 1fr); }
  .actions-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .dashboard-header { flex-direction: column; gap: 12px; }
  .page-title { font-size: 1.75rem; }
  .current-date { align-self: flex-start; }
  
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
  .actions-grid { grid-template-columns: 1fr; gap: 12px; }
  .action-card { padding: 16px; }
}
</style>
