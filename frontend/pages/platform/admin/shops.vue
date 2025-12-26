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
      <span class="mobile-title">Магазины</span>
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
            <h1 class="admin-title">Управление магазинами</h1>
            <p class="admin-subtitle">Все зарегистрированные магазины на платформе</p>
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
        <!-- Statistics Cards -->
        <div class="stats-overview">
          <div class="stat-card">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ shops?.length || 0 }}</div>
              <div class="stat-label">Всего магазинов</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon active">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ activeShopsCount }}</div>
              <div class="stat-label">Активных</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon trial">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 6v6l4 2"></path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ trialShopsCount }}</div>
              <div class="stat-label">Пробный период</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon expired">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ expiredShopsCount }}</div>
              <div class="stat-label">Истекшие</div>
            </div>
          </div>
        </div>

        <!-- Filters and Search -->
        <div class="filters-section">
          <div class="search-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Поиск по названию, slug, владельцу..." 
              class="search-input"
            />
          </div>
          
          <div class="filters-group">
            <select v-model="filterStatus" class="filter-select">
              <option value="">Все статусы</option>
              <option value="trial">Пробный период</option>
              <option value="active">Активные</option>
              <option value="expired">Истекшие</option>
              <option value="cancelled">Отмененные</option>
            </select>
            
            <select v-model="filterActive" class="filter-select">
              <option value="">Все магазины</option>
              <option value="true">Только активные</option>
              <option value="false">Только неактивные</option>
            </select>
            
            <button @click="clearFilters" class="clear-filters-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              Сбросить
            </button>
          </div>
        </div>

        <!-- Error State -->
        <div v-if="error" class="error-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p class="error-message">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
          <button @click="refresh" class="retry-btn">Повторить</button>
        </div>
        
        <!-- Loading State -->
        <div v-else-if="pending" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Магазины загружаются...</p>
        </div>

        <!-- Table -->
        <div v-else class="table-container">
          <div class="table-header">
            <div class="table-info">
              <span>Показано: {{ displayedShops.length }} из {{ shops?.length || 0 }}</span>
            </div>
            <div class="table-actions">
              <button @click="exportData" class="export-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Экспорт
              </button>
            </div>
          </div>

          <div class="shops-table-wrapper">
            <table class="shops-table">
              <thead>
                <tr>
                  <th @click="sortBy('id')" class="sortable">
                    <div class="th-content">
                      ID
                      <svg v-if="sortField === 'id'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('name')" class="sortable">
                    <div class="th-content">
                      Название
                      <svg v-if="sortField === 'name'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>Slug</th>
                  <th @click="sortBy('owner')" class="sortable">
                    <div class="th-content">
                      Владелец
                      <svg v-if="sortField === 'owner'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>План</th>
                  <th @click="sortBy('subscription_status')" class="sortable">
                    <div class="th-content">
                      Статус подписки
                      <svg v-if="sortField === 'subscription_status'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('expires_at')" class="sortable">
                    <div class="th-content">
                      Истекает
                      <svg v-if="sortField === 'expires_at'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('created_at')" class="sortable">
                    <div class="th-content">
                      Дата создания
                      <svg v-if="sortField === 'created_at'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('is_active')" class="sortable">
                    <div class="th-content">
                      Активен
                      <svg v-if="sortField === 'is_active'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="shop in paginatedShops" :key="shop.id" :class="{ 'expiring-soon': isExpiringSoon(shop) }">
                  <td>{{ shop.id }}</td>
                  <td>
                    <div class="shop-info">
                      <img 
                        v-if="shop.logo_url" 
                        :src="shop.logo_url" 
                        :alt="shop.name"
                        class="shop-logo"
                      />
                      <div class="shop-logo-placeholder" v-else>
                        {{ shop.name.charAt(0).toUpperCase() }}
                      </div>
                      <div class="shop-details">
                        <span class="shop-name">{{ shop.name }}</span>
                        <span v-if="shop.description" class="shop-description">{{ truncateText(shop.description, 40) }}</span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <code class="shop-slug" :title="shop.slug">{{ shop.slug }}</code>
                  </td>
                  <td>
                    <div class="owner-info">
                      <div class="owner-name">{{ shop.owner_name || `ID: ${shop.owner_id}` }}</div>
                      <div class="owner-phone" v-if="shop.owner_phone">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                        </svg>
                        {{ shop.owner_phone }}
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="plan-name-cell">{{ shop.subscription_plan_name || '-' }}</span>
                  </td>
                  <td>
                    <span :class="['status-badge', getStatusClass(shop.subscription_status)]">
                      {{ getStatusText(shop.subscription_status) }}
                    </span>
                    <div v-if="shop.subscription_expires_at" class="days-remaining" :class="getDaysRemainingClass(shop)">
                      {{ getDaysRemaining(shop) }}
                    </div>
                  </td>
                  <td>
                    <div class="expiry-date">
                      {{ shop.subscription_expires_at ? formatDate(shop.subscription_expires_at) : '-' }}
                    </div>
                    <div v-if="shop.subscription_expires_at" class="expiry-time">
                      {{ formatTime(shop.subscription_expires_at) }}
                    </div>
                  </td>
                  <td>
                    <div class="created-date">
                      {{ formatDate(shop.created_at) }}
                    </div>
                    <div class="created-time">
                      {{ formatTime(shop.created_at) }}
                    </div>
                  </td>
                  <td>
                    <span :class="['status-badge', shop.is_active ? 'status-active' : 'status-cancelled']">
                      {{ shop.is_active ? 'Да' : 'Нет' }}
                    </span>
                  </td>
                  <td>
                    <div class="actions">
                      <button 
                        @click="openShopDetails(shop)"
                        class="action-btn btn-icon"
                        title="Подробнее"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="16" x2="12" y2="12"></line>
                          <line x1="12" y1="8" x2="12.01" y2="8"></line>
                        </svg>
                      </button>
                      <button 
                        @click="toggleActive(shop)"
                        :class="['action-btn', shop.is_active ? 'btn-danger' : 'btn-success']"
                        :title="shop.is_active ? 'Деактивировать' : 'Активировать'"
                      >
                        {{ shop.is_active ? 'Деакт.' : 'Актив.' }}
                      </button>
                      <button 
                        @click="openSubscriptionModal(shop)"
                        class="action-btn btn-primary"
                        title="Управление подпиской"
                      >
                        Подписка
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <!-- Empty State -->
            <div v-if="displayedShops.length === 0" class="empty-state">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
              </svg>
              <p>Магазины не найдены</p>
              <p class="empty-subtitle">Попробуйте изменить фильтры поиска</p>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination">
            <button 
              @click="currentPage = 1" 
              :disabled="currentPage === 1"
              class="pagination-btn"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="11 17 6 12 11 7"></polyline>
                <polyline points="18 17 13 12 18 7"></polyline>
              </svg>
            </button>
            <button 
              @click="currentPage--" 
              :disabled="currentPage === 1"
              class="pagination-btn"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>
            
            <div class="pagination-info">
              Страница {{ currentPage }} из {{ totalPages }}
            </div>
            
            <button 
              @click="currentPage++" 
              :disabled="currentPage === totalPages"
              class="pagination-btn"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
            <button 
              @click="currentPage = totalPages" 
              :disabled="currentPage === totalPages"
              class="pagination-btn"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 17 18 12 13 7"></polyline>
                <polyline points="6 17 11 12 6 7"></polyline>
              </svg>
            </button>
          </div>
        </div>

        <!-- Subscription Modal -->
        <div v-if="showModal && selectedShop" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">Управление подпиской</h2>
              <button @click="closeModal" class="modal-close">×</button>
            </div>
            
            <div class="modal-shop-info">
              <h3>{{ selectedShop.name }}</h3>
              <p class="shop-slug-text">{{ selectedShop.slug }}</p>
              <div class="owner-info">
                <span class="owner-label">Владелец:</span>
                <span class="owner-value">{{ selectedShop.owner_name || `ID: ${selectedShop.owner_id}` }}</span>
                <span v-if="selectedShop.owner_phone" class="owner-phone">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                  </svg>
                  {{ selectedShop.owner_phone }}
                </span>
              </div>
            </div>

            <div class="current-status-section">
              <label class="status-label">Текущий тарифный план:</label>
              <div class="current-plan-name">{{ selectedShop.subscription_plan_name || 'Не выбран' }}</div>

              <label class="status-label">Текущий статус:</label>
              <span :class="['current-status-badge', getStatusClass(selectedShop.subscription_status)]">
                {{ getStatusText(selectedShop.subscription_status) }}
              </span>
              <div v-if="selectedShop.subscription_expires_at" class="expires-info">
                Истекает: {{ formatDate(selectedShop.subscription_expires_at) }}
                <span class="days-warning" :class="getDaysRemainingClass(selectedShop)">
                  ({{ getDaysRemaining(selectedShop) }})
                </span>
              </div>
            </div>

            <!-- История подписок -->
            <div class="subscription-history-section" v-if="subscriptionHistory.length > 0">
               <h3>История запросов</h3>
               <div class="history-list">
                 <div v-for="req in subscriptionHistory" :key="req.id" class="history-item">
                   <div class="history-main">
                     <span class="history-plan">{{ req.plan_name }}</span>
                     <span :class="['history-status', `status-${req.status}`]">{{ getRequestStatusText(req.status) }}</span>
                   </div>
                   <div class="history-meta">
                     <span>{{ formatDate(req.requested_at) }}</span>
                     <span>{{ req.duration_months }} мес.</span>
                   </div>
                 </div>
               </div>
            </div>

            <form @submit.prevent="updateSubscription" class="modal-form">
              <div class="form-group">
                <label>Статус подписки</label>
                <select v-model="subscriptionForm.status" class="form-input">
                  <option value="trial">Пробный период</option>
                  <option value="active">Активна</option>
                  <option value="expired">Истекла</option>
                  <option value="cancelled">Отменена</option>
                </select>
              </div>
              <div class="form-group">
                <label>Дата истечения</label>
                <input 
                  v-model="subscriptionForm.expires_at" 
                  type="datetime-local" 
                  class="form-input"
                />
                <div class="quick-actions">
                  <button type="button" @click="setExpiry(1)" class="quick-btn">+1 месяц</button>
                  <button type="button" @click="setExpiry(3)" class="quick-btn">+3 месяца</button>
                  <button type="button" @click="setExpiry(6)" class="quick-btn">+6 месяцев</button>
                  <button type="button" @click="setExpiry(12)" class="quick-btn">+1 год</button>
                </div>
              </div>
              <div class="modal-actions">
                <button type="button" @click="closeModal" class="btn-secondary">Отмена</button>
                <button type="submit" class="btn-primary">Активировать подписку</button>
              </div>
            </form>
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

