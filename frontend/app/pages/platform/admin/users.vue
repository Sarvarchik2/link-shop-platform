<template>
  <div class="platform-admin-users">
    <PlatformAdminSidebar :current-route="'users'" :model-value="sidebarOpen" @update:model-value="sidebarOpen = $event"
      @logout="handleLogout" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('platformAdmin.users.title') }}</h1>
            <p class="page-subtitle">Управление учетными записями всех пользователей системы</p>
          </div>
        </div>

        <div class="nav-right">
          <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
            <iconify-icon icon="lucide:rotate-cw" />
            <span>{{ $t('platformAdmin.dashboard.refresh') }}</span>
          </button>
          <button @click="exportData" class="export-btn">
            <iconify-icon icon="lucide:download" />
            <span>{{ $t('platformAdmin.shops.export') }}</span>
          </button>
        </div>
      </header>

      <div class="admin-scroll">
        <!-- Stats Row -->
        <div class="stats-row">
          <div class="stat-mini-card">
            <div class="stat-icon-s"><iconify-icon icon="lucide:users" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ users?.length || 0 }}</div>
              <div class="stat-lab">Всего</div>
            </div>
          </div>
          <div class="stat-mini-card">
            <div class="stat-icon-s admin"><iconify-icon icon="lucide:shield-check" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ adminUsersCount }}</div>
              <div class="stat-lab">Админы</div>
            </div>
          </div>
          <div class="stat-mini-card">
            <div class="stat-icon-s owner"><iconify-icon icon="lucide:store" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ shopOwnersCount }}</div>
              <div class="stat-lab">Владельцы</div>
            </div>
          </div>
          <div class="stat-mini-card">
            <div class="stat-icon-s user"><iconify-icon icon="lucide:user" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ regularUsersCount }}</div>
              <div class="stat-lab">Клиенты</div>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="filters-bar">
          <div class="search-input-wrap">
            <iconify-icon icon="lucide:search" />
            <input v-model="searchQuery" type="text" :placeholder="$t('platformAdmin.users.search')" />
          </div>

          <div class="filter-actions">
            <select v-model="filterRole" class="modern-select">
              <option value="">Все роли</option>
              <option value="platform_admin">Администраторы</option>
              <option value="shop_owner">Владельцы магазинов</option>
              <option value="user">Покупатели</option>
            </select>

            <button v-if="searchQuery || filterRole" @click="clearFilters" class="clear-btn">
              Сбросить
            </button>
          </div>
        </div>

        <!-- Table Card -->
        <div class="table-white-card">
          <div v-if="pending" class="loading-wrap">
            <div class="loader"></div>
          </div>
          <div v-else-if="displayedUsers.length === 0" class="empty-wrap">
            <iconify-icon icon="lucide:user-off" />
            <p>Пользователи не найдены</p>
          </div>
          <div v-else class="table-responsive">
            <table class="modern-table">
              <thead>
                <tr>
                  <th @click="sortBy('id')">ID <iconify-icon v-if="sortField === 'id'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th @click="sortBy('name')">Пользователь <iconify-icon v-if="sortField === 'name'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th @click="sortBy('phone')">Телефон <iconify-icon v-if="sortField === 'phone'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th>Роль</th>
                  <th @click="sortBy('shops')">Магазины <iconify-icon v-if="sortField === 'shops'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th @click="sortBy('orders')">Заказы <iconify-icon v-if="sortField === 'orders'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th @click="sortBy('created_at')">Регистрация <iconify-icon v-if="sortField === 'created_at'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in paginatedUsers" :key="user.id">
                  <td><span class="id-tag">#{{ user.id }}</span></td>
                  <td>
                    <div class="user-cell">
                      <div class="user-avatar" :class="getRoleClass(user.role)">
                        {{ getUserInitials(user) }}
                      </div>
                      <div class="user-info-text">
                        <div class="u-name">{{ getUserName(user) }}</div>
                        <div class="u-meta">ID: {{ user.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="phone-cell">
                      <iconify-icon icon="lucide:phone" />
                      {{ user.phone || '—' }}
                    </div>
                  </td>
                  <td>
                    <div class="role-pill" :class="getRoleClass(user.role)">
                      {{ getRoleText(user.role) }}
                    </div>
                  </td>
                  <td><span class="stat-count">{{ getUserShopsCount(user.id) }}</span></td>
                  <td><span class="stat-count">{{ getUserOrdersCount(user.id) }}</span></td>
                  <td>
                    <div class="date-cell">
                      <div class="d-val">{{ formatDate(user.created_at) }}</div>
                      <div class="d-time">{{ formatTime(user.created_at) }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="action-btns">
                      <button @click="viewUserDetails(user)" class="act-btn" v-tooltip="'Детали'">
                        <iconify-icon icon="lucide:eye" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="pagination-bar" v-if="totalPages > 1">
            <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn">
              <iconify-icon icon="lucide:chevron-left" />
            </button>
            <div class="page-info">Страница {{ currentPage }} из {{ totalPages }}</div>
            <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn">
              <iconify-icon icon="lucide:chevron-right" />
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t, locale } = useI18n()
const { token, logout } = useAuth()
const toast = useToast()
const config = useRuntimeConfig()
const router = useRouter()
const route = useRoute()

definePageMeta({ middleware: 'platform-admin' })

const sidebarOpen = ref(false)
const searchQuery = ref('')
const filterRole = ref('')
const sortField = ref('created_at')
const sortOrder = ref('desc')
const currentPage = ref(1)
const itemsPerPage = 12

const handleLogout = () => { logout(); toast.success(t('auth.loggedOut')) }

const { data: users, pending, error, refresh } = useFetch(config.public.apiBase + '/platform/admin/users', {
  lazy: true, watch: [token],
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const { data: shops } = useFetch(config.public.apiBase + '/platform/shops', {
  lazy: true, headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const { data: orders } = useFetch(config.public.apiBase + '/platform/admin/orders', {
  lazy: true, headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const adminUsersCount = computed(() => users.value?.filter(u => u.role === 'platform_admin').length || 0)
const shopOwnersCount = computed(() => users.value?.filter(u => u.role === 'shop_owner').length || 0)
const regularUsersCount = computed(() => users.value?.filter(u => u.role === 'user').length || 0)

const getUserShopsCount = (uid) => shops.value?.filter(s => s.owner_id === uid).length || 0
const getUserOrdersCount = (uid) => orders.value?.filter(o => o.user_id === uid).length || 0

const displayedUsers = computed(() => {
  let list = [...(users.value || [])]
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(u => `${u.first_name} ${u.last_name} ${u.phone}`.toLowerCase().includes(q))
  }
  if (filterRole.value) list = list.filter(u => u.role === filterRole.value)

  list.sort((a, b) => {
    let av = a[sortField.value], bv = b[sortField.value]
    if (sortField.value === 'shops') { av = getUserShopsCount(a.id); bv = getUserShopsCount(b.id) }
    else if (sortField.value === 'orders') { av = getUserOrdersCount(a.id); bv = getUserOrdersCount(b.id) }
    else if (sortField.value.includes('at')) { av = new Date(av).getTime(); bv = new Date(bv).getTime() }
    return sortOrder.value === 'asc' ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1)
  })
  return list
})

const totalPages = computed(() => Math.ceil(displayedUsers.value.length / itemsPerPage))
const paginatedUsers = computed(() => displayedUsers.value.slice((currentPage.value - 1) * itemsPerPage, currentPage.value * itemsPerPage))

const sortBy = (f) => {
  if (sortField.value === f) sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  else { sortField.value = f; sortOrder.value = 'asc' }
}

const clearFilters = () => { searchQuery.value = ''; filterRole.value = '' }

const formatDate = (d) => new Date(d).toLocaleDateString(locale.value, { day: 'numeric', month: 'short', year: 'numeric' })
const formatTime = (d) => new Date(d).toLocaleTimeString(locale.value, { hour: '2-digit', minute: '2-digit' })

const getUserInitials = (u) => {
  const f = u.first_name?.[0] || u.phone?.[0] || '?'
  const l = u.last_name?.[0] || ''
  return (f + l).toUpperCase()
}

const getUserName = (u) => `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.phone || 'Без имени'

const getRoleClass = (r) => ({ 'platform_admin': 'admin', 'shop_owner': 'owner', 'user': 'client' }[r] || 'client')
const getRoleText = (r) => ({ 'platform_admin': 'Админ', 'shop_owner': 'Владелец', 'user': 'Клиент' }[r] || r)

const viewUserDetails = (u) => toast.info(`Информация о пользователе ${getUserName(u)}`)
const exportData = () => {
  const csv = [['ID', 'Имя', 'Телефон', 'Роль', 'Создан'], ...(users.value || []).map(u => [u.id, getUserName(u), u.phone, u.role, u.created_at])].map(r => r.join(',')).join('\n')
  const b = new Blob([csv], { type: 'text/csv' }); const l = document.createElement('a')
  l.href = URL.createObjectURL(b); l.download = `users-${new Date().toISOString().split('T')[0]}.csv`; l.click()
}
</script>

<style scoped>
.platform-admin-users {
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

.nav-right {
  display: flex;
  gap: 12px;
}

.refresh-btn,
.export-btn {
  padding: 10px 18px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1.5px solid #e2e8f0;
  background: white;
}

.refresh-btn:hover,
.export-btn:hover {
  border-color: #111;
}

.admin-scroll {
  padding: 32px;
  flex: 1;
  overflow-y: auto;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-mini-card {
  background: white;
  padding: 24px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
}

.stat-icon-s {
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

.stat-icon-s.admin {
  background: #e0e7ff;
  color: #4338ca;
}

.stat-icon-s.owner {
  background: #dcfce7;
  color: #166534;
}

.stat-icon-s.user {
  background: #fef3c7;
  color: #92400e;
}

.stat-val {
  font-size: 1.5rem;
  font-weight: 950;
  color: #111;
}

.stat-lab {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
}

.filters-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 20px;
}

.search-input-wrap {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 12px 20px;
}

.search-input-wrap input {
  border: none;
  outline: none;
  width: 100%;
  font-weight: 600;
  font-size: 0.95rem;
}

.filter-actions {
  display: flex;
  gap: 12px;
}

.modern-select {
  padding: 12px 20px;
  border-radius: 16px;
  background: white;
  border: 1.5px solid #e2e8f0;
  font-weight: 700;
  font-size: 0.9rem;
  color: #1e293b;
  cursor: pointer;
}

.clear-btn {
  padding: 12px 20px;
  font-weight: 800;
  color: #ef4444;
  background: #fee2e2;
  border-radius: 16px;
  border: none;
  cursor: pointer;
  font-size: 0.85rem;
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
  cursor: pointer;
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

.user-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  color: #111;
  font-size: 0.9rem;
  border: 1.5px solid #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.user-avatar.admin {
  background: #e0e7ff;
  color: #4338ca;
}

.user-avatar.owner {
  background: #dcfce7;
  color: #166534;
}

.u-name {
  font-weight: 850;
  color: #111;
  font-size: 0.95rem;
}

.u-meta {
  font-size: 0.7rem;
  color: #94a3b8;
  font-weight: 700;
  margin-top: 2px;
}

.phone-cell {
  font-weight: 750;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #475569;
}

.phone-cell iconify-icon {
  color: #94a3b8;
}

.role-pill {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-pill.admin {
  background: #e0e7ff;
  color: #4338ca;
}

.role-pill.owner {
  background: #dcfce7;
  color: #166534;
}

.role-pill.client {
  background: #fef3c7;
  color: #92400e;
}

.stat-count {
  font-weight: 900;
  color: #111;
  background: #f8fafc;
  padding: 4px 12px;
  border-radius: 8px;
  display: inline-block;
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

.action-btns {
  display: flex;
  gap: 6px;
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
  font-size: 1.1rem;
}

.act-btn:hover {
  border-color: #111;
  color: #111;
  background: #f8fafc;
}

.pagination-bar {
  padding: 24px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.page-btn {
  width: 40px;
  height: 40px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-weight: 800;
  font-size: 0.85rem;
  color: #1e293b;
}

.loading-wrap,
.empty-wrap {
  padding: 100px 0;
  text-align: center;
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

.empty-wrap iconify-icon {
  font-size: 3rem;
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-wrap p {
  font-weight: 800;
  color: #64748b;
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

  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
