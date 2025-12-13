<template>
  <div class="platform-admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
            <path d="M2 17l10 5 10-5"></path>
            <path d="M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <h2 class="sidebar-title">Панель управления</h2>
      </div>
      
      <nav class="sidebar-nav">
        <NuxtLink to="/platform/admin" class="nav-item" :class="{ active: $route.path === '/platform/admin' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        
        <NuxtLink to="/platform/admin/shops" class="nav-item" :class="{ active: $route.path === '/platform/admin/shops' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
          </svg>
          <span>Магазины</span>
        </NuxtLink>
        
        <NuxtLink to="/platform/admin/users" class="nav-item" :class="{ active: $route.path === '/platform/admin/users' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>Пользователи</span>
        </NuxtLink>
        
        <NuxtLink to="/platform/admin/orders" class="nav-item" :class="{ active: $route.path === '/platform/admin/orders' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Заказы</span>
        </NuxtLink>
      </nav>
      
      <div class="sidebar-footer">
        <NuxtLink to="/" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>На главную</span>
        </NuxtLink>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div>
          <h1 class="admin-title">Управление магазинами</h1>
          <p class="admin-subtitle">Все зарегистрированные магазины на платформе</p>
        </div>
      </div>

      <div class="admin-content">
        <div v-if="error" class="text-center py-12 text-red-500">
          <p class="mt-4">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
          <button @click="refresh" class="mt-4 px-4 py-2 bg-black text-white rounded-lg">Повторить</button>
        </div>
        <div v-else-if="pending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Магазины загружаются...</p>
        </div>

        <div v-else class="shops-table-wrapper">
          <table class="shops-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Slug</th>
                <th>Владелец</th>
                <th>Статус подписки</th>
                <th>Истекает</th>
                <th>Активен</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="shop in shops" :key="shop.id">
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
                    <span class="shop-name">{{ shop.name }}</span>
                  </div>
                </td>
                <td>
                  <code class="shop-slug">{{ shop.slug }}</code>
                </td>
                <td>
                  <div class="owner-info">
                    <div class="owner-name">{{ shop.owner_name || `ID: ${shop.owner_id}` }}</div>
                    <div class="owner-phone" v-if="shop.owner_phone">{{ shop.owner_phone }}</div>
                  </div>
                </td>
                <td>
                  <span :class="['status-badge', getStatusClass(shop.subscription_status)]">
                    {{ getStatusText(shop.subscription_status) }}
                  </span>
                </td>
                <td>
                  {{ shop.subscription_expires_at ? formatDate(shop.subscription_expires_at) : '-' }}
                </td>
                <td>
                  <span :class="['status-badge', shop.is_active ? 'status-active' : 'status-cancelled']">
                    {{ shop.is_active ? 'Да' : 'Нет' }}
                  </span>
                </td>
                <td>
                  <div class="actions">
                    <button 
                      @click="toggleActive(shop)"
                      :class="['action-btn', shop.is_active ? 'btn-danger' : 'btn-success']"
                    >
                      {{ shop.is_active ? 'Деактивировать' : 'Активировать' }}
                    </button>
                    <button 
                      @click="openSubscriptionModal(shop)"
                      class="action-btn btn-primary"
                    >
                      Подписка
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Subscription Modal -->
        <div v-if="showModal" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <h2 class="modal-title">Управление подпиской</h2>
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
              </div>
              <div class="modal-actions">
                <button type="button" @click="closeModal" class="btn-secondary">Отмена</button>
                <button type="submit" class="btn-primary">Сохранить</button>
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

console.log('[Admin Shops] Страница загружается...')
console.log('[Admin Shops] Текущий путь:', useRoute().path)

const { token } = useAuth()
const toast = useToast()

onMounted(() => {
  console.log('[Admin Shops] Компонент смонтирован')
})

const { data: shops, pending, refresh, error } = await useFetch('http://localhost:8000/platform/admin/shops', {
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
    console.error('[Admin Shops] Ошибка загрузки магазинов:', newError)
    console.error('[Admin Shops] Детали ошибки:', {
      message: newError.message,
      statusCode: newError.statusCode,
      statusMessage: newError.statusMessage,
      data: newError.data
    })
  }
}, { immediate: true })

watch(token, () => {
  if (token.value) {
    console.log('[Admin Shops] Токен обновлен, обновляю данные...')
    refresh()
  }
}, { immediate: true })

watch(shops, (newShops) => {
  if (newShops) {
    console.log('[Admin Shops] Магазины загружены:', newShops)
  }
})

const showModal = ref(false)
const selectedShop = ref(null)
const subscriptionForm = reactive({
  status: 'trial',
  expires_at: ''
})

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

const openSubscriptionModal = (shop) => {
  selectedShop.value = shop
  subscriptionForm.status = shop.subscription_status
  subscriptionForm.expires_at = shop.subscription_expires_at ? new Date(shop.subscription_expires_at).toISOString().slice(0, 16) : ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedShop.value = null
}

const updateSubscription = async () => {
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
    toast.success('Подписка обновлена')
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
  background: #FAFAFA;
}

/* Sidebar - копируем из основной админки */
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
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  text-decoration: none;
  font-size: 0.875rem;
}

.back-link:hover {
  color: #111;
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

.shops-table-wrapper {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
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
  font-size: 0.875rem;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.shops-table td {
  padding: 16px;
  border-top: 1px solid #E5E7EB;
  font-size: 0.875rem;
}

.shop-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shop-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.shop-logo-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: #111;
}

.shop-name {
  font-weight: 600;
  color: #111;
}

.shop-slug {
  background: #F3F4F6;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-family: monospace;
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
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
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

.actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
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
  border-radius: 16px;
  padding: 32px;
  max-width: 500px;
  width: 90%;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 900;
  margin-bottom: 24px;
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

.form-group label {
  font-weight: 600;
  font-size: 0.875rem;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
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


