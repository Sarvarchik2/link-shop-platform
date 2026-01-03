<template>
  <div>
    <!-- Desktop Header -->
    <header class="header desktop-header">
      <div class="container">
        <div class="header-content">
          <!-- Logo / Shop Logo or Name -->
          <NuxtLink :to="localePath(homeLink)" class="logo">
            <template v-if="currentShop?.logo_url">
              <img :src="currentShop.logo_url" :alt="currentShop.name || $t('nav.shop')" class="shop-logo" />
            </template>
            <template v-else-if="currentShop?.name">
              <span class="shop-name-text">{{ currentShop.name }}</span>
            </template>
            <template v-else>
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                <line x1="1" y1="10" x2="23" y2="10"></line>
              </svg>
              <span>LinkShop</span>
            </template>
          </NuxtLink>

          <!-- Navigation (Desktop only) -->
          <nav class="nav-links">
            <NuxtLink :to="localePath(homeLink)" class="nav-link">{{ $t('nav.home') }}</NuxtLink>
            <NuxtLink :to="localePath(shopProductsLink)" class="nav-link">{{ $t('nav.shop') }}</NuxtLink>
            <a @click.prevent="navigateToAuth(localePath('/orders'))" :href="localePath('/orders')" class="nav-link">{{
              $t('nav.orders') }}</a>
          </nav>

          <!-- Actions -->
          <div class="header-actions">
            <!-- Language Switcher -->
            <LanguageSwitcher class="desktop-only" />

            <!-- Favorites -->
            <a @click.prevent="navigateToAuth(localePath('/favorites'))" :href="localePath('/favorites')"
              class="icon-btn desktop-only">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                </path>
              </svg>
            </a>

            <!-- Cart -->
            <a @click.prevent="navigateToAuth(localePath('/cart'))" :href="localePath('/cart')"
              class="icon-btn desktop-only cart-btn">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              <span v-if="totalItems > 0" class="cart-badge">{{ totalItems }}</span>
            </a>

            <!-- Profile icon - only visible for authenticated users -->
            <a v-if="user" @click.prevent="navigateToAuth(localePath(getProfileLink))"
              :href="localePath(getProfileLink)" class="icon-btn profile-btn">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </a>

            <!-- Login/Register buttons (only for guests) -->
            <template v-if="!user">
              <NuxtLink :to="localePath('/login')" class="btn-login">{{ $t('nav.login') }}</NuxtLink>
              <NuxtLink :to="localePath('/register')" class="btn-register">{{ $t('nav.register') }}</NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Bottom Navigation -->
    <nav v-if="!hideMobileNav" class="mobile-nav">
      <NuxtLink :to="localePath(homeLink)" class="mobile-nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        <span>{{ $t('nav.home') }}</span>
      </NuxtLink>

      <NuxtLink :to="localePath(shopProductsLink)" class="mobile-nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
        <span>{{ $t('nav.products') }}</span>
      </NuxtLink>

      <a @click.prevent="navigateToAuth(localePath('/cart'))" :href="localePath('/cart')"
        class="mobile-nav-item cart-nav-item">
        <div class="cart-icon-wrapper">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          <span v-if="totalItems > 0" class="cart-badge-mobile">{{ totalItems }}</span>
        </div>
        <span>{{ $t('nav.cart') }}</span>
      </a>

      <a @click.prevent="navigateToAuth(localePath('/orders'))" :href="localePath('/orders')" class="mobile-nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
        </svg>
        <span>{{ $t('nav.orders') }}</span>
      </a>

      <a @click.prevent="navigateToAuth(localePath('/favorites'))" :href="localePath('/favorites')"
        class="mobile-nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path
            d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
          </path>
        </svg>
        <span>{{ $t('nav.favorites') }}</span>
      </a>
    </nav>

    <!-- Auth Prompt Modal -->
    <Transition name="fade">
      <div v-if="showAuthModal" class="modal-overlay" @click="showAuthModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <h3>{{ $t('auth.login_required_modal_title') }}</h3>
          <p>{{ $t('auth.login_required_modal_text') }}</p>
          <div class="modal-buttons">
            <NuxtLink :to="localePath('/login')" class="modal-btn login" @click="showAuthModal = false">{{
              $t('auth.login_title') }}</NuxtLink>
            <NuxtLink :to="localePath('/register')" class="modal-btn register" @click="showAuthModal = false">{{
              $t('auth.register_title') }}
            </NuxtLink>
          </div>
          <button class="modal-close" @click="showAuthModal = false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
// Props
const props = defineProps({
  hideMobileNav: {
    type: Boolean,
    default: false
  }
})

const { totalItems } = useCart()
const { user, token } = useAuth()
const router = useRouter()
const { showAuthModal, openModal, closeModal } = useAuthModal()
const localePath = useLocalePath()

const navigateToAuth = (path) => {
  // Allow unauthenticated users to access cart page
  if (path === '/cart') {
    router.push(path)
    return
  }

  // For other protected routes, require authentication
  if (!user.value) {
    openModal()
    return
  }
  router.push(path)
}

// Only fetch shops if user is shop_owner or platform_admin
const shouldFetchShops = computed(() => {
  return token.value && (user.value?.role === 'shop_owner' || user.value?.role === 'platform_admin')
})

const myShops = ref([])
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
      return
    }
    // Log other errors
    if (e?.statusCode !== 404 && e?.statusCode !== 401) {
      shopsError.value = e
      console.error('[AppHeader] Ошибка загрузки магазинов:', e)
    }
    myShops.value = []
  }
}

// Обновляем список магазинов при изменении токена/роли
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
      console.error('[AppHeader] Ошибка загрузки пользователя:', e)
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

const route = useRoute()
const { getCurrentShopSlug, clearShopContext } = useShopContext()

