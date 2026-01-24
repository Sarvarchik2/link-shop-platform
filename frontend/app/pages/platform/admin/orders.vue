<template>
  <div class="platform-admin-orders">
    <PlatformAdminSidebar :current-route="'orders'" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">Все заказы</h1>
            <p class="page-subtitle">Мониторинг транзакций во всех магазинах системы</p>
          </div>
        </div>

        <div class="nav-right">
          <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
            <iconify-icon icon="lucide:rotate-cw" />
          </button>
        </div>
      </header>

      <div class="admin-scroll">
        <!-- Stats summary -->
        <div class="stats-row">
          <div class="mini-stat-box">
            <div class="ms-icon"><iconify-icon icon="lucide:shopping-bag" /></div>
            <div class="ms-body">
              <div class="ms-v">{{ orders?.length || 0 }}</div>
              <div class="ms-l">Всего заказов</div>
            </div>
          </div>
          <div class="mini-stat-box">
            <div class="ms-icon pending"><iconify-icon icon="lucide:clock" /></div>
            <div class="ms-body">
              <div class="ms-v">{{ pendingCount }}</div>
              <div class="ms-l">Ожидают</div>
            </div>
          </div>
          <div class="mini-stat-box">
            <div class="ms-icon done"><iconify-icon icon="lucide:check-circle" /></div>
            <div class="ms-body">
              <div class="ms-v">{{ deliveredCount }}</div>
              <div class="ms-l">Доставлено</div>
            </div>
          </div>
          <div class="mini-stat-box">
            <div class="ms-icon sum"><iconify-icon icon="lucide:banknote" /></div>
            <div class="ms-body">
              <div class="ms-v">{{ formatPrice(totalRevenue) }}</div>
              <div class="ms-l">Общий оборот</div>
            </div>
          </div>
        </div>

        <div v-if="pending" class="loading-state">
          <div class="loader"></div>
        </div>

        <div v-else-if="!orders || orders.length === 0" class="empty-state">
          <iconify-icon icon="lucide:package-x" />
          <h2>Заказов пока нет</h2>
          <p>Когда покупатели начнут совершать покупки в магазинах, они появятся в этом списке.</p>
        </div>

        <div v-else class="table-white-card">
          <div class="table-responsive">
            <table class="modern-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Магазин / Клиент</th>
                  <th>Статус</th>
                  <th>Товары</th>
                  <th>Сумма</th>
                  <th>Дата</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in orders" :key="order.id">
                  <td><span class="id-tag">#{{ order.id }}</span></td>
                  <td>
                    <div class="order-client-cell">
                      <div class="oc-shop">Магазин ID: {{ order.shop_id || '—' }}</div>
                      <div class="oc-name">{{ getUserName(order.user) }}</div>
                      <div class="oc-phone">{{ order.delivery_phone || order.user?.phone }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="status-pill" :class="order.status">
                      {{ getStatusText(order.status) }}
                    </div>
                  </td>
                  <td>
                    <div class="items-preview">
                      <div v-for="item in order.items.slice(0, 3)" :key="item.product_id" class="item-mini-img">
                        <img v-if="item.product_image" :src="item.product_image" />
                        <div v-else class="item-placeholder">?</div>
                      </div>
                      <div v-if="order.items.length > 3" class="items-more">+{{ order.items.length - 3 }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="amount-cell">
                      <div class="a-val">{{ formatPrice(order.total_price) }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="date-cell">
                      <div class="d-val">{{ formatDate(order.created_at) }}</div>
                      <div class="d-time">{{ formatTime(order.created_at) }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="action-btns">
                      <button class="act-btn" @click="viewOrder(order)" title="Детали"><iconify-icon
                          icon="lucide:eye" /></button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { token, logout } = useAuth()
const { formatPrice } = useCurrency()
const toast = useToast()
const config = useRuntimeConfig()
const { t, locale } = useI18n()

// Use internal URL for SSR, public URL for client
const apiBase = process.server ? config.apiBaseInternal : config.public.apiBase


definePageMeta({ middleware: 'platform-admin' })

const sidebarOpen = ref(false)
const handleLogout = () => { logout(); toast.success('Вы вышли') }

const { data: orders, pending, error, refresh } = useFetch(apiBase + '/platform/admin/orders', {
  lazy: true, watch: [token],
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const pendingCount = computed(() => orders.value?.filter(o => o.status === 'pending').length || 0)
const deliveredCount = computed(() => orders.value?.filter(o => o.status === 'delivered').length || 0)
const totalRevenue = computed(() => orders.value?.reduce((sum, o) => sum + (o.total_price || 0), 0) || 0)

const getStatusText = (s) => ({
  'pending': 'Ожидает', 'processing': 'В обработке', 'shipping': 'Доставка',
  'delivered': 'Доставлен', 'cancelled': 'Отменен'
}[s] || s)

const getUserName = (u) => u ? `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.phone : 'Гость'
const formatDate = (d) => new Date(d).toLocaleDateString(locale.value, { day: 'numeric', month: 'short', year: 'numeric' })
const formatTime = (d) => new Date(d).toLocaleTimeString(locale.value, { hour: '2-digit', minute: '2-digit' })

const viewOrder = (o) => toast.info(`Просмотр заказа #${o.id}`)
</script>

<style scoped>
.platform-admin-orders {
  background: #f8fafc;
  min-height: 100vh;
  display: flex;
}

.admin-main {
  flex: 1;
  margin-left: 280px;
  display: flex;
  flex-direction: column;
  transition: all 0.4s;
}

.top-nav {
  padding: 32px;
  background: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mobile-menu-btn {
  display: none;
  width: 44px;
  height: 44px;
  background: #f1f5f9;
  border: none;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 950;
  margin: 0;
  letter-spacing: -1px;
}

.page-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin-top: 4px;
  font-weight: 600;
}

.refresh-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  transition: all 0.2s;
}

.refresh-btn:hover {
  border-color: #111;
}

.refresh-btn.loading iconify-icon {
  animation: spin 1s linear infinite;
}

.admin-scroll {
  padding: 32px;
  flex: 1;
  overflow-y: auto;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.mini-stat-box {
  background: white;
  padding: 24px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
}

.ms-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.ms-icon.pending {
  background: #fef3c7;
  color: #92400e;
}

.ms-icon.done {
  background: #dcfce7;
  color: #166534;
}

.ms-icon.sum {
  background: #e0e7ff;
  color: #4338ca;
}

.ms-v {
  font-size: 1.4rem;
  font-weight: 950;
  color: #111;
}

.ms-l {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
}

.table-white-card {
  background: white;
  border-radius: 28px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  overflow: hidden;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.modern-table th {
  padding: 20px 24px;
  background: #f8fafc;
  font-size: 0.75rem;
  font-weight: 850;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #f1f5f9;
}

.modern-table td {
  padding: 16px 24px;
  border-bottom: 1px solid #f8fafc;
  vertical-align: middle;
}

.id-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 800;
}

.order-client-cell {
  display: grid;
  gap: 2px;
}

.oc-shop {
  font-size: 0.7rem;
  color: #94a3b8;
  font-weight: 800;
  text-transform: uppercase;
}

.oc-name {
  font-weight: 850;
  color: #111;
  font-size: 0.95rem;
}

.oc-phone {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
}

.status-pill {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 900;
  text-transform: uppercase;
}

.status-pill.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-pill.delivered {
  background: #dcfce7;
  color: #166534;
}

.status-pill.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.status-pill.processing {
  background: #e0e7ff;
  color: #4338ca;
}

.items-preview {
  display: flex;
  align-items: center;
  gap: 4px;
}

.item-mini-img {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
  background: #f8fafc;
}

.item-mini-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  color: #94a3b8;
  font-weight: 900;
}

.items-more {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 0.7rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}

.amount-cell {
  font-weight: 900;
  color: #111;
  font-size: 1rem;
}

.date-cell {
  font-size: 0.85rem;
  font-weight: 750;
}

.d-time {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 2px;
}

.act-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1.5px solid #e2e8f0;
  background: white;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.act-btn:hover {
  border-color: #111;
  color: #111;
}

.empty-state {
  text-align: center;
  padding: 100px 0;
}

.empty-state iconify-icon {
  font-size: 4rem;
  color: #cbd5e1;
  margin-bottom: 24px;
}

.empty-state h2 {
  font-weight: 950;
  font-size: 1.75rem;
  margin-bottom: 12px;
}

.empty-state p {
  font-weight: 600;
  color: #64748b;
  max-width: 400px;
  margin: 0 auto;
}

.loader {
  width: 40px;
  height: 40px;
  border: 4px solid #f1f5f9;
  border-top-color: #111;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
  }

  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