const route = useRoute()
const router = useRouter()
const { token, logout } = useAuth()
const toast = useToast()

const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const currentRoute = computed(() => {
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

const { data: shops, pending, refresh, error } = await useFetch('http://localhost:8000/platform/shops', {
  server: false,
  lazy: true,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Filters and Search
const searchQuery = ref('')
const filterStatus = ref('')
const filterActive = ref('')

// Sorting
const sortField = ref('id')
const sortOrder = ref('asc')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 20

// Modal
const showModal = ref(false)
const selectedShop = ref(null)
const subscriptionHistory = ref([])
const subscriptionForm = reactive({
  status: 'trial',
  expires_at: ''
})

// Computed stats
const activeShopsCount = computed(() => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.is_active).length
})

const trialShopsCount = computed(() => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.subscription_status === 'trial').length
})

const expiredShopsCount = computed(() => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.subscription_status === 'expired').length
})

// Filtered and sorted shops
const displayedShops = computed(() => {
  if (!shops.value) return []
  
  let filtered = [...shops.value]
  
  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(shop => 
      shop.name?.toLowerCase().includes(query) ||
      shop.slug?.toLowerCase().includes(query) ||
      shop.owner_name?.toLowerCase().includes(query) ||
      shop.owner_phone?.includes(query)
    )
  }
  
  // Status filter
  if (filterStatus.value) {
    filtered = filtered.filter(shop => shop.subscription_status === filterStatus.value)
  }
  
  // Active filter
  if (filterActive.value !== '') {
    const isActive = filterActive.value === 'true'
    filtered = filtered.filter(shop => shop.is_active === isActive)
  }
  
  // Sorting
  filtered.sort((a, b) => {
    let aVal, bVal
    
    switch (sortField.value) {
      case 'id':
        aVal = a.id
        bVal = b.id
        break
      case 'name':
        aVal = a.name?.toLowerCase() || ''
        bVal = b.name?.toLowerCase() || ''
        break
      case 'owner':
        aVal = a.owner_name?.toLowerCase() || ''
        bVal = b.owner_name?.toLowerCase() || ''
        break
      case 'subscription_status':
        aVal = a.subscription_status
        bVal = b.subscription_status
        break
      case 'expires_at':
        aVal = a.subscription_expires_at ? new Date(a.subscription_expires_at).getTime() : 0
        bVal = b.subscription_expires_at ? new Date(b.subscription_expires_at).getTime() : 0
        break
      case 'created_at':
        aVal = a.created_at ? new Date(a.created_at).getTime() : 0
        bVal = b.created_at ? new Date(b.created_at).getTime() : 0
        break
      case 'is_active':
        aVal = a.is_active ? 1 : 0
        bVal = b.is_active ? 1 : 0
        break
      default:
        return 0
    }
    
    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
  
  return filtered
})

// Paginated shops
const totalPages = computed(() => Math.ceil(displayedShops.value.length / itemsPerPage))

const paginatedShops = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return displayedShops.value.slice(start, end)
})

