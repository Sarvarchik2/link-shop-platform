<template>
  <aside class="admin-sidebar">
    <div class="sidebar-header">
      <div class="sidebar-logo">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
        </svg>
      </div>
      <h2 class="sidebar-title">Панель управления</h2>
    </div>
    
    <nav class="sidebar-nav">
      <NuxtLink :to="`/shop/${shopSlug}/admin`" class="nav-item" :class="{ active: currentRoute === 'dashboard' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"></rect>
          <rect x="14" y="3" width="7" height="7"></rect>
          <rect x="14" y="14" width="7" height="7"></rect>
          <rect x="3" y="14" width="7" height="7"></rect>
        </svg>
        <span>Главная</span>
      </NuxtLink>
      
      <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="nav-item" :class="{ active: currentRoute === 'products' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
        <span>Товары</span>
      </NuxtLink>
      
      <NuxtLink :to="`/shop/${shopSlug}/admin/orders`" class="nav-item" :class="{ active: currentRoute === 'orders' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
        </svg>
        <span>Заказы</span>
      </NuxtLink>
      
      <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="nav-item" :class="{ active: currentRoute === 'categories' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="8" y1="6" x2="21" y2="6"></line>
          <line x1="8" y1="12" x2="21" y2="12"></line>
          <line x1="8" y1="18" x2="21" y2="18"></line>
          <line x1="3" y1="6" x2="3.01" y2="6"></line>
          <line x1="3" y1="12" x2="3.01" y2="12"></line>
          <line x1="3" y1="18" x2="3.01" y2="18"></line>
        </svg>
        <span>Категории</span>
      </NuxtLink>
      
      <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="nav-item" :class="{ active: currentRoute === 'brands' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
          <line x1="7" y1="7" x2="7.01" y2="7"></line>
        </svg>
        <span>Бренды</span>
      </NuxtLink>
      
      <NuxtLink :to="`/shop/${shopSlug}/admin/banner`" class="nav-item" :class="{ active: currentRoute === 'banner' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <circle cx="8.5" cy="8.5" r="1.5"></circle>
          <polyline points="21 15 16 10 5 21"></polyline>
        </svg>
        <span>Баннер</span>
      </NuxtLink>
      
      <NuxtLink :to="`/shop/${shopSlug}/subscription`" class="nav-item" :class="{ active: currentRoute === 'subscription' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="1" x2="12" y2="23"></line>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
        </svg>
        <span>Подписка</span>
      </NuxtLink>
    </nav>
    
    <div class="sidebar-footer">
      <NuxtLink :to="`/${shopSlug}`" class="back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        <span>В магазин</span>
      </NuxtLink>
      <button @click="handleLogout" class="logout-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span>Выйти</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
const props = defineProps({
  shopSlug: {
    type: String,
    required: true
  },
  currentRoute: {
    type: String,
    default: 'dashboard'
  }
})

const { logout } = useAuth()

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}
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

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  gap: 12px;
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

@media (max-width: 1024px) {
  .admin-sidebar {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
}
</style>
