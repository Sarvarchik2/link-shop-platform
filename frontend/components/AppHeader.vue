<template>
  <div>
  <!-- Desktop Header -->
  <header class="header desktop-header">
    <div class="container">
      <div class="header-content">
        <!-- Logo -->
        <NuxtLink to="/" class="logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>EYEWEAR</span>
        </NuxtLink>

        <!-- Navigation (Desktop only) -->
        <nav class="nav-links">
          <ClientOnly>
            <NuxtLink :to="homeLink" class="nav-link">Главная</NuxtLink>
            <NuxtLink :to="shopProductsLink" class="nav-link">Магазин</NuxtLink>
            <template #fallback>
              <NuxtLink to="/" class="nav-link">Главная</NuxtLink>
              <NuxtLink to="/products" class="nav-link">Магазин</NuxtLink>
            </template>
          </ClientOnly>
          <NuxtLink v-if="user" to="/orders" class="nav-link">Заказы</NuxtLink>
        </nav>

        <!-- Actions -->
        <div class="header-actions">
          <template v-if="user">
          <!-- Desktop only icons -->
          <NuxtLink to="/favorites" class="icon-btn desktop-only">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
          </NuxtLink>
          
          <NuxtLink to="/cart" class="icon-btn desktop-only cart-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            <span v-if="totalItems > 0" class="cart-badge">{{ totalItems }}</span>
          </NuxtLink>
          
          <!-- Profile - visible on all screens -->
            <NuxtLink :to="getProfileLink" class="icon-btn profile-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </NuxtLink>
          </template>
          
          <template v-else>
            <!-- Login and Register buttons -->
            <NuxtLink to="/login" class="btn-login">Войти</NuxtLink>
            <NuxtLink to="/register" class="btn-register">Зарегистрироваться</NuxtLink>
          </template>
        </div>
      </div>
    </div>
  </header>

  <!-- Mobile Bottom Navigation -->
  <nav class="mobile-nav">
    <ClientOnly>
      <NuxtLink :to="homeLink" class="mobile-nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        <span>Bosh sahifa</span>
      </NuxtLink>
      
      <NuxtLink :to="shopProductsLink" class="mobile-nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
        <span>Mahsulotlar</span>
      </NuxtLink>
      <template #fallback>
        <NuxtLink to="/" class="mobile-nav-item">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Bosh sahifa</span>
        </NuxtLink>
        
        <NuxtLink to="/products" class="mobile-nav-item">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>Mahsulotlar</span>
        </NuxtLink>
      </template>
    </ClientOnly>
    
    <NuxtLink to="/cart" class="mobile-nav-item cart-nav-item">
      <div class="cart-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <span v-if="totalItems > 0" class="cart-badge-mobile">{{ totalItems }}</span>
      </div>
      <span>Savatcha</span>
    </NuxtLink>
    
    <NuxtLink to="/orders" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
      </svg>
      <span>Buyurtmalar</span>
    </NuxtLink>
    
    <NuxtLink to="/favorites" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
      <span>Sevimlilar</span>
    </NuxtLink>
  </nav>
  </div>
</template>

<script setup>
const { totalItems } = useCart()
const { user, token } = useAuth()

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
  height: 80px;
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

.nav-links {
  display: none;
  gap: 40px;
}

.nav-link {
  font-weight: 600;
  font-size: 0.95rem;
  color: #666;
  transition: color 0.2s;
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
  transition: all 0.2s;
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
  box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
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
  transition: all 0.2s;
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
  transition: all 0.2s;
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
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

@media (max-width: 767px) {
  .btn-login,
  .btn-register {
    padding: 8px 16px;
    font-size: 0.75rem;
  }
}
</style>