// Watch for filter changes and reset page
watch([searchQuery, filterStatus, filterActive], () => {
  currentPage.value = 1
})

// Functions
const clearFilters = () => {
  searchQuery.value = ''
  filterStatus.value = ''
  filterActive.value = ''
}

const sortBy = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
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
    'trial': 'Пробный период',
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

const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

const getDaysRemaining = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return null
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  const days = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
  
  if (days < 0) return 'Истекла'
  if (days === 0) return 'Истекает сегодня'
  if (days === 1) return 'Истекает завтра'
  return `${days} дн.`
}

const getDaysRemainingClass = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return ''
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  const days = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
  
  if (days <= 0) return 'days-expired'
  if (days <= 3) return 'days-critical'
  if (days <= 7) return 'days-warning'
  return 'days-normal'
}

const isExpiringSoon = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return false
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  const days = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
  return days > 0 && days <= 7
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const openShopDetails = (shop) => {
  router.push(`/platform/admin/shops/${shop.id}`)
}

const exportData = () => {
  const csv = [
    ['ID', 'Название', 'Slug', 'Владелец', 'Телефон', 'Статус подписки', 'Истекает', 'Активен', 'Дата создания'],
    ...displayedShops.value.map(shop => [
      shop.id,
      shop.name,
      shop.slug,
      shop.owner_name || '',
      shop.owner_phone || '',
      getStatusText(shop.subscription_status),
      shop.subscription_expires_at ? formatDate(shop.subscription_expires_at) : '',
      shop.is_active ? 'Да' : 'Нет',
      formatDate(shop.created_at)
    ])
  ].map(row => row.join(',')).join('\n')
  
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `shops-${new Date().toISOString().split('T')[0]}.csv`
  link.click()
  toast.success('Данные экспортированы')
}

