<template>
  <div class="platform-admin-shops">
    <PlatformAdminSidebar :current-route="'shops'" :model-value="sidebarOpen" @update:model-value="sidebarOpen = $event"
      @logout="handleLogout" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('platformAdmin.shops.title') }}</h1>
            <p class="page-subtitle">{{ $t('platformAdmin.shops.subtitle') }}</p>
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
            <div class="stat-icon-s"><iconify-icon icon="lucide:store" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ shops?.length || 0 }}</div>
              <div class="stat-lab">Всего магазинов</div>
            </div>
          </div>
          <div class="stat-mini-card">
            <div class="stat-icon-s active"><iconify-icon icon="lucide:check-circle" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ activeShopsCount }}</div>
              <div class="stat-lab">Работают</div>
            </div>
          </div>
          <div class="stat-mini-card">
            <div class="stat-icon-s trial"><iconify-icon icon="lucide:clock" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ trialShopsCount }}</div>
              <div class="stat-lab">На триале</div>
            </div>
          </div>
          <div class="stat-mini-card">
            <div class="stat-icon-s expired"><iconify-icon icon="lucide:alert-triangle" /></div>
            <div class="stat-body">
              <div class="stat-val">{{ expiredShopsCount }}</div>
              <div class="stat-lab">Срок истек</div>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="filters-bar">
          <div class="search-input-wrap">
            <iconify-icon icon="lucide:search" />
            <input v-model="searchQuery" type="text" :placeholder="$t('platformAdmin.shops.search')" />
          </div>

          <div class="filter-actions">
            <select v-model="filterStatus" class="modern-select">
              <option value="">Все статусы</option>
              <option value="trial">Триал</option>
              <option value="active">Активные</option>
              <option value="expired">Истекли</option>
            </select>

            <select v-model="filterActive" class="modern-select">
              <option value="">Все типы</option>
              <option value="true">Активные маг.</option>
              <option value="false">Деактивированные</option>
            </select>

            <button v-if="searchQuery || filterStatus || filterActive" @click="clearFilters" class="clear-btn">
              Сбросить
            </button>
          </div>
        </div>

        <!-- Table Card -->
        <div class="table-white-card">
          <div v-if="pending" class="loading-wrap">
            <div class="loader"></div>
          </div>
          <div v-else-if="displayedShops.length === 0" class="empty-wrap">
            <iconify-icon icon="lucide:search-x" />
            <p>Ничего не найдено</p>
          </div>
          <div v-else class="table-responsive">
            <table class="modern-table">
              <thead>
                <tr>
                  <th @click="sortBy('id')">ID <iconify-icon v-if="sortField === 'id'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th @click="sortBy('name')">Магазин <iconify-icon v-if="sortField === 'name'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th>Slug / Ссылка</th>
                  <th @click="sortBy('owner')">Владелец <iconify-icon v-if="sortField === 'owner'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th>Статус</th>
                  <th @click="sortBy('expires_at')">Истекает <iconify-icon v-if="sortField === 'expires_at'"
                      :icon="sortOrder === 'asc' ? 'lucide:arrow-up' : 'lucide:arrow-down'" /></th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="shop in paginatedShops" :key="shop.id" :class="{ 'expiring-soon': isExpiringSoon(shop) }">
                  <td><span class="id-tag">#{{ shop.id }}</span></td>
                  <td>
                    <div class="shop-cell">
                      <div class="shop-img">
                        <img v-if="shop.logo_url" :src="shop.logo_url" />
                        <span v-else>{{ shop.name.charAt(0) }}</span>
                      </div>
                      <div class="shop-info-text">
                        <div class="s-name">{{ shop.name }}</div>
                        <div class="s-date">Создан: {{ formatDate(shop.created_at) }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="slug-cell">
                      <code>{{ shop.slug }}</code>
                      <a :href="'/' + shop.slug" target="_blank"><iconify-icon icon="lucide:external-link" /></a>
                    </div>
                  </td>
                  <td>
                    <div class="owner-cell">
                      <div class="o-name">{{ shop.owner_name || '—' }}</div>
                      <div class="o-phone" v-if="shop.owner_phone">
                        <iconify-icon icon="lucide:phone" /> {{ shop.owner_phone }}
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="status-pill" :class="shop.subscription_status">
                      {{ getStatusText(shop.subscription_status) }}
                    </div>
                  </td>
                  <td>
                    <div class="expiry-cell">
                      <div class="e-date">{{ shop.subscription_expires_at ? formatDate(shop.subscription_expires_at) :
                        'Бессрочно' }}</div>
                      <div v-if="shop.subscription_expires_at" class="e-days" :class="getDaysRemainingClass(shop)">
                        {{ getDaysRemaining(shop) }}
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="action-btns">
                      <button @click="openSubscriptionModal(shop)" class="act-btn sub" v-tooltip="'Подписка'">
                        <iconify-icon icon="lucide:credit-card" />
                      </button>
                      <button @click="openPasswordModal('activate', shop)" class="act-btn"
                        :class="shop.is_active ? 'deactivate' : 'activate'"
                        v-tooltip="shop.is_active ? 'Выключить' : 'Включить'">
                        <iconify-icon :icon="shop.is_active ? 'lucide:power-off' : 'lucide:power'" />
                      </button>
                      <button @click="openPasswordModal('delete', shop)" class="act-btn delete" v-tooltip="'Удалить'">
                        <iconify-icon icon="lucide:trash-2" />
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

    <!-- Subscription Modal -->
    <Transition name="scale">
      <div v-if="showModal && selectedShop" class="modal-overlay" @click="closeModal">
        <div class="modal-win" @click.stop>
          <div class="modal-header">
            <h3>Управление подпиской</h3>
            <button @click="closeModal" class="close-modal"><iconify-icon icon="lucide:x" /></button>
          </div>

          <div class="modal-body">
            <div class="shop-preview">
              <div class="sp-logo">
                <img v-if="selectedShop.logo_url" :src="selectedShop.logo_url" />
                <span v-else>{{ selectedShop.name.charAt(0) }}</span>
              </div>
              <div class="sp-text">
                <h4>{{ selectedShop.name }}</h4>
                <p>{{ selectedShop.owner_name }} • {{ selectedShop.slug }}</p>
              </div>
            </div>

            <div class="current-sub-box">
              <div class="cs-label">Текущий тариф: <span>{{ selectedShop.subscription_plan_name || 'Нет' }}</span></div>
              <div class="cs-label">Статус: <span :class="selectedShop.subscription_status">{{
                getStatusText(selectedShop.subscription_status) }}</span></div>
            </div>

            <form @submit.prevent="updateSubscription" class="sub-form">
              <div class="f-group">
                <label>Изменить статус</label>
                <select v-model="subscriptionForm.status" class="modern-input">
                  <option value="trial">Пробный период</option>
                  <option value="active">Активна</option>
                  <option value="expired">Срок истек</option>
                  <option value="cancelled">Отменена</option>
                </select>
              </div>

              <div class="f-group">
                <label>Дата истечения</label>
                <input v-model="subscriptionForm.expires_at" type="datetime-local" class="modern-input" />
              </div>

              <div class="quick-dates">
                <button type="button" v-for="m in [1, 3, 6, 12]" :key="m" @click="setExpiry(m)">
                  +{{ m }} мес.
                </button>
              </div>

              <div class="form-btns">
                <button type="button" @click="closeModal" class="btn-cancel">Отмена</button>
                <button type="submit" class="btn-save" :disabled="isUpdating">
                  <span v-if="isUpdating" class="loader-sm"></span>
                  <span v-else>Сохранить изменения</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Password Confirmation Modal -->
    <Transition name="fade">
      <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
        <div class="pwd-modal" @click.stop>
          <div class="pwd-header">
            <div class="pwd-icon" :class="pendingAction?.type"><iconify-icon
                :icon="pendingAction?.type === 'delete' ? 'lucide:alert-triangle' : 'lucide:lock'" /></div>
            <h3>Подтверждение</h3>
          </div>
          <p class="pwd-msg">{{ passwordModalMessage }}</p>
          <form @submit.prevent="confirmPasswordAction">
            <input v-model="passwordInput" type="password" placeholder="Введите ваш пароль администратора" required
              class="modern-input" />
            <div class="pwd-btns">
              <button type="button" @click="closePasswordModal" class="btn-cancel">Отмена</button>
              <button type="submit" class="btn-confirm" :class="pendingAction?.type" :disabled="isConfirming">
                {{ isConfirming ? 'Ждите...' : 'Подтверждаю' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
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
const filterStatus = ref('')
const filterActive = ref('')
const sortField = ref('created_at')
const sortOrder = ref('desc')
const currentPage = ref(1)
const itemsPerPage = 12

const showModal = ref(false)
const selectedShop = ref(null)
const subscriptionHistory = ref([])
const subscriptionForm = reactive({ status: 'trial', expires_at: '' })
const isUpdating = ref(false)

const showPasswordModal = ref(false)
const passwordInput = ref('')
const pendingAction = ref(null)
const isConfirming = ref(false)

const { data: shops, pending, refresh, error } = useFetch(config.public.apiBase + '/platform/shops', {
  lazy: true,
  watch: [token],
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const handleLogout = () => { logout(); toast.success(t('auth.loggedOut')) }

const activeShopsCount = computed(() => shops.value?.filter(s => s.is_active).length || 0)
const trialShopsCount = computed(() => shops.value?.filter(s => s.subscription_status === 'trial').length || 0)
const expiredShopsCount = computed(() => shops.value?.filter(s => s.subscription_status === 'expired').length || 0)

const displayedShops = computed(() => {
  let list = [...(shops.value || [])]
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(s => s.name.toLowerCase().includes(q) || s.slug.toLowerCase().includes(q) || (s.owner_name && s.owner_name.toLowerCase().includes(q)))
  }
  if (filterStatus.value) list = list.filter(s => s.subscription_status === filterStatus.value)
  if (filterActive.value !== '') list = list.filter(s => String(s.is_active) === filterActive.value)

  list.sort((a, b) => {
    let av = a[sortField.value], bv = b[sortField.value]
    if (sortField.value.includes('at')) { av = new Date(av).getTime(); bv = new Date(bv).getTime() }
    return sortOrder.value === 'asc' ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1)
  })
  return list
})

const totalPages = computed(() => Math.ceil(displayedShops.value.length / itemsPerPage))
const paginatedShops = computed(() => displayedShops.value.slice((currentPage.value - 1) * itemsPerPage, currentPage.value * itemsPerPage))

const sortBy = (f) => {
  if (sortField.value === f) sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  else { sortField.value = f; sortOrder.value = 'asc' }
}

const clearFilters = () => { searchQuery.value = ''; filterStatus.value = ''; filterActive.value = '' }

const getStatusText = (s) => t(`platformAdmin.dashboard.status.${s}`) || s
const formatDate = (d) => new Date(d).toLocaleDateString(locale.value, { day: 'numeric', month: 'short', year: 'numeric' })

const getDaysRemaining = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return ''
  const diff = Math.ceil((new Date(shop.subscription_expires_at) - new Date()) / (1000 * 60 * 60 * 24))
  return diff <= 0 ? 'Истек' : `${diff} дн. осталось`
}

const getDaysRemainingClass = (shop) => {
  if (!shop.subscription_expires_at) return ''
  const diff = Math.ceil((new Date(shop.subscription_expires_at) - new Date()) / (1000 * 60 * 60 * 24))
  return diff <= 3 ? 'critical' : (diff <= 7 ? 'warning' : 'normal')
}

const isExpiringSoon = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return false
  const diff = Math.ceil((new Date(shop.subscription_expires_at) - new Date()) / (1000 * 60 * 60 * 24))
  return diff > 0 && diff <= 7
}

const openSubscriptionModal = (shop) => {
  selectedShop.value = shop
  subscriptionForm.status = shop.subscription_status
  subscriptionForm.expires_at = shop.subscription_expires_at ? new Date(shop.subscription_expires_at).toISOString().slice(0, 16) : ''
  showModal.value = true
}

const closeModal = () => { showModal.value = false; selectedShop.value = null }

const setExpiry = (m) => {
  const d = new Date(); d.setMonth(d.getMonth() + m)
  subscriptionForm.expires_at = d.toISOString().slice(0, 16)
  subscriptionForm.status = 'active'
}

const updateSubscription = async () => {
  isUpdating.value = true
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/shops/${selectedShop.value.id}/subscription`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body: {
        subscription_status: subscriptionForm.status,
        expires_at: subscriptionForm.expires_at ? new Date(subscriptionForm.expires_at).toISOString() : null
      }
    })
    toast.success('Подписка обновлена')
    closeModal(); refresh()
  } catch (e) { toast.error(e.data?.detail || 'Ошибка') } finally { isUpdating.value = false }
}

const passwordModalMessage = computed(() => {
  if (pendingAction.value?.type === 'delete') return `Вы уверены, что хотите УДАЛИТЬ магазин "${pendingAction.value.shop.name}"? Это действие необратимо и удалит все данные.`
  return `Вы хотите ${pendingAction.value?.shop.is_active ? 'ДЕАКТИВИРОВАТЬ' : 'АКТИВИРОВАТЬ'} магазин "${pendingAction.value?.shop.name}"?`
})

const openPasswordModal = (type, shop) => { pendingAction.value = { type, shop }; passwordInput.value = ''; showPasswordModal.value = true }
const closePasswordModal = () => { showPasswordModal.value = false; pendingAction.value = null }

const confirmPasswordAction = async () => {
  isConfirming.value = true
  try {
    const { type, shop } = pendingAction.value
    if (type === 'activate') {
      await $fetch(`${config.public.apiBase}/platform/admin/shops/${shop.id}/activate`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token.value}` },
        body: { is_active: !shop.is_active, password: passwordInput.value }
      })
      toast.success(shop.is_active ? 'Магазин выключен' : 'Магазин включен')
    } else if (type === 'delete') {
      await $fetch(`${config.public.apiBase}/platform/admin/shops/${shop.id}/delete`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token.value}` },
        body: { password: passwordInput.value }
      })
      toast.success('Магазин удален')
    }
    refresh(); closePasswordModal()
  } catch (e) { toast.error(e.data?.detail || 'Ошибка пароля') } finally { isConfirming.value = false }
}

const exportData = () => {
  const csv = [['ID', 'Название', 'Slug', 'Владелец', 'Статус', 'Истекает', 'Создан'], ...(shops.value || []).map(s => [s.id, s.name, s.slug, s.owner_name, s.subscription_status, s.subscription_expires_at, s.created_at])].map(r => r.join(',')).join('\n')
  const b = new Blob([csv], { type: 'text/csv' }); const l = document.createElement('a')
  l.href = URL.createObjectURL(b); l.download = `shops-${new Date().toISOString().split('T')[0]}.csv`; l.click()
}
</script>

<style scoped>
.platform-admin-shops {
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
  font-weight: 500;
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
  color: #1e293b;
}

.refresh-btn:hover,
.export-btn:hover {
  border-color: #111;
  background: #f8fafc;
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

.stat-icon-s.active {
  background: #dcfce7;
  color: #166534;
}

.stat-icon-s.trial {
  background: #fef3c7;
  color: #92400e;
}

.stat-icon-s.expired {
  background: #fee2e2;
  color: #991b1b;
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
  transition: all 0.2s;
}

.search-input-wrap:focus-within {
  border-color: #111;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.03);
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

.shop-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.shop-img {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-weight: 900;
  color: #111;
  border: 1px solid #e2e8f0;
}

.shop-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.s-name {
  font-weight: 850;
  color: #111;
  font-size: 0.95rem;
}

.s-date {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 2px;
}

.slug-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.slug-cell code {
  background: #f8fafc;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #111;
  font-family: 'JetBrains Mono', monospace;
}

.slug-cell a {
  color: #94a3b8;
  transition: color 0.2s;
}

.slug-cell a:hover {
  color: #111;
}

.o-name {
  font-weight: 750;
  font-size: 0.9rem;
}

.o-phone {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 2px;
}

.status-pill {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 850;
  text-transform: uppercase;
}

.status-pill.active {
  background: #dcfce7;
  color: #166534;
}

.status-pill.trial {
  background: #fef3c7;
  color: #92400e;
}

.status-pill.expired {
  background: #fee2e2;
  color: #991b1b;
}

.status-pill.cancelled {
  background: #f1f5f9;
  color: #475569;
}

.expiry-cell {
  font-size: 0.85rem;
  font-weight: 700;
}

.e-days {
  font-size: 0.7rem;
  margin-top: 4px;
  font-weight: 850;
}

.e-days.critical {
  color: #ef4444;
}

.e-days.warning {
  color: #f59e0b;
}

.e-days.normal {
  color: #10b981;
}

.action-btns {
  display: flex;
  gap: 6px;
}

.act-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
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

.act-btn.sub:hover {
  color: #2563eb;
  border-color: #2563eb;
  background: #eff6ff;
}

.act-btn.activate:hover {
  color: #10b981;
  border-color: #10b981;
  background: #f0fdf4;
}

.act-btn.deactivate:hover {
  color: #f97316;
  border-color: #f97316;
  background: #fff7ed;
}

.act-btn.delete:hover {
  color: #ef4444;
  border-color: #ef4444;
  background: #fef2f2;
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
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #111;
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

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-win {
  background: white;
  border-radius: 32px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 32px 32px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 950;
  letter-spacing: -1px;
}

.close-modal {
  background: #f1f5f9;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.modal-body {
  padding: 32px;
}

.shop-preview {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #f8fafc;
  padding: 20px;
  border-radius: 20px;
  margin-bottom: 24px;
}

.sp-logo {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 950;
}

.sp-logo img {
  width: 100%;
  height: 100%;
  border-radius: 14px;
  object-fit: cover;
}

.sp-text h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 900;
}

.sp-text p {
  margin: 4px 0 0;
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 700;
}

.current-sub-box {
  margin-bottom: 24px;
  display: grid;
  gap: 8px;
}

.cs-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: #64748b;
}

.cs-label span {
  color: #111;
  font-weight: 900;
  margin-left: 8px;
}

.cs-label span.active {
  color: #10b981;
}

.sub-form {
  display: grid;
  gap: 20px;
}

.f-group {
  display: grid;
  gap: 8px;
}

.f-group label {
  font-size: 0.8rem;
  font-weight: 850;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modern-input {
  width: 100%;
  padding: 14px 20px;
  border-radius: 16px;
  border: 1.5px solid #e2e8f0;
  font-weight: 700;
  outline: none;
  transition: all 0.2s;
}

.modern-input:focus {
  border-color: #111;
}

.quick-dates {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-dates button {
  flex: 1;
  padding: 10px;
  background: #f1f5f9;
  border: none;
  border-radius: 10px;
  font-weight: 900;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-dates button:hover {
  background: #111;
  color: white;
}

.form-btns {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

.btn-cancel {
  flex: 1;
  padding: 14px;
  border-radius: 16px;
  background: #f1f5f9;
  color: #475569;
  border: none;
  font-weight: 800;
  cursor: pointer;
}

.btn-save {
  flex: 2;
  padding: 14px;
  border-radius: 16px;
  background: #111;
  color: white;
  border: none;
  font-weight: 900;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-sm {
  border: 3px solid rgba(255, 255, 255, 0.2);
  border-top: 3px solid #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 0.8s linear infinite;
}

/* PWD Modal */
.pwd-modal {
  background: white;
  border-radius: 32px;
  width: 100%;
  max-width: 400px;
  padding: 32px;
  box-shadow: 0 30px 60px -12px rgba(15, 23, 42, 0.2);
}

.pwd-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.pwd-icon {
  width: 50px;
  height: 50px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.pwd-icon.delete {
  background: #fee2e2;
  color: #ef4444;
}

.pwd-icon.activate {
  background: #f1f5f9;
  color: #111;
}

.pwd-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 950;
  letter-spacing: -0.5px;
}

.pwd-msg {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 24px;
  font-weight: 600;
}

.pwd-btns {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-confirm {
  flex: 2;
  padding: 14px;
  border-radius: 16px;
  background: #111;
  color: white;
  border: none;
  font-weight: 900;
  cursor: pointer;
}

.btn-confirm.delete {
  background: #ef4444;
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

  .filter-actions {
    overflow-x: auto;
    padding-bottom: 8px;
  }
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
