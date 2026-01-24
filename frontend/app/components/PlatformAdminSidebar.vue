<template>
  <!-- Sidebar Overlay -->
  <Transition name="fade">
    <div v-if="isOpen" class="sidebar-overlay" @click="closeSidebar"></div>
  </Transition>

  <aside class="admin-sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <div class="brand">
        <div class="brand-logo">
          <iconify-icon icon="lucide:layout-dashboard" />
        </div>
        <div class="brand-info">
          <h2 class="brand-title">Storely</h2>
          <span class="brand-tag">Platform Admin</span>
        </div>
      </div>
      <button class="close-btn" @click="closeSidebar">
        <iconify-icon icon="lucide:x" />
      </button>
    </div>

    <div class="sidebar-scroll">
      <nav class="sidebar-nav">
        <div class="nav-label">{{ $t('platformAdmin.nav.main') || 'Main Menu' }}</div>

        <NuxtLink :to="localePath('/platform/admin')" class="nav-item"
          :class="{ active: currentRoute === 'dashboard' }">
          <div class="nav-icon"><iconify-icon icon="lucide:pie-chart" /></div>
          <span>{{ $t('platformAdmin.nav.dashboard') }}</span>
        </NuxtLink>

        <NuxtLink :to="localePath('/platform/admin/shops')" class="nav-item"
          :class="{ active: currentRoute === 'shops' }">
          <div class="nav-icon"><iconify-icon icon="lucide:store" /></div>
          <span>{{ $t('platformAdmin.nav.shops') }}</span>
          <span v-if="shopsCount" class="nav-badge">{{ shopsCount }}</span>
        </NuxtLink>

        <NuxtLink :to="localePath('/platform/admin/users')" class="nav-item"
          :class="{ active: currentRoute === 'users' }">
          <div class="nav-icon"><iconify-icon icon="lucide:users" /></div>
          <span>{{ $t('platformAdmin.nav.users') }}</span>
        </NuxtLink>

        <div class="nav-divider"></div>
        <div class="nav-label">{{ $t('platformAdmin.nav.finance') || 'Finance' }}</div>

        <NuxtLink :to="localePath('/platform/admin/billing')" class="nav-item"
          :class="{ active: currentRoute === 'billing' }">
          <div class="nav-icon"><iconify-icon icon="lucide:arrow-right-left" /></div>
          <span>{{ $t('platformAdmin.nav.finance') }}</span>
        </NuxtLink>

        <NuxtLink :to="localePath('/platform/admin/subscription-requests')" class="nav-item"
          :class="{ active: currentRoute === 'subscription-requests' }">
          <div class="nav-icon"><iconify-icon icon="lucide:credit-card" /></div>
          <span>{{ $t('platformAdmin.nav.requests') }}</span>
          <span v-if="pendingRequestsCount" class="nav-badge pulse">{{ pendingRequestsCount }}</span>
        </NuxtLink>

        <NuxtLink :to="localePath('/platform/admin/subscription-plans')" class="nav-item"
          :class="{ active: currentRoute === 'subscription-plans' }">
          <div class="nav-icon"><iconify-icon icon="lucide:package-check" /></div>
          <span>{{ $t('platformAdmin.nav.plans') }}</span>
        </NuxtLink>

        <div class="nav-divider"></div>
        <div class="nav-label">{{ $t('platformAdmin.nav.content') || 'Content' }}</div>

        <NuxtLink :to="localePath('/platform/admin/offers')" class="nav-item"
          :class="{ active: currentRoute === 'offers' }">
          <div class="nav-icon"><iconify-icon icon="lucide:gift" /></div>
          <span>{{ $t('platformAdmin.nav.offers') }}</span>
        </NuxtLink>
      </nav>
    </div>

    <div class="sidebar-footer">
      <div class="lang-switcher-wrap">
        <LanguageSwitcher direction="up" />
      </div>

      <div class="footer-actions">
        <NuxtLink :to="localePath('/')" class="action-btn home" title="Home">
          <iconify-icon icon="lucide:home" />
        </NuxtLink>
        <button @click="$emit('logout')" class="action-btn logout" title="Logout">
          <iconify-icon icon="lucide:log-out" />
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
const props = defineProps({
  currentRoute: { type: String, default: 'dashboard' },
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['logout', 'update:modelValue'])
const localePath = useLocalePath()
const config = useRuntimeConfig()
const { token } = useAuth()

const isOpen = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v)
})

const closeSidebar = () => isOpen.value = false

// Optional: Fetch counts for badges
const { data: shops } = useFetch(config.public.apiBase + '/platform/shops', {
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` })),
  server: false
})
const shopsCount = computed(() => shops.value?.length || 0)

const { data: requests } = useFetch(config.public.apiBase + '/platform/admin/subscription-requests', {
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` })),
  server: false
})
const pendingRequestsCount = computed(() => requests.value?.filter(r => r.status === 'pending').length || 0)

const route = useRoute()
watch(() => route.path, closeSidebar)

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
  background: #ffffff;
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 1000;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.02);
}

.sidebar-header {
  padding: 32px 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-logo {
  width: 44px;
  height: 44px;
  background: #111;
  color: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.brand-title {
  font-size: 1.25rem;
  font-weight: 950;
  margin: 0;
  letter-spacing: -0.5px;
}

.brand-tag {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #71717a;
  letter-spacing: 0.5px;
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px;
}

.sidebar-scroll::-webkit-scrollbar {
  width: 4px;
}

.sidebar-scroll::-webkit-scrollbar-thumb {
  background: #f1f1f1;
  border-radius: 10px;
}

.nav-label {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #a1a1aa;
  padding: 24px 12px 12px;
  letter-spacing: 1px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  color: #52525b;
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 4px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover {
  background: #f8fafc;
  color: #111;
}

.nav-item.active {
  background: #111;
  color: white;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  font-size: 1.25rem;
  display: flex;
  align-items: center;
}

.nav-badge {
  margin-left: auto;
  font-size: 0.7rem;
  font-weight: 800;
  background: #f1f5f9;
  color: #334155;
  padding: 2px 8px;
  border-radius: 20px;
}

.active .nav-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.nav-badge.pulse {
  background: #fee2e2;
  color: #ef4444;
  animation: badge-pulse 2s infinite;
}

@keyframes badge-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }

  70% {
    box-shadow: 0 0 0 6px rgba(239, 68, 68, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

.nav-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 16px 12px;
}

.sidebar-footer {
  padding: 24px;
  background: #f8fafc;
  border-radius: 24px 24px 0 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.footer-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  border: 1.5px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.action-btn:hover {
  border-color: #111;
  color: #111;
}

.action-btn.logout:hover {
  background: #fee2e2;
  border-color: #fca5a5;
  color: #ef4444;
}

.close-btn {
  display: none;
}

@media (max-width: 1024px) {
  .admin-sidebar {
    transform: translateX(-100%);
    box-shadow: none;
  }

  .admin-sidebar.open {
    transform: translateX(0);
    box-shadow: 20px 0 50px rgba(0, 0, 0, 0.1);
  }

  .close-btn {
    display: flex;
    width: 36px;
    height: 36px;
    background: #f1f5f9;
    border: none;
    border-radius: 10px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-left: auto;
  }
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 999;
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
