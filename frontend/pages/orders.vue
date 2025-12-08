<template>
  <div class="orders-page">
    <!-- Desktop Header -->
    <AppHeader class="desktop-header" />
    
    <!-- Mobile Header -->
    <header class="orders-header mobile-header">
      <button @click="$router.back()" class="back-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <h1 class="page-title">Mening buyurtmalarim</h1>
      <div class="spacer"></div>
    </header>

    <main class="orders-content">
    <!-- Search -->
      <div class="search-box">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Buyurtma ID bo'yicha qidirish..." 
          class="search-input"
        />
    </div>

      <!-- Status Filters -->
      <div class="status-filters">
      <button 
        v-for="status in statuses" 
          :key="status.value"
          class="filter-btn"
          :class="{ active: selectedStatus === status.value }"
          @click="selectedStatus = status.value"
      >
          <span class="filter-icon">
            <!-- All -->
            <svg v-if="status.value === 'all'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <!-- Pending -->
            <svg v-else-if="status.value === 'pending'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <!-- Processing -->
            <svg v-else-if="status.value === 'processing'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24"></path>
            </svg>
            <!-- Shipping -->
            <svg v-else-if="status.value === 'shipping'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="3" width="15" height="13"></rect>
              <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
              <circle cx="5.5" cy="18.5" r="2.5"></circle>
              <circle cx="18.5" cy="18.5" r="2.5"></circle>
            </svg>
            <!-- Delivered -->
            <svg v-else-if="status.value === 'delivered'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <!-- Cancelled -->
            <svg v-else-if="status.value === 'cancelled'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
          </span>
          {{ status.label }}
      </button>
    </div>

      <!-- Loading State -->
      <div v-if="pending" class="loading-state">
        <div class="spinner"></div>
        <p>Buyurtmalar yuklanmoqda...</p>
    </div>

      <!-- Empty State -->
      <div v-else-if="filteredOrders.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
          </svg>
        </div>
        <h2 class="empty-title">Hozircha buyurtmalar yo'q</h2>
        <p class="empty-text">Xarid qilganingizdan so'ng buyurtmalaringiz shu yerda ko'rinadi</p>
        <NuxtLink to="/products" class="btn-shop">Xarid qilishni boshlash</NuxtLink>
      </div>

      <!-- Orders List -->
      <div v-else class="orders-list">
        <div 
          v-for="order in filteredOrders" 
          :key="order.id" 
          class="order-card"
          :class="{ expanded: expandedOrder === order.id }"
        >
          <!-- Order Header -->
          <div class="order-header" @click="toggleOrder(order.id)">
            <div class="order-info">
              <span class="order-id">Buyurtma #{{ order.id }}</span>
              <span class="order-date">{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="order-status" :class="order.status">
              {{ formatStatus(order.status) }}
            </div>
        </div>

          <!-- Order Items Preview -->
          <div class="order-items-preview">
            <div v-for="(item, idx) in order.items?.slice(0, 2)" :key="idx" class="item-preview">
              <img :src="item.product_image" :alt="item.product_name" class="item-img" />
              <div class="item-details">
                <span class="item-name">{{ item.product_name }}</span>
                <div class="item-options" v-if="item.selected_color || item.selected_size">
                  <span v-if="item.selected_color" class="option-tag color">{{ item.selected_color }}</span>
                  <span v-if="item.selected_size" class="option-tag size">{{ item.selected_size }}</span>
                </div>
                <span class="item-qty">Soni: {{ item.quantity }}</span>
              </div>
              <span class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
            <div v-if="order.items?.length > 2" class="more-items">
              +{{ order.items.length - 2 }} ta mahsulot
            </div>
          </div>

          <!-- Order Footer -->
          <div class="order-footer">
            <div class="order-total">
              <span class="total-label">Jami</span>
              <span class="total-value">${{ order.total_price.toFixed(2) }}</span>
            </div>
            <button class="expand-btn" @click="toggleOrder(order.id)">
              {{ expandedOrder === order.id ? 'Yashirish' : 'Batafsil' }}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ rotated: expandedOrder === order.id }">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
          </div>

          <!-- Expanded Details -->
          <div v-if="expandedOrder === order.id" class="order-details">
            <!-- Timeline -->
            <div class="timeline-section">
              <h3 class="section-label">Buyurtma holati</h3>
              <div class="timeline">
                <div class="timeline-item" :class="{ active: isStatusActive(order.status, 'pending'), completed: isStatusCompleted(order.status, 'pending') }">
                  <div class="timeline-dot"></div>
                  <span>Buyurtma berildi</span>
                </div>
                <div class="timeline-item" :class="{ active: isStatusActive(order.status, 'processing'), completed: isStatusCompleted(order.status, 'processing') }">
                  <div class="timeline-dot"></div>
                  <span>Jarayonda</span>
                </div>
                <div class="timeline-item" :class="{ active: isStatusActive(order.status, 'shipping'), completed: isStatusCompleted(order.status, 'shipping') }">
                  <div class="timeline-dot"></div>
                  <span>Yetkazilmoqda</span>
                </div>
                <div class="timeline-item" :class="{ active: isStatusActive(order.status, 'delivered'), completed: isStatusCompleted(order.status, 'delivered') }">
                  <div class="timeline-dot"></div>
                  <span>Yetkazildi</span>
                </div>
              </div>
            </div>

            <!-- Delivery Info -->
            <div v-if="order.delivery_address" class="delivery-section">
              <h3 class="section-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                Yetkazib berish manzili
              </h3>
              <div class="delivery-info">
                <p class="delivery-name">{{ order.recipient_name }}</p>
                <p class="delivery-address">{{ order.delivery_address }}, {{ order.delivery_city }}</p>
                <p class="delivery-phone">{{ order.delivery_phone }}</p>
              </div>
            </div>

            <!-- Payment Method -->
            <div class="payment-section">
              <h3 class="section-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                  <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
                To'lov usuli
              </h3>
              <div class="payment-badge" :class="order.payment_method">
                {{ order.payment_method === 'cash' ? 'Naqd pul' : 'Karta orqali' }}
          </div>
        </div>

            <!-- All Items -->
            <div class="items-section">
              <h3 class="section-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                  <line x1="3" y1="6" x2="21" y2="6"></line>
                  <path d="M16 10a4 4 0 0 1-8 0"></path>
                </svg>
                Mahsulotlar ({{ order.items?.length || 0 }})
              </h3>
              <div class="items-list">
                <div v-for="(item, idx) in order.items" :key="idx" class="item-full">
                  <img :src="item.product_image" :alt="item.product_name" class="item-img-full" />
                  <div class="item-info">
                    <span class="item-name-full">{{ item.product_name }}</span>
                    <div class="item-options" v-if="item.selected_color || item.selected_size">
                      <span v-if="item.selected_color" class="option-tag color">{{ item.selected_color }}</span>
                      <span v-if="item.selected_size" class="option-tag size">{{ item.selected_size }}</span>
                    </div>
                    <span class="item-meta">Soni: {{ item.quantity }} × ${{ item.price.toFixed(2) }}</span>
                  </div>
                  <span class="item-total">${{ (item.price * item.quantity).toFixed(2) }}</span>
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
definePageMeta({
  middleware: 'auth'
})

