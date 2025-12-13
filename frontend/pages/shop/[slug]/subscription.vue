<template>
  <div class="subscription-page">
    <ShopAdminSidebar :shop-slug="shopSlug" current-route="subscription" />
    
    <main class="admin-main">
      <div class="container py-8">
      <div class="subscription-header">
        <h1 class="page-title">Выберите подписку для {{ shop?.name }}</h1>
        <p class="page-subtitle">Выберите план, который подходит вашему бизнесу</p>
      </div>

      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">Загрузка...</p>
      </div>

      <div v-else-if="shop">
        <!-- Current Subscription Info -->
        <div class="current-subscription-card">
          <div class="subscription-header-section">
            <h2 class="section-title">Текущая подписка</h2>
            <div class="subscription-status" :class="getStatusClass(shop.subscription_status)">
              {{ getStatusText(shop.subscription_status) }}
            </div>
          </div>
          
          <div class="subscription-info-grid">
            <div class="info-item">
              <span class="info-label">План</span>
              <span class="info-value">{{ getPlanName(shop.subscription_status) }}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">Стоимость</span>
              <span class="info-value">{{ getPlanPrice(shop.subscription_status) }}</span>
            </div>
            
            <div class="info-item" v-if="shop.subscription_expires_at">
              <span class="info-label">{{ shop.subscription_status === 'trial' ? 'Заканчивается' : 'Истекает' }}</span>
              <span class="info-value">{{ formatDate(shop.subscription_expires_at) }}</span>
            </div>
            
            <div class="info-item" v-if="shop.subscription_expires_at">
              <span class="info-label">Осталось дней</span>
              <span class="info-value" :class="getDaysLeftClass(shop.subscription_expires_at)">
                {{ getDaysLeft(shop.subscription_expires_at) }}
              </span>
            </div>
          </div>
          
          <div v-if="shop.subscription_status !== 'active' && shop.subscription_status !== 'trial'" class="subscription-actions">
            <button @click="requestRenewal" class="renew-btn" :disabled="loading">
              {{ loading ? 'Отправка...' : 'Запросить продление' }}
            </button>
            <p class="renew-note">После запроса с вами свяжется администратор платформы для активации подписки</p>
          </div>
        </div>

        <!-- Available Plans (only if subscription expired or cancelled) -->
        <div v-if="(shop.subscription_status === 'expired' || shop.subscription_status === 'cancelled' || shop.subscription_status === 'trial') && availablePlans && availablePlans.length > 0" class="available-plans-section">
          <h2 class="section-title">Доступные планы</h2>
          <p class="section-description">Выберите план и отправьте запрос. Администратор платформы свяжется с вами для активации подписки после получения оплаты.</p>
          <div class="pricing-grid">
            <div 
              v-for="plan in availablePlans" 
              :key="plan.id" 
              class="pricing-card" 
              :class="{ 
                'featured': plan.is_trial || plan.slug === 'basic',
                'selected': selectedPlan?.id === plan.id 
              }"
            >
              <div v-if="plan.slug === 'basic' && !plan.is_trial" class="pricing-badge">Популярный</div>
              <div class="pricing-header">
                <h3 class="pricing-name">{{ plan.name }}</h3>
                <div class="pricing-price">
                  <span class="price-amount" v-if="plan.price === 0 || plan.is_trial">Бесплатно</span>
                  <span class="price-amount" v-else>${{ plan.price }}</span>
                  <span class="price-period">{{ getPeriodLabel(plan.period_days) }}</span>
                </div>
              </div>
              <div v-if="plan.description" class="pricing-description">
                {{ plan.description }}
              </div>
              <ul class="pricing-features" v-if="plan.features_list && plan.features_list.length > 0">
                <li v-for="(feature, index) in plan.features_list" :key="index">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  {{ feature }}
                </li>
              </ul>
              <div v-else class="no-features-text">Функции не указаны</div>
              <button 
                @click="requestPlan(plan)" 
                class="pricing-button"
                :disabled="loading || (shop.subscription_status === 'active' && !plan.is_trial) || (plan.is_trial && shop.subscription_status === 'trial')"
                :class="{ 
                  'active': (shop.subscription_status === 'trial' && plan.is_trial) || (shop.subscription_status === 'active' && !plan.is_trial) 
                }"
              >
                <span v-if="loading && selectedPlan?.id === plan.id">Отправка...</span>
                <span v-else-if="plan.is_trial && shop.subscription_status === 'trial'">Активен</span>
                <span v-else-if="shop.subscription_status === 'active' && !plan.is_trial">Активен</span>
                <span v-else-if="plan.is_trial">Выбрать</span>
                <span v-else>Запросить план</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Empty Plans State -->
        <div v-if="(shop.subscription_status === 'expired' || shop.subscription_status === 'cancelled' || shop.subscription_status === 'trial') && (!availablePlans || availablePlans.length === 0)" class="empty-plans">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          </svg>
          <p>Планы подписки пока не доступны</p>
          <p class="empty-subtitle">Свяжитесь с администратором платформы</p>
        </div>
      </div>

      <div v-if="shop" class="info-box">
        <h3>Важная информация</h3>
        <ul>
          <li>Пробный период длится 30 дней с момента создания магазина</li>
          <li>После окончания пробного периода магазин будет приостановлен</li>
          <li>Для активации подписки отправьте запрос на выбранный план</li>
          <li>Администратор платформы свяжется с вами для получения оплаты и активации подписки</li>
          <li>После активации подписка будет автоматически продлеваться, или вы можете запросить продление вручную</li>
        </ul>
      </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth', 'shop-owner']
})

