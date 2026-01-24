<template>
  <div class="platform-admin-layout">
    <!-- Sidebar -->
    <PlatformAdminSidebar :current-route="currentRoute" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <!-- Main Content Wrapper -->
    <div class="admin-wrapper" :class="{ 'sidebar-open': sidebarOpen }">
      <main class="admin-main">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
const route = useRoute()
const { logout } = useAuth()
const localePath = useLocalePath()
const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success(t('auth.loggedOut'))
}

const currentRoute = computed(() => {
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  if (route.path.includes('/subscription-requests')) return 'subscription-requests'
  if (route.path.includes('/subscription-plans')) return 'subscription-plans'
  if (route.path.includes('/offers')) return 'offers'
  return 'dashboard'
})

// Close sidebar on navigation on mobile
watch(() => route.path, () => {
  sidebarOpen.value = false
})
</script>

<style scoped>
.platform-admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.admin-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 280px;
  /* Sidebar width */
  transition: margin-left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.admin-main {
  flex: 1;
  width: 100%;
}

@media (max-width: 1024px) {
  .admin-wrapper {
    margin-left: 0;
  }
}
</style>
