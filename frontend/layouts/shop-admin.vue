<template>
    <div class="shop-admin-layout">
        <!-- Mobile Header -->
        <header class="mobile-header">
            <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
                <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="2">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
                <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
            <span class="mobile-title">{{ $t('admin.panel') }}</span>
            <NuxtLink :to="`/${shopSlug}`" class="home-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </NuxtLink>
        </header>

        <ShopAdminSidebar v-if="shopSlug" :shop-slug="shopSlug" :current-route="currentRoute" :model-value="sidebarOpen"
            @update:model-value="sidebarOpen = $event" />

        <!-- Main Content -->
        <main class="admin-main">
            <slot />
        </main>
    </div>
</template>

<script setup>
const route = useRoute()
const sidebarOpen = ref(false)

// Extract shop slug from route params
// Support both 'shop' and 'slug' params as it depends on directory naming
const shopSlug = computed(() => {
    return route.params.slug || route.params.shop || ''
})

const currentRoute = computed(() => {
    const path = route.path
    if (path.includes('/orders')) return 'orders'
    if (path.includes('/products')) return 'products'
    if (path.includes('/categories')) return 'categories'
    if (path.includes('/brands')) return 'brands'
    if (path.includes('/banner')) return 'banner'
    if (path.includes('/info')) return 'info'
    if (path.includes('/delivery')) return 'delivery'
    if (path.includes('/subscription')) return 'subscription'
    return 'dashboard'
})
</script>

<style scoped>
.shop-admin-layout {
    display: flex;
    min-height: 100vh;
    background: #f8fafc;
}

.admin-main {
    flex: 1;
    padding: 32px;
    margin-left: 280px;
    /* Sidebar width */
    width: calc(100% - 280px);
}

.mobile-header {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 0 16px;
    align-items: center;
    justify-content: space-between;
    z-index: 40;
}

.menu-btn,
.home-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    color: #374151;
    cursor: pointer;
    border-radius: 8px;
}

.menu-btn:hover,
.home-btn:hover {
    background: #f3f4f6;
}

.mobile-title {
    font-weight: 600;
    font-size: 1.125rem;
    color: #111827;
}

@media (max-width: 1024px) {
    .shop-admin-layout {
        padding-top: 64px;
    }

    .admin-main {
        margin-left: 0;
        width: 100%;
        padding: 20px;
    }

    .mobile-header {
        display: flex;
    }
}
</style>
