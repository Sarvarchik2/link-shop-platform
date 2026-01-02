<template>
  <div class="profile-page">
    <AppHeader />

    <div class="container">
      <h1 class="page-title">{{ $t('profile.title') }}</h1>

      <div class="content-grid">
        <!-- Sidebar -->
        <aside class="sidebar">
          <div class="user-card">
            <div class="avatar-circles">
              <div class="circle circle-1"></div>
              <div class="circle circle-2"></div>
              <div class="user-avatar">
                <span>{{ userInitials }}</span>
              </div>
            </div>
            <div class="user-info">
              <h3 class="user-name">{{ fullName }}</h3>
              <p class="user-id">ID: {{ user?.id }}</p>
              <div class="user-roles">
                <span v-for="role in user?.roles" :key="role" class="role-badge" :class="role">
                  {{ getRoleName(role) }}
                </span>
              </div>
            </div>
          </div>

          <nav class="profile-nav">
            <NuxtLink v-if="token" to="/orders" class="nav-item">
              <div class="nav-icon">📦</div>
              <span>{{ $t('profile.actions.orders') }}</span>
              <div class="arrow-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14m-7-7 7 7-7 7" />
                </svg>
              </div>
            </NuxtLink>

            <button class="nav-item" disabled>
              <div class="nav-icon">❤️</div>
              <span>{{ $t('profile.actions.favorites') }}</span>
              <div class="arrow-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14m-7-7 7 7-7 7" />
                </svg>
              </div>
            </button>

            <!-- Admin Links -->
            <template v-if="isAdmin">
              <div class="nav-divider"></div>
              <NuxtLink to="/platform/admin" class="nav-item admin">
                <div class="nav-icon">🛡️</div>
                <span>{{ $t('profile.links.platformAdmin') }}</span>
              </NuxtLink>
            </template>

            <!-- Shop Owner Links -->
            <template v-if="isShopOwner">
              <div class="nav-divider"></div>
              <div v-for="shop in shops" :key="shop.id" class="shop-nav-group">
                <div class="nav-item shop-header">
                  <div class="nav-icon">🏪</div>
                  <span>{{ shop.name }}</span>
                  <span class="shop-status-badge" :class="shop.subscription_status">
                    {{ getShopStatusText(shop.subscription_status) }}
                  </span>
                </div>
                <div class="shop-actions">
                  <NuxtLink :to="`/shop/${shop.slug}/admin`" class="sub-nav-item">
                    {{ $t('profile.shops.actions.admin') }}
                  </NuxtLink>
                  <a :href="`http://${shop.slug}.localhost:3000`" target="_blank" class="sub-nav-item">
                    {{ $t('profile.shops.actions.open') }}
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                  </a>
                  <NuxtLink :to="`/shop/${shop.slug}/admin/settings/subscription`" class="sub-nav-item highlight">
                    {{ $t('profile.shops.actions.subscription') }}
                  </NuxtLink>
                </div>
              </div>

              <!-- Create Another Shop Button (if allowed) -->
              <NuxtLink v-if="true" to="/register-shop" class="nav-item create-shop">
                <div class="nav-icon">✨</div>
                <span>{{ $t('profile.links.createShop') }}</span>
              </NuxtLink>
            </template>

            <div class="nav-footer">
              <button @click="logout" class="logout-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                {{ $t('profile.actions.logout') }}
              </button>
            </div>
          </nav>
        </aside>

        <!-- Main Content Area -->
        <main class="main-content">
          <!-- Active Shops Status Cards -->
          <section v-if="isShopOwner && shops.length > 0" class="status-cards">
            <div v-for="shop in shops" :key="shop.id" class="status-card" :class="shop.subscription_status">
              <div class="card-header">
                <div>
                  <h3>{{ shop.name }}</h3>
                  <a :href="`http://${shop.slug}.localhost:3000`" target="_blank" class="shop-link">
                    {{ shop.slug }}.link-shop.uz
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                  </a>
                </div>
                <div class="status-pill" :class="shop.subscription_status">
                  {{ getShopStatusText(shop.subscription_status) }}
                </div>
              </div>

              <div class="card-body">
                <div class="expiry-info">
                  <span class="label">{{ $t('profile.shops.expires.date', {
                    date:
                      formatDate(shop.subscription_expires_at)
                  })
                    }}</span>
                  <span class="value">{{ getDaysLeftText(shop.subscription_expires_at) }}</span>
                </div>
                <div class="progress-bar">
                  <div class="progress" :style="{ width: getProgressWidth(shop) + '%' }"></div>
                </div>
              </div>

              <div class="card-footer">
                <NuxtLink :to="`/shop/${shop.slug}/admin`" class="btn-dashboard">
                  {{ $t('profile.shops.actions.admin') }}
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </NuxtLink>
              </div>
            </div>
          </section>

          <!-- Shop Owner Teaser (for non-owners) - HIDDEN as per request -->
          <section v-if="false" class="promo-card">
            <div class="promo-content">
              <h2>{{ $t('profile.shopPromo.title') }}</h2>
              <p>{{ $t('profile.shopPromo.desc') }}</p>
              <NuxtLink to="/register-shop" class="btn-create-shop">
                {{ $t('profile.links.createShop') }}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </NuxtLink>
            </div>
            <div class="promo-image">
              <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"
                class="shop-icon">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </div>
          </section>

          <!-- Personal Info Edit Form -->
          <section class="info-section">
            <h2 class="section-title">{{ $t('profile.info.title') }}</h2>
            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-grid">
                <div class="form-group">
                  <label>{{ $t('profile.info.firstName') }}</label>
                  <input v-model="form.first_name" type="text" :placeholder="$t('profile.info.firstName')" />
                </div>
                <div class="form-group">
                  <label>{{ $t('profile.info.lastName') }}</label>
                  <input v-model="form.last_name" type="text" :placeholder="$t('profile.info.lastName')" />
                </div>
                <div class="form-group">
                  <label>{{ $t('profile.info.phone') }}</label>
                  <input v-model="form.phone" type="tel" readonly disabled />
                  <span class="field-hint">{{ $t('profile.info.phoneChangeHint') }}</span>
                </div>
              </div>

              <div class="form-actions">
                <button type="submit" class="btn-save" :disabled="loading">
                  {{ loading ? $t('common.saving') : $t('common.save') }}
                </button>
              </div>
            </form>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { user, token, logout, fetchUser } = useAuth()
