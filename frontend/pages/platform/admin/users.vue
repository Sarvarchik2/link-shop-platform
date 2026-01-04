<template>
  <div class="platform-admin-page">
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
      <span class="mobile-title">{{ $t('platformAdmin.users.title') }}</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar :current-route="currentRoute" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div class="header-content">
          <div>
            <h1 class="admin-title">{{ $t('platformAdmin.users.title') }}</h1>
            <p class="admin-subtitle">{{ $t('platformAdmin.users.subtitle') }}</p>
          </div>
          <button @click="refresh" class="refresh-btn" :disabled="pending">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              :class="{ spinning: pending }">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span>{{ $t('platformAdmin.dashboard.refresh') }}</span>
          </button>
        </div>
      </div>

      <div class="admin-content">
        <!-- Statistics Cards -->
        <div class="stats-overview">
          <div class="stat-card">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ users?.length || 0 }}</div>
              <div class="stat-label">{{ $t('platformAdmin.users.total') }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon admin">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ adminUsersCount }}</div>
              <div class="stat-label">{{ $t('platformAdmin.users.admins') }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon owner">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z">
                </path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ shopOwnersCount }}</div>
              <div class="stat-label">{{ $t('platformAdmin.users.shopOwners') }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon user">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ regularUsersCount }}</div>
              <div class="stat-label">{{ $t('platformAdmin.users.regular') }}</div>
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
            <input v-model="searchQuery" type="text" :placeholder="$t('platformAdmin.users.search')"
              class="search-input" />
          </div>

          <div class="filters-group">
            <select v-model="filterRole" class="filter-select">
              <option value="">{{ $t('platformAdmin.users.filterRole') }}</option>
              <option value="platform_admin">{{ $t('platformAdmin.users.roles.admin') }}</option>
              <option value="shop_owner">{{ $t('platformAdmin.users.roles.owner') }}</option>
              <option value="user">{{ $t('platformAdmin.users.roles.user') }}</option>
            </select>

            <button @click="clearFilters" class="clear-filters-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              {{ $t('platformAdmin.shops.clear') }}
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
          <p class="error-message">{{ $t('platformAdmin.dashboard.error') }}: {{ error.message || 'Unknown' }}</p>
          <button @click="refresh" class="retry-btn">{{ $t('platformAdmin.dashboard.refresh') }}</button>
        </div>

        <!-- Loading State -->
        <div v-else-if="pending" class="loading-state">
          <div class="loading-spinner"></div>
          <p>{{ $t('platformAdmin.dashboard.loading') }}</p>
        </div>

        <!-- Table -->
        <div v-else class="table-container">
          <div class="table-header">
            <div class="table-info">
              <span>{{ $t('common.showing') }} {{ displayedUsers.length }} {{ $t('common.of') }} {{ users?.length || 0
              }}</span>
            </div>
            <div class="table-actions">
              <button @click="exportData" class="export-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                {{ $t('platformAdmin.shops.export') }}
              </button>
            </div>
          </div>

          <div class="users-table-wrapper">
            <table class="users-table">
              <thead>
                <tr>
                  <th @click="sortBy('id')" class="sortable">
                    <div class="th-content">
                      ID
                      <svg v-if="sortField === 'id'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('name')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.users.table.name') }}
                      <svg v-if="sortField === 'name'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('phone')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.users.table.phone') }}
                      <svg v-if="sortField === 'phone'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('role')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.users.table.role') }}
                      <svg v-if="sortField === 'role'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('shops')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.users.table.shops') }}
                      <svg v-if="sortField === 'shops'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('orders')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.users.table.orders') }}
                      <svg v-if="sortField === 'orders'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('created_at')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.users.table.created') }}
                      <svg v-if="sortField === 'created_at'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>{{ $t('platformAdmin.users.table.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in paginatedUsers" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>
                    <div class="user-info">
                      <div class="user-avatar" :class="getRoleClass(user.role)">
                        {{ getUserInitials(user) }}
                      </div>
                      <div class="user-details">
                        <div class="user-name">{{ getUserName(user) }}</div>
                        <div v-if="user.first_name || user.last_name" class="user-phone-text">{{ user.phone }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="phone-cell">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2">
                        <path
                          d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                        </path>
                      </svg>
                      {{ user.phone }}
                    </div>
                  </td>
                  <td>
                    <span :class="['role-badge', getRoleClass(user.role)]">
                      {{ getRoleText(user.role) }}
                    </span>
                  </td>
                  <td>
                    <div class="stats-cell">
                      <span class="stat-value-small">{{ getUserShopsCount(user.id) }}</span>
                    </div>
                  </td>
                  <td>
                    <div class="stats-cell">
                      <span class="stat-value-small">{{ getUserOrdersCount(user.id) }}</span>
                    </div>
                  </td>
                  <td>
                    <div class="date-cell">
                      <div class="date-main">{{ formatDate(user.created_at) }}</div>
                      <div class="date-time">{{ formatTime(user.created_at) }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="actions">
                      <button @click="viewUserDetails(user)" class="action-btn btn-icon"
                        :title="$t('platformAdmin.users.details')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="16" x2="12" y2="12"></line>
                          <line x1="12" y1="8" x2="12.01" y2="8"></line>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty State -->
            <div v-if="displayedUsers.length === 0" class="empty-state">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <p>{{ $t('platformAdmin.users.notFound') }}</p>
              <p class="empty-subtitle"></p>
            </div>
          </div>

          <!-- Mobile Cards View -->
          <div class="mobile-users-list">
            <div v-for="user in paginatedUsers" :key="user.id" class="user-mobile-card">
              <!-- User Header -->
              <div class="mobile-card-header">
                <div class="user-info-mobile">
                  <div class="user-avatar-mobile" :class="getRoleClass(user.role)">
                    {{ getUserInitials(user) }}
                  </div>
                  <div class="user-details-mobile">
                    <h3 class="user-name-mobile">{{ getUserName(user) }}</h3>
                    <div class="user-phone-mobile">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2">
                        <path
                          d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                        </path>
                      </svg>
                      {{ user.phone }}
                    </div>
                  </div>
                </div>
                <span :class="['role-badge-mobile', getRoleClass(user.role)]">
                  {{ getRoleText(user.role) }}
                </span>
              </div>

              <!-- User Info Grid -->
              <div class="mobile-card-info">
                <div class="info-row">
                  <span class="info-label">ID:</span>
                  <span class="info-value">{{ user.id }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Магазинов:</span>
                  <span class="info-value">{{ getUserShopsCount(user.id) }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Заказов:</span>
                  <span class="info-value">{{ getUserOrdersCount(user.id) }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Регистрация:</span>
                  <span class="info-value">{{ formatDate(user.created_at) }}</span>
                </div>
              </div>

              <!-- Actions -->
              <div class="mobile-card-actions">
                <button @click="viewUserDetails(user)" class="mobile-action-btn btn-details">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                  </svg>
                  {{ $t('platformAdmin.users.details') }}
                </button>
              </div>
            </div>

            <!-- Empty State for Mobile -->
            <div v-if="displayedUsers.length === 0" class="empty-state-mobile">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <p>{{ $t('platformAdmin.users.notFound') }}</p>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination">
            <button @click="currentPage = 1" :disabled="currentPage === 1" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="11 17 6 12 11 7"></polyline>
                <polyline points="18 17 13 12 18 7"></polyline>
              </svg>
            </button>
            <button @click="currentPage--" :disabled="currentPage === 1" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>

            <div class="pagination-info">
              {{ $t('common.page') }} {{ currentPage }} {{ $t('common.of') }} {{ totalPages }}
            </div>

            <button @click="currentPage++" :disabled="currentPage === totalPages" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
            <button @click="currentPage = totalPages" :disabled="currentPage === totalPages" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 17 18 12 13 7"></polyline>
                <polyline points="6 17 11 12 6 7"></polyline>
              </svg>
            </button>
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
const { token, logout } = useAuth()
const toast = useToast()

const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success(t('auth.loggedOut'))
}

const currentRoute = computed(() => {
  if (route.path.includes('/subscription-plans')) return 'subscription-plans'
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

const { data: users, pending, error, refresh } = await useFetch(useRuntimeConfig().public.apiBase + '/platform/admin/users', {
  server: false,
  lazy: true,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Fetch shops and orders for stats
const { data: shops } = await useFetch(useRuntimeConfig().public.apiBase + '/platform/shops', {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

const { data: orders } = await useFetch(useRuntimeConfig().public.apiBase + '/platform/admin/orders', {
  server: false,
  lazy: true,
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Filters and Search
const searchQuery = ref('')
const filterRole = ref('')

// Sorting
const sortField = ref('id')
const sortOrder = ref('asc')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 20

// Computed stats
const adminUsersCount = computed(() => {
  if (!users.value) return 0
  return users.value.filter(u => u.role === 'platform_admin').length
})

const shopOwnersCount = computed(() => {
  if (!users.value) return 0
  return users.value.filter(u => u.role === 'shop_owner').length
})

const regularUsersCount = computed(() => {
  if (!users.value) return 0
  return users.value.filter(u => u.role === 'user').length
})

// Get user shops count
const getUserShopsCount = (userId) => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.owner_id === userId).length
}

// Get user orders count
const getUserOrdersCount = (userId) => {
  if (!orders.value) return 0
  return orders.value.filter(o => o.user_id === userId).length
}

// Filtered and sorted users
const displayedUsers = computed(() => {
  if (!users.value) return []

  let filtered = [...users.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user => {
      const fullName = getUserName(user).toLowerCase()
      const phone = user.phone?.toLowerCase() || ''
      return fullName.includes(query) || phone.includes(query)
    })
  }

  // Role filter
  if (filterRole.value) {
    filtered = filtered.filter(user => user.role === filterRole.value)
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
        aVal = getUserName(a).toLowerCase()
        bVal = getUserName(b).toLowerCase()
        break
      case 'phone':
        aVal = a.phone || ''
        bVal = b.phone || ''
        break
      case 'role':
        aVal = a.role
        bVal = b.role
        break
      case 'shops':
        aVal = getUserShopsCount(a.id)
        bVal = getUserShopsCount(b.id)
        break
      case 'orders':
        aVal = getUserOrdersCount(a.id)
        bVal = getUserOrdersCount(b.id)
        break
      case 'created_at':
        aVal = a.created_at ? new Date(a.created_at).getTime() : 0
        bVal = b.created_at ? new Date(b.created_at).getTime() : 0
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

// Paginated users
const totalPages = computed(() => Math.ceil(displayedUsers.value.length / itemsPerPage))

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return displayedUsers.value.slice(start, end)
})

// Watch for filter changes and reset page
watch([searchQuery, filterRole], () => {
  currentPage.value = 1
})

// Functions
const { t, locale } = useI18n()
const clearFilters = () => {
  searchQuery.value = ''
  filterRole.value = ''
}

const sortBy = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
}

const getUserInitials = (user) => {
  const first = user.first_name?.[0] || user.phone?.[0] || '?'
  const last = user.last_name?.[0] || ''
  return (first + last).toUpperCase().slice(0, 2)
}

const getUserName = (user) => {
  return `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.phone || t('common.noName')
}

const getRoleClass = (role) => {
  const roleMap = {
    'platform_admin': 'role-admin',
    'shop_owner': 'role-owner',
    'user': 'role-user'
  }
  return roleMap[role] || 'role-user'
}

const getRoleText = (role) => {
  const roleMap = {
    'platform_admin': t('platformAdmin.users.roles.admin'),
    'shop_owner': t('platformAdmin.users.roles.owner'),
    'user': t('platformAdmin.users.roles.user')
  }
  return roleMap[role] || role
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString(locale.value, { day: 'numeric', month: 'long', year: 'numeric' })
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString(locale.value, { hour: '2-digit', minute: '2-digit' })
}

const viewUserDetails = (user) => {
  // Можно добавить модальное окно с деталями
  toast.info(t('platformAdmin.users.userInfo', { name: getUserName(user) }))
}

const exportData = () => {
  const csv = [
    [
      t('platformAdmin.users.table.id'),
      t('platformAdmin.users.table.name'),
      t('platformAdmin.users.table.phone'),
      t('platformAdmin.users.table.role'),
      t('platformAdmin.users.table.shops'),
      t('platformAdmin.users.table.orders'),
      t('platformAdmin.users.table.created')
    ],
    ...displayedUsers.value.map(user => [
      user.id,
      getUserName(user),
      user.phone || '',
      getRoleText(user.role),
      getUserShopsCount(user.id),
      getUserOrdersCount(user.id),
      formatDate(user.created_at)
    ])
  ].map(row => row.join(',')).join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `users-${new Date().toISOString().split('T')[0]}.csv`
  link.click()
  toast.success(t('common.saved'))
}
</script>

<style scoped>
.platform-admin-page {
  min-height: 100vh;
  display: flex;
  background: #F5F7FA;
  width: 100%;
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
  width: 100%;
  margin-left: 280px;
  min-height: 100vh;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
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

@media (max-width: 768px) {
  .admin-main {
    padding-left: 0;
    padding-right: 0;
  }

  .admin-header {
    padding: 20px 16px;
  }

  .admin-content {
    padding: 0;
  }
}


/* Statistics Overview */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 1280px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 640px) {
  .stats-overview {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #E5E7EB;
  transition: all 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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

.stat-icon.admin {
  background: #1a1a1a;
  color: white;
}

.stat-icon.owner {
  background: #DBEAFE;
  color: #1E40AF;
}

.stat-icon.user {
  background: #D1FAE5;
  color: #065F46;
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #E5E7EB;
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-group {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: 0;
  }

  .filter-select,
  .clear-filters-btn {
    width: 100%;
  }
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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

.users-table-wrapper {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.users-table {
  width: 100%;
  min-width: 800px;
  border-collapse: collapse;
}

.users-table thead {
  background: #F9FAFB;
}

.users-table th {
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

.users-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.users-table th.sortable:hover {
  background: #F3F4F6;
}

.users-table td {
  padding: 16px;
  border-top: 1px solid #E5E7EB;
  font-size: 0.875rem;
}

.users-table tbody tr {
  transition: background 0.2s;
}

.users-table tbody tr:hover {
  background: #F9FAFB;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.user-avatar.role-admin {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.user-avatar.role-owner {
  background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
}

.user-avatar.role-user {
  background: linear-gradient(135deg, #065F46 0%, #10B981 100%);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 600;
  color: #111;
}

.user-phone-text {
  font-size: 0.75rem;
  color: #6B7280;
}

.phone-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #111;
  font-weight: 500;
}

.phone-cell svg {
  color: #6B7280;
  flex-shrink: 0;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.role-admin {
  background: #1a1a1a;
  color: white;
}

.role-owner {
  background: #DBEAFE;
  color: #1E40AF;
}

.role-user {
  background: #F3F4F6;
  color: #4B5563;
}

.stats-cell {
  display: flex;
  align-items: center;
}

.stat-value-small {
  font-weight: 700;
  color: #111;
  font-size: 0.9375rem;
}

.date-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.date-main {
  font-weight: 500;
  color: #111;
}

.date-time {
  font-size: 0.75rem;
  color: #6B7280;
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Mobile Users Cards Styles */
.mobile-users-list {
  display: none;
}

.user-mobile-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #E5E7EB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.mobile-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.user-info-mobile {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.user-avatar-mobile {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: white;
  flex-shrink: 0;
}

.user-avatar-mobile.role-admin {
  background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
}

.user-avatar-mobile.role-owner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.user-avatar-mobile.role-user {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.user-details-mobile {
  min-width: 0;
  flex: 1;
}

.user-name-mobile {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-phone-mobile {
  font-size: 12px;
  color: #6B7280;
  display: flex;
  align-items: center;
  gap: 4px;
}

.role-badge-mobile {
  flex-shrink: 0;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.role-badge-mobile.role-admin {
  background: #FEE2E2;
  color: #991B1B;
}

.role-badge-mobile.role-owner {
  background: #E0E7FF;
  color: #3730A3;
}

.role-badge-mobile.role-user {
  background: #DBEAFE;
  color: #1E40AF;
}

.mobile-card-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  padding: 12px 0;
  border-top: 1px solid #F3F4F6;
  border-bottom: 1px solid #F3F4F6;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.info-label {
  color: #6B7280;
  font-weight: 500;
}

.info-value {
  color: #111;
  font-weight: 600;
  text-align: right;
}

.mobile-card-actions {
  display: flex;
  gap: 8px;
}

.mobile-action-btn {
  flex: 1;
  min-width: fit-content;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.mobile-action-btn.btn-details {
  background: #F3F4F6;
  color: #111;
}

.mobile-action-btn.btn-details:active {
  background: #E5E7EB;
}

.empty-state-mobile {
  text-align: center;
  padding: 60px 20px;
  color: #6B7280;
}

.empty-state-mobile svg {
  margin: 0 auto 16px;
  opacity: 0.3;
}

.empty-state-mobile p {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
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

  .users-table-wrapper {
    display: none;
  }

  .mobile-users-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 12px;
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
