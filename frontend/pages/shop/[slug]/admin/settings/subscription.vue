<template>
    <div class="subscription-page">
        <div class="page-header">
            <h1 class="page-title">{{ $t('shopSettings.subscription.title') }}</h1>
            <p class="page-subtitle">{{ $t('shopSettings.subscription.subtitle') }}</p>
        </div>

        <div v-if="pending" class="loading-state">
            <div class="spinner"></div>
        </div>

        <div v-else class="content-grid">
            <!-- Current Plan Card -->
            <div class="card current-plan">
                <div class="plan-header">
                    <div>
                        <h2 class="section-title">{{ $t('shopSettings.subscription.currentPlan') }}</h2>
                        <div class="status-badge" :class="shop?.subscription_status">
                            {{ getStatusText(shop?.subscription_status) }}
                        </div>
                    </div>
                    <div class="expiry-date" v-if="shop?.subscription_expires_at">
                        <span class="label">{{ $t('shopSettings.subscription.expires') }}</span>
                        <span class="date">{{ formatDate(shop.subscription_expires_at) }}</span>
                    </div>
                </div>

                <div class="usage-stats">
                    <div class="stat-item">
                        <span class="stat-label">{{ $t('shopSettings.subscription.products') }}</span>
                        <span class="stat-value">{{ productsCount }} / {{ PLAN_LIMITS.products }}</span>
                        <div class="progress-bar">
                            <div class="progress"
                                :style="{ width: getProgress(productsCount, PLAN_LIMITS.products) + '%' }"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Plans Grid -->
            <div class="plans-section">
                <h2 class="section-title">{{ $t('shopSettings.subscription.plans') }}</h2>
                <div class="plans-grid">
                    <div v-for="plan in plans" :key="plan.id" class="plan-card" :class="{ 'featured': plan.featured }">
                        <div class="plan-header">
                            <h3 class="plan-name">{{ plan.name }}</h3>
                            <div class="plan-price">
                                <span class="amount">{{ plan.priceFormatted }}</span>
                                <span class="period">/ {{ $t('shopSettings.subscription.month') }}</span>
                            </div>
                        </div>

                        <ul class="plan-features">
                            <li v-for="(feature, idx) in plan.features" :key="idx">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                {{ feature }}
                            </li>
                        </ul>

                        <button class="plan-btn" :class="{ 'primary': plan.featured }" @click="selectPlan(plan)">
                            {{ $t('shopSettings.subscription.select') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    layout: 'shop-admin'
})

const route = useRoute()
const { t } = useI18n()
const config = useRuntimeConfig()
const shopSlug = route.params.slug

// Mock Data & Limits
const PLAN_LIMITS = {
    products: 100
}

const plans = [
    {
        id: 'basic',
        name: 'Basic',
        priceFormatted: '50 000 UZS',
        featured: false,
        features: [
            '100 ta mahsulot',
            'Telegram bot',
            'Admin panel'
        ]
    },
    {
        id: 'pro',
        name: 'Pro',
        priceFormatted: '150 000 UZS',
        featured: true,
        features: [
            'Cheksiz mahsulotlar',
            'Barcha funksiyalar',
            'Premium qo\'llab quvvatlash'
        ]
    }
]

// Fetch Shop Data
const { data: shop, pending } = await useFetch(`${config.public.apiBase}/platform/shops/${shopSlug}`, {
    headers: { Authorization: `Bearer ${useAuth().token.value}` }
})

// Mock products count for now
const productsCount = ref(45)

const formatDate = (date) => {
    return new Date(date).toLocaleDateString('uz-UZ')
}

const getProgress = (current, max) => {
    return Math.min((current / max) * 100, 100)
}

const getStatusText = (status) => {
    const map = {
        active: t('admin.status.active'),
        trial: t('admin.status.trial'),
        expired: t('admin.status.expired'),
        cancelled: t('admin.status.cancelled')
    }
    return map[status] || status
}

const selectPlan = (plan) => {
    // TODO: Implement payment flow
    console.log('Selected plan:', plan)
}
</script>

<style scoped>
.subscription-page {
    padding: 24px;
}

.page-header {
    margin-bottom: 32px;
}

.page-title {
    font-size: 1.875rem;
    font-weight: 800;
    color: #111;
    margin-bottom: 8px;
}

.page-subtitle {
    color: #6B7280;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #E5E7EB;
    margin-bottom: 32px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 16px;
}

.current-plan .plan-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 24px;
}

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
    margin-top: 8px;
}

.status-badge.active {
    background: #D1FAE5;
    color: #065F46;
}

.status-badge.trial {
    background: #FEF3C7;
    color: #92400E;
}

.status-badge.expired {
    background: #FEE2E2;
    color: #991B1B;
}

.usage-stats {
    max-width: 400px;
}

.stat-item {
    margin-bottom: 16px;
}

.stat-label {
    display: block;
    font-size: 0.875rem;
    color: #6B7280;
    margin-bottom: 4px;
}

.progress-bar {
    height: 8px;
    background: #F3F4F6;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 8px;
}

.progress {
    height: 100%;
    background: #111;
    border-radius: 4px;
}

.plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

.plan-card {
    background: white;
    border-radius: 20px;
    padding: 32px;
    border: 1px solid #E5E7EB;
    display: flex;
    flex-direction: column;
}

.plan-card.featured {
    border: 2px solid #111;
    position: relative;
}

.plan-name {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 16px;
}

.plan-price {
    margin-bottom: 24px;
}

.amount {
    font-size: 2rem;
    font-weight: 900;
}

.period {
    color: #6B7280;
}

.plan-features {
    list-style: none;
    padding: 0;
    margin: 0 0 32px 0;
    flex-grow: 1;
}

.plan-features li {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    color: #374151;
}

.plan-features svg {
    color: #10B981;
}

.plan-btn {
    width: 100%;
    padding: 16px;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    background: #F3F4F6;
    color: #111;
    border: none;
    transition: all 0.2s;
}

.plan-btn.primary {
    background: #111;
    color: white;
}

.plan-btn:hover {
    transform: translateY(-2px);
}
</style>
