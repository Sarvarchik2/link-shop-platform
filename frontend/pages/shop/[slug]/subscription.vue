<template>
  <div class="subscription-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">{{ $t('admin.subscriptionPage.title') }}</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" current-route="subscription" v-model="sidebarOpen" />

    <main class="admin-main">
      <!-- <div class="container"> -->
      <div class="page-header">
        <h1 class="page-title">{{ $t('admin.subscriptionPage.pageTitle') }}</h1>
        <p class="page-subtitle">{{ $t('admin.subscriptionPage.pageSubtitle') }}</p>
      </div>

      <div v-if="pending" class="loading-container">
        <div class="loading-spinner"></div>
        <p>{{ $t('common.loading') }}</p>
      </div>

      <div v-else-if="shop">
        <!-- Current Subscription Card -->
        <div class="current-subscription-card">
          <div class="card-header-row">
            <h2 class="card-title">{{ $t('admin.subscriptionPage.current') }}</h2>
            <div class="subscription-status-badge" :class="getStatusClass(shop.subscription_status)">
              {{ getStatusText(shop.subscription_status) }}
            </div>
          </div>

          <!-- Active Subscription Request -->
          <div v-if="subscriptionRequest && subscriptionRequest.status === 'pending'" class="request-alert">
            <div class="alert-icon">⏳</div>
            <div class="alert-content">
              <h3 class="alert-title">{{ $t('admin.subscriptionPage.requestPending') }}</h3>
              <p class="alert-details">
                {{ $t('admin.subscriptionPage.labels.plan') }}: <strong>{{ subscriptionRequest.plan_name }}</strong> •
                {{ $t('admin.subscriptionPage.labels.duration') }}: <strong>{{ subscriptionRequest.duration_months }} {{
                  getMonthsLabel(subscriptionRequest.duration_months) }}</strong> •
                {{ $t('admin.subscriptionPage.labels.sent') }}: {{ formatDate(subscriptionRequest.requested_at) }}
              </p>
              <p class="alert-info mt-2 text-sm text-green-700">
                {{ $t('admin.subscriptionPage.requestNote') }}
              </p>
              <p v-if="subscriptionRequest.notes" class="alert-notes">{{ subscriptionRequest.notes }}</p>
            </div>
          </div>

          <!-- Subscription Info Grid -->
          <div class="info-grid">
            <div class="info-box">
              <div class="info-label">{{ $t('admin.subscriptionPage.labels.plan') }}</div>
              <div class="info-value">{{ getCurrentPlanId() }}</div>
            </div>

            <div class="info-box">
              <div class="info-label">{{ $t('admin.subscriptionPage.labels.price') }}</div>
              <div class="info-value">{{ getPlanPrice(shop.subscription_status) }}</div>
            </div>

            <div class="info-box" v-if="shop.subscription_expires_at">
              <div class="info-label">{{ $t('admin.subscriptionPage.labels.expires') }}</div>
              <div class="info-value">{{ formatDate(shop.subscription_expires_at) }}</div>
            </div>

            <div class="info-box" v-if="shop.subscription_expires_at">
              <div class="info-label">{{ $t('admin.subscriptionPage.labels.daysLeft') }}</div>
              <div class="info-value" :class="getDaysLeftClass(shop.subscription_expires_at)">
                {{ getDaysLeft(shop.subscription_expires_at) }}
              </div>
            </div>

            <div class="info-box">
              <div class="info-label">{{ $t('admin.subscriptionPage.labels.products') }}</div>
              <div class="info-value">
                {{ getProductStats().current }} <span class="text-sm font-normal text-gray-500">/ {{
                  getProductStats().limit }}</span>
              </div>
              <div class="usage-bar">
                <div class="usage-fill" :style="{ width: getProductStats().percent + '%' }"
                  :class="{ 'over-limit': getProductStats().percent >= 100 }"></div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons" v-if="shop.subscription_status === 'active'">
            <button @click="showRenewModal = true" class="btn-renew" :disabled="loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10"></polyline>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
              </svg>
              {{ $t('admin.subscriptionPage.actions.renew') }}
            </button>
            <button @click="showCancelModal = true" class="btn-cancel" :disabled="loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
              {{ $t('admin.subscriptionPage.actions.cancel') }}
            </button>
          </div>
        </div>

        <!-- Available Plans (only if not active) -->
        <div v-if="shop.subscription_status !== 'active' && availablePlans && availablePlans.length > 0"
          class="plans-section">
          <h2 class="section-title">{{ $t('admin.subscriptionPage.availablePlans') }}</h2>
          <p class="section-description">{{ $t('admin.subscriptionPage.availablePlansDesc') }}</p>

          <div class="plans-grid">
            <div v-for="plan in availablePlans" :key="plan.id" class="plan-card"
              :class="{ 'plan-featured': plan.slug === 'basic' }">
              <div v-if="plan.slug === 'basic'" class="plan-badge">{{ $t('admin.subscriptionPage.popular') }}</div>

              <div class="plan-header">
                <h3 class="plan-name">{{ plan.name }}</h3>
                <div class="plan-price">
                  <span class="price-amount">${{ plan.price }}</span>
                  <span class="price-period">{{ $t('admin.subscriptionPage.month') }}</span>
                </div>
              </div>

              <p class="plan-description">{{ plan.description }}</p>

              <!-- Duration Selection -->
              <div v-if="!plan.is_trial && plan.price > 0" class="duration-selector">
                <label class="duration-label">{{ $t('admin.subscriptionPage.selectDuration') }}</label>
                <div class="duration-grid">
                  <button v-for="duration in durations" :key="duration.months"
                    @click="setPlanDuration(plan.id, duration.months)" class="duration-btn"
                    :class="{ active: getPlanDuration(plan.id) === duration.months }">
                    {{ duration.label }}
                    <span v-if="duration.discount > 0" class="discount-badge">-{{ duration.discount }}%</span>
                  </button>
                </div>

                <div class="price-summary">
                  <div class="summary-row">
                    <span>{{ $t('admin.subscriptionPage.priceFor', {
                      duration: getPlanDuration(plan.id), unit:
                        getMonthsLabel(getPlanDuration(plan.id))
                    }) }}</span>
                    <span>${{ calculatePrice(plan, getPlanDuration(plan.id)).total.toFixed(2) }}</span>
                  </div>
                  <div v-if="calculatePrice(plan, getPlanDuration(plan.id)).discount > 0" class="summary-row discount">
                    <span>{{ $t('admin.subscriptionPage.discount') }} {{ calculatePrice(plan,
                      getPlanDuration(plan.id)).discount }}%:</span>
                    <span>-${{ calculatePrice(plan, getPlanDuration(plan.id)).discountAmount.toFixed(2) }}</span>
                  </div>
                  <div class="summary-row total">
                    <span><strong>{{ $t('admin.subscriptionPage.total') }}</strong></span>
                    <span><strong>${{ calculatePrice(plan, getPlanDuration(plan.id)).final.toFixed(2)
                        }}</strong></span>
                  </div>
                </div>
              </div>

              <ul class="plan-features" v-if="plan.features_list && plan.features_list.length > 0">
                <li v-for="(feature, index) in plan.features_list" :key="index">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  {{ feature }}
                </li>
              </ul>

              <button @click="requestPlan(plan)" class="plan-button"
                :disabled="loading || subscriptionRequest?.status === 'pending'">
                {{ loading && selectedPlan?.id === plan.id ? $t('admin.subscriptionPage.actions.sending') :
                  subscriptionRequest?.status === 'pending'
                    ? $t('admin.subscriptionPage.requestSent') : $t('admin.plans.card.active') }}
              </button>
            </div>
          </div>
        </div>

        <!-- Offers Section -->
        <div v-if="offers && offers.length > 0" class="offers-section">
          <h2 class="section-title">{{ $t('admin.subscriptionPage.specialOffers') }}</h2>
          <p class="section-description">{{ $t('admin.subscriptionPage.specialOffersDesc') }}</p>

          <div class="offers-grid">
            <div v-for="offer in offers" :key="offer.id" class="offer-card">
              <div class="offer-header">
                <h3 class="offer-title">{{ offer.title }}</h3>
                <div class="offer-price">{{ offer.price_text || `$${offer.price}` }}</div>
              </div>
              <p class="offer-description">{{ offer.description }}</p>
              <p class="offer-contact">{{ offer.contact_text }}</p>
              <div class="offer-actions">
                <a v-if="offer.contact_email" :href="`mailto:${offer.contact_email}`" class="offer-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                    <polyline points="22,6 12,13 2,6"></polyline>
                  </svg>
                  {{ $t('admin.subscriptionPage.contact.email') }}
                </a>
                <a v-if="offer.contact_phone" :href="`tel:${offer.contact_phone}`" class="offer-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path
                      d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                    </path>
                  </svg>
                  {{ $t('admin.subscriptionPage.contact.call') }}
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Important Information -->
        <div class="info-section">
          <h3 class="info-title">{{ $t('admin.subscriptionPage.importantInfo') }}</h3>
          <ul class="info-list">
            <li>ℹ️ {{ $t('admin.subscriptionPage.infoList.trial') }}</li>
            <li>ℹ️ {{ $t('admin.subscriptionPage.infoList.suspension') }}</li>
            <li>ℹ️ {{ $t('admin.subscriptionPage.infoList.activation') }}</li>
            <li>ℹ️ {{ $t('admin.subscriptionPage.infoList.payment') }}</li>
            <li>ℹ️ {{ $t('admin.subscriptionPage.infoList.renewal') }}</li>
          </ul>
        </div>
      </div>
    </main>

    <!-- Renew Modal -->
    <div v-if="showRenewModal" class="modal-overlay" @click="showRenewModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ $t('admin.subscriptionPage.modals.renewTitle') }}</h2>
          <button @click="showRenewModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <p>{{ $t('admin.subscriptionPage.modals.renewDesc') }}</p>

          <div class="form-group">
            <label>{{ $t('admin.subscriptionPage.modals.selectPlan') }}</label>
            <select v-model="renewForm.plan_id" class="form-input">
              <option v-for="plan in availablePlans?.filter(p => !p.is_trial)" :key="plan.id" :value="plan.id">
                {{ plan.name }} - ${{ plan.price }}/{{ $t('admin.subscriptionPage.months.one') }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Длительность</label>
            <div class="duration-grid-modal">
              <button v-for="duration in durations" :key="duration.months"
                @click="renewForm.duration_months = duration.months" class="duration-btn-modal"
                :class="{ active: renewForm.duration_months === duration.months }" type="button">
                {{ duration.label }}
                <span v-if="duration.discount > 0" class="discount-badge">-{{ duration.discount }}%</span>
              </button>
            </div>
          </div>

          <!-- Price Summary -->
          <div v-if="renewForm.plan_id" class="modal-price-summary">
            <div class="summary-row">
              <span>{{ getSelectedPlanName() }} × {{ renewForm.duration_months }} {{
                getMonthsLabel(renewForm.duration_months) }}</span>
              <span>${{ getRenewTotalPrice().total.toFixed(2) }}</span>
            </div>
            <div v-if="getRenewTotalPrice().discount > 0" class="summary-row discount">
              <span>{{ $t('admin.subscriptionPage.discount') }} {{ getRenewTotalPrice().discount }}%</span>
              <span>-${{ getRenewTotalPrice().discountAmount.toFixed(2) }}</span>
            </div>
            <div class="summary-row total">
              <span><strong>{{ $t('admin.subscriptionPage.modals.total') }}</strong></span>
              <span><strong>${{ getRenewTotalPrice().final.toFixed(2) }}</strong></span>
            </div>
            <div v-if="getRenewTotalPrice().savings > 0" class="savings-note">
              💰 {{ $t('admin.subscriptionPage.modals.savings') }} ${{ getRenewTotalPrice().savings.toFixed(2) }}
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showRenewModal = false" class="btn-secondary">{{ $t('platformAdmin.plans.cancel') }}</button>
          <button @click="renewSubscription" class="btn-primary" :disabled="loading">
            {{ loading ? $t('admin.subscriptionPage.actions.sending') : $t('admin.subscriptionPage.modals.sendRequest')
            }}
          </button>
        </div>
      </div>
    </div>

    <!-- Cancel Modal -->
    <div v-if="showCancelModal" class="modal-overlay" @click="showCancelModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ $t('admin.subscriptionPage.modals.cancelTitle') }}</h2>
          <button @click="showCancelModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <p class="warning-text">⚠️ {{ $t('admin.subscriptionPage.modals.cancelConfirm') }}</p>
          <p>{{ $t('admin.subscriptionPage.modals.cancelWarning') }}</p>

          <div class="form-group">
            <label>{{ $t('admin.subscriptionPage.modals.reason') }}</label>
            <textarea v-model="cancelReason" rows="3" class="form-input"
              :placeholder="$t('admin.subscriptionPage.modals.reasonPlaceholder')"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCancelModal = false" class="btn-secondary">{{ $t('platformAdmin.plans.cancel') }}</button>
          <button @click="cancelSubscription" class="btn-danger" :disabled="loading">
            {{ loading ? $t('common.loading') : $t('admin.subscriptionPage.modals.confirmCancel') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth', 'shop-owner']
})

const route = useRoute()
const shopSlug = route.params.slug
const { token } = useAuth()
const toast = useToast()
const { t } = useI18n()

const sidebarOpen = ref(false)
const planDurations = ref({})
const loading = ref(false)
const selectedPlan = ref(null)
const subscriptionRequest = ref(null)
const showRenewModal = ref(false)
const showCancelModal = ref(false)
const cancelReason = ref('')
const renewForm = reactive({
  plan_id: null,
  duration_months: 1
})

const { data: shop, pending, refresh } = await useFetch(`http://localhost:8000/platform/shops/${shopSlug}`, {
  key: `shop-data-${shopSlug}`,
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

const { data: availablePlans } = await useFetch('http://localhost:8000/subscription-plans', {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

const { data: offers } = await useFetch('http://localhost:8000/offers', {
  server: false
})

const { data: stats } = await useFetch(`http://localhost:8000/shop/${shopSlug}/admin/stats`, {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

const fetchSubscriptionRequest = async () => {
  if (!token.value || !shop.value) return

  try {
    const request = await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription/request`, {
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      onResponseError({ response }) {
        if (response.status === 404) return
      }
    })
    subscriptionRequest.value = request
  } catch (e) {
    if (e?.statusCode === 404 || e?.statusCode === 401) {
      subscriptionRequest.value = null
      return
    }
    subscriptionRequest.value = null
  }
}

watch(shop, async (newShop) => {
  if (newShop) {
    await fetchSubscriptionRequest()
    if (availablePlans.value && availablePlans.value.length > 0) {
      renewForm.plan_id = availablePlans.value.find(p => !p.is_trial)?.id
    }
  }
}, { immediate: true })

// Auto-request plan from query param
watch([availablePlans, shop], async ([plans, currentShop]) => {
  if (plans && plans.length > 0 && currentShop && route.query.plan) {
    const planSlug = route.query.plan
    const plan = plans.find(p => p.slug === planSlug)

    // Only auto-request if:
    // 1. Plan exists
    // 2. It's not a trial plan (trials rely on default logic usually, or we can allow it)
    // 3. We don't already have a pending request
    // 4. We aren't already on this plan
    if (plan && !plan.is_trial) {
      if (subscriptionRequest.value?.status === 'pending') {
        // Already have a request, just clear the query to be clean
        router.replace({ query: { ...route.query, plan: undefined } })
        return
      }

      if (currentShop.subscription_plan_id === plan.id) {
        router.replace({ query: { ...route.query, plan: undefined } })
        return
      }

      // Auto-request with default duration (1 month)
      console.log('Auto-requesting plan:', plan.name)
      await requestPlan(plan)

      // Clear query param so it doesn't trigger again on reload/navigation
      router.replace({ query: { ...route.query, plan: undefined } })
    }
  }
})

const durations = computed(() => [
  { months: 1, label: `1 ${t('admin.subscriptionPage.months.one')}`, discount: 0 },
  { months: 3, label: `3 ${t('admin.subscriptionPage.months.few')}`, discount: 5 },
  { months: 6, label: `6 ${t('admin.subscriptionPage.months.many')}`, discount: 10 },
  { months: 12, label: `12 ${t('admin.subscriptionPage.months.many')}`, discount: 15 }
])

const getPlanDuration = (planId) => {
  return planDurations.value[planId] || 1
}

const setPlanDuration = (planId, duration) => {
  planDurations.value[planId] = duration
}

const calculatePrice = (plan, durationMonths) => {
  if (plan.is_trial || plan.price === 0) return { total: 0, discount: 0, discountAmount: 0, final: 0, savings: 0 }

  const duration = durations.find(d => d.months === durationMonths)
  const discount = duration ? duration.discount : 0
  const monthlyPrice = plan.price
  const totalPrice = monthlyPrice * durationMonths
  const discountAmount = (totalPrice * discount) / 100
  const finalPrice = totalPrice - discountAmount

  return {
    monthly: monthlyPrice,
    total: totalPrice,
    discount: discount,
    discountAmount: discountAmount,
    final: finalPrice,
    savings: discountAmount
  }
}

const getCurrentPlanId = () => {
  if (!availablePlans.value) return 'Загрузка...'

  if (shop.value.subscription_plan_id) {
    const plan = availablePlans.value.find(p => p.id === shop.value.subscription_plan_id)
    return plan ? plan.name : 'Архивный план'
  }

  if (shop.value.subscription_status === 'trial') {
    return t('admin.subscriptionPage.status.trial')
  }

  return t('admin.subscriptionPage.status.free')
}

const getProductStats = () => {
  if (!stats.value) return { current: 0, limit: 0, percent: 0 }

  let limit = 50 // Default trial limit

  if (shop.value.subscription_plan_id && availablePlans.value) {
    const plan = availablePlans.value.find(p => p.id === shop.value.subscription_plan_id)
    if (plan && plan.max_products) {
      limit = plan.max_products
    }
  } else if (shop.value.subscription_status === 'trial') {
    // Find trial plan if exists?
    const trial = availablePlans.value?.find(p => p.is_trial)
    if (trial && trial.max_products) limit = trial.max_products
  }

  const current = stats.value.total_products || 0
  const percent = limit > 0 ? Math.min(Math.round((current / limit) * 100), 100) : 0

  return { current, limit, percent }
}

const getPlanPrice = (status) => {
  if (!availablePlans.value) {
    if (status === 'trial') return t('admin.subscriptionPage.status.free')
    if (status === 'active') return '$29' + t('admin.subscriptionPage.month')
    return '—'
  }

  if (status === 'trial') {
    return t('admin.subscriptionPage.status.free')
  }

  if (status === 'active') {
    const activePlan = availablePlans.value.find(p => !p.is_trial && p.is_active)
    if (activePlan) {
      if (activePlan.price === 0) return t('admin.subscriptionPage.status.free')
      return `$${activePlan.price} ` + t('admin.subscriptionPage.month')
    }
    return '$29' + t('admin.subscriptionPage.month')
  }

  return '—'
}

const formatDate = (dateString) => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const getDaysLeft = (dateString) => {
  if (!dateString) return 0
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = date - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 ? diffDays : 0
}

const getDaysLeftClass = (dateString) => {
  const days = getDaysLeft(dateString)
  if (days <= 7) return 'days-critical'
  if (days <= 30) return 'days-warning'
  return 'days-ok'
}

const getMonthsLabel = (months) => {
  if (months === 1) return t('admin.subscriptionPage.months.one')
  if (months >= 2 && months <= 4) return t('admin.subscriptionPage.months.few')
  return t('admin.subscriptionPage.months.many')
}

const requestPlan = async (plan) => {
  if (subscriptionRequest.value?.status === 'pending') {
    toast.warning(t('alerts.shop.requestTheSame'))
    return
  }

  loading.value = true
  selectedPlan.value = plan

  const selectedDuration = getPlanDuration(plan.id)

  try {
    const requestData = {
      plan_id: plan.id,
      duration_months: selectedDuration
    }

    const request = await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription/request`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body: requestData
    })

    subscriptionRequest.value = request


    toast.success(t('alerts.shop.planRequestSent', { plan: plan.name }))
    await fetchSubscriptionRequest()
  } catch (e) {
    const errorMessage = e.data?.detail || e.message || t('alerts.shop.requestError')
    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}

const renewSubscription = async () => {
  if (!renewForm.plan_id) {
    toast.warning(t('alerts.shop.selectPlan'))
    return
  }

  loading.value = true
  try {
    const plan = availablePlans.value.find(p => p.id === renewForm.plan_id)

    await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription/request`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body: {
        plan_id: renewForm.plan_id,
        duration_months: renewForm.duration_months
      }
    })

    toast.success(t('alerts.shop.renewalSent', { plan: plan.name }))
    showRenewModal.value = false
    await fetchSubscriptionRequest()
    await refresh()
  } catch (e) {
    toast.error(e.data?.detail || t('alerts.shop.renewalError'))
  } finally {
    loading.value = false
  }
}

const cancelSubscription = async () => {
  loading.value = true
  try {
    await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription/cancel`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token.value}` }
    })

    toast.success(t('alerts.shop.subscriptionCancelled'))
    showCancelModal.value = false
    cancelReason.value = ''
    await refresh()
  } catch (e) {
    toast.error(e.data?.detail || t('alerts.shop.cancellationError'))
  } finally {
    loading.value = false
  }
}

const getSelectedPlanName = () => {
  if (!renewForm.plan_id || !availablePlans.value) return ''
  const plan = availablePlans.value.find(p => p.id === renewForm.plan_id)
  return plan ? plan.name : ''
}

const getRenewTotalPrice = () => {
  if (!renewForm.plan_id || !availablePlans.value) {
    return { total: 0, discount: 0, discountAmount: 0, final: 0, savings: 0 }
  }

  const plan = availablePlans.value.find(p => p.id === renewForm.plan_id)
  if (!plan) {
    return { total: 0, discount: 0, discountAmount: 0, final: 0, savings: 0 }
  }

  return calculatePrice(plan, renewForm.duration_months)
}

const getStatusText = (status) => {
  const statusMap = {
    'trial': t('admin.subscriptionPage.status.trial'),
    'active': t('admin.subscriptionPage.status.active'),
    'expired': t('admin.subscriptionPage.status.expired'),
    'cancelled': t('admin.subscriptionPage.status.cancelled')
  }
  return statusMap[status] || status
}

const getStatusClass = (status) => {
  const statusMap = {
    'trial': 'status-trial',
    'active': 'status-active',
    'expired': 'status-expired',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || 'status-trial'
}

</script>

<style scoped>
.subscription-page {
  min-height: 100vh;
  background: #fdfdfd;
}

.admin-main {
  margin-left: 280px;
  padding: 40px;
  min-height: 100vh;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
}

/* Current Subscription */
.current-subscription-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  margin-bottom: 48px;
  border: 1px solid #f1f1f1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.02);
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin: 0;
}

.subscription-status-badge {
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.subscription-status-badge.status-active {
  background: #E6FFFA;
  color: #047857;
}

.subscription-status-badge.status-trial {
  background: #FFFBEB;
  color: #B45309;
}

.subscription-status-badge.status-expired,
.subscription-status-badge.status-cancelled {
  background: #FEF2F2;
  color: #B91C1C;
}

.request-alert {
  background: #E6FFFA;
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  gap: 16px;
  border: 1px solid #BEE3F8;
}

.alert-icon {
  font-size: 20px;
}

.alert-title {
  font-size: 1rem;
  font-weight: 700;
  color: #065F46;
  margin-bottom: 4px;
}

.alert-details {
  font-size: 0.875rem;
  color: #047857;
}

.alert-notes {
  font-size: 0.8rem;
  font-style: italic;
  color: #059669;
  margin-top: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.info-box {
  background: #f9f9f9;
  border-radius: 14px;
  padding: 20px;
  border: 1px solid #f1f1f1;
}

.info-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.info-value {
  font-size: 1.15rem;
  font-weight: 800;
  color: #111;
}

.info-value.days-critical {
  color: #EF4444;
}

.info-value.days-warning {
  color: #F59E0B;
}

.info-value.days-ok {
  color: #10B981;
}

.usage-bar {
  height: 6px;
  background: #E5E7EB;
  border-radius: 10px;
  margin-top: 10px;
  overflow: hidden;
}

.usage-fill {
  height: 100%;
  background: #111;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.usage-fill.over-limit {
  background: #EF4444;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid #f5f5f5;
}

.btn-renew,
.btn-cancel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 24px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-renew {
  background: #111;
  color: white;
}

.btn-renew:hover:not(:disabled) {
  background: #000;
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.btn-cancel {
  background: #f9fafb;
  color: #4B5563;
  border: 1px solid #e5e7eb;
}

.btn-cancel:hover:not(:disabled) {
  background: #FEF2F2;
  color: #B91C1C;
  border-color: #FECACA;
}

/* Plans Section */
.plans-section {
  margin-bottom: 64px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 12px;
  text-align: center;
}

.section-description {
  text-align: center;
  color: #6B7280;
  margin-bottom: 40px;
  font-size: 1rem;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.plan-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #f1f1f1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.02);
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.plan-card:hover {
  border-color: #111;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.plan-featured {
  border: 2px solid #111;
}

.plan-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #111;
  color: white;
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
}

.plan-name {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 16px;
}

.plan-price {
  margin-bottom: 24px;
}

.price-amount {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
}

.price-period {
  color: #9CA3AF;
  font-size: 1rem;
}

.plan-description {
  color: #6B7280;
  margin-bottom: 32px;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Plan Features */
.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 32px;
  flex: 1;
}

.plan-features li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  color: #374151;
  font-size: 0.95rem;
}

.plan-features svg {
  color: #10B981;
}

.plan-button {
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border: none;
  border-radius: 14px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.plan-button:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

/* Duration Selector */
.duration-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.duration-btn {
  padding: 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.duration-btn.active {
  background: #111;
  border-color: #111;
  color: white;
}

.discount-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #10B981;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.65rem;
  font-weight: 800;
}

.price-summary {
  background: #f9fafb;
  border-radius: 14px;
  padding: 20px;
  border: 1px dashed #e5e7eb;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.summary-row.total {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  font-weight: 800;
  font-size: 1.1rem;
}

/* Offers Section */
.offers-section {
  margin-top: 48px;
}

.offers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.offer-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid #f1f1f1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.offer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.offer-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin: 0;
}

.offer-price {
  font-weight: 900;
  font-size: 1.25rem;
  color: #111;
}

.offer-description {
  color: #6B7280;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 24px;
}

.offer-btn {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #f3f4f6;
  color: #111;
  transition: all 0.2s;
}

.offer-btn:hover {
  background: #e5e7eb;
}

/* Info Section (Important Information) */
.info-section {
  background: #F0F9FF;
  border-radius: 16px;
  padding: 32px;
  margin-top: 48px;
  border: 1px solid #BAE6FD;
}

.info-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #0369A1;
  margin-bottom: 16px;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-list li {
  color: #075985;
  font-size: 0.9rem;
  margin-bottom: 10px;
  display: flex;
  gap: 10px;
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  padding: 24px 32px;
  border-bottom: 1px solid #f1f1f1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #9CA3AF;
}

.modal-body {
  padding: 32px;
}

.modal-body p {
  color: #6B7280;
  margin-bottom: 24px;
  line-height: 1.6;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-weight: 700;
  font-size: 0.875rem;
  margin-bottom: 10px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.95rem;
  background: #f9fafb;
}

.duration-grid-modal {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 24px;
}

.duration-btn-modal {
  padding: 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.duration-btn-modal.active {
  background: #111;
  color: white;
  border-color: #111;
}

.modal-price-summary {
  background: #f9fafb;
  border-radius: 14px;
  padding: 20px;
  border: 1px dashed #e5e7eb;
}

.modal-footer {
  padding: 24px 32px;
  background: #f9fafb;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.btn-secondary {
  background: white;
  border: 1px solid #e5e7eb;
  color: #111;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary {
  background: #111;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.btn-danger {
  background: #EF4444;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.mobile-header {
  display: none;
}

/* Mobile */
@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 0px;
    padding-top: 84px;
  }

  .mobile-header {
    display: flex;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: white;
    height: 64px;
    padding: 0 20px;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #f1f1f1;
    z-index: 1000;
  }

  .menu-btn,
  .home-btn {
    background: #f9fafb;
    border: 1px solid #f1f1f1;
    border-radius: 10px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #111;
  }
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }

  .duration-grid {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-direction: column;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  text-align: center;
  color: #6B7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #111;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}
</style>
