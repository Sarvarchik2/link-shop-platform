<template>
    <div class="shop-admin-page">
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
            <span class="mobile-title">{{ $t('admin.delivery.title') }}</span>
            <NuxtLink :to="localePath(`/${shopSlug}`)" class="home-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </NuxtLink>
        </header>

        <ShopAdminSidebar :shop-slug="shopSlug" current-route="delivery" v-model="sidebarOpen" />

        <main class="admin-main">
            <h1 class="page-title">{{ $t('admin.delivery.title') }}</h1>
            <p class="page-subtitle">{{ $t('admin.deliverySettingsSubtitle') }}</p>

            <div v-if="pending" class="loading-state">
                <div class="spinner"></div>
            </div>

            <form v-else @submit.prevent="saveSettings" class="settings-form">
                <!-- Delivery Mode Selection -->
                <div class="settings-card">
                    <h3 class="card-title">{{ $t('admin.deliveryType') }}</h3>

                    <div class="delivery-types">
                        <label class="type-option" :class="{ active: settings.type === 'free' }">
                            <input type="radio" v-model="settings.type" value="free" />
                            <div class="type-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                                </svg>
                            </div>
                            <div class="type-info">
                                <span class="type-name">{{ $t('admin.deliveryFree') }}</span>
                                <span class="type-desc">{{ $t('admin.deliveryFreeDesc') }}</span>
                            </div>
                        </label>

                        <label class="type-option" :class="{ active: settings.type === 'fixed' }">
                            <input type="radio" v-model="settings.type" value="fixed" />
                            <div class="type-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <rect x="1" y="3" width="15" height="13"></rect>
                                    <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                                    <circle cx="5.5" cy="18.5" r="2.5"></circle>
                                    <circle cx="18.5" cy="18.5" r="2.5"></circle>
                                </svg>
                            </div>
                            <div class="type-info">
                                <span class="type-name">{{ $t('admin.deliveryFixed') }}</span>
                                <span class="type-desc">{{ $t('admin.deliveryFixedDesc') }}</span>
                            </div>
                        </label>

                        <label class="type-option" :class="{ active: settings.type === 'regional' }">
                            <input type="radio" v-model="settings.type" value="regional" />
                            <div class="type-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                    <circle cx="12" cy="10" r="3"></circle>
                                </svg>
                            </div>
                            <div class="type-info">
                                <span class="type-name">{{ $t('admin.deliveryRegional') }}</span>
                                <span class="type-desc">{{ $t('admin.deliveryRegionalDesc') }}</span>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Fixed Price Input -->
                <div v-if="settings.type === 'fixed'" class="settings-card fade-in">
                    <h3 class="card-title">{{ $t('admin.deliveryFixed') }}</h3>
                    <div class="form-group">
                        <label class="form-label">{{ $t('admin.deliveryPrice') }} (UZS)</label>
                        <input v-model.number="settings.price" type="number" class="form-input" placeholder="20000"
                            min="0" required />
                    </div>
                </div>

                <!-- Regional Settings -->
                <div v-if="settings.type === 'regional'" class="settings-card fade-in">
                    <h3 class="card-title">{{ $t('admin.deliveryRegional') }}</h3>
                    <p class="section-desc">{{ $t('admin.deliveryRegionalInfo') }}</p>

                    <div class="regional-grid">
                        <div v-for="region in regions" :key="region" class="region-item">
                            <label class="region-name">{{ region }}</label>
                            <div class="price-input-wrapper">
                                <input v-model.number="settings.regions[region]" type="number" class="form-input"
                                    placeholder="0" min="0" />
                                <span class="currency-suffix">UZS</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Submit Button -->
                <div class="form-actions">
                    <button type="submit" class="save-btn" :disabled="saving">
                        <span v-if="saving" class="spinner-small"></span>
                        {{ saving ? $t('common.saving') : $t('common.save') }}
                    </button>
                </div>
            </form>
        </main>
    </div>
</template>

<script setup>
definePageMeta({
    layout: false
})

const route = useRoute()
const { t } = useI18n()
const shopSlug = route.params.slug
const toast = useToast()
const { token } = useAuth()
const sidebarOpen = ref(false)
const localePath = useLocalePath()

const regions = [
    'Toshkent', 'Samarqand', 'Buxoro', 'Namangan',
    'Andijon', "Farg'ona", 'Boshqa'
]

const settings = reactive({
    type: 'free',
    price: 0,
    regions: {}
})

// Initialize regions
regions.forEach(r => {
    if (!(r in settings.regions)) {
        settings.regions[r] = 0
    }
})

const saving = ref(false)

const config = useRuntimeConfig()
// Fetch initial data
const { data: shop, pending } = useFetch(`${config.public.apiBase}/platform/shops/${shopSlug}`, {
    headers: {
        'Authorization': `Bearer ${token.value}`
    },
    server: false
})

