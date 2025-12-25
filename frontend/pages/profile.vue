<template>
  <div class="profile-page">
    <AppHeader />
    
    <main class="profile-content">
      <div class="profile-layout">
        <!-- Left Column - Profile Card -->
        <div class="profile-left">
        <div class="profile-header">
            <div class="profile-card">
              <div class="profile-avatar">
                <span class="avatar-text">{{ getInitials }}</span>
              </div>
              <h1 class="profile-name">{{ fullName || 'User' }}</h1>
          
              
              <!-- Links based on role -->
              <div class="profile-role-links">
                <NuxtLink 
                  v-if="user?.role === 'platform_admin'" 
                  to="/platform/admin" 
                  class="role-link platform-link"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                  </svg>
                  Открыть админку платформы
                </NuxtLink>
                <template v-else-if="user?.role === 'shop_owner' && myShops && myShops.length > 0">
                  <NuxtLink 
                    :to="`/${myShops[0].slug}`" 
                    class="role-link shop-link"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                      <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                    Мой магазин
                  </NuxtLink>
                  <NuxtLink 
                    :to="`/shop/${myShops[0].slug}/admin`" 
                    class="role-link shop-admin-link"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                      <path d="M2 17l10 5 10-5"></path>
                      <path d="M2 12l10 5 10-5"></path>
                    </svg>
                    Админка магазина
                  </NuxtLink>
                </template>
              </div>
              
              <!-- Desktop Quick Stats -->
              <div class="profile-stats">
                <div class="stat-item">
                  <span class="stat-value">#{{ user?.id }}</span>
                  <span class="stat-label">Foydalanuvchi ID</span>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-item">
                  <span class="stat-value role-indicator" :class="user?.role">
                    {{ user?.role === 'platform_admin' ? 'Admin' : user?.role === 'shop_owner' ? 'Владелец магазина' : 'Foydalanuvchi' }}
                  </span>
                  <span class="stat-label">Rol</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="quick-actions" v-if="user">
            <NuxtLink to="/orders" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
              </div>
              <span>Buyurtmalarim</span>
            </NuxtLink>
            <NuxtLink to="/favorites" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
        </div>
              <span>Sevimlilar</span>
            </NuxtLink>
            <NuxtLink to="/cart" class="action-card">
              <div class="action-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
              <span>Savatcha</span>
            </NuxtLink>
            <NuxtLink to="/products" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                  <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
            </div>
              <span>Mahsulotlar</span>
          </NuxtLink>
          </div>
        </div>

        <!-- Right Column - Info & Actions -->
        <div class="profile-right">
          <!-- User Info Section -->
          <div class="info-section">
            <h2 class="section-title">Shaxsiy ma'lumotlar</h2>
            
            <div class="info-card">
              <div class="info-item">
                <div class="info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div class="info-content">
                  <span class="info-label">Ism</span>
                  <span class="info-value">{{ user?.first_name || '—' }}</span>
                </div>
              </div>

              <div class="info-item">
                <div class="info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div class="info-content">
                  <span class="info-label">Familiya</span>
                  <span class="info-value">{{ user?.last_name || '—' }}</span>
                </div>
              </div>

              <div class="info-item">
                <div class="info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                  </svg>
                </div>
                <div class="info-content">
                  <span class="info-label">Telefon raqam</span>
                  <span class="info-value">{{ user?.phone || '—' }}</span>
                </div>
              </div>

             
            </div>
          </div>

          <!-- Info for users without shops -->
          <div v-if="(!myShops || myShops.length === 0) && user?.role !== 'shop_owner' && user?.role !== 'platform_admin'" class="no-shops-section">
            <div class="info-box">
              <h3>Профиль владельца магазина</h3>
              <p>Этот профиль предназначен для владельцев магазинов. Если вы хотите создать магазин, нажмите кнопку ниже.</p>
              <NuxtLink to="/register-shop" class="create-shop-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
                Создать магазин
          </NuxtLink>
              <p class="redirect-note">
                Если вы покупатель, перейдите в <NuxtLink to="/customer-profile" class="redirect-link">профиль покупателя</NuxtLink>
              </p>
            </div>
          </div>

          <!-- My Shops Section -->
          <div v-if="shopsPending" class="text-center py-8 text-gray-400">
            <div class="loading-spinner"></div>
            <p class="mt-4">Загрузка магазинов...</p>
          </div>
          
          <div v-else-if="myShops && myShops.length > 0" class="shops-section">
            <h2 class="section-title">Мои магазины</h2>
            <div class="shops-list">
              <div v-for="shop in myShops" :key="shop.id" class="shop-item">
                <div class="shop-info">
                  <div class="shop-logo-small">
                    <img v-if="shop.logo_url" :src="shop.logo_url" :alt="shop.name" />
                    <span v-else>{{ shop.name.charAt(0).toUpperCase() }}</span>
                  </div>
                  <div class="shop-details">
                    <h3 class="shop-name-small">{{ shop.name }}</h3>
                    <p class="shop-url">link-platform-shop.uz/{{ shop.slug }}</p>
                    
                    <!-- Subscription Info -->
                    <div class="subscription-info">
                      <span :class="['shop-status-badge', getStatusClass(shop.subscription_status)]">
                        {{ getStatusText(shop.subscription_status) }}
                      </span>
                      <span v-if="shop.subscription_expires_at" class="subscription-expires">
                        {{ formatDate(shop.subscription_expires_at) }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="shop-actions">
                  <NuxtLink :to="`/${shop.slug}`" class="shop-action-btn view" target="_blank">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                    Открыть магазин
                  </NuxtLink>
                  <NuxtLink :to="`/shop/${shop.slug}/admin`" class="shop-action-btn admin">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                      <path d="M2 17l10 5 10-5"></path>
                      <path d="M2 12l10 5 10-5"></path>
                    </svg>
                    Админка магазина
                  </NuxtLink>
                  <NuxtLink v-if="shop.subscription_status === 'trial' || shop.subscription_status === 'expired'" :to="`/shop/${shop.slug}/subscription`" class="shop-action-btn subscription">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="12" y1="1" x2="12" y2="23"></line>
                      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                    </svg>
                    Подписка
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>


          <!-- Platform Admin Section -->
          <div v-if="user?.role === 'platform_admin'" class="platform-admin-section">
            <h2 class="section-title">Админка платформы</h2>
            <div class="admin-info-card">
              <div class="admin-info">
                <div class="admin-icon">👑</div>
                <div class="admin-details">
                  <h3>Панель управления платформой</h3>
                  <p>Управляйте всеми магазинами, подписками и пользователями платформы</p>
                </div>
              </div>
              <NuxtLink to="/platform/admin" class="admin-panel-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                  <path d="M2 17l10 5 10-5"></path>
                  <path d="M2 12l10 5 10-5"></path>
                </svg>
                Открыть админку платформы
              </NuxtLink>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">

            <!-- Logout Button -->
            <button @click="handleLogout" class="logout-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              Chiqish
            </button>
            </div>

          <!-- App Version -->
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

// Профиль только для владельцев магазинов
// Покупатели должны использовать обычный профиль покупателя

const { user, logout, token } = useAuth()

// Only fetch shops if user is shop_owner or platform_admin
const shouldFetchShops = computed(() => {
  return token.value && (user.value?.role === 'shop_owner' || user.value?.role === 'platform_admin')
})

const myShops = ref([])
const shopsPending = ref(false)
const shopsError = ref(null)

const refreshShops = async () => {
  // Дополнительная проверка перед запросом
  if (!token.value || !user.value) {
    myShops.value = []
    return
  }
  
  // Проверяем роль пользователя перед запросом
  const userRole = user.value?.role
  if (!userRole || (userRole !== 'shop_owner' && userRole !== 'platform_admin')) {
    myShops.value = []
    return
  }
  
  shopsPending.value = true
  shopsError.value = null
  
  try {
    const shops = await $fetch('http://localhost:8000/platform/shops/me', {
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      // Не выводить ошибки в консоль для 404 - это нормально, если у пользователя нет магазинов
      onResponseError({ response }) {
        if (response.status === 404) {
          // 404 означает, что у пользователя нет магазинов - это нормально
          return
        }
      }
    })
    myShops.value = shops || []
  } catch (e) {
    // Ignore 404 and 401 errors silently - user might not have shops or not authenticated yet
    if (e?.statusCode === 404 || e?.statusCode === 401) {
      myShops.value = []
      shopsPending.value = false
      return
    }
    // Log other errors
    if (e?.statusCode !== 404 && e?.statusCode !== 401) {
      shopsError.value = e
      console.error('[Profile] Ошибка загрузки магазинов:', e)
    }
    myShops.value = []
  } finally {
    shopsPending.value = false
  }
}


// Обновляем список магазинов при загрузке страницы и при изменении токена/роли
watch([token, user], async ([newToken, newUser]) => {
  // Не делаем запрос, если нет токена или пользователя
  if (!newToken || !newUser || !newUser.role) {
    myShops.value = []
    return
  }
  
  // Проверяем роль перед запросом
  const userRole = newUser.role
  if (userRole === 'shop_owner' || userRole === 'platform_admin') {
    await refreshShops()
  } else {
    myShops.value = []
  }
}, { immediate: false })

// Обновляем при монтировании компонента
onMounted(async () => {
  // Если пользователь еще не загружен, загружаем его
  if (token.value && !user.value) {
    const { fetchUser } = useAuth()
    try {
      await fetchUser()
    } catch (e) {
      console.error('[Profile] Ошибка загрузки пользователя:', e)
      return
    }
  }
  
  // Небольшая задержка, чтобы убедиться, что все загружено
  await nextTick()
  
  // Делаем запрос только если пользователь загружен и имеет нужную роль
  if (token.value && user.value?.role) {
    const userRole = user.value.role
    if (userRole === 'shop_owner' || userRole === 'platform_admin') {
      // Добавляем небольшую задержку, чтобы избежать гонки условий
      setTimeout(() => {
        if (token.value && user.value?.role) {
          refreshShops()
        }
      }, 100)
    }
  }
})

const fullName = computed(() => {
  if (!user.value) return ''
  return `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim()
})

const getInitials = computed(() => {
  if (!user.value) return '?'
  const first = user.value.first_name?.[0] || user.value.phone?.[0] || '?'
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase()
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
    'active': 'Активен',
    'expired': 'Истек',
    'cancelled': 'Отменен'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = date - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return 'Истекла'
  } else if (diffDays === 0) {
    return 'Истекает сегодня'
  } else if (diffDays === 1) {
    return 'Истекает завтра'
  } else if (diffDays <= 7) {
    return `Истекает через ${diffDays} дн.`
  } else {
    return `Истекает ${date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })}`
  }
}

const handleLogout = () => {
  logout()
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.profile-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Profile Left Column */
.profile-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  margin: -20px -20px 0;
  padding: 40px 20px 60px;
  border-radius: 0 0 32px 32px;
}

.profile-card {
  background: white;
  border-radius: 24px;
  padding: 40px 24px 32px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  position: relative;
  margin-top: 30px;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #111;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -70px auto 20px;
  border: 4px solid white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.avatar-text {
  font-size: 2rem;
  font-weight: 800;
  color: white;
}

.profile-name {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
}

.profile-role {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 16px;
}

.profile-role-links {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  width: 100%;
  justify-content: center;
}

.role-link.platform-link {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.role-link.platform-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.role-link.shop-link {
  background: #111;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.role-link.shop-link:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.role-link.shop-admin-link {
  background: linear-gradient(135deg, #000000 0%, #000000 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.role-link.shop-admin-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.role-link svg {
  flex-shrink: 0;
}

.profile-stats {
  display: none;
}

/* Quick Actions */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 20px 12px;
  text-align: center;
  text-decoration: none;
  color: #111;
  transition: all 0.2s;
  border: 1px solid #E5E7EB;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  border-color: #111;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  color: #111;
  transition: all 0.2s;
}

.action-card:hover .action-icon {
  background: #111;
  color: white;
}

.action-card span {
  font-size: 0.8rem;
  font-weight: 600;
}

/* Profile Right Column */
.profile-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Info Section */
.info-section {
  flex: 1;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  text-transform: none;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
  margin-bottom: 12px;
  padding-left: 4px;
}

.info-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #F3F4F6;
  transition: background 0.2s;
}

.info-item:hover {
  background: #FAFAFA;
}

.info-item:last-child {
  border-bottom: none;
}

.info-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  margin-right: 16px;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.info-value {
  font-size: 1rem;
  font-weight: 600;
  color: #111;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  width: fit-content;
}

.role-badge.admin {
  background: #111;
  color: white;
}

.role-badge.user {
  background: #F3F4F6;
  color: #6B7280;
}

.role-indicator {
  font-weight: 700;
}

.role-indicator.admin {
  color: #111;
}

/* Shops Section */
.shops-section {
  margin-top: 32px;
}

.shops-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.shop-item {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column; /* Mobile first: stack vertically */
  gap: 20px;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.shop-item:hover {
  border-color: #D1D5DB;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.shop-info {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  flex: 1;
}

.shop-logo-small {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-weight: 700;
  font-size: 1.5rem;
  color: #111;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.shop-logo-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.shop-details {
  flex: 1;
}

.shop-name-small {
  font-size: 1.125rem;
  font-weight: 800;
  margin: 0 0 6px 0;
  color: #111;
  letter-spacing: -0.01em;
}

.shop-url {
  font-size: 0.8125rem;
  color: #6B7280;
  margin: 0 0 12px 0;
  font-weight: 500;
}

.shop-status-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.shop-status-badge.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.shop-status-badge.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.shop-status-badge.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.shop-status-badge.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.shop-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%; /* Mobile first: full width buttons */
}

.shop-action-btn {
  padding: 12px 18px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  white-space: nowrap;
}

.shop-action-btn.view {
  background: #F9FAFB;
  color: #111;
  border: 2px solid #E5E7EB;
}

.shop-action-btn.view:hover {
  background: #F3F4F6;
  border-color: #D1D5DB;
  transform: translateY(-1px);
}

.shop-action-btn.admin {
  background: linear-gradient(135deg, #000000 0%, #000000 100%);
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.shop-action-btn.admin:hover {
  background: linear-gradient(135deg, #000000 0%, #000000 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  transform: translateY(-1px);
}

.shop-action-btn.subscription {
  background: linear-gradient(135deg, #FCD34D 0%, #FBBF24 100%);
  color: #92400E;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
  font-weight: 700;
}

.shop-action-btn.subscription:hover {
  background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
  transform: translateY(-2px);
}

.shop-action-btn svg {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
}

.subscription-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.subscription-expires {
  font-size: 0.8125rem;
  color: #6B7280;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.subscription-expires::before {
  content: '⏰';
  font-size: 0.875rem;
}

.create-shop-section {
  margin-top: 24px;
}

.create-shop-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px;
  background: linear-gradient(135deg, #111 0%, #374151 100%);
  border: none;
  border-radius: 16px;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.create-shop-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.no-shops-section {
  margin-top: 24px;
}

.no-shops-section .info-box {
  background: #F9FAFB;
  border-radius: 16px;
  padding: 32px;
  border: 2px solid #E5E7EB;
  text-align: center;
}

.no-shops-section .info-box h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #111;
}

.no-shops-section .info-box p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 24px;
}

.redirect-note {
  margin-top: 16px;
  font-size: 0.875rem;
  color: #666;
}

.redirect-link {
  color: #111;
  font-weight: 600;
  text-decoration: none;
}

.redirect-link:hover {
  text-decoration: underline;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Admin Button */
.admin-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px;
  background: #111;
  border: none;
  border-radius: 16px;
  color: white;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.admin-btn:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* Logout Button */
.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px;
  background: white;
  border: 2px solid #FEE2E2;
  border-radius: 16px;
  color: #DC2626;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #FEF2F2;
  border-color: #FECACA;
  transform: translateY(-2px);
}

.logout-btn:active {
  transform: translateY(0);
}

.app-version {
  text-align: center;
  font-size: 0.75rem;
  color: #9CA3AF;
}

/* Mobile Styles */
@media (max-width: 767px) {
  .profile-content {
    padding: 16px;
  }
  
  .profile-header {
    margin: -16px -16px 0;
    padding: 32px 16px 50px;
  }
  
  .profile-card {
    padding: 32px 20px 24px;
  }
  
  .profile-avatar {
    width: 80px;
    height: 80px;
    margin-top: -56px;
  }
  
  .avatar-text {
    font-size: 1.5rem;
  }
  
  .profile-name {
    font-size: 1.5rem;
  }
  
  .quick-actions {
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
  }
  
  .action-card {
    padding: 16px 8px;
  }
  
  .action-icon {
    width: 40px;
    height: 40px;
  }
  
  .action-card span {
    font-size: 0.65rem;
  }

  .shop-item {
    padding: 16px;
    gap: 16px;
  }

  .shop-info {
    gap: 12px;
  }

  .shop-logo-small {
    width: 60px;
    height: 60px;
  }

  .shop-details {
    overflow: hidden;
  }

  .shop-url {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .shop-actions {
    gap: 8px;
  }

  .shop-action-btn {
    padding: 10px 14px;
    font-size: 0.8125rem;
  }
}

/* Desktop Styles */
@media (min-width: 768px) {
  .profile-page {
    padding-bottom: 40px;
  }
  
  .profile-content {
    padding: 40px;
  }
  
  .profile-layout {
    flex-direction: row;
    align-items: flex-start;
    gap: 40px;
  }
  
  .profile-left {
    width: 380px;
    flex-shrink: 0;
    position: sticky;
    top: 100px;
  }
  
  .profile-header {
    margin: 0;
    padding: 32px 24px 50px;
    border-radius: 24px;
  }
  
  .profile-card {
    margin-top: 20px;
    padding: 50px 32px 32px;
  }
  
  .profile-avatar {
    width: 110px;
    height: 110px;
    margin-top: -75px;
  }
  
  .avatar-text {
    font-size: 2.25rem;
  }
  
  .profile-name {
    font-size: 1.5rem;
  }
  
  .profile-stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #E5E7EB;
  }
  
  .stat-item {
    text-align: center;
  }
  
  .stat-value {
    display: block;
    font-size: 1.25rem;
    font-weight: 800;
    color: #111;
    margin-bottom: 4px;
  }
  
  .stat-label {
    font-size: 0.75rem;
    color: #9CA3AF;
    font-weight: 500;
  }
  
  .stat-divider {
    width: 1px;
    height: 40px;
    background: #E5E7EB;
  }
  
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .action-card {
    padding: 24px 16px;
    border-radius: 20px;
  }
  
  .action-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    margin-bottom: 12px;
  }
  
  .action-card span {
    font-size: 0.9rem;
  }
  
  .profile-right {
    flex: 1;
    min-width: 0;
  }
  
  .info-card {
    border-radius: 24px;
  }
  
  .info-item {
    padding: 20px 24px;
  }
  
  .info-icon {
    width: 50px;
    height: 50px;
  }
  
  .info-value {
    font-size: 1.1rem;
  }
  
  .action-buttons {
    flex-direction: row;
    gap: 16px;
  }
  
  .admin-btn,
  .logout-btn {
    flex: 1;
    border-radius: 20px;
  }
  
  .app-version {
    text-align: left;
    margin-top: 8px;
  }
  
  /* Shop items on desktop */
  .shop-item {
    flex-direction: row; /* Desktop: horizontal layout */
    justify-content: space-between;
    align-items: center;
    padding: 24px;
  }
  
  .shop-info {
    width: auto;
  }
  
  .shop-actions {
    width: auto;
    min-width: 180px;
  }
  
  .shop-action-btn {
    width: auto;
  }
}

/* Large Desktop */
@media (min-width: 1200px) {
  .profile-left {
    width: 420px;
  }
  
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
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

/* Platform Admin Section */
.platform-admin-section {
  margin-top: 32px;
}

.admin-info-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 20px;
  padding: 24px;
  color: white;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.admin-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.admin-details h3 {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 8px;
  color: white;
}

.admin-details p {
  font-size: 0.875rem;
  color: rgba(255,255,255,0.8);
  line-height: 1.5;
  margin: 0;
}

.admin-panel-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: #10B981;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.admin-panel-btn:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16,185,129,0.3);
}
</style>
