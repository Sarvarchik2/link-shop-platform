<template>
  <!-- Sidebar Overlay -->
  <div v-if="isOpen" class="sidebar-overlay" @click="closeSidebar"></div>

  <aside class="admin-sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <div class="sidebar-logo">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
          <path d="M2 17l10 5 10-5"></path>
          <path d="M2 12l10 5 10-5"></path>
        </svg>
      </div>
      <h2 class="sidebar-title">{{ $t('platformAdmin.dashboard.title') }}</h2>
      <button class="close-btn" @click="closeSidebar">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <nav class="sidebar-nav">
      <NuxtLink :to="localePath('/platform/admin')" class="nav-item" :class="{ active: currentRoute === 'dashboard' }"
        @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"></rect>
          <rect x="14" y="3" width="7" height="7"></rect>
          <rect x="14" y="14" width="7" height="7"></rect>
          <rect x="3" y="14" width="7" height="7"></rect>
        </svg>
        <span>{{ $t('platformAdmin.nav.dashboard') }}</span>
      </NuxtLink>

      <NuxtLink :to="localePath('/platform/admin/shops')" class="nav-item" :class="{ active: currentRoute === 'shops' }"
        @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path
            d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z">
          </path>
        </svg>
        <span>{{ $t('platformAdmin.nav.shops') }}</span>
      </NuxtLink>

      <NuxtLink :to="localePath('/platform/admin/users')" class="nav-item" :class="{ active: currentRoute === 'users' }"
        @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        <span>{{ $t('platformAdmin.nav.users') }}</span>
      </NuxtLink>

      <!-- <NuxtLink :to="localePath('/platform/admin/orders')" class="nav-item" :class="{ active: currentRoute === 'orders' }"
        @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
        </svg>
        <span>{{ $t('platformAdmin.nav.orders') }}</span>
      </NuxtLink> -->

      <NuxtLink :to="localePath('/platform/admin/subscription-plans')" class="nav-item"
        :class="{ active: currentRoute === 'subscription-plans' }" @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
          <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"></path>
        </svg>
        <span>{{ $t('platformAdmin.nav.plans') }}</span>
      </NuxtLink>

      <NuxtLink :to="localePath('/platform/admin/subscription-requests')" class="nav-item"
        :class="{ active: currentRoute === 'subscription-requests' }" @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path
            d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z">
          </path>
          <polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline>
          <polyline points="7.5 19.79 7.5 14.6 3 12"></polyline>
          <polyline points="21 12 16.5 14.6 16.5 19.79"></polyline>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
          <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>
        <span>{{ $t('platformAdmin.nav.requests') }}</span>
      </NuxtLink>

      <NuxtLink :to="localePath('/platform/admin/offers')" class="nav-item"
        :class="{ active: currentRoute === 'offers' }" @click="closeSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
          <path d="M2 17l10 5 10-5"></path>
          <path d="M2 12l10 5 10-5"></path>
        </svg>
        <span>{{ $t('platformAdmin.nav.offers') }}</span>
      </NuxtLink>
    </nav>

    <div class="sidebar-footer">
      <div class="language-section">
        <LanguageSwitcher direction="up" />
      </div>
      <NuxtLink :to="localePath('/')" class="back-link" @click="closeSidebar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        <span>{{ $t('nav.home') }}</span>
      </NuxtLink>
      <button @click="$emit('logout')" class="logout-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span>{{ $t('common.logout') }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
const { t } = useI18n()
const localePath = useLocalePath()
const props = defineProps({
  currentRoute: {
    type: String,
    default: 'dashboard'
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['logout', 'update:modelValue'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const closeSidebar = () => {
  isOpen.value = false
}

// Close sidebar on route change
const route = useRoute()
watch(() => route.path, () => {
  closeSidebar()
})

// Lock body scroll when sidebar is open on mobile
onMounted(() => {
  watch(isOpen, (newValue) => {
    if (window.innerWidth <= 1024) {
      if (newValue) {
        document.body.style.overflow = 'hidden'
        document.body.style.position = 'fixed'
        document.body.style.width = '100%'
      } else {
        document.body.style.overflow = ''
        document.body.style.position = ''
        document.body.style.width = ''
      }
    }
  })
})

</script>

<style scoped>
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

.nav-item svg {
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.language-section {
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid #E5E7EB;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: #111;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #EF4444;
  background: none;
  border: none;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
  font-family: inherit;
}

.logout-btn:hover {
  color: #DC2626;
}

/* Sidebar Overlay */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1001;
}

/* Close Button */
.close-btn {
  display: none;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  color: #111;
  transition: all 0.2s;
  margin-left: auto;
}

.close-btn:hover {
  background: #E5E7EB;
}

@media (max-width: 1024px) {
  .sidebar-overlay {
    display: block;
  }

  .admin-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1002;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  }

  .admin-sidebar.open {
    transform: translateX(0);
  }

  .close-btn {
    display: flex;
  }
}

@media (max-width: 640px) {
  .admin-sidebar {
    width: 100%;
    max-width: 320px;
  }

  .nav-item {
    padding: 16px;
    font-size: 1rem;
  }
}
</style>