const getRequestStatusText = (status) => {
  const map = {
    pending: 'Ожидает',
    approved: 'Одобрен',
    rejected: 'Отклонен'
  }
  return map[status] || status
}

const openSubscriptionModal = async (shop) => {
  selectedShop.value = shop
  subscriptionForm.status = shop.subscription_status
  subscriptionForm.expires_at = shop.subscription_expires_at ? new Date(shop.subscription_expires_at).toISOString().slice(0, 16) : ''
  
  // Fetch history
  try {
    const { data } = await useFetch(`http://localhost:8000/platform/admin/subscription-requests`, {
       query: { shop_id: shop.id },
       headers: {
          'Authorization': `Bearer ${token.value}`
       }
    })
    subscriptionHistory.value = data.value || []
  } catch (e) {
    console.error('Failed to fetch subscription history', e)
    subscriptionHistory.value = []
  }

  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedShop.value = null
}

const setExpiry = (months) => {
  const date = new Date()
  date.setMonth(date.getMonth() + months)
  subscriptionForm.expires_at = date.toISOString().slice(0, 16)
  if (subscriptionForm.status !== 'active') {
    subscriptionForm.status = 'active'
  }
}

const updateSubscription = async () => {
  if (!subscriptionForm.expires_at && subscriptionForm.status === 'active') {
    toast.warning('Укажите дату истечения для активной подписки')
    return
  }

  try {
    const body = {
      subscription_status: subscriptionForm.status
    }
    if (subscriptionForm.expires_at) {
      body.expires_at = new Date(subscriptionForm.expires_at).toISOString()
    }
    
    await $fetch(`http://localhost:8000/platform/admin/shops/${selectedShop.value.id}/subscription`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: body
    })
    
    const planName = subscriptionForm.status === 'active' ? 'Подписка активирована' : 'Подписка обновлена'
    toast.success(planName)
    closeModal()
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при обновлении подписки')
  }
}

