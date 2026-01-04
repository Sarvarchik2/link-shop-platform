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
      <span class="mobile-title">{{ $t('admin.ordersPage.title') }}</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" :current-route="currentRoute" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <div>
            <h1 class="page-title">{{ $t('admin.ordersPage.title') }}</h1>
            <p class="page-subtitle">{{ $t('admin.ordersPage.subtitle') }}</p>
          </div>
          <div class="filters">
            <button v-for="status in statuses" :key="status.value" @click="selectedStatus = status.value"
              class="filter-btn" :class="{ active: selectedStatus === status.value, [status.value]: true }">
              {{ status.label }}
              <span v-if="getStatusCount(status.value) > 0" class="filter-count">
                {{ getStatusCount(status.value) }}
              </span>
            </button>
          </div>
        </div>

        <div class="admin-content">
          <div v-if="!filteredOrders || filteredOrders.length === 0" class="empty-state">
            <p>{{ $t('admin.ordersPage.empty') }}</p>
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
                <select :value="order.status" @click.stop @change="updateStatus(order.id, $event.target.value)"
                  class="status-select" :class="order.status">
                  <option value="pending">{{ $t('admin.status.pending') }}</option>
                  <option value="processing">{{ $t('admin.status.processing') }}</option>
                  <option value="shipping">{{ $t('admin.status.shipping') }}</option>
                  <option value="delivered">{{ $t('admin.status.delivered') }}</option>
                  <option value="cancelled">{{ $t('admin.status.cancelled') }}</option>
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
                    {{ $t('admin.ordersPage.delivery') }}
                  </h3>
                  <div class="detail-grid">
                    <div class="detail-item">
                      <span class="detail-label">{{ $t('admin.ordersPage.recipient') }}</span>
                      <span class="detail-value">{{ order.recipient_name || $t('common.na') }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">{{ $t('admin.ordersPage.phone') }}</span>
                      <span class="detail-value">{{ order.delivery_phone || $t('common.na') }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">{{ $t('admin.ordersPage.city') }}</span>
                      <span class="detail-value">{{ order.delivery_city || $t('common.na') }}</span>
                    </div>
                    <div class="detail-item full-width">
                      <span class="detail-label">{{ $t('admin.ordersPage.address') }}</span>
                      <span class="detail-value">{{ order.delivery_address || $t('common.na') }}</span>
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
                    {{ $t('admin.ordersPage.payment') }}
                  </h3>
                  <div class="payment-badge" :class="order.payment_method">
                    {{ order.payment_method === 'cash' ? $t('admin.ordersPage.cash') : $t('admin.ordersPage.card') }}
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
                    {{ $t('admin.ordersPage.items') }} ({{ order.items?.length || 0 }})
                  </h3>
                  <div class="items-list">
                    <NuxtLink v-for="(item, idx) in order.items" :key="idx"
                      :to="`/${shopSlug}/products/${item.product_id}`" class="order-item">
                      <img :src="item.product_image" :alt="item.product_name" class="item-image" />
                      <div class="item-info">
                        <span class="item-name">{{ item.product_name }}</span>
                        <div class="item-options" v-if="item.selected_color || item.selected_size">
                          <span v-if="item.selected_color" class="item-option color">{{ item.selected_color }}</span>
                          <span v-if="item.selected_size" class="item-option size">{{ item.selected_size }}</span>
                        </div>
                        <span class="item-meta">{{ $t('admin.ordersPage.qty') }}: {{ item.quantity }} × ${{
                          item.price.toFixed(2) }}</span>
                      </div>
                      <span class="item-total">${{ (item.quantity * item.price).toFixed(2) }}</span>
                    </NuxtLink>
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
                    {{ $t('admin.ordersPage.notes') }}
                  </h3>
                  <p class="notes-text">{{ order.notes }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t, locale } = useI18n()
definePageMeta({
  middleware: ['auth', 'shop-owner']
})

const route = useRoute()
const shopSlug = route.params.slug
const { token, logout } = useAuth()

const sidebarOpen = ref(false)

const currentRoute = computed(() => 'orders')

const expandedOrder = ref(null)
const selectedStatus = ref('all')

const statuses = computed(() => [
  { value: 'all', label: t('admin.periods.all') },
  { value: 'pending', label: t('admin.status.pending') },
  { value: 'processing', label: t('admin.status.processing') },
  { value: 'shipping', label: t('admin.status.shipping') },
  { value: 'delivered', label: t('admin.status.delivered') },
  { value: 'cancelled', label: t('admin.status.cancelled') }
])

const { data: orders, refresh } = await useFetch(`${useRuntimeConfig().public.apiBase}/shop/${shopSlug}/admin/orders`, {
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
  return new Date(dateStr).toLocaleDateString(locale.value, {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateStatus = async (id, newStatus) => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBase}/shop/${shopSlug}/admin/orders/${id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { status: newStatus }
    })
    refresh()
    useToast().success(t('admin.ordersPage.statusUpdateSuccess'))
  } catch (e) {
    useToast().error(t('admin.ordersPage.statusUpdateError'))
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}


/* Sidebar styles handled by ShopAdminSidebar component */

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
  align-items: flex-start;
  margin-bottom: 40px;
  gap: 24px;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 8px 0;
  letter-spacing: -0.03em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.admin-content {
  padding: 0;
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
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.filter-btn.active {
  background: #111;
  border-color: #111;
  color: white;
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
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
}

.filter-btn.active .filter-count {
  background: rgba(0, 0, 0, 0.1);
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
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.02);
  border: 1px solid #f1f1f1;
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

.status-select.pending {
  background: #FFF3E0;
  color: #EF6C00;
}

.status-select.processing {
  background: #E3F2FD;
  color: #1565C0;
}

.status-select.shipping {
  background: #FFF8E1;
  color: #F9A825;
}

.status-select.delivered {
  background: #E8F5E9;
  color: #2E7D32;
}

.status-select.cancelled {
  background: #FFEBEE;
  color: #C62828;
}

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
  .mobile-header {
    display: flex;
  }

  .admin-main {
    margin-left: 0;
    padding-top: 60px;
    width: 100%;
    min-width: 0;
  }
}

@media (max-width: 768px) {

  /* Fixed Filters on Mobile */
  .page-header {
    padding: 12px 16px;
    gap: 12px;
    position: sticky;
    top: 60px;
    /* Below the 60px fixed mobile header */
    z-index: 990;
    /* Below header (1000) but above content */
    background: white;
    border-bottom: 1px solid #eee;
  }

  .admin-main {
    margin-left: 0;
    padding: 60px 0 0 0;
    width: 100%;
    min-width: 0;
  }

  .container {
    padding: 0;
  }

  /* Hide large title/subtitle on mobile since we have the Mobile Header */
  .page-title,
  .page-subtitle {
    display: none;
  }

  .filters {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 2px;
    flex-wrap: nowrap;
    -webkit-overflow-scrolling: touch;
    gap: 8px;
    scrollbar-width: none;
  }

  .filters::-webkit-scrollbar {
    display: none;
  }

  .filter-btn {
    flex-shrink: 0;
    padding: 6px 12px;
    white-space: nowrap;
    font-size: 0.75rem;
  }

  .admin-content {
    padding: 12px;
    overflow-x: hidden;
  }

  /* Grid Layout for Order Card Header on Mobile */
  .order-header {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 8px;
    padding: 12px;
  }

  /* Compact Typography for Mobile */
  .order-id {
    font-size: 0.8125rem;
  }

  .order-date {
    font-size: 0.75rem;
  }

  .customer-name {
    font-size: 0.875rem;
  }

  .customer-phone {
    font-size: 0.75rem;
  }

  .order-total {
    font-size: 0.9375rem;
  }

  .status-select {
    font-size: 0.75rem;
    padding: 4px 8px;
  }

  /* 
    Mobile Layout Idea:
    Row 1: ID & Date (Left), Expand Btn (Right)
    Row 2: Customer Name & Phone
    Row 3: Total (Left), Status (Right)
  */

  .order-main-info {
    grid-column: 1;
    grid-row: 1;
    margin-right: 40px;
    /* Space for expand button */
  }

  .expand-btn {
    grid-column: 2;
    grid-row: 1;
    justify-self: end;
  }

  .order-customer {
    grid-column: 1 / -1;
    grid-row: 2;
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    padding-top: 8px;
    margin-top: 8px;
    border-top: 1px solid #F3F4F6;
  }

  .order-total {
    grid-column: 1;
    grid-row: 3;
    text-align: left;
    align-self: center;
  }

  .status-select {
    grid-column: 2;
    grid-row: 3;
    width: auto;
    min-width: 0;
    justify-self: end;
  }

  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>
