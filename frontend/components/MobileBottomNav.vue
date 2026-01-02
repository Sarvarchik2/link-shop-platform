<template>
  <!-- Mobile Bottom Navigation -->
  <nav class="mobile-nav">
    <NuxtLink :to="localePath(homeLink)" class="mobile-nav-item" :class="{ 'is-active': isHomeActive }">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span>{{ $t('nav.home') }}</span>
    </NuxtLink>

    <NuxtLink :to="localePath(productsLink)" class="mobile-nav-item" :class="{ 'is-active': isProductsActive }">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
        <line x1="1" y1="10" x2="23" y2="10"></line>
      </svg>
      <span>{{ $t('nav.products') }}</span>
    </NuxtLink>

    <NuxtLink :to="localePath('/cart')" class="mobile-nav-item cart-nav-item" :class="{ 'is-active': isCartActive }">
      <div class="cart-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <span v-if="totalItems > 0" class="cart-badge-mobile">{{ totalItems }}</span>
      </div>
      <span>{{ $t('nav.cart') }}</span>
    </NuxtLink>

    <NuxtLink :to="localePath('/orders')" class="mobile-nav-item" :class="{ 'is-active': isOrdersActive }">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
      </svg>
      <span>{{ $t('nav.orders') }}</span>
    </NuxtLink>

    <NuxtLink :to="localePath('/favorites')" class="mobile-nav-item" :class="{ 'is-active': isFavoritesActive }">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path
          d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
        </path>
      </svg>
      <span>{{ $t('nav.favorites') }}</span>
    </NuxtLink>
  </nav>
</template>

<script setup>
const localePath = useLocalePath()
const { totalItems } = useCart()
const route = useRoute()
const { getCurrentShopSlug } = useShopContext()

// Get shop slug from route or saved context
const shopSlug = computed(() => getCurrentShopSlug(route))

// Determine home link - if on shop page or have saved shop context, link to shop home, otherwise to platform home
const homeLink = computed(() => {
  if (shopSlug.value) {
    return `/${shopSlug.value}`
  }
  // Otherwise link to platform home
  return '/'
})

// Determine products link - if on shop page or have saved shop context, link to shop products, otherwise to platform products
const productsLink = computed(() => {
  if (shopSlug.value) {
    return `/${shopSlug.value}/products`
  }
  // Otherwise link to platform products (all shops)
  return '/products'
})

// Active state detection
const isHomeActive = computed(() => {
  const path = route.path
  const currentShopSlug = route.params.shop || route.params.slug

  if (currentShopSlug) {
    // On shop pages, active if we're on shop home
    return path === `/${currentShopSlug}` || path === `/${currentShopSlug}/`
  }
  // On platform, active if we're on root (and no shop context saved)
  if (!shopSlug.value) {
    return path === '/' || path === ''
  }
  return false
})

const isProductsActive = computed(() => {
  const path = route.path
  const currentShopSlug = route.params.shop || route.params.slug

  if (currentShopSlug) {
    // On shop pages, active if we're on shop products
    return path.startsWith(`/${currentShopSlug}/products`)
  }
  // On platform, active if we're on /products (and no shop context saved)
  if (!shopSlug.value) {
    return path === '/products' || path.startsWith('/products/')
  }
  return false
})

const isCartActive = computed(() => {
  return route.path === '/cart' || route.path.startsWith('/cart')
})

const isOrdersActive = computed(() => {
  return route.path === '/orders' || route.path.startsWith('/orders')
})

const isFavoritesActive = computed(() => {
  return route.path === '/favorites' || route.path.startsWith('/favorites')
})
</script>

<style scoped>
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
  transition: all 0.2s;
  text-decoration: none;
}

.mobile-nav-item.router-link-active,
.mobile-nav-item.router-link-exact-active,
.mobile-nav-item.is-active {
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
  padding: 0 4px;
}

/* Desktop Breakpoint */
@media (min-width: 768px) {
  .mobile-nav {
    display: none;
  }
}
</style>
