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
      <span class="mobile-title">Заказы</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar 
      current-route="orders" 
      :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event"
    />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div>
          <h1 class="admin-title">Управление заказами</h1>
          <p class="admin-subtitle">Все заказы со всех магазинов платформы</p>
        </div>
      </div>

      <div class="admin-content">
        <div v-if="error" class="text-center py-12 text-red-500">
          <p class="mt-4">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
          <button @click="refresh" class="mt-4 px-4 py-2 bg-black text-white rounded-lg">Повторить</button>
        </div>
        <div v-else-if="pending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Заказы загружаются...</p>
        </div>

        <div v-else class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-card">
            <div class="order-header">
              <div class="order-info">
                <div class="order-id">Заказ #{{ order.id }}</div>
                <div class="order-date">{{ formatDate(order.created_at) }}</div>
              </div>
              <span :class="['status-badge', getStatusClass(order.status)]">
                {{ getStatusText(order.status) }}
              </span>
            </div>
            
            <div class="order-details">
              <div class="detail-row">
                <span class="detail-label">Клиент:</span>
                <span class="detail-value">{{ getUserName(order.user) }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Телефон:</span>
                <span class="detail-value">{{ order.delivery_phone || order.user?.phone }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Адрес:</span>
                <span class="detail-value">{{ order.delivery_address }}, {{ order.delivery_city }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Сумма:</span>
                <span class="detail-value amount">${{ order.total_price.toFixed(2) }}</span>
              </div>
            </div>
            
            <div v-if="order.items && order.items.length > 0" class="order-items">
              <div class="items-title">Товары:</div>
              <NuxtLink v-for="item in order.items" :key="item.product_id" :to="item.shop_slug ? `/${item.shop_slug}/products/${item.product_id}` : `/products/${item.product_id}`" class="order-item">
                <img v-if="item.product_image" :src="item.product_image" :alt="item.product_name" class="item-image" />
                <div class="item-info">
                  <div class="item-name">{{ item.product_name }}</div>
                  <div class="item-details">
                    Количество: {{ item.quantity }} × ${{ item.price.toFixed(2) }}
                  </div>
                </div>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'platform-admin'
})

const { token, logout } = useAuth()
const router = useRouter()
const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const currentRoute = computed(() => 'orders')

const { data: orders, pending, error, refresh } = await useFetch(useRuntimeConfig().public.apiBase + '/platform/admin/orders', {
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
    console.error('[Admin Orders] Ошибка загрузки заказов:', newError)
    console.error('[Admin Orders] Детали ошибки:', {
      message: newError.message,
      statusCode: newError.statusCode,
      statusMessage: newError.statusMessage,
      data: newError.data
    })
  }
}, { immediate: true })

watch(token, () => {
  if (token.value) {
    console.log('[Admin Orders] Токен обновлен, обновляю данные...')
    refresh()
  }
}, { immediate: true })

watch(orders, (newOrders) => {
  if (newOrders) {
    console.log('[Admin Orders] Заказы загружены:', newOrders)
  }
})

const getStatusClass = (status) => {
  const statusMap = {
    'pending': 'status-pending',
    'processing': 'status-processing',
    'shipping': 'status-shipping',
    'delivered': 'status-delivered',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || 'status-pending'
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': 'Ожидает',
    'processing': 'В обработке',
    'shipping': 'Доставляется',
    'delivered': 'Доставлен',
    'cancelled': 'Отменен'
  }
  return statusMap[status] || status
}

const getUserName = (user) => {
  if (!user) return 'Неизвестно'
  return `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.phone
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
/* Базовые стили из shops.vue */
.platform-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
  width: 100%;
}

/* New mobile header styles */
.mobile-header {
  display: none; /* Hidden by default, shown on smaller screens */
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.mobile-header .menu-btn,
.mobile-header .home-btn {
  background: none;
  border: none;
  color: #111;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-header .mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

/* Adjust main content margin for desktop */
.admin-main {
  flex: 1;
  margin-left: 280px; /* Default for desktop */
  min-height: 100vh;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .mobile-header {
    display: flex; /* Show mobile header */
  }

  .admin-main {
    margin-left: 0; /* No margin on smaller screens */
    padding-top: 80px;
    padding-left: 16px;
    padding-right: 16px;
  }
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

@media (max-width: 640px) {
  .admin-title {
    font-size: 1.25rem !important;
    line-height: 1.2 !important;
  }
  
  .admin-header {
    padding: 20px !important;
  }
}

.admin-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
}

.admin-content {
  padding: 40px;
}

@media (max-width: 640px) {
  .admin-content {
    padding: 16px !important;
  }
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #E5E7EB;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-id {
  font-weight: 800;
  font-size: 1.125rem;
  color: #111;
}

.order-date {
  font-size: 0.875rem;
  color: #6B7280;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-pending {
  background: #FEF3C7;
  color: #92400E;
}

.status-processing {
  background: #DBEAFE;
  color: #1E40AF;
}

.status-shipping {
  background: #D1FAE5;
  color: #065F46;
}

.status-delivered {
  background: #D1FAE5;
  color: #065F46;
}

.status-cancelled {
  background: #FEE2E2;
  color: #991B1B;
}

.order-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.detail-row {
  display: flex;
  gap: 8px;
}

.detail-label {
  font-weight: 600;
  color: #6B7280;
  font-size: 0.875rem;
}

.detail-value {
  color: #111;
  font-size: 0.875rem;
}

.detail-value.amount {
  font-weight: 800;
  font-size: 1rem;
}

.order-items {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E5E7EB;
}

.items-title {
  font-weight: 700;
  margin-bottom: 12px;
  color: #111;
}

.order-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #F9FAFB;
  border-radius: 8px;
  margin-bottom: 8px;
}

.item-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: 600;
  margin-bottom: 4px;
  color: #111;
}

.item-details {
  font-size: 0.875rem;
  color: #6B7280;
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
</style>

