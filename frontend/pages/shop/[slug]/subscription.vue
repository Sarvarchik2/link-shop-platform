<template>
  <div class="subscription-page">
    <div class="container py-8">
      <div class="subscription-header">
        <h1 class="page-title">Выберите подписку для {{ shop?.name }}</h1>
        <p class="page-subtitle">Выберите план, который подходит вашему бизнесу</p>
      </div>

      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">Загрузка...</p>
      </div>

      <div v-else-if="shop" class="pricing-grid">
        <div class="pricing-card" :class="{ 'featured': shop.subscription_status === 'trial' }">
          <div class="pricing-header">
            <h3 class="pricing-name">Пробный период</h3>
            <div class="pricing-price">
              <span class="price-amount">Бесплатно</span>
              <span class="price-period">30 дней</span>
            </div>
          </div>
          <ul class="pricing-features">
            <li>✓ Полный доступ ко всем функциям</li>
            <li>✓ Неограниченное количество товаров</li>
            <li>✓ Управление заказами</li>
            <li>✓ Аналитика и статистика</li>
          </ul>
          <button 
            @click="selectPlan('trial')" 
            class="pricing-button"
            :disabled="shop.subscription_status === 'trial'"
            :class="{ 'active': shop.subscription_status === 'trial' }"
          >
            {{ shop.subscription_status === 'trial' ? 'Активен' : 'Выбрать' }}
          </button>
        </div>

        <div class="pricing-card featured" :class="{ 'selected': selectedPlan === 'basic' }">
          <div class="pricing-badge">Популярный</div>
          <div class="pricing-header">
            <h3 class="pricing-name">Базовый</h3>
            <div class="pricing-price">
              <span class="price-amount">$29</span>
              <span class="price-period">в месяц</span>
            </div>
          </div>
          <ul class="pricing-features">
            <li>✓ Все функции пробного периода</li>
            <li>✓ Приоритетная поддержка</li>
            <li>✓ Расширенная аналитика</li>
            <li>✓ Интеграции с платежными системами</li>
          </ul>
          <button 
            @click="selectPlan('basic')" 
            class="pricing-button"
            :disabled="loading"
            :class="{ 'active': shop.subscription_status === 'active' && selectedPlan === 'basic' }"
          >
            {{ loading ? 'Обработка...' : 'Выбрать план' }}
          </button>
        </div>

        <div class="pricing-card" :class="{ 'selected': selectedPlan === 'pro' }">
          <div class="pricing-header">
            <h3 class="pricing-name">Профессиональный</h3>
            <div class="pricing-price">
              <span class="price-amount">$79</span>
              <span class="price-period">в месяц</span>
            </div>
          </div>
          <ul class="pricing-features">
            <li>✓ Все функции базового плана</li>
            <li>✓ API доступ</li>
            <li>✓ Кастомный дизайн</li>
            <li>✓ Персональный менеджер</li>
          </ul>
          <button 
            @click="selectPlan('pro')" 
            class="pricing-button"
            :disabled="loading"
            :class="{ 'active': shop.subscription_status === 'active' && selectedPlan === 'pro' }"
          >
            {{ loading ? 'Обработка...' : 'Выбрать план' }}
          </button>
        </div>
      </div>

      <div class="info-box">
        <h3>Важная информация</h3>
        <ul>
          <li>Пробный период длится 30 дней с момента создания магазина</li>
          <li>После окончания пробного периода магазин будет приостановлен</li>
          <li>Вы можете изменить план в любое время в админке магазина</li>
          <li>Оплата производится ежемесячно</li>
        </ul>
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

const selectPlan = async (plan) => {
  if (plan === 'trial') {
    toast.info('Пробный период уже активен')
    return
  }

  loading.value = true
  selectedPlan.value = plan

  try {
    // Здесь должна быть интеграция с платежной системой
    // Пока просто обновляем статус подписки
    const expiresAt = new Date()
    expiresAt.setMonth(expiresAt.getMonth() + 1) // +1 месяц

    await $fetch(`http://localhost:8000/shop/${shopSlug}/subscription`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: {
        subscription_status: 'active',
        expires_at: expiresAt.toISOString()
      }
    })

    toast.success('Подписка активирована!')
    await refresh()
    
    // Небольшая задержка для обновления данных
    await new Promise(resolve => setTimeout(resolve, 300))
    
    router.push(`/shop/${shopSlug}/admin`)
  } catch (e) {
    toast.error('Ошибка при активации подписки')
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.subscription-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
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
  .pricing-grid {
    grid-template-columns: 1fr;
  }
  
  .pricing-card.featured {
    transform: scale(1);
  }
}
</style>