const { token } = useAuth()
const { data: orders, pending } = await useFetch('http://localhost:8000/orders/me', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const statuses = [
  { value: 'all', label: 'Hammasi' },
  { value: 'pending', label: 'Kutilmoqda' },
  { value: 'processing', label: 'Jarayonda' },
  { value: 'shipping', label: 'Yetkazilmoqda' },
  { value: 'delivered', label: 'Yetkazildi' },
  { value: 'cancelled', label: 'Bekor qilindi' }
]

const selectedStatus = ref('all')
const searchQuery = ref('')
const expandedOrder = ref(null)

const filteredOrders = computed(() => {
  if (!orders.value) return []
  
  let result = orders.value
  
  // Filter by status
  if (selectedStatus.value !== 'all') {
    result = result.filter(o => o.status.toLowerCase() === selectedStatus.value)
  }
  
  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(o => 
      o.id.toString().includes(query) ||
      o.items?.some(i => i.product_name.toLowerCase().includes(query))
    )
  }
  
  return result
})

const toggleOrder = (orderId) => {
  expandedOrder.value = expandedOrder.value === orderId ? null : orderId
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { 
    day: 'numeric',
    month: 'short', 
    year: 'numeric'
  })
}

const formatStatus = (status) => {
  const statusMap = {
    pending: 'Pending',
    processing: 'Processing',
    shipping: 'Shipping',
    delivered: 'Delivered',
    cancelled: 'Cancelled'
  }
  return statusMap[status.toLowerCase()] || status
}