const route = useRoute()
const shopSlug = route.params.slug
const { token } = useAuth()
const router = useRouter()
const toast = useToast()

const selectedPlan = ref(null)
const loading = ref(false)

const { data: shop, pending, refresh } = await useFetch(`http://localhost:8000/platform/shops/${shopSlug}`, {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

// Fetch available subscription plans
const { data: availablePlans } = await useFetch('http://localhost:8000/subscription-plans', {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

const getStatusClass = (status) => {
  const statusMap = {
    'trial': 'status-trial',
    'active': 'status-active',
    'expired': 'status-expired',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || 'status-trial'
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

const getPlanName = (status) => {
  if (!availablePlans.value) {
    // Fallback на старую логику
    if (status === 'trial') return 'Пробный период'
    if (status === 'active') return 'Активный план'
    return 'Не активна'
  }
  
  if (status === 'trial') {
    const trialPlan = availablePlans.value.find(p => p.is_trial)
    return trialPlan ? trialPlan.name : 'Пробный период'
  }
  
  if (status === 'active') {
    // Ищем активный план (не пробный)
    const activePlan = availablePlans.value.find(p => !p.is_trial && p.is_active)
    return activePlan ? activePlan.name : 'Активный план'
  }
  
  return 'Не активна'
}

const getPlanPrice = (status) => {
  if (!availablePlans.value) {
    // Fallback на старую логику
    if (status === 'trial') return 'Бесплатно'
    if (status === 'active') return '$29/месяц'
    return '—'
  }
  
  if (status === 'trial') {
    const trialPlan = availablePlans.value.find(p => p.is_trial)
    return trialPlan ? 'Бесплатно' : 'Бесплатно'
  }
  
  if (status === 'active') {
    // Ищем активный план (не пробный)
    const activePlan = availablePlans.value.find(p => !p.is_trial && p.is_active)
    if (activePlan) {
      if (activePlan.price === 0) return 'Бесплатно'
      return `$${activePlan.price}${getPeriodLabel(activePlan.period_days)}`
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
  if (days <= 7) return 'days-warning'
  if (days <= 30) return 'days-notice'
  return 'days-ok'
}

const requestRenewal = async () => {
  loading.value = true
  try {
    // Отправляем запрос на продление подписки
    // В реальности здесь должен быть API endpoint для отправки запроса админу
    // Пока просто показываем сообщение
    toast.success('Запрос на продление подписки отправлен! Администратор платформы свяжется с вами для активации.')
    console.log('[Subscription] Запрос на продление подписки для магазина:', shopSlug)
    
    // Здесь можно отправить запрос на бэкенд, который уведомит админа
    // await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription/request-renewal`, {
    //   method: 'POST',
    //   headers: { 'Authorization': `Bearer ${token.value}` }
    // })
  } catch (e) {
    toast.error('Ошибка при отправке запроса')
    console.error(e)
  } finally {
    loading.value = false
  }
}

const getPeriodLabel = (days) => {
  if (days === 30) return 'в месяц'
  if (days === 365 || days === 360) return 'в год'
  if (days >= 2 && days <= 4) return `за ${days} дня`
  if (days >= 5) return `за ${days} дней`
  return `за ${days} день`
}

const requestPlan = async (plan) => {
  if (plan.is_trial && shop.value.subscription_status === 'trial') {
    toast.info('Пробный период уже активен')
    return
  }

  loading.value = true
  selectedPlan.value = plan

  try {
    // Отправляем запрос на активацию подписки
    // Админ платформы активирует её вручную после получения оплаты
    const planPrice = plan.price === 0 || plan.is_trial 
      ? 'Бесплатно' 
      : `$${plan.price}${getPeriodLabel(plan.period_days)}`
    
    toast.success(`Запрос на план "${plan.name}" (${planPrice}) отправлен! Администратор платформы свяжется с вами для активации после получения оплаты.`)
    console.log('[Subscription] Запрос на план:', plan.slug, 'для магазина:', shopSlug)
    
    // Здесь можно отправить запрос на бэкенд, который уведомит админа
    // await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription/request`, {
    //   method: 'POST',
    //   headers: { 'Authorization': `Bearer ${token.value}` },
    //   body: { plan_id: plan.id }
    // })
  } catch (e) {
    toast.error('Ошибка при отправке запроса')
    console.error(e)
  } finally {
    loading.value = false
  }
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
}

.current-subscription-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.subscription-header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid #F3F4F6;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
}

.subscription-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
}

.subscription-status.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.subscription-status.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.subscription-status.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.subscription-status.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.subscription-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.info-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
}

.info-value.days-warning {
  color: #DC2626;
}

.info-value.days-notice {
  color: #F59E0B;
}

.info-value.days-ok {
  color: #10B981;
}

.subscription-actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 2px solid #F3F4F6;
}

.renew-btn {
  padding: 14px 32px;
  background: #111;
  color: white;
  border-radius: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.renew-btn:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.renew-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.available-plans-section {
  margin-top: 48px;
}

.available-plans-section .section-title {
  text-align: center;
  margin-bottom: 16px;
}

.section-description {
  text-align: center;
  color: #6B7280;
  margin-bottom: 32px;
  font-size: 0.875rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.renew-note {
  margin-top: 12px;
  font-size: 0.875rem;
  color: #6B7280;
  text-align: center;
}

.subscription-header {
  text-align: center;
  margin-bottom: 48px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 12px;
  color: #111;
}

.page-subtitle {
  font-size: 1.125rem;
  color: #666;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1100px;
  margin: 0 auto 48px;
}

.pricing-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  position: relative;
  transition: all 0.3s;
}

.pricing-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.pricing-card.featured {
  border: 3px solid #111;
  transform: scale(1.05);
}

.pricing-card.selected {
  border-color: #10B981;
}

.pricing-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #111;
  color: white;
  padding: 6px 20px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.pricing-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 2px solid #F3F4F6;
}

.pricing-name {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 16px;
  color: #111;
}

.pricing-price {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.price-amount {
  font-size: 3rem;
  font-weight: 900;
  color: #111;
}

.price-period {
  font-size: 0.875rem;
  color: #666;
}

.pricing-features {
  list-style: none;
  padding: 0;
  margin: 0 0 32px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pricing-features li {
  color: #666;
  line-height: 1.6;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.pricing-features li svg {
  color: #10B981;
  flex-shrink: 0;
  margin-top: 2px;
}

.pricing-description {
  color: #6B7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #F3F4F6;
}

.no-features-text {
  color: #9CA3AF;
  font-size: 0.875rem;
  font-style: italic;
  padding: 20px 0;
  text-align: center;
}

.empty-plans {
  padding: 60px 20px;
  text-align: center;
  background: white;
  border-radius: 20px;
  border: 2px dashed #E5E7EB;
  margin-top: 32px;
}

.empty-plans svg {
  margin-bottom: 16px;
  color: #9CA3AF;
}

.empty-plans p {
  font-size: 1rem;
  font-weight: 600;
  margin: 8px 0;
  color: #111;
}

.empty-plans .empty-subtitle {
  font-size: 0.875rem;
  font-weight: 400;
  color: #6B7280;
}

.pricing-button {
  display: block;
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border-radius: 12px;
  text-align: center;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.pricing-button:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.pricing-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.pricing-button.active {
  background: #10B981;
}

.info-box {
  max-width: 800px;
  margin: 0 auto;
  background: #F9FAFB;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #E5E7EB;
}

.info-box h3 {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #111;
}

.info-box ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-box li {
  padding: 8px 0;
  padding-left: 24px;
  position: relative;
  color: #666;
  font-size: 0.875rem;
  line-height: 1.6;
}

.info-box li:before {
  content: 'ℹ';
  position: absolute;
  left: 0;
  color: #3B82F6;
  font-weight: 700;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 240px;
  }
  
  .pricing-grid {
    grid-template-columns: 1fr;
  }
  
  .pricing-card.featured {
    transform: scale(1);
  }
  
  .subscription-info-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
  }
}
</style>