// Get shop slug from route or saved context
const shopSlug = computed(() => getCurrentShopSlug(route))

// Fetch current shop data if on shop page
const { data: currentShop } = await useFetch(() => {
  if (!shopSlug.value) return null
  return `http://localhost:8000/platform/shops/${shopSlug.value}`
}, {
  server: false,
  watch: [shopSlug]
})

// Clear shop context when explicitly navigating to platform pages (not user pages)
watch(() => route.path, (newPath) => {
  // Don't clear context on user-specific pages (cart, profile, favorites, orders, checkout)
  const userPages = ['/cart', '/profile', '/favorites', '/orders', '/checkout', '/login', '/register']
  if (userPages.some(page => newPath === page || newPath.startsWith(page + '/'))) {
    return
  }

  // Clear context if user navigates to platform pages (not shop pages)
  if (newPath === '/' || newPath === '/products' || newPath.startsWith('/platform')) {
    // Only clear if we're not on a shop page
    const routeSlug = route.params?.shop || route.params?.slug
    if (!routeSlug) {
      clearShopContext()
    }
  }
}, { immediate: false })

// Determine home link - if on shop page or have saved shop context, link to shop home, otherwise to platform home
const homeLink = computed(() => {
  if (shopSlug.value) {
    return `/${shopSlug.value}`
  }
  // Otherwise link to platform home
  return '/'
})

// Determine shop products link - if on shop page or have saved shop context, link to its products, otherwise to platform
const shopProductsLink = computed(() => {
  if (shopSlug.value) {
    return `/${shopSlug.value}/products`
  }
  // Otherwise link to platform products (all shops)
  return '/products'
})

const getProfileLink = computed(() => {
  if (!user.value) return '/login'

  // Platform admin goes to platform admin
  if (user.value.role === 'platform_admin') {
    return '/platform/admin'
  }

  // If user has shops, go to owner profile
  if (myShops.value && myShops.value.length > 0) {
    return '/profile'
  }

  // Otherwise customer profile
  return '/profile'
})
</script>

<style scoped>
/* Desktop Header */
.desktop-header {
  background: white;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 900;
  font-size: 1.25rem;
  color: #111;
  letter-spacing: 1px;
}

.shop-logo {
  height: 40px;
  width: auto;
  max-width: 150px;
  object-fit: contain;
  border-radius: 4px;
}

.shop-name-text {
  font-weight: 900;
  font-size: 1.25rem;
  color: #111;
  letter-spacing: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.nav-links {
  display: none;
  gap: 40px;
}

.nav-link {
  font-weight: 600;
  font-size: 0.95rem;
  color: #666;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #111;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background: #111;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  color: #111;
}

.icon-btn:hover {
  background: #111;
  color: white;
  transform: translateY(-2px);
}

.cart-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #EF4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

/* Hide on mobile */
.desktop-only {
  display: none;
}

/* Mobile Navigation */
.mobile-nav {
  display: flex;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #f0f0f0;
  padding: 8px 0;
  padding-bottom: calc(8px + env(safe-area-inset-bottom));
  z-index: 100;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
}

.mobile-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px;
  color: #999;
  font-size: 0.65rem;
  font-weight: 600;
  font-size: 0.65rem;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-nav-item.router-link-active {
  color: #111;
}

.mobile-nav-item svg {
  stroke-width: 2;
}

.cart-icon-wrapper {
  position: relative;
}

.cart-badge-mobile {
  position: absolute;
  top: -6px;
  right: -8px;
  background: #EF4444;
  color: white;
  font-size: 0.6rem;
  font-weight: 700;
  min-width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

/* Desktop Breakpoint */
@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }

  .mobile-nav {
    display: none;
  }

  .desktop-only {
    display: flex;
  }

  .nav-link::after {
    bottom: -28px;
  }
}

/* Mobile styles */
@media (max-width: 767px) {
  .desktop-header .nav-links {
    display: none;
  }

  .header-content {
    height: 60px;
  }

  .logo span {
    font-size: 1.1rem;
  }

  .shop-name-text {
    font-size: 1.1rem;
  }

  .shop-logo {
    height: 32px;
    max-width: 120px;
  }

  .logo svg {
    width: 28px;
    height: 28px;
  }

  .icon-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
  }

  .header-actions {
    gap: 8px;
  }
}

.btn-login,
.btn-register {
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-login {
  background: transparent;
  color: #111;
  border: 2px solid #E5E7EB;
}

.btn-login:hover {
  border-color: #111;
  background: #F9FAFB;
}

.btn-register {
  background: #111;
  color: white;
}

.btn-register:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@media (max-width: 767px) {

  .btn-login,
  .btn-register {
    padding: 8px 16px;
    font-size: 0.75rem;
  }
}

/* Auth Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  width: 100%;
  height: 100vh;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 400px;
  border-radius: 32px;
  padding: 40px 32px;
  text-align: center;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modalIn {
  from {
    transform: scale(0.9) translateY(20px);
    opacity: 0;
  }

  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.modal-icon {
  width: 80px;
  height: 80px;
  background: #F3F4F6;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: #111;
}

.modal-content h3 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 12px;
}

.modal-content p {
  color: #6B7280;
  line-height: 1.6;
  margin-bottom: 32px;
}

.modal-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-btn {
  padding: 16px;
  border-radius: 16px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.modal-btn.login {
  background: #111;
  color: white;
}

.modal-btn.login:hover {
  background: #000;
  transform: translateY(-2px);
}

.modal-btn.register {
  background: white;
  color: #111;
  border: 2px solid #E5E7EB;
}

.modal-btn.register:hover {
  border-color: #111;
  background: #F9FAFB;
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  cursor: pointer;
  color: #6B7280;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #E5E7EB;
  color: #111;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