const toggleActive = async (shop) => {
  try {
    await $fetch(`http://localhost:8000/platform/admin/shops/${shop.id}/activate`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: {
        is_active: !shop.is_active
      }
    })
    toast.success(`Магазин ${shop.is_active ? 'деактивирован' : 'активирован'}`)
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при изменении статуса')
  }
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

.refresh-btn svg.spinning {
  animation: spin 1s linear infinite;
}

.admin-content {
  padding: 32px;
}

/* Statistics Overview */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
  transition: all 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
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
  flex-shrink: 0;
}

.stat-icon.active {
  background: #D1FAE5;
  color: #065F46;
}

.stat-icon.trial {
  background: #FEF3C7;
  color: #92400E;
}

.stat-icon.expired {
  background: #FEE2E2;
  color: #991B1B;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 900;
  color: #111;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

/* Filters Section */
.filters-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 300px;
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 12px 16px;
}

.search-box svg {
  color: #6B7280;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.875rem;
  color: #111;
  outline: none;
}

.search-input::placeholder {
  color: #9CA3AF;
}

.filters-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 10px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  background: white;
  font-size: 0.875rem;
  font-weight: 500;
  color: #111;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
}

.filter-select:hover {
  border-color: #D1D5DB;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-filters-btn:hover {
  background: #E5E7EB;
  color: #111;
}

/* Table Container */
.table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
}

.table-header {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #F9FAFB;
}