// Watch for data and populate form
watch(shop, (newShop) => {
    if (newShop && newShop.delivery_settings) {
        if (newShop.delivery_settings.type) settings.type = newShop.delivery_settings.type
        if (newShop.delivery_settings.price) settings.price = newShop.delivery_settings.price

        // Merge regions
        if (newShop.delivery_settings.regions) {
            regions.forEach(r => {
                settings.regions[r] = newShop.delivery_settings.regions[r] || 0
            })
        }
    }
}, { immediate: true })

const saveSettings = async () => {
    saving.value = true
    try {
        const payload = {
            delivery_settings: {
                type: settings.type,
                price: settings.price,
                regions: settings.regions
            }
        }

        await $fetch(`${config.public.apiBase}/shop/${shopSlug}/admin/info`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token.value}`
            },
            body: payload
        })

        toast.success(t('alerts.shop.saved'))
    } catch (e) {
        toast.error(t('alerts.shop.error'))
        console.error(e)
    } finally {
        saving.value = false
    }
}
</script>

<style scoped>
.delivery-settings-page {
    min-height: 100vh;
    background: #F5F7FA;
}

.admin-content {
    padding: 40px;
    max-width: 1000px;
    margin: 0 auto;
}

@media (max-width: 768px) {
    .admin-content {
        padding: 20px;
    }
}

.content-wrapper {
    max-width: 800px;
}

.page-title {
    font-size: 2rem;
    font-weight: 800;
    color: #111;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.page-subtitle {
    color: #6B7280;
    margin-bottom: 32px;
}

.settings-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid #E5E7EB;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 20px;
    color: #111;
}

.delivery-types {
    display: grid;
    gap: 16px;
}

.type-option {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}

.type-option:hover {
    border-color: #D1D5DB;
}

.type-option.active {
    border-color: #111;
    background: #F9FAFB;
}

.type-option input {
    display: none;
}

.type-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: #fff;
    border: 1px solid #E5E7EB;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #111;
    flex-shrink: 0;
}

.type-option.active .type-icon {
    background: #111;
    color: white;
    border-color: #111;
}

.type-info {
    flex: 1;
}

.type-name {
    display: block;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 4px;
    color: #111;
}

.type-desc {
    font-size: 0.85rem;
    color: #6B7280;
    line-height: 1.4;
}

.form-group {
    margin-bottom: 0;
}

.form-label {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
    color: #374151;
}

.form-input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #E5E7EB;
    border-radius: 10px;
    font-size: 1rem;
    transition: all 0.2s;
}

.form-input:focus {
    border-color: #111;
    outline: none;
}

.regional-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}

.region-item {
    background: #F9FAFB;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #E5E7EB;
}

.region-name {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.price-input-wrapper {
    position: relative;
}

.currency-suffix {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #9CA3AF;
    font-size: 0.85rem;
    font-weight: 600;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 32px;
}

.save-btn {
    background: #111;
    color: white;
    padding: 12px 32px;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
}

.save-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.save-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.fade-in {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>

<style scoped>
/* Layout Styles */
.shop-admin-page {
    min-height: 100vh;
    display: flex;
    background: #FAFAFA;
}

.admin-main {
    flex: 1;
    margin-left: 280px;
    min-height: 100vh;
    padding: 40px;
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

@media (max-width: 1024px) {
    .admin-main {
        margin-left: 0;
        padding-top: 80px;
        /* Space for mobile header */
    }

    .mobile-header {
        display: flex;
    }
}

/* Page Specific */
.content-wrapper {
    max-width: 800px;
    margin: 0 auto;
}

.page-title {
    font-size: 2rem;
    font-weight: 800;
    color: #111;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.page-subtitle {
    color: #6B7280;
    margin-bottom: 32px;
}

.settings-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid #E5E7EB;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 20px;
    color: #111;
}

.delivery-types {
    display: grid;
    gap: 16px;
}

.type-option {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}

.type-option:hover {
    border-color: #D1D5DB;
}

.type-option.active {
    border-color: #111;
    background: #F9FAFB;
}

.type-option input {
    display: none;
}

.type-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: #fff;
    border: 1px solid #E5E7EB;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #111;
    flex-shrink: 0;
}

.type-option.active .type-icon {
    background: #111;
    color: white;
    border-color: #111;
}

.type-info {
    flex: 1;
}

.type-name {
    display: block;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 4px;
    color: #111;
}

.type-desc {
    font-size: 0.85rem;
    color: #6B7280;
    line-height: 1.4;
}

.form-group {
    margin-bottom: 0;
}

.form-label {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
    color: #374151;
}

.form-input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #E5E7EB;
    border-radius: 10px;
    font-size: 1rem;
    transition: all 0.2s;
}

.form-input:focus {
    border-color: #111;
    outline: none;
}

.regional-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}

.region-item {
    background: #F9FAFB;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #E5E7EB;
}

.region-name {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.price-input-wrapper {
    position: relative;
}

.currency-suffix {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #9CA3AF;
    font-size: 0.85rem;
    font-weight: 600;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 32px;
}

.save-btn {
    background: #111;
    color: white;
    padding: 12px 32px;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
}

.save-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.save-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.fade-in {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>
