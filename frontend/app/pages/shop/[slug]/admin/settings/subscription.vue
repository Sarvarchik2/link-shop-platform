<template>
    <div class="subscription-premium-page">
        <!-- Activation Success Header -->
        <Transition name="slide-down">
            <div v-if="route.query.activated" class="activation-welcome">
                <div class="welcome-content">
                    <div class="welcome-icon">🎉</div>
                    <div>
                        <h2>{{ $t('admin.subscriptionPage.premium.welcomeTitle') }}</h2>
                        <p>{{ $t('admin.subscriptionPage.premium.welcomeDesc') }}</p>
                    </div>
                </div>
                <button class="close-welcome" @click="removeActivatedQuery">
                    <iconify-icon icon="lucide:x"></iconify-icon>
                </button>
            </div>
        </Transition>

        <div class="page-header">
            <div class="header-left">
                <h1 class="page-title">{{ $t('admin.subscriptionPage.premium.pageTitle') }}</h1>
                <p class="page-subtitle">{{ $t('admin.subscriptionPage.premium.pageSubtitle') }}</p>
            </div>

            <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/wallet`)" class="wallet-pill">
                <div class="wallet-icon">
                    <iconify-icon icon="lucide:wallet"></iconify-icon>
                </div>
                <div class="wallet-details">
                    <span class="label">{{ $t('admin.subscriptionPage.premium.yourBalance') }}</span>
                    <span class="amount">{{ formatPrice(walletBalance) }}</span>
                </div>
                <div class="wallet-add">
                    <iconify-icon icon="lucide:plus"></iconify-icon>
                </div>
            </NuxtLink>
        </div>

        <div v-if="pending" class="loading-full">
            <div class="premium-loader"></div>
        </div>

        <div v-else class="subscription-content">
            <!-- Current Plan & Stats Overview -->
            <div class="overview-grid">
                <div class="card current-plan-card" :class="shop?.subscription_status">
                    <div class="card-header">
                        <div class="plan-info">
                            <span class="current-label">{{ $t('admin.subscriptionPage.premium.currentPlan') }}</span>
                            <h2 class="current-name">{{ shop?.subscription_plan_id ?
                                getPlanNameById(shop.subscription_plan_id) : $t('admin.subscriptionPage.premium.noPlan')
                            }}</h2>
                        </div>
                        <div class="status-badge-wrap">
                            <span class="status-pill" :class="shop?.subscription_status">
                                <span class="dot"></span>
                                {{ getStatusText(shop?.subscription_status) }}
                            </span>
                        </div>
                    </div>

                    <div class="card-body">
                        <div class="expiry-info" v-if="shop?.subscription_expires_at">
                            <iconify-icon icon="lucide:calendar"></iconify-icon>
                            <span>{{ $t('admin.subscriptionPage.premium.expiresAt') }} <strong>{{
                                formatDateString(shop.subscription_expires_at) }}</strong></span>
                        </div>

                        <div class="auto-renew-toggle" @click="toggleAutoRenewal">
                            <div class="toggle-text">
                                <span class="toggle-title">{{ $t('admin.subscriptionPage.premium.autoRenew') }}</span>
                                <span class="toggle-desc">{{ $t('admin.subscriptionPage.premium.autoRenewDesc')
                                }}</span>
                            </div>
                            <div class="toggle-switch" :class="{ active: autoRenewalEnabled }">
                                <div class="toggle-dot"></div>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer" v-if="shop?.subscription_status === 'active'">
                        <button @click="openCancelModal" class="btn-cancel-sub">{{
                            $t('admin.subscriptionPage.premium.cancelSub') }}</button>
                    </div>
                </div>

                <div class="card stats-card">
                    <h3 class="stats-title">{{ $t('admin.subscriptionPage.premium.limitsTitle') }}</h3>
                    <div class="stats-list">
                        <div class="stat-row">
                            <div class="stat-info">
                                <span>{{ $t('admin.products') }}</span>
                                <span class="stat-count">{{ stats?.total_products || 0 }} / {{
                                    stats?.plan_limit_products || '∞' }}</span>
                            </div>
                            <div class="progress-box">
                                <div class="progress-bg"></div>
                                <div class="progress-fill"
                                    :style="{ width: calculatePercent(stats?.total_products || 0, stats?.plan_limit_products) + '%' }">
                                </div>
                            </div>
                        </div>
                        <div class="stat-row">
                            <div class="stat-info">
                                <span>{{ $t('admin.banner') }}</span>
                                <span class="stat-count">{{ stats?.total_banners || 0 }} / {{ stats?.plan_limit_banners
                                    || 1 }}</span>
                            </div>
                            <div class="progress-box">
                                <div class="progress-bg"></div>
                                <div class="progress-fill"
                                    :style="{ width: calculatePercent(stats?.total_banners || 0, stats?.plan_limit_banners) + '%' }">
                                </div>
                            </div>
                        </div>
                        <!-- Broadcasts Stats -->
                        <div class="stat-row">
                            <div class="stat-info">
                                <span>{{ $t('admin.broadcasts.title') }}</span>
                                <span class="stat-count">{{ stats?.total_broadcasts || 0 }} / {{
                                    stats?.plan_can_broadcast ? '∞' : 0 }}</span>
                            </div>
                            <div class="progress-box">
                                <div class="progress-bg"></div>
                                <div class="progress-fill"
                                    :style="{ width: (stats?.plan_can_broadcast ? 0 : 100) + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Available Plans Section -->
            <div class="plans-section">
                <h2 class="section-title">{{ $t('admin.subscriptionPage.premium.allPlans') }}</h2>
                <div class="plans-grid">
                    <div v-for="plan in availablePlans" :key="plan.id" class="plan-item"
                        :class="{ highlight: plan.slug === 'premium', current: shop?.subscription_plan_id === plan.id }">
                        <div class="plan-item-header">
                            <div class="name-status">
                                <h3 class="name">{{ getLocalizedValue(plan, 'name') }}</h3>
                                <span v-if="shop?.subscription_plan_id === plan.id" class="badge-current">{{
                                    $t('admin.status.active') }}</span>
                            </div>
                            <div class="price">
                                <span class="val">{{ formatPrice(plan.price) }}</span>
                                <span class="mo">/ {{ $t('home.pricing.month') }}</span>
                            </div>
                        </div>
                        <p class="desc">{{ getLocalizedValue(plan, 'description') }}</p>

                        <ul class="plan-limits">
                            <li>
                                <iconify-icon icon="lucide:check-circle-2"></iconify-icon>
                                <span>{{ $t('admin.subscriptionPage.premium.limits.products', {
                                    count: plan.max_products
                                        || $t('admin.subscriptionPage.premium.limits.unlimited')
                                }) }}</span>
                            </li>
                            <li>
                                <iconify-icon icon="lucide:check-circle-2"></iconify-icon>
                                <span>{{ $t('admin.subscriptionPage.premium.limits.banners', {
                                    count: plan.max_banners
                                        || $t('admin.subscriptionPage.premium.limits.unlimited')
                                }) }}</span>
                            </li>
                            <li>
                                <iconify-icon :icon="plan.can_broadcast ? 'lucide:check-circle-2' : 'lucide:x-circle'"
                                    :class="{ 'text-muted': !plan.can_broadcast }"></iconify-icon>
                                <span>{{ $t('admin.subscriptionPage.premium.limits.broadcasts', {
                                    count:
                                        plan.can_broadcast ? '∞' : 0
                                }) }}</span>
                            </li>
                        </ul>

                        <div class="duration-selector" v-if="plan.price > 0">
                            <label>{{ $t('admin.subscriptionPage.premium.paymentPeriod') }}</label>
                            <div class="duration-chips">
                                <button v-for="d in durations" :key="d.months"
                                    @click="setPlanDuration(plan.id, d.months)" class="chip"
                                    :class="{ active: getPlanDuration(plan.id) === d.months }">
                                    <span class="months-val">{{ d.months }}м</span>
                                    <span v-if="d.discount" class="disc-badge">-{{ d.discount }}%</span>
                                </button>
                            </div>
                        </div>

                        <div class="total-calc" v-if="plan.price > 0">
                            <span class="label">{{ $t('admin.subscriptionPage.premium.toPay') }}</span>
                            <span class="total-val">{{ formatPrice(calculatePrice(plan, getPlanDuration(plan.id)).final)
                            }}</span>
                        </div>

                        <button class="btn-select-plan" @click="initiatePurchase(plan)" :disabled="loading">
                            {{ (shop?.subscription_plan_id === plan.id && shop?.subscription_status === 'active') ?
                                $t('admin.subscriptionPage.premium.renew') : $t('admin.subscriptionPage.premium.select') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Confirm Purchase Modal -->
        <Transition name="modal">
            <div v-if="showPurchaseModal" class="modal-overlay" @click.self="showPurchaseModal = false">
                <div class="modal-card">
                    <div class="modal-header">
                        <h2>{{ $t('admin.subscriptionPage.premium.modalTitle') }}</h2>
                        <button class="close-modal" @click="showPurchaseModal = false"><iconify-icon
                                icon="lucide:x"></iconify-icon></button>
                    </div>
                    <div class="modal-body">
                        <div class="summary-box">
                            <div class="summary-line">
                                <span>{{ $t('admin.subscriptionPage.labels.plan') }}:</span>
                                <strong>{{ getLocalizedValue(selectedPlan, 'name') }}</strong>
                            </div>
                            <div class="summary-line">
                                <span>{{ $t('admin.subscriptionPage.labels.duration') }}:</span>
                                <strong>{{ currentDuration }} {{ $t('admin.subscriptionPage.months.few') }}</strong>
                            </div>
                            <div class="summary-divider"></div>
                            <div class="summary-line total">
                                <span>{{ $t('admin.subscriptionPage.premium.totalToCharge') }}</span>
                                <strong class="total-price">{{ formatPrice(currentPrice.final) }}</strong>
                            </div>
                        </div>

                        <div class="payment-method-box" :class="{ error: walletBalance < currentPrice.final }">
                            <div class="p-info">
                                <div class="p-icon"><iconify-icon icon="lucide:wallet"></iconify-icon></div>
                                <div class="p-text">
                                    <span class="p-label">{{ $t('admin.subscriptionPage.premium.walletSource') }}</span>
                                    <span class="p-balance" :class="{ low: walletBalance < currentPrice.final }">{{
                                        $t('admin.subscriptionPage.premium.available') }} {{ formatPrice(walletBalance)
                                        }}</span>
                                </div>
                            </div>
                            <NuxtLink v-if="walletBalance < currentPrice.final"
                                :to="localePath(`/shop/${shopSlug}/admin/wallet`)" class="top-up-link">{{
                                    $t('admin.subscriptionPage.premium.topUp') }}</NuxtLink>
                        </div>

                        <p v-if="walletBalance < currentPrice.final" class="error-text">{{
                            $t('admin.subscriptionPage.premium.insufficientFunds') }}</p>
                    </div>
                    <div class="modal-actions">
                        <button class="btn-ghost" @click="showPurchaseModal = false">{{ $t('common.cancel') }}</button>
                        <button class="btn-primary" @click="confirmPurchase"
                            :disabled="loading || walletBalance < currentPrice.final">
                            {{ loading ? '...' : $t('admin.subscriptionPage.premium.payAndActivate') }}
                        </button>
                    </div>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script setup>
definePageMeta({
    layout: 'shop-admin',
    middleware: ['auth', 'shop-owner']
})

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()
const { formatPrice } = useCurrency()
const config = useRuntimeConfig()
const toast = useToast()
const { token } = useAuth()
const shopSlug = route.params.slug
const localePath = useLocalePath()

const loading = ref(false)
const showPurchaseModal = ref(false)
const selectedPlan = ref(null)
const planDurations = ref({})
const walletBalance = ref(0)
const autoRenewalEnabled = ref(true)

// --- Data Fetching ---
const { data: shop, pending: shopPending, refresh: refreshShop } = useFetch(`${config.public.apiBase}/platform/shops/${shopSlug}`, {
    headers: { Authorization: `Bearer ${token.value}` },
    server: false
})

const { data: availablePlans, pending: plansPending } = useFetch(`${config.public.apiBase}/subscription-plans`, {
    headers: { Authorization: `Bearer ${token.value}` },
    server: false
})

const { data: stats, refresh: refreshStats } = useFetch(`${config.public.apiBase}/shop/${shopSlug}/admin/stats`, {
    headers: { Authorization: `Bearer ${token.value}` },
    server: false
})

const fetchWallet = async () => {
    try {
        const data = await $fetch(`${config.public.apiBase}/wallet/balance`, {
            params: { shop_slug: shopSlug },
            headers: { Authorization: `Bearer ${token.value}` }
        })
        walletBalance.value = data.balance
    } catch (e) { }
}

watch(shop, (newVal) => {
    if (newVal) autoRenewalEnabled.value = newVal.auto_renewal_enabled
}, { immediate: true })

onMounted(() => {
    fetchWallet()
})

const pending = computed(() => shopPending.value || plansPending.value)

// --- Business Logic ---
const durations = [
    { months: 1, discount: 0 },
    { months: 3, discount: 10 },
    { months: 6, discount: 20 },
    { months: 12, discount: 30 }
]

const getPlanDuration = (planId) => planDurations.value[planId] || 1
const setPlanDuration = (planId, m) => planDurations.value[planId] = m

const calculatePrice = (plan, durationMonths) => {
    if (!plan) return { total: 0, final: 0, discount: 0 }
    const duration = durations.find(d => d.months === durationMonths) || durations[0]
    const total = plan.price * durationMonths
    const discountAmount = (total * duration.discount) / 100
    return { total, discount: duration.discount, final: total - discountAmount }
}

const currentDuration = computed(() => selectedPlan.value ? getPlanDuration(selectedPlan.value.id) : 1)
const currentPrice = computed(() => calculatePrice(selectedPlan.value, currentDuration.value))

const getLocalizedValue = (obj, key) => obj?.[`${key}_${locale.value}`] || obj?.[key] || ''
const getPlanNameById = (id) => availablePlans.value?.find(p => p.id === id)?.name || 'Plan'
const formatDateString = (d) => new Date(d).toLocaleDateString(locale.value)
const calculatePercent = (val, max) => {
    if (!max || typeof max === 'string') return 0
    return Math.min(100, Math.round((val / max) * 100))
}

const removeActivatedQuery = () => {
    const query = { ...route.query }
    delete query.activated
    router.replace({ query })
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

const initiatePurchase = (plan) => {
    selectedPlan.value = plan
    showPurchaseModal.value = true
}

const confirmPurchase = async () => {
    loading.value = true
    try {
        await $fetch(`${config.public.apiBase}/subscription/purchase`, {
            method: 'POST',
            params: { shop_slug: shopSlug },
            body: { plan_slug: selectedPlan.value.slug, period_months: currentDuration.value, payment_method: 'wallet' },
            headers: { Authorization: `Bearer ${token.value}` }
        })
        toast.success(t('admin.subscriptionPage.premium.successMsg'))
        showPurchaseModal.value = false
        refreshShop(); refreshStats(); fetchWallet();
    } catch (e) {
        toast.error(e.data?.detail || t('admin.subscriptionPage.premium.errorMsg'))
    } finally {
        loading.value = false
    }
}

const toggleAutoRenewal = async () => {
    const next = !autoRenewalEnabled.value
    autoRenewalEnabled.value = next // Optimistic update
    try {
        await $fetch(`${config.public.apiBase}/subscription/auto-renewal`, {
            method: 'PATCH', params: { shop_slug: shopSlug },
            body: { enabled: next }, headers: { Authorization: `Bearer ${token.value}` }
        })
        toast.success(next ? t('admin.subscriptionPage.premium.autoRenew') : t('admin.subscriptionPage.premium.autoRenew'))
    } catch (e) {
        autoRenewalEnabled.value = !next // Revert on error
        toast.error(t('common.error'))
    }
}

const openCancelModal = () => { /* Logic to call cancel sub endpoint */ }
</script>

<style scoped>
.subscription-premium-page {
    padding: 40px;
}

/* Activation Banner */
.activation-welcome {
    background: #111;
    color: white;
    border-radius: 20px;
    padding: 24px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.welcome-content {
    display: flex;
    align-items: center;
    gap: 20px;
}

.welcome-icon {
    font-size: 2.5rem;
}

.welcome-content h2 {
    margin: 0 0 4px 0;
    font-size: 1.5rem;
    font-weight: 800;
}

.welcome-content p {
    margin: 0;
    color: #a1a1aa;
}

.close-welcome {
    background: none;
    border: none;
    color: #52525b;
    cursor: pointer;
    font-size: 1.5rem;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
}

.page-title {
    font-size: 2.25rem;
    font-weight: 900;
    letter-spacing: -1.5px;
    margin: 0;
}

.page-subtitle {
    color: #71717a;
    margin-top: 4px;
}

/* Wallet Pill */
.wallet-pill {
    background: white;
    border: 1.5px solid #E5E7EB;
    border-radius: 100px;
    padding: 8px 8px 8px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s;
}

.wallet-pill:hover {
    border-color: #111;
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.wallet-icon {
    font-size: 1.2rem;
    color: #111;
}

.wallet-details {
    display: flex;
    flex-direction: column;
}

.wallet-details .label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #a1a1aa;
    text-transform: uppercase;
}

.wallet-details .amount {
    font-size: 1.1rem;
    font-weight: 800;
    color: #111;
}

.wallet-add {
    width: 36px;
    height: 36px;
    background: #111;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Content Grid */
.overview-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 32px;
    margin-bottom: 48px;
}

.card {
    background: white;
    border-radius: 24px;
    border: 1.5px solid #E5E7EB;
    padding: 32px;
}

/* Current Plan Card */
.current-plan-card.active {
    border-color: #4ade80;
    background: #f0fdf4;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}

.current-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: #71717a;
    text-transform: uppercase;
}

.current-name {
    font-size: 2rem;
    font-weight: 900;
    margin: 4px 0 0 0;
}

.status-pill {
    padding: 6px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-pill.active {
    background: #dcfce7;
    color: #15803d;
}

.status-pill.trial {
    background: #fef9c3;
    color: #a16207;
}

.status-pill.expired {
    background: #fee2e2;
    color: #b91c1c;
}

.status-pill .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
}

.expiry-info {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #52525b;
    font-size: 0.95rem;
    margin-bottom: 20px;
}

.auto-renew-toggle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background: rgba(0, 0, 0, 0.03);
    border-radius: 16px;
    cursor: pointer;
}

.toggle-title {
    font-weight: 700;
    display: block;
}

.toggle-desc {
    font-size: 0.8rem;
    color: #71717a;
}

.toggle-switch {
    width: 44px;
    height: 24px;
    background: #e5e7eb;
    border-radius: 100px;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toggle-switch.active {
    background: #111;
}

.toggle-dot {
    width: 18px;
    height: 18px;
    background: white;
    border-radius: 50%;
    position: absolute;
    top: 3px;
    left: 3px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.active .toggle-dot {
    transform: translateX(20px);
}

/* Stats Card */
.stats-title {
    margin: 0 0 24px 0;
    font-size: 1.25rem;
    font-weight: 800;
}

.stat-row {
    margin-bottom: 20px;
}

.stat-info {
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 10px;
}

.stat-count {
    color: #111;
}

.progress-box {
    height: 10px;
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #f1f5f9;
}

.progress-fill {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background: linear-gradient(90deg, #111, #333);
    border-radius: 10px;
    transition: width 0.8s cubic-bezier(0.65, 0, 0.35, 1);
}

/* Plans Section */
.section-title {
    font-size: 1.75rem;
    font-weight: 900;
    margin: 0 0 32px 0;
}

.plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
}

.plan-item {
    background: white;
    border: 1.5px solid #E5E7EB;
    border-radius: 24px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    transition: 0.3s;
}

.plan-item.highlight {
    border-color: #111;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.plan-item.current {
    background: #f8fafc;
    border-style: dashed;
}

.plan-item-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
}

.name-status {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.badge-current {
    font-size: 0.65rem;
    font-weight: 800;
    background: #e2e8f0;
    color: #475569;
    padding: 2px 8px;
    border-radius: 100px;
    text-transform: uppercase;
    width: fit-content;
}

.plan-item-header .name {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0;
}

.plan-item-header .price {
    display: flex;
    align-items: baseline;
    gap: 4px;
}

.plan-item-header .val {
    font-size: 1.25rem;
    font-weight: 900;
}

.plan-item-header .mo {
    font-size: 0.8rem;
    color: #a1a1aa;
}

.plan-item .desc {
    color: #71717a;
    font-size: 0.9rem;
    margin-bottom: 24px;
    min-height: 44px;
}

/* Plan Limits List */
.plan-limits {
    list-style: none;
    padding: 0;
    margin: 0 0 32px 0;
    border-top: 1px solid #f1f5f9;
    padding-top: 24px;
}

.plan-limits li {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
    color: #334155;
    font-weight: 600;
    font-size: 0.95rem;
}

.plan-limits li iconify-icon {
    color: #111;
    font-size: 1.2rem;
}

.duration-selector label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 10px;
    display: block;
}

.duration-chips {
    display: flex;
    background: #F1F5F9;
    padding: 6px;
    border-radius: 20px;
    gap: 4px;
    margin-bottom: 24px;
    border: 1px solid #E2E8F0;
}

.chip {
    flex: 1;
    height: 48px;
    border: none;
    background: transparent;
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    z-index: 1;
}

.chip.active {
    background: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    color: #111;
}

.chip:not(.active):hover {
    background: rgba(255, 255, 255, 0.5);
}

.months-val {
    font-size: 0.85rem;
    font-weight: 800;
    color: inherit;
}

.disc-badge {
    font-size: 0.6rem;
    font-weight: 900;
    color: #10B981;
    background: #DCFCE7;
    padding: 1px 5px;
    border-radius: 5px;
    margin-top: 1px;
}

.active .disc-badge {
    background: #10B981;
    color: white;
}

.chip:not(.active) .months-val {
    color: #64748B;
}

.total-calc {
    padding-top: 18px;
    border-top: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.total-calc .label {
    font-weight: 700;
    color: #64748b;
}

.total-calc .total-val {
    font-size: 1.35rem;
    font-weight: 900;
    color: #111;
}

.btn-select-plan {
    height: 52px;
    border-radius: 16px;
    border: 2px solid #111;
    background: white;
    font-weight: 800;
    cursor: pointer;
    transition: 0.2s;
}

.btn-select-plan:hover {
    background: #111;
    color: white;
}

.highlight .btn-select-plan {
    background: #111;
    color: white;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(8px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-card {
    background: white;
    border-radius: 32px;
    width: 100%;
    max-width: 480px;
    padding: 40px;
    margin: 20px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 24px;
}

.modal-header h2 {
    font-size: 1.75rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
}

.close-modal {
    background: none;
    border: none;
    color: #cbd5e1;
    cursor: pointer;
    font-size: 1.5rem;
    transition: 0.2s;
}

.close-modal:hover {
    color: #111;
}

.summary-box {
    background: #f8fafc;
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 28px;
    border: 1px solid #f1f5f9;
}

.summary-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 14px;
    font-weight: 600;
}

.summary-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 20px 0;
}

.summary-line.total .total-price {
    font-size: 1.75rem;
    font-weight: 950;
}

.payment-method-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 2px solid #f1f5f9;
    border-radius: 20px;
    padding: 20px;
    transition: 0.2s;
}

.payment-method-box.error {
    border-color: #fee2e2;
    background: #fffafb;
}

.p-info {
    display: flex;
    gap: 16px;
    align-items: center;
}

.p-icon {
    font-size: 1.5rem;
    color: #111;
}

.p-label {
    font-weight: 800;
    display: block;
    font-size: 0.95rem;
}

.p-balance {
    font-size: 0.85rem;
    font-weight: 700;
    color: #059669;
}

.p-balance.low {
    color: #dc2626;
}

.top-up-link {
    color: #111;
    font-weight: 900;
    font-size: 0.9rem;
    text-decoration: underline;
}

.error-text {
    color: #dc2626;
    font-size: 0.85rem;
    font-weight: 700;
    margin-top: 14px;
    text-align: center;
}

.modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 36px;
}

.modal-actions .btn-primary {
    flex: 1.6;
}

.modal-actions .btn-ghost {
    flex: 1;
}

.btn-primary {
    height: 56px;
    background: #111;
    color: white;
    border: none;
    border-radius: 16px;
    font-weight: 800;
    cursor: pointer;
    font-size: 1rem;
    transition: 0.2s;
}

.btn-primary:active {
    transform: scale(0.98);
}

.btn-ghost {
    height: 56px;
    background: #f1f5f9;
    color: #1e293b;
    border: none;
    border-radius: 16px;
    font-weight: 700;
    cursor: pointer;
    font-size: 1rem;
}

/* Responsive Viewports */
@media (max-width: 1024px) {
    .overview-grid {
        grid-template-columns: 1fr;
        gap: 24px;
    }

    .subscription-premium-page {
        padding: 20px;
    }
}

@media (max-width: 640px) {
    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 20px;
    }

    .wallet-pill {
        width: 100%;
        padding: 12px 18px;
        border-radius: 24px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
    }

    .wallet-details .amount {
        font-size: 1.25rem;
    }

    .current-name {
        font-size: 1.75rem;
    }

    .card {
        padding: 24px;
        border-radius: 28px;
    }

    .plans-grid {
        grid-template-columns: 1fr;
    }

    .plan-item {
        padding: 28px;
        border-radius: 28px;
    }

    .duration-chips {
        flex-wrap: wrap;
    }

    .chip {
        min-width: calc(50% - 4px);
    }

    .modal-card {
        padding: 28px;
        border-radius: 40px;
    }
}

.text-muted {
    opacity: 0.4;
}
</style>
