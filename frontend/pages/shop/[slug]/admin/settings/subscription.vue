<template>
    <div class="subscription-page">
        <div class="page-header">
            <h1 class="page-title">{{ $t('shopSettings.subscription.title') }}</h1>
            <p class="page-subtitle">{{ $t('shopSettings.subscription.subtitle') }}</p>
        </div>

        <!-- Error State -->
        <div v-if="error" class="error-state">
            <p>{{ $t('alerts.shop.errorLoadingData') }}</p>
            <button @click="retryFetch" class="btn-secondary">{{ $t('common.retry') }}</button>
        </div>

        <div v-if="pending" class="loading-state">
            <div class="spinner"></div>
        </div>

        <div v-else class="content-grid">
            <!-- Inactive/Expired Warning -->
            <div v-if="!shop?.is_active || shop?.subscription_status === 'expired' || (shop?.subscription_expires_at && new Date(shop.subscription_expires_at) < new Date())"
                class="expiry-warning-banner">
                <div class="warning-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path
                            d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z">
                        </path>
                        <line x1="12" y1="9" x2="12" y2="13"></line>
                        <line x1="12" y1="17" x2="12.01" y2="17"></line>
                    </svg>
                </div>
                <div class="warning-text">
                    <h3>{{ !shop?.is_active ? $t('shopSettings.subscription.shopInactive') || 'Shop Deactivated' :
                        $t('shopSettings.subscription.expiredTitle') || 'Subscription Expired' }}</h3>
                    <p>{{ !shop?.is_active ? $t('shopSettings.subscription.contactSupport') || 'Your shop has been
                        deactivated by the administrator.Please contact support.' :
                    $t('shopSettings.subscription.expiredDesc') || 'Your subscription has ended. Please choose a
                        plan below to reactive your shop and continue selling.' }}</p>
                </div>
            </div>

            <!-- Current Subscription Card -->
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

                <!-- Active Request Banner -->
                <div v-if="subscriptionRequest && subscriptionRequest.status === 'pending'" class="request-banner">
                    <div class="banner-content">
                        <h3>{{ $t('shopSettings.subscription.pendingTitle') }}</h3>
                        <p>{{ $t('shopSettings.subscription.pendingDesc', { plan: subscriptionRequest.plan_name }) }}
                        </p>
                        <p class="text-sm text-gray-500 mt-1">
                            {{ $t('shopSettings.subscription.duration') }}: {{ subscriptionRequest.duration_months }} {{
                                getMonthsLabel(subscriptionRequest.duration_months) }}
                        </p>
                    </div>
                    <div class="banner-status">Pending</div>
                </div>

                <div class="usage-stats">
                    <!-- Products Limit -->
                    <div class="stat-item">
                        <div class="stat-header">
                            <span class="stat-label">{{ $t('shopSettings.subscription.products') }}</span>
                            <span class="stat-value">
                                {{ stats?.total_products || 0 }} / {{ stats?.plan_limit_products || '∞' }}
                            </span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress" :style="{ width: (stats?.products_usage_percent || 0) + '%' }"
                                :class="{ 'over-limit': (stats?.products_usage_percent || 0) >= 100 }"></div>
                        </div>
                    </div>

                    <!-- Banners Limit -->
                    <div class="stat-item">
                        <div class="stat-header">
                            <span class="stat-label">{{ $t('platformAdmin.plans.form.maxBanners') }}</span>
                            <span class="stat-value">
                                {{ stats?.total_banners || 0 }} / {{ stats?.plan_limit_banners || 1 }}
                            </span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress" :style="{ width: (stats?.banners_usage_percent || 0) + '%' }"
                                :class="{ 'over-limit': (stats?.banners_usage_percent || 0) >= 100 }"></div>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="plan-actions" v-if="shop?.subscription_status === 'active'">
                    <button @click="openRenewModal" class="btn-primary-outline">
                        {{ $t('shopSettings.subscription.renewTitle') }}
                    </button>
                    <button @click="openCancelModal" class="btn-danger-text">
                        Cancel Subscription
                    </button>
                </div>
            </div>

            <!-- Plans Grid (Available Plans) -->
            <div v-if="shop?.subscription_status !== 'active' && availablePlans?.length > 0" class="plans-section">
                <h2 class="section-title">{{ $t('shopSettings.subscription.plans') }}</h2>
                <div class="plans-grid">
                    <div v-for="plan in availablePlans" :key="plan.id" class="plan-card"
                        :class="{ 'featured': plan.slug === 'pro' }">
                        <div class="plan-header">
                            <h3 class="plan-name">{{ getLocalizedValue(plan, 'name') }}</h3>
                            <div class="plan-price">
                                <span class="amount" v-if="plan.price > 0">${{ plan.price }}</span>
                                <span class="amount" v-else>Free</span>
                                <span class="period" v-if="plan.price > 0">/ {{ $t('shopSettings.subscription.month')
                                }}</span>
                            </div>
                        </div>

                        <div class="plan-desc">{{ getLocalizedValue(plan, 'description') }}</div>

                        <ul class="plan-features">
                            <li v-for="(feature, idx) in getLocalizedFeatures(plan)" :key="idx">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                {{ feature }}
                            </li>
                        </ul>

                        <!-- Duration Selector -->
                        <div v-if="plan.price > 0" class="duration-selector">
                            <div class="duration-options">
                                <button v-for="duration in durations" :key="duration.months"
                                    @click="setPlanDuration(plan.id, duration.months)" class="duration-chip"
                                    :class="{ active: getPlanDuration(plan.id) === duration.months }">
                                    {{ duration.label }}
                                </button>
                            </div>
                            <div class="price-calc">
                                Total: ${{ calculatePrice(plan, getPlanDuration(plan.id)).final.toFixed(2) }}
                            </div>
                        </div>

                        <button class="plan-btn" :class="{ 'primary': plan.slug === 'pro' }" @click="requestPlan(plan)"
                            :disabled="loading || subscriptionRequest?.status === 'pending'">
                            {{ loading && selectedPlan?.id === plan.id ? 'Sending...' :
                                $t('shopSettings.subscription.select') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Renew Modal -->
        <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
            <div class="modal-content">
                <h2>{{ modalMode === 'renew' ? $t('shopSettings.subscription.renewTitle') :
                    $t('shopSettings.subscription.changeTitle') }}</h2>

                <div class="modal-body">
                    <div class="form-group">
                        <label>{{ $t('shopSettings.subscription.plans') }}</label>
                        <select v-model="renewForm.plan_id" class="form-input">
                            <option v-for="plan in availablePlans?.filter(p => !p.is_trial)" :key="plan.id"
                                :value="plan.id">
                                {{ getLocalizedValue(plan, 'name') }} - ${{ plan.price }}/mo
                            </option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>{{ $t('shopSettings.subscription.duration') }}</label>
                        <div class="duration-grid-modal">
                            <button v-for="duration in durations" :key="duration.months"
                                @click="renewForm.duration_months = duration.months" class="duration-btn-modal"
                                :class="{ active: renewForm.duration_months === duration.months }">
                                {{ duration.label }}
                                <span v-if="duration.discount > 0" class="discount-pill">-{{ duration.discount
                                }}%</span>
                            </button>
                        </div>
                    </div>

                    <div class="price-summary" v-if="renewForm.plan_id">
                        <div class="summary-row total">
                            <span>Total:</span>
                            <span>${{ getRenewTotalPrice().final.toFixed(2) }}</span>
                        </div>
                    </div>
                </div>

                <div class="modal-actions">
                    <button class="btn-cancel" @click="closeModal">{{ $t('common.cancel') }}</button>
                    <button class="btn-confirm" @click="submitRequest" :disabled="loading">
                        {{ loading ? '...' : $t('common.confirm') }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Cancel Modal -->
        <div v-if="showCancelModal" class="modal-overlay" @click.self="showCancelModal = false">
            <div class="modal-content">
                <h2>Cancel Subscription</h2>
                <p>Are you sure you want to cancel your subscription?</p>
                <div class="modal-actions">
                    <button class="btn-cancel" @click="showCancelModal = false">No, Keep it</button>
                    <button class="btn-danger" @click="cancelSubscription" :disabled="loading">Yes, Cancel</button>
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
const { t, locale } = useI18n()
const config = useRuntimeConfig()
const toast = useToast()
const { token } = useAuth()
const shopSlug = route.params.slug

const loading = ref(false)
const showModal = ref(false)
const showCancelModal = ref(false)
const modalMode = ref('new')
const selectedPlan = ref(null)
const planDurations = ref({})

const renewForm = reactive({
    plan_id: null,
    duration_months: 1
})

// --- Data Fetching ---

const { data: shop, pending: shopPending, refresh: refreshShop, error: shopError } = await useFetch(`${config.public.apiBase}/platform/shops/${shopSlug}`, {
    headers: { Authorization: `Bearer ${token.value}` }
})

const { data: availablePlans, pending: plansPending, error: plansError } = await useFetch(`${config.public.apiBase}/subscription-plans`, {
    headers: { Authorization: `Bearer ${token.value}` }
})

const { data: stats, pending: statsPending, refresh: refreshStats } = await useFetch(`${config.public.apiBase}/shop/${shopSlug}/admin/stats`, {
    headers: { Authorization: `Bearer ${token.value}` }
})

// Subscription Requests
const subscriptionRequest = ref(null)

const fetchSubscriptionRequest = async () => {
    try {
        const request = await $fetch(`${config.public.apiBase}/shop/${shopSlug}/subscription/request`, {
            headers: { Authorization: `Bearer ${token.value}` }
        })
        subscriptionRequest.value = request
    } catch (e) {
        subscriptionRequest.value = null
    }
}

// Initial load
await fetchSubscriptionRequest()

// Composite loading/error state
const pending = computed(() => shopPending.value || plansPending.value || statsPending.value)
const error = computed(() => shopError.value || plansError.value)

const retryFetch = () => {
    refreshShop()
    refreshStats()
    fetchSubscriptionRequest()
}

// --- Helpers ---

const getLocalizedValue = (obj, key) => {
    const current = locale.value
    if (current === 'ru' && obj[key + '_ru']) return obj[key + '_ru']
    if (current === 'en' && obj[key + '_en']) return obj[key + '_en']
    if (current === 'uz' && obj[key + '_uz']) return obj[key + '_uz']
    return obj[key] || ''
}

const getLocalizedFeatures = (plan) => {
    const current = locale.value
    let featuresStr = plan.features // default
    if (current === 'ru' && plan.features_ru) featuresStr = plan.features_ru
    if (current === 'en' && plan.features_en) featuresStr = plan.features_en
    if (current === 'uz' && plan.features_uz) featuresStr = plan.features_uz

    if (!featuresStr) return []
    return featuresStr.split(',')
}

const formatDate = (date) => new Date(date).toLocaleDateString(locale.value)

const getStatusText = (status) => {
    const map = {
        active: t('admin.status.active'),
        trial: t('admin.status.trial'),
        expired: t('admin.status.expired'),
        cancelled: t('admin.status.cancelled')
    }
    return map[status] || status
}

const durations = computed(() => [
    { months: 1, label: `1 ${t('shopSettings.subscription.month')}`, discount: 0 },
    { months: 3, label: `3 ${t('shopSettings.subscription.months')}`, discount: 5 },
    { months: 6, label: `6 ${t('shopSettings.subscription.months')}`, discount: 10 },
    { months: 12, label: `12 ${t('shopSettings.subscription.months')}`, discount: 15 }
])

const getMonthsLabel = (months) => {
    if (months === 1) return t('shopSettings.subscription.month')
    return t('shopSettings.subscription.months')
}

// --- Duration Logic ---

const getPlanDuration = (planId) => planDurations.value[planId] || 1
const setPlanDuration = (planId, m) => planDurations.value[planId] = m

const calculatePrice = (plan, durationMonths) => {
    const duration = durations.value.find(d => d.months === durationMonths) || durations.value[0]
    const discount = duration.discount
    const total = plan.price * durationMonths
    const discountAmount = (total * discount) / 100
    return {
        total,
        discount,
        discountAmount,
        final: total - discountAmount
    }
}

// --- Actions ---

const requestPlan = async (plan) => {
    if (subscriptionRequest.value?.status === 'pending') {
        toast.warning(t('alerts.shop.requestTheSame'))
        return
    }

    loading.value = true
    selectedPlan.value = plan
    try {
        const duration = getPlanDuration(plan.id)
        await $fetch(`${config.public.apiBase}/shop/${shopSlug}/subscription/request`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${token.value}` },
            body: {
                plan_id: plan.id,
                duration_months: duration,
                type: 'new'
            }
        })
        toast.success(t('shopSettings.subscription.requestSent'))
        await fetchSubscriptionRequest()
    } catch (e) {
        toast.error(e.data?.detail || 'Error')
    } finally {
        loading.value = false
    }
}

const openRenewModal = () => {
    if (availablePlans.value?.length) {
        renewForm.plan_id = shop.value.subscription_plan_id || availablePlans.value[0].id
    }
    modalMode.value = 'renew'
    showModal.value = true
}

const closeModal = () => {
    showModal.value = false
}

const getRenewTotalPrice = () => {
    if (!renewForm.plan_id || !availablePlans.value) return { final: 0 }
    const plan = availablePlans.value.find(p => p.id === renewForm.plan_id)
    if (!plan) return { final: 0 }
    return calculatePrice(plan, renewForm.duration_months)
}

const submitRequest = async () => {
    loading.value = true
    try {
        await $fetch(`${config.public.apiBase}/shop/${shopSlug}/subscription/request`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${token.value}` },
            body: {
                plan_id: renewForm.plan_id,
                duration_months: renewForm.duration_months,
                type: modalMode.value
            }
        })
        toast.success(t('shopSettings.subscription.requestSent'))
        closeModal()
        await fetchSubscriptionRequest()
    } catch (e) {
        toast.error(e.data?.detail || 'Error')
    } finally {
        loading.value = false
    }
}

const openCancelModal = () => showCancelModal.value = true

const cancelSubscription = async () => {
    loading.value = true
    try {
        await $fetch(`${config.public.apiBase}/shop/${shopSlug}/subscription/cancel`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${token.value}` }
        })
        toast.success('Subscription cancelled')
        showCancelModal.value = false
        refreshShop()
    } catch (e) {
        toast.error(e.data?.detail || 'Error')
    } finally {
        loading.value = false
    }
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

.plan-header {
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
    text-transform: capitalize;
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
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 24px;
}

.stat-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #374151;
}

.progress-bar {
    height: 8px;
    background: #F3F4F6;
    border-radius: 4px;
    overflow: hidden;
}

.progress {
    height: 100%;
    background: #111;
    border-radius: 4px;
    transition: width 0.3s ease;
}

.progress.over-limit {
    background: #EF4444;
}

.plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

.plan-card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid #E5E7EB;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s;
}

.plan-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.plan-card.featured {
    border: 2px solid #111;
}

.plan-name {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.plan-price {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 16px;
}

.plan-desc {
    color: #6B7280;
    margin-bottom: 16px;
    font-size: 0.9rem;
}

.plan-features {
    list-style: none;
    padding: 0;
    margin: 0 0 24px 0;
    flex-grow: 1;
}

.plan-features li {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #4B5563;
}

.plan-btn {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    background: #F3F4F6;
    border: none;
    margin-top: 16px;
}

.plan-btn.primary {
    background: #111;
    color: white;
}

.plan-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.duration-selector {
    background: #F9FAFB;
    padding: 12px;
    border-radius: 12px;
    margin-top: auto;
}

.duration-options {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 8px;
}

.duration-chip {
    padding: 4px 12px;
    border-radius: 100px;
    border: 1px solid #E5E7EB;
    background: white;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
}

.duration-chip.active {
    background: #111;
    color: white;
    border-color: #111;
}

.price-calc {
    font-size: 0.9rem;
    font-weight: 700;
    text-align: right;
}

.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 32px;
    border-radius: 20px;
    width: 90%;
    max-width: 450px;
}

.modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
}

.btn-primary-outline,
.btn-danger-text,
.btn-confirm,
.btn-cancel,
.btn-danger {
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
}

.btn-primary-outline {
    background: white;
    border: 1px solid #111;
    color: #111;
}

.btn-danger-text {
    background: none;
    border: none;
    color: #EF4444;
}

.btn-confirm {
    background: #111;
    color: white;
    border: none;
    flex: 1;
}

.btn-cancel {
    background: #F3F4F6;
    border: none;
    flex: 1;
}

.btn-danger {
    background: #EF4444;
    color: white;
    border: none;
    flex: 1;
}

.request-banner {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.duration-grid-modal {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}

.duration-btn-modal {
    padding: 12px;
    border: 1px solid #E5E7EB;
    background: white;
    border-radius: 8px;
    cursor: pointer;
    text-align: center;
}

.duration-btn-modal.active {
    background: #111;
    color: white;
    border-color: #111;
}

.form-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    margin-top: 4px;
}

.expiry-warning-banner {
    display: flex;
    gap: 16px;
    background: #FEF2F2;
    border: 1px solid #FEE2E2;
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 32px;
}

.warning-icon {
    flex-shrink: 0;
    color: #EF4444;
}

.warning-text h3 {
    margin: 0 0 4px 0;
    font-size: 1.125rem;
    font-weight: 800;
    color: #991B1B;
}

.warning-text p {
    margin: 0;
    font-size: 0.95rem;
    color: #B91C1C;
    line-height: 1.5;
}
</style>