.table-info {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.table-actions {
  display: flex;
  gap: 12px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover {
  background: #F9FAFB;
  border-color: #D1D5DB;
}

.shops-table-wrapper {
  overflow-x: auto;
}

.shops-table {
  width: 100%;
  border-collapse: collapse;
}

.shops-table thead {
  background: #F9FAFB;
}

.shops-table th {
  padding: 16px;
  text-align: left;
  font-weight: 700;
  font-size: 0.8125rem;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.th-content svg {
  transition: transform 0.2s;
}

.th-content svg.reverse {
  transform: rotate(180deg);
}

.shops-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.shops-table th.sortable:hover {
  background: #F3F4F6;
}

.shops-table td {
  padding: 16px;
  border-top: 1px solid #E5E7EB;
  font-size: 0.875rem;
}

.shops-table tbody tr {
  transition: background 0.2s;
}

.shops-table tbody tr:hover {
  background: #F9FAFB;
}

.shops-table tbody tr.expiring-soon {
  background: #FEF3C7;
}

.shop-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shop-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
}

.shop-logo-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: white;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.shop-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.shop-name {
  font-weight: 600;
  color: #111;
}

.shop-description {
  font-size: 0.75rem;
  color: #6B7280;
}

.shop-slug {
  background: #F3F4F6;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-family: 'Monaco', 'Courier New', monospace;
  color: #111;
  display: inline-block;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.owner-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.owner-name {
  font-weight: 600;
  color: #111;
}

.owner-phone {
  font-size: 0.75rem;
  color: #6B7280;
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.days-remaining {
  margin-top: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.days-normal {
  color: #6B7280;
}

.days-warning {
  color: #F59E0B;
}

.days-critical {
  color: #EF4444;
  font-weight: 700;
}

.days-expired {
  color: #991B1B;
  font-weight: 700;
}

.expiry-date,
.created-date {
  font-weight: 500;
  color: #111;
}

.expiry-time,
.created-time {
  font-size: 0.75rem;
  color: #6B7280;
  margin-top: 2px;
}

.actions {
  display: flex;
  gap: 6px;
  align-items: center;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-icon {
  background: #F3F4F6;
  color: #111;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: #E5E7EB;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #000;
}

.btn-danger {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-danger:hover {
  background: #FECACA;
}

.btn-success {
  background: #D1FAE5;
  color: #065F46;
}

.btn-success:hover {
  background: #A7F3D0;
}

/* Empty State */
.empty-state {
  padding: 80px 20px;
  text-align: center;
  color: #6B7280;
}

.empty-state svg {
  margin-bottom: 16px;
  color: #9CA3AF;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 600;
  margin: 8px 0;
}

.empty-subtitle {
  font-size: 0.875rem;
  font-weight: 400;
  color: #9CA3AF;
}

/* Pagination */
.pagination {
  padding: 20px 24px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  background: #F9FAFB;
}

.pagination-btn {
  padding: 8px 12px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
}

.pagination-btn:hover:not(:disabled) {
  background: #F3F4F6;
  border-color: #D1D5DB;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
  padding: 0 16px;
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
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
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

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid #F3F4F6;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 900;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6B7280;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #F3F4F6;
  color: #111;
}

.modal-shop-info {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.modal-shop-info h3 {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0 0 8px 0;
  color: #111;
}

.shop-slug-text {
  color: #6B7280;
  font-size: 0.875rem;
  margin: 0 0 12px 0;
}

.modal-shop-info .owner-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.owner-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.owner-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
}

.modal-shop-info .owner-phone {
  font-size: 0.875rem;
  color: #6B7280;
  display: flex;
  align-items: center;
  gap: 6px;
}

.current-status-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #F9FAFB;
  border-radius: 12px;
}

.status-label {
  display: block;
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 8px;
  font-weight: 500;
}

.current-status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.current-status-badge.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.current-status-badge.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.current-status-badge.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.current-status-badge.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.expires-info {
  margin-top: 8px;
  font-size: 0.875rem;
  color: #6B7280;
}

.days-warning {
  font-weight: 600;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.quick-btn {
  padding: 6px 12px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-btn:hover {
  background: #111;
  color: white;
  border-color: #111;
}

.form-group label {
  font-weight: 600;
  font-size: 0.875rem;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #111;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 12px 24px;
  background: #F3F4F6;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

/* Responsive */
@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }
  
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
  
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
}

@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .shops-table-wrapper {
    overflow-x: scroll;
  }
  
  .shops-table {
    min-width: 1200px;
  }
}


.plan-name-cell {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 14px;
}

/* Subscription History */
.subscription-history-section {
  margin-top: 20px;
  border-top: 1px solid var(--border-color);
  padding-top: 15px;
}

.subscription-history-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-primary);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 150px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: var(--bg-secondary);
  border-radius: 6px;
  font-size: 14px;
}

.history-main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.history-plan {
  font-weight: 500;
  color: var(--text-primary);
}

.history-status {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: uppercase;
}

.status-pending { background-color: #fff7ed; color: #c2410c; }
.status-approved { background-color: #f0fdf4; color: #15803d; }
.status-rejected { background-color: #fef2f2; color: #b91c1c; }

.history-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
