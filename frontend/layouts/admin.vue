<template>
  <div class="admin-layout">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">Boshqaruv paneli</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <!-- Sidebar Overlay -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay" 
      @click="sidebarOpen = false"
    ></div>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <div class="logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
          <span>Boshqaruv paneli</span>
        </div>
        <button class="close-btn" @click="sidebarOpen = false">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <nav class="nav">
        <NuxtLink to="/admin" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Boshqaruv</span>
        </NuxtLink>
        
        <NuxtLink to="/admin/banner" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
          </svg>
          <span>Banner</span>
        </NuxtLink>
        
        <NuxtLink to="/admin/products" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>Mahsulotlar</span>
        </NuxtLink>
        
        <NuxtLink to="/admin/brands" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <line x1="7" y1="7" x2="7.01" y2="7"></line>
          </svg>
          <span>Brendlar</span>
        </NuxtLink>
        
        <NuxtLink to="/admin/categories" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
          <span>Kategoriyalar</span>
        </NuxtLink>
        
        <NuxtLink to="/admin/users" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>Foydalanuvchilar</span>
        </NuxtLink>
        
        <NuxtLink to="/admin/orders" class="nav-item" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Buyurtmalar</span>
        </NuxtLink>
      </nav>
      
      <div class="sidebar-footer">
        <NuxtLink to="/" class="nav-item back-home" @click="closeSidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Do'konga qaytish</span>
        </NuxtLink>
      </div>
    </aside>
    
    <main class="content">
      <slot />
    </main>
  </div>
</template>

<script setup>
const sidebarOpen = ref(false)

const closeSidebar = () => {
  sidebarOpen.value = false
}

// Close sidebar on route change
const route = useRoute()
watch(() => route.path, () => {
  sidebarOpen.value = false
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6f8;
}

/* Mobile Header */
.mobile-header {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
  z-index: 1000;
}

.menu-btn,
.home-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  color: #111;
  transition: all 0.2s;
}

.menu-btn:hover,
.home-btn:hover {
  background: #111;
  color: white;
}

.mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

/* Sidebar Overlay */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1001;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
}

.close-btn {
  display: none;
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: #666;
}

.nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  color: #6B7280;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s;
  text-decoration: none;
}

.nav-item:hover {
  background: #F3F4F6;
  color: #111;
}

.nav-item.router-link-active {
  background: #111;
  color: white;
}

.nav-item svg {
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #F3F4F6;
}

.back-home {
  color: #9CA3AF;
}

.back-home:hover {
  background: #FEF2F2;
  color: #DC2626;
}

/* Content */
.content {
  flex: 1;
  min-width: 0;
  overflow-x: hidden;
  padding: 32px;
}

/* Unified page styles */
.content :deep(.page-title) {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.content :deep(.page-header) {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.content :deep(.page-header > .page-title) {
  margin-bottom: 0;
  flex-shrink: 0;
}

.content :deep(.page-header > .filters) {
  flex: 1;
  min-width: 0;
}

.content :deep(.page-header > .btn),
.content :deep(.page-header > a.btn) {
  flex-shrink: 0;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .content {
    padding: 20px 16px;
    padding-bottom: 40px;
  }
  
  .content :deep(.page-title) {
    font-size: 1.5rem;
  }
  
  .content :deep(.page-header) {
    flex-direction: column;
    align-items: stretch;
    margin-bottom: 20px;
    gap: 16px;
  }
  
  .content :deep(.page-header > .page-title) {
    margin-bottom: 0;
  }
  
  .content :deep(.page-header > .filters) {
    width: 100%;
  }
  
  .content :deep(.page-header > .btn),
  .content :deep(.page-header > a.btn) {
    width: 100%;
    justify-content: center;
  }
}

/* Mobile Styles */
@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }
  
  .sidebar-overlay {
    display: block;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s;
  }
  
  .sidebar-overlay.show,
  .sidebar.open ~ .sidebar-overlay {
    opacity: 1;
    visibility: visible;
  }
  
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1002;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
  
  .close-btn {
    display: flex;
  }
  
  .content {
    padding-top: 60px;
  }
}

@media (max-width: 640px) {
  .sidebar {
    width: 100%;
    max-width: 320px;
  }
  
  .nav-item {
    padding: 16px;
    font-size: 1rem;
  }
}
</style>