const statusOrder = ['pending', 'processing', 'shipping', 'delivered']

const isStatusActive = (currentStatus, checkStatus) => {
  return currentStatus.toLowerCase() === checkStatus
}

const isStatusCompleted = (currentStatus, checkStatus) => {
  const currentIdx = statusOrder.indexOf(currentStatus.toLowerCase())
  const checkIdx = statusOrder.indexOf(checkStatus)
  return currentIdx > checkIdx
}
</script>

<style scoped>
.orders-page {
  min-height: 100vh;
  background: #F5F5F5;
}

/* Desktop header hidden on mobile */
.desktop-header {
    display: none;
}

/* Mobile header */
.mobile-header {
  display: flex;
}

.orders-header {
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid #f0f0f0;
}

.back-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: #111;
  border-radius: 50%;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #f5f5f5;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
}

.spacer {
  width: 44px;
}

.orders-content {
  padding: 16px;
  padding-bottom: 40px;
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
}

.search-box {
  position: relative;
  margin-bottom: 16px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #9CA3AF;
}

.search-input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  font-size: 1rem;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #111;
}

.status-filters {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 16px;
  margin-bottom: 8px;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.status-filters::-webkit-scrollbar {
  display: none;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #111;
  color: #111;
}

.filter-btn.active {
  background: #111;
  border-color: #111;
  color: white;
}

.filter-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.filter-icon svg {
  width: 18px;
  height: 18px;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #9CA3AF;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 24px;
  margin-top: 20px;
}

.empty-icon {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.empty-text {
  color: #9CA3AF;
  margin-bottom: 24px;
}

.btn-shop {
  display: inline-block;
  padding: 14px 32px;
  background: #111;
  color: white;
  border-radius: 30px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-shop:hover {
  background: #000;
  transform: translateY(-2px);
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s;
}

.order-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  border-bottom: 1px solid #F3F4F6;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-id {
  font-weight: 700;
  color: #111;
}

.order-date {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.order-status {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.order-status.pending { background: #FEF3C7; color: #D97706; }
.order-status.processing { background: #DBEAFE; color: #2563EB; }
.order-status.shipping { background: #E0E7FF; color: #4F46E5; }
.order-status.delivered { background: #D1FAE5; color: #059669; }
.order-status.cancelled { background: #FEE2E2; color: #DC2626; }

.order-items-preview {
  padding: 12px 20px;
}

.item-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.item-preview + .item-preview {
  border-top: 1px solid #F3F4F6;
}

.item-img {
  width: 50px;
  height: 50px;
  object-fit: contain;
  background: #F9FAFB;
  border-radius: 10px;
  padding: 4px;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
}

.item-qty {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.item-options {
  display: flex;
  gap: 4px;
  margin: 4px 0;
}

.option-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 600;
}

.option-tag.color {
  background: #E0E7FF;
  color: #3730A3;
}

.option-tag.size {
  background: #FEE2E2;
  color: #991B1B;
}

.item-price {
  font-weight: 600;
  color: #111;
}

.more-items {
  font-size: 0.75rem;
  color: #6B7280;
  text-align: center;
  padding: 8px;
  background: #F9FAFB;
  border-radius: 8px;
  margin-top: 8px;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #FAFAFA;
}

.order-total {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.total-label {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.total-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
}

.expand-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.expand-btn:hover {
  border-color: #111;
}

.expand-btn svg {
  transition: transform 0.3s;
}

.expand-btn svg.rotated {
  transform: rotate(180deg);
}

.order-details {
  padding: 20px;
  background: #F9FAFB;
  border-top: 1px solid #E5E7EB;
}

.section-label {
  font-size: 0.875rem;
  font-weight: 700;
  color: #374151;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-label svg {
  flex-shrink: 0;
  color: #6B7280;
}

.timeline-section {
  margin-bottom: 24px;
}

.timeline {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 12px;
  left: 20px;
  right: 20px;
  height: 2px;
  background: #E5E7EB;
}

.timeline-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.timeline-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  border: 2px solid #E5E7EB;
  transition: all 0.3s;
}

.timeline-item.active .timeline-dot {
  background: #111;
  border-color: #111;
  box-shadow: 0 0 0 4px rgba(0,0,0,0.1);
}

.timeline-item.completed .timeline-dot {
  background: #10B981;
  border-color: #10B981;
}

.timeline-item span {
  font-size: 0.7rem;
  color: #9CA3AF;
  text-align: center;
}

.timeline-item.active span,
.timeline-item.completed span {
  color: #111;
  font-weight: 600;
}

.delivery-section,
.payment-section {
  margin-bottom: 24px;
}

.delivery-info {
  background: white;
  padding: 16px;
  border-radius: 12px;
}

.delivery-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.delivery-address {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 4px;
}

.delivery-phone {
  font-size: 0.875rem;
  color: #9CA3AF;
}

.payment-badge {
  display: inline-block;
  padding: 10px 16px;
  border-radius: 10px;
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

.items-section {
  margin-bottom: 0;
}

.items-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.item-full {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
}

.item-full + .item-full {
  border-top: 1px solid #F3F4F6;
}

.item-img-full {
  width: 60px;
  height: 60px;
  object-fit: contain;
  background: #F9FAFB;
  border-radius: 10px;
  padding: 6px;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name-full {
  font-weight: 600;
  font-size: 0.875rem;
}

.item-meta {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.item-total {
  font-weight: 700;
  font-size: 0.875rem;
}

@media (min-width: 768px) {
  .desktop-header {
    display: block;
  }
  
  .mobile-header {
    display: none;
  }
  
  .orders-page {
    padding-bottom: 40px;
    background: #FAFAFA;
  }
  
  .orders-content {
    padding: 40px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .search-box {
    max-width: 500px;
    margin-bottom: 24px;
  }
  
  .status-filters {
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 24px;
  }
  
  .filter-btn {
    padding: 12px 24px;
    font-size: 0.95rem;
  }
  
  .orders-list {
    gap: 24px;
    display: grid;
    grid-template-columns: 1fr;
  }
  
  .order-card {
    border-radius: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .order-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  }
  
  .order-header {
    padding: 24px 28px;
  }
  
  .order-items-preview {
    padding: 20px 28px;
  }
  
  .item-preview {
    padding: 12px 0;
  }
  
  .item-img {
    width: 70px;
    height: 70px;
  }
  
  .item-name {
    font-size: 0.95rem;
  }
  
  .order-footer {
    padding: 20px 28px;
  }
  
  .order-details {
    padding: 28px;
  }
  
  .timeline {
    padding: 0 40px;
  }
  
  .timeline::before {
    left: 40px;
    right: 40px;
  }
  
  .empty-state {
    padding: 100px 60px;
    margin-top: 40px;
    border-radius: 24px;
  }
  
  .empty-title {
    font-size: 1.75rem;
  }
}

@media (min-width: 1024px) {
  .orders-content {
    padding: 48px 60px;
    max-width: 1400px;
  }
  
  .search-box {
    max-width: 600px;
  }
  
  .orders-list {
    gap: 28px;
  }
  
  .order-card {
    border-radius: 28px;
  }
  
  .order-header {
    padding: 28px 32px;
  }
  
  .order-items-preview {
    padding: 24px 32px;
  }
  
  .order-footer {
    padding: 24px 32px;
  }
  
  .order-details {
    padding: 32px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  
  .timeline-section {
    grid-column: 1 / -1;
  }
  
  .delivery-section,
  .payment-section,
  .items-section {
    margin-bottom: 0;
  }
  
  .item-full {
    padding: 16px 20px;
  }
  
  .item-img-full {
    width: 80px;
    height: 80px;
  }
}

@media (min-width: 1440px) {
  .orders-content {
    padding: 60px 80px;
  }
  
  .orders-list {
    gap: 32px;
  }
}
</style>
