<template>
  <div class="subscription-page">
    <ShopAdminSidebar :shop-slug="shopSlug" current-route="subscription" />
    
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">Выберите подписку</h1>
          <p class="page-subtitle">Выберите план, который подходит вашему бизнесу</p>
        </div>

        <div v-if="pending" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Загрузка...</p>
        </div>

        <div v-else-if="shop">
          <!-- Current Subscription Card -->
          <div class="current-subscription-card">
            <div class="card-header-row">
              <h2 class="card-title">Текущая подписка</h2>
              <div class="subscription-status-badge" :class="getStatusClass(shop.subscription_status)">
                {{ getStatusText(shop.subscription_status) }}
              </div>
            </div>
            
            <!-- Active Subscription Request -->
            <div v-if="subscriptionRequest && subscriptionRequest.status === 'pending'" class="request-alert success">
              <div class="alert-icon">✅</div>
              <div class="alert-content">
                <h3 class="alert-title">Запрос одобрен</h3>
                <p class="alert-details">
                  План: <strong>{{ subscriptionRequest.plan_name }}</strong> • 
                  Длительность: <strong>{{ subscriptionRequest.duration_months }} {{ getMonthsLabel(subscriptionRequest.duration_months) }}</strong> • 
                  Отправлен: {{ formatDate(subscriptionRequest.requested_at) }}
                </p>
                <p v-if="subscriptionRequest.notes" class="alert-notes">{{ subscriptionRequest.notes }}</p>
              </div>
            </div>

            <!-- Subscription Info Grid -->
            <div class="info-grid">
              <div class="info-box">
                <div class="info-label">ПЛАН</div>
                <div class="info-value">{{ getCurrentPlanId() }}</div>
              </div>
              
              <div class="info-box">
                <div class="info-label">СТОИМОСТЬ</div>
                <div class="info-value">{{ getPlanPrice(shop.subscription_status) }}</div>
              </div>
              
              <div class="info-box" v-if="shop.subscription_expires_at">
                <div class="info-label">ИСТЕКАЕТ</div>
                <div class="info-value">{{ formatDate(shop.subscription_expires_at) }}</div>
              </div>
              
              <div class="info-box" v-if="shop.subscription_expires_at">
                <div class="info-label">ОСТАЛОСЬ ДНЕЙ</div>
                <div class="info-value" :class="getDaysLeftClass(shop.subscription_expires_at)">
                  {{ getDaysLeft(shop.subscription_expires_at) }}
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
                Продлить подписку
              </button>
              <button @click="showCancelModal = true" class="btn-cancel" :disabled="loading">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="15" y1="9" x2="9" y2="15"></line>
                  <line x1="9" y1="9" x2="15" y2="15"></line>
                </svg>
                Отменить подписку
              </button>
            </div>
          </div>

          <!-- Available Plans (only if not active) -->
          <div v-if="shop.subscription_status !== 'active' && availablePlans && availablePlans.length > 0" class="plans-section">
            <h2 class="section-title">Доступные планы</h2>
            <p class="section-description">Выберите план и отправьте запрос. Администратор платформы свяжется с вами для активации подписки после получения оплаты.</p>
            
            <div class="plans-grid">
              <div 
                v-for="plan in availablePlans" 
                :key="plan.id" 
                class="plan-card"
                :class="{ 'plan-featured': plan.slug === 'basic' }"
              >
                <div v-if="plan.slug === 'basic'" class="plan-badge">Популярный</div>
                
                <div class="plan-header">
                  <h3 class="plan-name">{{ plan.name }}</h3>
                  <div class="plan-price">
                    <span class="price-amount">${{ plan.price }}</span>
                    <span class="price-period">/месяц</span>
                  </div>
                </div>
                
                <p class="plan-description">{{ plan.description }}</p>
                
                <!-- Duration Selection -->
                <div v-if="!plan.is_trial && plan.price > 0" class="duration-selector">
                  <label class="duration-label">Выберите длительность:</label>
                  <div class="duration-grid">
                    <button
                      v-for="duration in durations"
                      :key="duration.months"
                      @click="setPlanDuration(plan.id, duration.months)"
                      class="duration-btn"
                      :class="{ active: getPlanDuration(plan.id) === duration.months }"
                    >
                      {{ duration.label }}
                      <span v-if="duration.discount > 0" class="discount-badge">-{{ duration.discount }}%</span>
                    </button>
                  </div>
                  
                  <div class="price-summary">
                    <div class="summary-row">
                      <span>Цена за {{ getPlanDuration(plan.id) }} {{ getMonthsLabel(getPlanDuration(plan.id)) }}:</span>
                      <span>${{ calculatePrice(plan, getPlanDuration(plan.id)).total.toFixed(2) }}</span>
                    </div>
                    <div v-if="calculatePrice(plan, getPlanDuration(plan.id)).discount > 0" class="summary-row discount">
                      <span>Скидка {{ calculatePrice(plan, getPlanDuration(plan.id)).discount }}%:</span>
                      <span>-${{ calculatePrice(plan, getPlanDuration(plan.id)).discountAmount.toFixed(2) }}</span>
                    </div>
                    <div class="summary-row total">
                      <span><strong>Итого:</strong></span>
                      <span><strong>${{ calculatePrice(plan, getPlanDuration(plan.id)).final.toFixed(2) }}</strong></span>
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
                
                <button 
                  @click="requestPlan(plan)" 
                  class="plan-button"
                  :disabled="loading || subscriptionRequest?.status === 'pending'"
                >
                  {{ loading && selectedPlan?.id === plan.id ? 'Отправка...' : subscriptionRequest?.status === 'pending' ? 'Запрос отправлен' : 'Запросить план' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Offers Section -->
          <div v-if="offers && offers.length > 0" class="offers-section">
            <h2 class="section-title">Специальные предложения</h2>
            <p class="section-description">Дополнительные услуги и решения</p>
            
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
                    Написать
                  </a>
                  <a v-if="offer.contact_phone" :href="`tel:${offer.contact_phone}`" class="offer-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                    </svg>
                    Позвонить
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Important Information -->
          <div class="info-section">
            <h3 class="info-title">Важная информация</h3>
            <ul class="info-list">
              <li>ℹ️ Пробный период длится 30 дней с момента создания магазина</li>
              <li>ℹ️ После окончания пробного периода магазин будет приостановлен</li>
              <li>ℹ️ Для активации подписки отправьте запрос на выбранный план</li>
              <li>ℹ️ Администратор платформы свяжется с вами для получения оплаты и активации подписки</li>
              <li>ℹ️ После активации подписка будет автоматически продлеваться, или вы можете запросить продление вручную</li>
            </ul>
          </div>
        </div>
      </div>
    </main>

    <!-- Renew Modal -->
    <div v-if="showRenewModal" class="modal-overlay" @click="showRenewModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Продлить подписку</h2>
          <button @click="showRenewModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <p>Выберите план и длительность для продления подписки:</p>
          
          <div class="form-group">
            <label>План подписки</label>
            <select v-model="renewForm.plan_id" class="form-input">
              <option v-for="plan in availablePlans?.filter(p => !p.is_trial)" :key="plan.id" :value="plan.id">
                {{ plan.name }} - ${{ plan.price }}/мес
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Длительность</label>
            <div class="duration-grid-modal">
              <button
                v-for="duration in durations"
                :key="duration.months"
                @click="renewForm.duration_months = duration.months"
                class="duration-btn-modal"
                :class="{ active: renewForm.duration_months === duration.months }"
                type="button"
              >
                {{ duration.label }}
                <span v-if="duration.discount > 0" class="discount-badge">-{{ duration.discount }}%</span>
              </button>
            </div>
          </div>
          
          <!-- Price Summary -->
          <div v-if="renewForm.plan_id" class="modal-price-summary">
            <div class="summary-row">
              <span>{{ getSelectedPlanName() }} × {{ renewForm.duration_months }} {{ getMonthsLabel(renewForm.duration_months) }}</span>
              <span>${{ getRenewTotalPrice().total.toFixed(2) }}</span>
            </div>
            <div v-if="getRenewTotalPrice().discount > 0" class="summary-row discount">
              <span>Скидка {{ getRenewTotalPrice().discount }}%</span>
              <span>-${{ getRenewTotalPrice().discountAmount.toFixed(2) }}</span>
            </div>
            <div class="summary-row total">
              <span><strong>Итого к оплате:</strong></span>
              <span><strong>${{ getRenewTotalPrice().final.toFixed(2) }}</strong></span>
            </div>
            <div v-if="getRenewTotalPrice().savings > 0" class="savings-note">
              💰 Вы экономите ${{ getRenewTotalPrice().savings.toFixed(2) }}
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showRenewModal = false" class="btn-secondary">Отмена</button>
          <button @click="renewSubscription" class="btn-primary" :disabled="loading">
            {{ loading ? 'Отправка...' : 'Отправить запрос' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Cancel Modal -->
    <div v-if="showCancelModal" class="modal-overlay" @click="showCancelModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Отменить подписку</h2>
          <button @click="showCancelModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <p class="warning-text">⚠️ Вы уверены, что хотите отменить подписку?</p>
          <p>После отмены подписки ваш магазин будет деактивирован и вы потеряете доступ ко всем функциям платформы.</p>
          
          <div class="form-group">
            <label>Причина отмены (необязательно)</label>
            <textarea v-model="cancelReason" rows="3" class="form-input" placeholder="Укажите причину отмены..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCancelModal = false" class="btn-secondary">Отмена</button>
          <button @click="cancelSubscription" class="btn-danger" :disabled="loading">
            {{ loading ? 'Отмена...' : 'Подтвердить отмену' }}
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

const selectedPlan = ref(null)
const planDurations = ref({})
const loading = ref(false)
const subscriptionRequest = ref(null)
const showRenewModal = ref(false)
const showCancelModal = ref(false)
const cancelReason = ref('')
const renewForm = reactive({
  plan_id: null,
  duration_months: 1
})

const { data: shop, pending, refresh } = await useFetch(`http://localhost:8000/platform/shops/${shopSlug}`, {
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

const durations = [
  { months: 1, label: '1 месяц', discount: 0 },
  { months: 3, label: '3 месяца', discount: 5 },
  { months: 6, label: '6 месяцев', discount: 10 },
  { months: 12, label: '12 месяцев', discount: 15 }
]

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
  if (!availablePlans.value) return 'Неизвестно'
  
  if (shop.value.subscription_status === 'trial') {
    const trialPlan = availablePlans.value.find(p => p.is_trial)
    return trialPlan?.slug || 'trial'
  }
  
  if (shop.value.subscription_status === 'active') {
    const activePlan = availablePlans.value.find(p => !p.is_trial && p.is_active)
    return activePlan?.slug || 'basic'
  }
  
  return 'Не активна'
}

const getPlanPrice = (status) => {
  if (!availablePlans.value) {
    if (status === 'trial') return 'Бесплатно'
    if (status === 'active') return '$29/месяц'
    return '—'
  }
  
  if (status === 'trial') {
    return 'Бесплатно'
  }
  
  if (status === 'active') {
    const activePlan = availablePlans.value.find(p => !p.is_trial && p.is_active)
    if (activePlan) {
      if (activePlan.price === 0) return 'Бесплатно'
      return `$${activePlan.price} в месяц`
    }
    return '$29/месяц'
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
  if (months === 1) return 'месяц'
  if (months >= 2 && months <= 4) return 'месяца'
  return 'месяцев'
}

const requestPlan = async (plan) => {
  if (subscriptionRequest.value?.status === 'pending') {
    toast.warning('У вас уже есть активный запрос на рассмотрении')
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
    
    toast.success(`Запрос на план "${plan.name}" отправлен! Администратор платформы свяжется с вами для активации.`)
    await fetchSubscriptionRequest()
  } catch (e) {
    const errorMessage = e.data?.detail || e.message || 'Ошибка при отправке запроса'
    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}

const renewSubscription = async () => {
  if (!renewForm.plan_id) {
    toast.warning('Выберите план подписки')
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
    
    toast.success(`Запрос на продление подписки "${plan.name}" отправлен!`)
    showRenewModal.value = false
    await fetchSubscriptionRequest()
    await refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при отправке запроса на продление')
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
    
    toast.success('Подписка успешно отменена')
    showCancelModal.value = false
    cancelReason.value = ''
    await refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при отмене подписки')
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
    'trial': 'Пробный период',
    'active': 'Активна',
    'expired': 'Истекла',
    'cancelled': 'Отменена'
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
  display: flex;
  background: #FAFAFA;
}

.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
  padding: 32px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 6px;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Current Subscription Card */
.current-subscription-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  border: 2px solid #111;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.subscription-status-badge {
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 0.8125rem;
  font-weight: 700;
  white-space: nowrap;
}

.subscription-status-badge.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.subscription-status-badge.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.subscription-status-badge.status-expired,
.subscription-status-badge.status-cancelled {
  background: #FEE2E2;
  color: #991B1B;
}

.request-alert {
  background: #D1FAE5;
  border-left: 3px solid #10B981;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.alert-icon {
  font-size: 18px;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #065F46;
  margin-bottom: 4px;
}

.alert-details {
  font-size: 0.8125rem;
  color: #047857;
  margin-bottom: 4px;
}

.alert-notes {
  font-size: 0.75rem;
  color: #059669;
  font-style: italic;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.info-box {
  background: #F9FAFB;
  border-radius: 10px;
  padding: 14px;
  border: 1px solid #E5E7EB;
}

.info-label {
  font-size: 0.625rem;
  font-weight: 700;
  color: #6B7280;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.info-value {
  font-size: 1.125rem;
  font-weight: 800;
  color: #111;
}

.info-value.days-critical {
  color: #DC2626;
}

.info-value.days-warning {
  color: #F59E0B;
}

.info-value.days-ok {
  color: #10B981;
}

.action-buttons {
  display: flex;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #F3F4F6;
}

.btn-renew,
.btn-cancel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.875rem;
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
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn-cancel {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-cancel:hover:not(:disabled) {
  background: #FEF2F2;
  transform: translateY(-1px);
}

.btn-renew:disabled,
.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.info-value.days-critical {
  color: #DC2626;
}

.info-value.days-warning {
  color: #F59E0B;
}

.info-value.days-ok {
  color: #10B981;
}

.action-buttons {
  display: flex;
  gap: 16px;
  padding-top: 24px;
  border-top: 2px solid #F3F4F6;
}

.btn-renew,
.btn-cancel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 32px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-renew {
  background: #111;
  color: white;
}

.btn-renew:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.btn-cancel {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-cancel:hover:not(:disabled) {
  background: #FEF2F2;
  transform: translateY(-2px);
}

.btn-renew:disabled,
.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Plans Section */
.plans-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #111;
  text-align: center;
  margin-bottom: 8px;
}

.section-description {
  text-align: center;
  color: #6B7280;
  margin-bottom: 32px;
  font-size: 0.9375rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.plan-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #E5E7EB;
  position: relative;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}

.plan-card:hover {
  border-color: #111;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.plan-featured {
  border: 2px solid #111;
}

.plan-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: #111;
  color: white;
  padding: 4px 16px;
  border-radius: 16px;
  font-size: 0.6875rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.plan-header {
  margin-bottom: 16px;
}

.plan-name {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 10px;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-amount {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
}

.price-period {
  font-size: 0.875rem;
  color: #6B7280;
}

.plan-description {
  color: #6B7280;
  margin-bottom: 20px;
  line-height: 1.5;
  font-size: 0.875rem;
}

.duration-selector {
  margin-bottom: 20px;
}

.duration-label {
  display: block;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #111;
  margin-bottom: 10px;
}

.duration-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 14px;
}

.duration-btn {
  padding: 10px;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.8125rem;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.duration-btn:hover {
  border-color: #111;
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
  border-radius: 12px;
  font-size: 0.625rem;
  font-weight: 800;
}

.price-summary {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 16px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.9375rem;
  color: #111;
}

.summary-row.discount {
  color: #10B981;
}

.summary-row.total {
  border-top: 2px solid #E5E7EB;
  margin-top: 8px;
  padding-top: 12px;
  font-size: 1.125rem;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  flex: 1;
}

.plan-features li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  color: #374151;
  font-size: 0.9375rem;
}

.plan-features svg {
  color: #10B981;
  flex-shrink: 0;
}

.plan-button {
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.plan-button:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.plan-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Offers Section */
.offers-section {
  margin-bottom: 40px;
}

.offers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.offer-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #E5E7EB;
  transition: all 0.2s;
}

.offer-card:hover {
  border-color: #111;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.offer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.offer-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
}

.offer-price {
  font-size: 1.5rem;
  font-weight: 900;
  color: #111;
}

.offer-description {
  color: #6B7280;
  margin-bottom: 16px;
  line-height: 1.6;
}

.offer-contact {
  color: #374151;
  margin-bottom: 20px;
  font-size: 0.9375rem;
}

.offer-actions {
  display: flex;
  gap: 12px;
}

.offer-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: #111;
  color: white;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s;
}

.offer-btn:hover {
  background: #000;
  transform: translateY(-2px);
}

/* Info Section */
.info-section {
  background: #EFF6FF;
  border-left: 3px solid #3B82F6;
  border-radius: 12px;
  padding: 24px;
}

.info-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: #1E40AF;
  margin-bottom: 12px;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-list li {
  padding: 6px 0;
  color: #1E3A8A;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #F3F4F6;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.modal-close {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  color: #111;
  font-size: 24px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #E5E7EB;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  color: #4B5563;
  margin-bottom: 24px;
  line-height: 1.6;
}

.warning-text {
  color: #DC2626 !important;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #111;
  margin-bottom: 8px;
  font-size: 0.9375rem;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.9375rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #111;
}

textarea.form-input {
  resize: vertical;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 2px solid #F3F4F6;
}

.btn-secondary,
.btn-primary,
.btn-danger {
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.btn-secondary {
  background: #F3F4F6;
  color: #111;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #000;
}

.btn-danger {
  background: #EF4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #DC2626;
}

.btn-primary:disabled,
.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.duration-grid-modal {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.duration-btn-modal {
  padding: 12px;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.875rem;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.duration-btn-modal:hover {
  border-color: #111;
}

.duration-btn-modal.active {
  background: #111;
  border-color: #111;
  color: white;
}

.modal-price-summary {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 16px;
  margin-top: 20px;
}

.modal-price-summary .summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.9375rem;
  color: #111;
}

.modal-price-summary .summary-row.discount {
  color: #10B981;
}

.modal-price-summary .summary-row.total {
  border-top: 2px solid #E5E7EB;
  margin-top: 8px;
  padding-top: 12px;
  font-size: 1.125rem;
}

.modal-price-summary .savings-note {
  text-align: center;
  margin-top: 12px;
  padding: 8px;
  background: #D1FAE5;
  border-radius: 8px;
  color: #065F46;
  font-size: 0.875rem;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 24px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .plans-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.75rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .duration-grid {
    grid-template-columns: 1fr;
  }
  
  .duration-grid-modal {
    grid-template-columns: 1fr;
  }
}
</style>
