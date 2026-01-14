<template>
  <!-- Sidebar Overlay -->
  <div v-if="isOpen" class="sidebar-overlay" @click="closeSidebar"></div>

  <aside class="admin-sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <div class="shop-branding">
        <div class="sidebar-logo">
          <img v-if="shop?.logo_url && !imageError" :src="shop.logo_url" :alt="shop.name" class="shop-logo-img"
            @error="imageError = true" />
          <div v-else class="logo-placeholder">
            {{ shop?.name?.charAt(0) || 'S' }}
          </div>
        </div>
        <div class="shop-info-text">
          <span class="shop-name-label">{{ shop?.name || $t('common.loading') }}</span>
          <span class="admin-panel-label">{{ $t('admin.panel') }}</span>
        </div>
      </div>
      <button class="close-btn" @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="nav-section-title">{{ $t('admin.analytics') }}</div>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin`)" class="nav-item"
          :class="{ active: currentRoute === 'dashboard' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>{{ $t('admin.overview') }}</span>
        </NuxtLink>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/orders`)" class="nav-item"
          :class="{ active: currentRoute === 'orders' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>{{ $t('admin.orders') }}</span>
        </NuxtLink>
      </div>

      <div class="nav-section">
        <div class="nav-section-title">{{ $t('admin.shop') }}</div>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/products`)" class="nav-item"
          :class="{ active: currentRoute === 'products' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <path d="M7 7h10"></path>
            <path d="M7 12h10"></path>
            <path d="M7 17h10"></path>
          </svg>
          <span>{{ $t('admin.products') }}</span>
        </NuxtLink>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/categories`)" class="nav-item"
          :class="{ active: currentRoute === 'categories' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
          </svg>
          <span>{{ $t('admin.categories') }}</span>
        </NuxtLink>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/brands`)" class="nav-item"
          :class="{ active: currentRoute === 'brands' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <circle cx="7" cy="7" r=".5"></circle>
          </svg>
          <span>{{ $t('admin.brand') }}</span>
        </NuxtLink>
      </div>

      <div class="nav-section">
        <div class="nav-section-title">{{ $t('admin.settings') }}</div>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/banner`)" class="nav-item"
          :class="{ active: currentRoute === 'banner' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span>{{ $t('admin.banner') }}</span>
        </NuxtLink>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/info`)" class="nav-item"
          :class="{ active: currentRoute === 'info' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
          <span>{{ $t('admin.aboutShop') }}</span>
        </NuxtLink>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/settings/delivery`)" class="nav-item"
          :class="{ active: currentRoute === 'delivery' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="1" y="3" width="15" height="13"></rect>
            <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
            <circle cx="5.5" cy="18.5" r="2.5"></circle>
            <circle cx="18.5" cy="18.5" r="2.5"></circle>
          </svg>
          <span>{{ $t('admin.delivery.title') }}</span>
        </NuxtLink>
        <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/settings/subscription`)" class="nav-item"
          :class="{ active: currentRoute === 'subscription' }" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M16 8l-8 8"></path>
            <path d="M12 7V17"></path>
          </svg>
          <span>{{ $t('admin.subscription') }}</span>
        </NuxtLink>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="language-section">
        <LanguageSwitcher />
      </div>
      <NuxtLink :to="localePath(`/${shopSlug}`)" class="footer-link-btn view-shop" @click="closeSidebar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
        <span>{{ $t('admin.viewShop') }}</span>
      </NuxtLink>
      <button @click="handleLogout" class="footer-link-btn logout">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span>{{ $t('admin.logout') }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
const config = useRuntimeConfig()
const localePath = useLocalePath()
const props = defineProps({
  shopSlug: {
    type: String,
    required: true
  },
  currentRoute: {
    type: String,
    default: 'dashboard'
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const closeSidebar = () => {
  isOpen.value = false
}

// Fetch shop data with a unique key per shop but shared across page instances
const { data: shop } = useFetch(() => `${config.public.apiBase}/platform/shops/${props.shopSlug}`, {
  key: `shop-data-${props.shopSlug}`,
  server: false,
  watch: [() => props.shopSlug]
})

const imageError = ref(false)
watch(() => shop.value?.logo_url, () => {
  imageError.value = false
})

const { logout } = useAuth()

const handleLogout = () => {
  logout()
  useToast().success(t('alerts.shop.loggedOut'))
}

// Close sidebar on route change
const route = useRoute()
watch(() => route.path, () => {
  closeSidebar()
})
</script>

<style scoped>
.admin-sidebar {
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #f1f1f1;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 1000;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-header {
  padding: 32px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.shop-branding {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-logo {
  width: 40px;
  height: 40px;
  background: #fdfdfd;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #eee;
  overflow: hidden;
  flex-shrink: 0;
}

.shop-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo-placeholder {
  font-weight: 800;
  font-size: 1.1rem;
  color: #111;
}

.shop-info-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  /* Allow shrinking for name */
}

.shop-name-label {
  font-weight: 700;
  font-size: 0.9rem;
  color: #111;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

.admin-panel-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-top: 1px;
}

.sidebar-nav {
  flex: 1;
  padding: 8px 16px;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 24px;
}

.nav-section-title {
  padding: 0 12px 12px;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #9CA3AF;
  letter-spacing: 0.1em;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: #4B5563;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  margin-bottom: 2px;
}

.nav-item:hover {
  background: #f9fafb;
  color: #111;
}

.nav-item.active {
  background: #111;
  color: #fff;
}

.nav-item svg {
  flex-shrink: 0;
  opacity: 0.7;
}

.nav-item.active svg {
  opacity: 1;
}

.sidebar-footer {
  padding: 24px 16px;
  border-top: 1px solid #f1f1f1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.language-section {
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid #f1f1f1;
}

.footer-link-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.2s;
  border: none;
  background: none;
  cursor: pointer;
  width: 100%;
}

.view-shop {
  background: #f9fafb;
  color: #111;
}

.view-shop:hover {
  background: #f3f4f6;
}

.logout {
  color: #EF4444;
}

.logout:hover {
  background: #FEF2F2;
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 999;
}

.close-btn {
  display: none;
  padding: 8px;
  background: #f3f4f6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

@media (max-width: 1024px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar.open {
    transform: translateX(0);
  }

  .close-btn {
    display: flex;
  }
}
</style>
