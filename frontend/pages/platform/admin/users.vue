<template>
  <div class="platform-admin-page">
    <!-- Sidebar - копируем из основной админки -->
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
          <h1 class="admin-title">Управление пользователями</h1>
          <p class="admin-subtitle">Все зарегистрированные пользователи платформы</p>
        </div>
      </div>

      <div class="admin-content">
        <div v-if="error" class="text-center py-12 text-red-500">
          <p class="mt-4">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
          <button @click="refresh" class="mt-4 px-4 py-2 bg-black text-white rounded-lg">Повторить</button>
        </div>
        <div v-else-if="pending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Пользователи загружаются...</p>
        </div>

        <div v-else class="users-table-wrapper">
          <table class="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Имя</th>
                <th>Телефон</th>
                <th>Роль</th>
                <th>Дата регистрации</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>
                  <div class="user-info">
                    <div class="user-avatar">
                      {{ getUserInitials(user) }}
                    </div>
                    <span class="user-name">{{ getUserName(user) }}</span>
                  </div>
                </td>
                <td>{{ user.phone }}</td>
                <td>
                  <span :class="['role-badge', getRoleClass(user.role)]">
                    {{ getRoleText(user.role) }}
                  </span>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'platform-admin'
})

const { token } = useAuth()

const { data: users, pending, error, refresh } = await useFetch('http://localhost:8000/platform/admin/users', {
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
    console.error('[Admin Users] Ошибка загрузки пользователей:', newError)
    console.error('[Admin Users] Детали ошибки:', {
      message: newError.message,
      statusCode: newError.statusCode,
      statusMessage: newError.statusMessage,
      data: newError.data
    })
  }
}, { immediate: true })

watch(token, () => {
  if (token.value) {
    console.log('[Admin Users] Токен обновлен, обновляю данные...')
    refresh()
  }
}, { immediate: true })

watch(users, (newUsers) => {
  if (newUsers) {
    console.log('[Admin Users] Пользователи загружены:', newUsers)
  }
})

const getUserInitials = (user) => {
  const first = user.first_name?.[0] || user.phone?.[0] || '?'
  const last = user.last_name?.[0] || ''
  return (first + last).toUpperCase()
}

const getUserName = (user) => {
  return `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.phone
}

const getRoleClass = (role) => {
  const roleMap = {
    'platform_admin': 'role-admin',
    'user': 'role-user'
  }
  return roleMap[role] || 'role-user'
}

const getRoleText = (role) => {
  const roleMap = {
    'platform_admin': 'Админ платформы',
    'user': 'Пользователь'
  }
  return roleMap[role] || role
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>

<style scoped>
/* Используем те же стили что и в shops.vue */
.platform-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

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

.users-table-wrapper {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: #F9FAFB;
}

.users-table th {
  padding: 16px;
  text-align: left;
  font-weight: 700;
  font-size: 0.875rem;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table td {
  padding: 16px;
  border-top: 1px solid #E5E7EB;
  font-size: 0.875rem;
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
}

.user-name {
  font-weight: 600;
  color: #111;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.role-admin {
  background: #111;
  color: white;
}

.role-user {
  background: #F3F4F6;
  color: #4B5563;
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