const { t } = useI18n()
const config = useRuntimeConfig()

// Initialize form with safe defaults
const form = reactive({
  first_name: user.value?.first_name || '',
  last_name: user.value?.last_name || '',
  phone: user.value?.phone || ''
})

// Watch user changes to update form if it loads later
watch(() => user.value, (newUser) => {
  if (newUser) {
    form.first_name = newUser.first_name || ''
    form.last_name = newUser.last_name || ''
    form.phone = newUser.phone || ''
  }
}, { immediate: true })

const fullName = computed(() => {
  if (!user.value) return 'User'
  const name = `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim()
  return name || 'User'
})

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.first_name?.[0] || ''
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase() || 'U'
})

const isAdmin = computed(() => user.value?.role === 'platform_admin' || user.value?.roles?.includes('admin'))
const isShopOwner = computed(() =>
  shops.value.length > 0 ||
  user.value?.role === 'shop_owner' ||
  user.value?.roles?.includes('shop_owner') ||
  user.value?.roles?.includes('admin')
)

// Fetch user shops
const shops = ref([])
const fetchShops = async () => {
  if (!user.value || !token.value) return

  try {
    const data = await $fetch(`${config.public.apiBase}/platform/shops/me`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    shops.value = data || []
  } catch (e) {
    console.error('Error fetching shops:', e)
  }
}

onMounted(async () => {
  if (token.value && !user.value) {
    await fetchUser()
  }
  fetchShops()
})

const loading = ref(false)
const toast = useToast()

const updateProfile = async () => {
  loading.value = true
  try {
    await $fetch(`${config.public.apiBase}/users/profile`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        first_name: form.first_name,
        last_name: form.last_name
      }
    })

    // Update local user state
    if (user.value) {
      user.value.first_name = form.first_name
      user.value.last_name = form.last_name
    }

    toast.success(t('common.saved'))
  } catch (e) {
    console.error(e)
    toast.error(t('platformAdmin.dashboard.error'))
  } finally {
    loading.value = false
  }
}

// Helper functions for UI
const getRoleName = (role) => {
  const roles = {
    'platform_admin': t('profile.roles.admin'),
    'admin': t('profile.roles.admin'),
    'shop_owner': t('profile.roles.shopOwner'),
    'user': t('profile.roles.user')
  }
  return roles[role] || role
}

const getShopStatusText = (status) => {
  const statuses = {
    'trial': t('profile.shops.status.trial'),
    'active': t('profile.shops.status.active'),
    'expired': t('profile.shops.status.expired'),
    'cancelled': t('profile.shops.status.cancelled')
  }
  return statuses[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const locale = useI18n().locale.value
  return new Date(dateString).toLocaleDateString(locale, {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const getDaysLeftText = (dateString) => {
  if (!dateString) return ''
  const end = new Date(dateString)
  const now = new Date()
  const diffTime = end - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return t('profile.shops.expires.expired')
  if (diffDays === 0) return t('profile.shops.expires.today')
  if (diffDays === 1) return t('profile.shops.expires.tomorrow')
  return t('profile.shops.expires.days', { days: diffDays })
}

const getProgressWidth = (shop) => {
  // Logic to calculate progress of subscription period
  if (!shop.subscription_expires_at) return 0

  // Assuming 30 days total for now if no start date
  const totalDays = 30
  const end = new Date(shop.subscription_expires_at)
  const now = new Date()
  const diffTime = end - now
  const diffDays = Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)))

  const progress = ((totalDays - diffDays) / totalDays) * 100
  return Math.min(100, Math.max(0, progress))
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  /* padding: 24px 0; */
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.content-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

/* Sidebar Styles */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.avatar-circles {
  position: relative;
  width: 100px;
  height: 100px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #111;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
  position: relative;
  z-index: 2;
  border: 4px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.circle {
  position: absolute;
  border-radius: 50%;
  z-index: 1;
}

.circle-1 {
  width: 100%;
  height: 100%;
  top: 4px;
  left: 4px;
  border: 2px solid #e5e7eb;
}

.circle-2 {
  width: 100%;
  height: 100%;
  top: -4px;
  left: -4px;
  background: #f3f4f6;
}

.user-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin: 0 0 4px 0;
}

.user-id {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0 0 12px 0;
  font-family: monospace;
}

.user-roles {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.role-badge {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
}

.role-badge.admin {
  background: #fee2e2;
  color: #991b1b;
}

.role-badge.platform_admin {
  background: #fee2e2;
  color: #991b1b;
}

.role-badge.shop_owner {
  background: #dbeafe;
  color: #1e40af;
}

.role-badge.user {
  background: #f3f4f6;
  color: #374151;
}

.profile-nav {
  background: white;
  border-radius: 20px;
  padding: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  color: #374151;
  text-decoration: none;
  transition: all 0.2s;
  font-weight: 500;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.nav-item:hover:not(:disabled) {
  background: #f3f4f6;
  color: #111;
}

.nav-item:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-item.active {
  background: #111;
  color: white;
}

.nav-icon {
  font-size: 1.25rem;
  width: 24px;
  display: flex;
  justify-content: center;
}

.arrow-icon {
  margin-left: auto;
  color: #9ca3af;
}

.nav-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 8px 0;
}

.nav-item.admin {
  color: #7f1d1d;
  background: #fef2f2;
}

.nav-item.admin:hover {
  background: #fee2e2;
}

.shop-nav-group {
  margin: 4px 0;
  padding: 4px;
  background: #f8fafc;
  border-radius: 12px;
}

.shop-header {
  padding: 8px 12px;
  background: none;
}

.shop-status-badge {
  margin-left: auto;
  font-size: 0.625rem;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
}

.shop-status-badge.trial {
  background: #fef3c7;
  color: #92400e;
}

.shop-status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.shop-status-badge.expired {
  background: #fee2e2;
  color: #991b1b;
}

.shop-actions {
  display: flex;
  flex-direction: column;
  border-top: 1px solid #e2e8f0;
  margin-top: 4px;
}

.sub-nav-item {
  display: flex;
  align-items: center;
  padding: 8px 12px 8px 48px;
  font-size: 0.875rem;
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s;
  gap: 6px;
}

.sub-nav-item:hover {
  color: #0f172a;
  background: #f1f5f9;
}

.sub-nav-item.highlight {
  color: #2563eb;
}

.create-shop {
  color: #059669;
  background: #ecfdf5;
}

.create-shop:hover {
  background: #d1fae5;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  margin-top: 8px;
  border: 2px solid #fee2e2;
  background: white;
  color: #ef4444;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #fee2e2;
  color: #991b1b;
}

/* Main Content Styles */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.status-cards {
  display: grid;
  gap: 16px;
}

.status-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

/* .status-card.trial {
  border-left: 4px solid #f59e0b;
}

.status-card.active {
  border-left: 4px solid #10b981;
}

.status-card.expired {
  border-left: 4px solid #ef4444;
} */

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin: 0 0 4px 0;
}

.shop-link {
  font-size: 0.875rem;
  color: #4b5563;
  display: flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
}

.shop-link:hover {
  color: #2563eb;
}

.status-pill {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-pill.trial {
  background: #fef3c7;
  color: #92400e;
}

.status-pill.active {
  background: #d1fae5;
  color: #065f46;
}

.status-pill.expired {
  background: #fee2e2;
  color: #991b1b;
}

.card-body {
  margin-bottom: 24px;
}

.expiry-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 8px;
}

.expiry-info .label {
  font-size: 0.875rem;
  color: #6b7280;
}

.expiry-info .value {
  font-size: 1rem;
  font-weight: 600;
  color: #111;
}

.progress-bar {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #111;
  border-radius: 4px;
}

.trial .progress {
  background: #f59e0b;
}

.active .progress {
  background: #10b981;
}

.expired .progress {
  background: #ef4444;
}

.card-footer {
  display: flex;
  gap: 12px;
}

.btn-dashboard {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #111;
  color: white;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s;
}

.btn-dashboard:hover {
  opacity: 0.9;
}

.promo-card {
  background: linear-gradient(135deg, #111 0%, #333 100%);
  border-radius: 24px;
  padding: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
}

.promo-content {
  flex: 1;
}

.promo-content h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.promo-content p {
  color: #e5e5e5;
  margin-bottom: 24px;
  max-width: 400px;
  line-height: 1.5;
}

.btn-create-shop {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #111;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s;
}

.btn-create-shop:hover {
  transform: translateY(-2px);
}

.shop-icon {
  opacity: 0.2;
}

.info-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f9fafb;
}

.form-group input:focus {
  outline: none;
  border-color: #111;
  background: white;
}

.form-group input:disabled {
  background: #f3f4f6;
  color: #6b7280;
  cursor: not-allowed;
}

.field-hint {
  display: block;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 6px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-save {
  padding: 12px 32px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-save:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-save:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
    /* Hide sidebar on mobile for now, or implement drawer */
  }

  .container {
    padding: 0 16px;
  }
}

/* Mobile-first override for sidebar content if needed */
@media (max-width: 900px) {
  .profile-page {
    padding-bottom: 100px;
  }

  .sidebar {
    display: flex;
  }
}
</style>
