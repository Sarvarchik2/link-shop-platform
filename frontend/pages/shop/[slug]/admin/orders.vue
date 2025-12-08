<template>
  <div class="shop-admin-page">
    <!-- Sidebar - same as products.vue -->
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
        <NuxtLink :to="`/shop/${shopSlug}/admin`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>Товары</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/orders`" class="nav-item active">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Заказы</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="nav-item">
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
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <line x1="7" y1="7" x2="7.01" y2="7"></line>
          </svg>
          <span>Бренды</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/banner`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span>Баннер</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/subscription`" class="nav-item">
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
      <div class="admin-header">
        <div>
          <h1 class="admin-title">Заказы</h1>
          <p class="admin-subtitle">Управление заказами магазина</p>
        </div>
        <div class="filters">
          <button 
            v-for="status in statuses" 
            :key="status.value"
            @click="selectedStatus = status.value"
            class="filter-btn"
            :class="{ active: selectedStatus === status.value, [status.value]: true }"
          >
            {{ status.label }}
            <span v-if="getStatusCount(status.value) > 0" class="filter-count">
              {{ getStatusCount(status.value) }}
            </span>
          </button>
        </div>
      </div>

      <div class="admin-content">
        <div v-if="!filteredOrders || filteredOrders.length === 0" class="empty-state">
          <p>Заказы не найдены.</p>
        </div>
        
        <div v-else class="orders-list">
          <div v-for="order in filteredOrders" :key="order.id" class="order-card">
            <div class="order-header" @click="toggleOrder(order.id)">
              <div class="order-main-info">
                <span class="order-id">#{{ order.id }}</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="order-customer">
                <span class="customer-name">{{ order.user?.first_name }} {{ order.user?.last_name }}</span>
                <span class="customer-phone">{{ order.user?.phone }}</span>
              </div>
              <div class="order-total">${{ order.total_price.toFixed(2) }}</div>
              <select 
                :value="order.status" 
                @click.stop
                @change="updateStatus(order.id, $event.target.value)"
                class="status-select"
                :class="order.status"
              >
                <option value="pending">Ожидает</option>
                <option value="processing">В обработке</option>
                <option value="shipping">Доставляется</option>
                <option value="delivered">Доставлен</option>
                <option value="cancelled">Отменен</option>
              </select>
              <button class="expand-btn" :class="{ expanded: expandedOrder === order.id }">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
            </div>
            
            <div v-if="expandedOrder === order.id" class="order-details">
              <!-- Delivery Info -->
              <div class="detail-section">
                <h3 class="detail-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  Доставка
                </h3>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Получатель</span>
                    <span class="detail-value">{{ order.recipient_name || 'N/A' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Телефон</span>
                    <span class="detail-value">{{ order.delivery_phone || 'N/A' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Город</span>
                    <span class="detail-value">{{ order.delivery_city || 'N/A' }}</span>
                  </div>
                  <div class="detail-item full-width">
                    <span class="detail-label">Адрес</span>
                    <span class="detail-value">{{ order.delivery_address || 'N/A' }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Payment Info -->
              <div class="detail-section">
                <h3 class="detail-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                    <line x1="1" y1="10" x2="23" y2="10"></line>
                  </svg>
                  Оплата
                </h3>
                <div class="payment-badge" :class="order.payment_method">
                  {{ order.payment_method === 'cash' ? 'Наличными' : 'Картой' }}
                </div>
              </div>
              
              <!-- Order Items -->
              <div class="detail-section">
                <h3 class="detail-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                  </svg>
                  Товары ({{ order.items?.length || 0 }})
                </h3>
                <div class="items-list">
                  <div v-for="(item, idx) in order.items" :key="idx" class="order-item">
                    <img :src="item.product_image" :alt="item.product_name" class="item-image" />
                    <div class="item-info">
                      <span class="item-name">{{ item.product_name }}</span>
                      <div class="item-options" v-if="item.selected_color || item.selected_size">
                        <span v-if="item.selected_color" class="item-option color">{{ item.selected_color }}</span>
                        <span v-if="item.selected_size" class="item-option size">{{ item.selected_size }}</span>
                      </div>
                      <span class="item-meta">Кол-во: {{ item.quantity }} × ${{ item.price.toFixed(2) }}</span>
                    </div>
                    <span class="item-total">${{ (item.quantity * item.price).toFixed(2) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Notes -->
              <div v-if="order.notes" class="detail-section">
                <h3 class="detail-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                  </svg>
                  Примечания
                </h3>
                <p class="notes-text">{{ order.notes }}</p>
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

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const expandedOrder = ref(null)
const selectedStatus = ref('all')

const statuses = [
  { value: 'all', label: 'Все' },
  { value: 'pending', label: 'Ожидают' },
  { value: 'processing', label: 'В обработке' },
  { value: 'shipping', label: 'Доставляются' },
  { value: 'delivered', label: 'Доставлены' },
  { value: 'cancelled', label: 'Отменены' }
]

const { data: orders, refresh } = await useFetch(`http://localhost:8000/shop/${shopSlug}/admin/orders`, {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const filteredOrders = computed(() => {
  if (!orders.value) return []
  if (selectedStatus.value === 'all') return orders.value
  return orders.value.filter(o => o.status === selectedStatus.value)
})

const getStatusCount = (status) => {
  if (!orders.value) return 0
  if (status === 'all') return orders.value.length
  return orders.value.filter(o => o.status === status).length
}

const toggleOrder = (orderId) => {
  expandedOrder.value = expandedOrder.value === orderId ? null : orderId
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateStatus = async (id, newStatus) => {
  try {
    await $fetch(`http://localhost:8000/shop/${shopSlug}/admin/orders/${id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { status: newStatus }
    })
    refresh()
    useToast().success('Статус заказа обновлен!')
  } catch (e) {
    useToast().error('Ошибка при обновлении статуса')
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

/* Sidebar - same as products.vue */
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

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border: 2px solid rgba(255,255,255,0.2);
  border-radius: 10px;
  background: rgba(255,255,255,0.1);
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: rgba(255,255,255,0.2);
}

.filter-btn.active {
  background: white;
  border-color: white;
  color: #111;
}

.filter-btn.active.pending {
  background: #F59E0B;
  border-color: #F59E0B;
  color: white;
}

.filter-btn.active.processing {
  background: #3B82F6;
  border-color: #3B82F6;
  color: white;
}

.filter-btn.active.shipping {
  background: #6366F1;
  border-color: #6366F1;
  color: white;
}

.filter-btn.active.delivered {
  background: #10B981;
  border-color: #10B981;
  color: white;
}

.filter-btn.active.cancelled {
  background: #EF4444;
  border-color: #EF4444;
  color: white;
}

.filter-count {
  background: rgba(0,0,0,0.2);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
}

.filter-btn.active .filter-count {
  background: rgba(0,0,0,0.1);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  color: #9CA3AF;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.order-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.order-header:hover {
  background: #F9FAFB;
}

.order-main-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 100px;
}

.order-id {
  font-weight: 700;
  font-size: 1rem;
}

.order-date {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.order-customer {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.customer-name {
  font-weight: 600;
}

.customer-phone {
  font-size: 0.875rem;
  color: #6B7280;
}

.order-total {
  font-size: 1.125rem;
  font-weight: 700;
  min-width: 100px;
  text-align: right;
}

.status-select {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  min-width: 120px;
}

.status-select.pending { background: #FFF3E0; color: #EF6C00; }
.status-select.processing { background: #E3F2FD; color: #1565C0; }
.status-select.shipping { background: #FFF8E1; color: #F9A825; }
.status-select.delivered { background: #E8F5E9; color: #2E7D32; }
.status-select.cancelled { background: #FFEBEE; color: #C62828; }

.expand-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #F3F4F6;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.expand-btn.expanded {
  transform: rotate(180deg);
}

.order-details {
  padding: 0 20px 20px;
  border-top: 1px solid #E5E7EB;
  background: #FAFAFA;
}

.detail-section {
  padding: 20px 0;
  border-bottom: 1px solid #E5E7EB;
}

.detail-section:last-child {
  border-bottom: none;
}

.detail-title {
  font-size: 0.875rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-title svg {
  flex-shrink: 0;
  color: #6B7280;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.detail-value {
  font-weight: 500;
  color: #111;
}

.payment-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.payment-badge.cash {
  background: #FEF3C7;
  color: #92400E;
}

.payment-badge.card {
  background: #DBEAFE;
  color: #1E40AF;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 12px;
}

.item-image {
  width: 50px;
  height: 50px;
  object-fit: contain;
  border-radius: 8px;
  background: #F9FAFB;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.item-options {
  display: flex;
  gap: 6px;
  margin: 4px 0;
}

.item-option {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.item-option.color {
  background: #E0E7FF;
  color: #3730A3;
}

.item-option.size {
  background: #FEE2E2;
  color: #991B1B;
}

.item-meta {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.item-total {
  font-weight: 700;
}

.notes-text {
  padding: 12px;
  background: white;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #6B7280;
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
  
  .filters {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 8px;
  }
  
  .filter-btn {
    padding: 8px 14px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  
  .order-header {
    flex-wrap: wrap;
    gap: 12px;
    padding: 16px;
  }
  
  .order-main-info {
    min-width: auto;
    flex: 1;
  }
  
  .order-customer {
    order: 3;
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    padding-top: 12px;
    border-top: 1px solid #F3F4F6;
  }
  
  .order-total {
    min-width: auto;
    font-size: 1rem;
    text-align: left;
  }
  
  .status-select {
    min-width: 100px;
    font-size: 0.7rem;
    padding: 6px 12px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>

