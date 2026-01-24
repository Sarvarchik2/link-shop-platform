<template>
  <div class="register-shop-premium">
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <div class="register-container">
      <header class="register-header">
        <NuxtLink :to="localePath('/')" class="logo-link">
          <span class="logo-text">Store<span>ly</span></span>
        </NuxtLink>
        <div class="header-steps">
          <div class="step-indicator" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
            <span class="step-num">1</span>
            <span class="step-name">{{ $t('shopRegistration.premium.step1') }}</span>
          </div>
          <div class="step-line" :class="{ completed: currentStep > 1 }"></div>
          <div class="step-indicator" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
            <span class="step-num">2</span>
            <span class="step-name">{{ $t('shopRegistration.premium.step2') }}</span>
          </div>
        </div>
      </header>

      <div class="register-content">
        <!-- Step 1: Shop Info -->
        <div v-if="currentStep === 1" class="step-view fade-in">
          <div class="text-center mb-10">
            <h1 class="title">{{ $t('shopRegistration.premium.title') }}</h1>
            <p class="subtitle">{{ $t('shopRegistration.premium.subtitle') }}</p>
          </div>

          <form @submit.prevent="currentStep = 2" class="premium-form">
            <div class="form-group">
              <label>{{ $t('shopRegistration.premium.shopName') }}</label>
              <div class="input-wrapper">
                <iconify-icon icon="lucide:shopping-bag" class="input-icon"></iconify-icon>
                <input v-model="form.name" type="text" required
                  :placeholder="$t('shopRegistration.form.namePlaceholder')" class="premium-input" />
              </div>
            </div>

            <div class="form-group">
              <label>{{ $t('shopRegistration.premium.shopUrl') }}</label>
              <div class="input-wrapper slug-wrapper">
                <span class="url-prefix">storely.uz/</span>
                <input v-model="form.slug" type="text" required placeholder="urban-style"
                  class="premium-input slug-input" @input="formatSlug" />
              </div>
              <p class="hint">{{ $t('shopRegistration.premium.urlHint') }}</p>
            </div>

            <div class="form-group">
              <label>{{ $t('shopRegistration.premium.description') || $t('shopRegistration.form.desc') }} ({{
                $t('common.optional') }})</label>
              <textarea v-model="form.description" rows="3" :placeholder="$t('shopRegistration.form.descPlaceholder')"
                class="premium-input"></textarea>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-next" :disabled="!form.name || !form.slug">
                {{ $t('shopRegistration.premium.continue') }}
                <iconify-icon icon="lucide:arrow-right"></iconify-icon>
              </button>
            </div>
          </form>
        </div>

        <!-- Step 2: Plan Selection -->
        <div v-else-if="currentStep === 2" class="step-view fade-in">
          <div class="text-center mb-10">
            <h1 class="title">{{ $t('shopRegistration.premium.selectPlan') }}</h1>
            <p class="subtitle">{{ $t('shopRegistration.premium.selectPlanSubtitle') }}</p>
          </div>

          <div v-if="plansPending" class="loading-plans">
            <div class="spinner"></div>
          </div>

          <div v-else class="plans-grid">
            <div v-for="plan in plans" :key="plan.id" class="plan-card"
              :class="{ featured: plan.slug === 'premium', selected: selectedPlan?.id === plan.id }"
              @click="selectedPlan = plan">
              <div v-if="plan.slug === 'premium'" class="popular-badge">{{ $t('shopRegistration.premium.popular') }}
              </div>
              <div class="plan-header">
                <h3 class="plan-name">{{ getLocalizedValue(plan, 'name') }}</h3>
                <div class="plan-price">
                  <span class="amount">{{ formatPrice(plan.price) }}</span>
                  <span class="period">/{{ $t('home.pricing.month') }}</span>
                </div>
              </div>
              <div class="plan-desc">{{ getLocalizedValue(plan, 'description') }}</div>
              <ul class="plan-features">
                <li v-for="(f, i) in getLocalizedFeatures(plan)" :key="i">
                  <iconify-icon icon="lucide:check" class="check"></iconify-icon>
                  <span>{{ f }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="form-actions mt-10">
            <button @click="currentStep = 1" class="btn-back">
              <iconify-icon icon="lucide:arrow-left"></iconify-icon>
              {{ $t('shopRegistration.back') }}
            </button>
            <button @click="registerShop" class="btn-submit" :disabled="loading || !selectedPlan">
              <span v-if="loading" class="spinner-small"></span>
              <span v-else>{{ $t('shopRegistration.premium.launch') }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { token, user } = useAuth()
const config = useRuntimeConfig()
const router = useRouter()
const toast = useToast()
const { locale } = useI18n()
const { formatPrice } = useCurrency()
const localePath = useLocalePath()

const currentStep = ref(1)
const loading = ref(false)
const selectedPlan = ref(null)

const form = reactive({
  name: '',
  slug: '',
  description: '',
  logo_url: ''
})

// Fetch Plans
const { data: plans, pending: plansPending } = await useFetch(config.public.apiBase + '/subscription-plans', {
  server: false,
  transform: (data) => data?.filter(p => p.is_active)?.sort((a, b) => (a.display_order || 0) - (b.display_order || 0)) || []
})

const formatSlug = () => {
  form.slug = form.slug.toLowerCase().replace(/[^a-z0-9-]/g, '').replace(/-+/g, '-').replace(/^-|-$/g, '')
}

const getLocalizedValue = (obj, key) => obj[`${key}_${locale.value}`] || obj[key] || ''
const getLocalizedFeatures = (plan) => {
  const str = plan[`features_${locale.value}`] || plan.features || ''
  return str.split(',').map(s => s.trim()).filter(Boolean)
}

const registerShop = async () => {
  if (!selectedPlan.value) return
  loading.value = true

  try {
    const data = await $fetch(`${config.public.apiBase}/platform/shops/register`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { ...form, subscription_plan_id: selectedPlan.value.id }
    })

    toast.success('Магазин успешно создан!')
    // Redirect to subscription activation page
    router.push(localePath(`/shop/${data.slug}/admin/settings/subscription?activated=true`))
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка создания магазина')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-shop-premium {
  min-height: 100vh;
  background: #ffffff;
  color: #09090b;
  position: relative;
  overflow: hidden;
  padding: 40px 20px;
}

.background-blobs {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.blob {
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(228, 228, 231, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(80px);
}

.blob-1 {
  top: -200px;
  right: -100px;
}

.blob-2 {
  bottom: -200px;
  left: -100px;
  background: radial-gradient(circle, rgba(244, 244, 245, 0.4) 0%, transparent 70%);
}

.register-container {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 10;
}

.register-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 60px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: -1px;
  color: #09090b;
}

.logo-text span {
  color: #71717a;
}

.header-steps {
  display: flex;
  align-items: center;
  gap: 20px;
}

.step-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  opacity: 0.4;
  transition: all 0.3s;
}

.step-indicator.active {
  opacity: 1;
}

.step-indicator.completed {
  color: #22c55e;
  opacity: 1;
}

.step-num {
  width: 28px;
  height: 28px;
  background: #f4f4f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  border: 1px solid #e4e4e7;
}

.step-indicator.active .step-num {
  background: #09090b;
  color: white;
  border-color: #09090b;
}

.step-indicator.completed .step-num {
  background: #22c55e;
  color: white;
  border-color: #22c55e;
}

.step-name {
  font-size: 0.9rem;
  font-weight: 600;
}

.step-line {
  width: 40px;
  height: 2px;
  background: #e4e4e7;
  border-radius: 2px;
}

.step-line.completed {
  background: #22c55e;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -1.5px;
  margin-bottom: 12px;
  color: #09090b;
}

.subtitle {
  color: #71717a;
  font-size: 1.1rem;
}

/* Form Styles */
.premium-form {
  background: white;
  border: 1px solid #e4e4e7;
  border-radius: 24px;
  padding: 48px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #52525b;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  color: #a1a1aa;
}

.premium-input {
  width: 100%;
  background: #fafafa;
  border: 1.5px solid #e4e4e7;
  border-radius: 12px;
  padding: 14px 16px 14px 44px;
  color: #09090b;
  font-size: 1rem;
  transition: all 0.2s;
}

.premium-input:focus {
  border-color: #09090b;
  background: white;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.slug-wrapper .premium-input {
  padding-left: 95px;
  font-family: monospace;
  font-weight: 600;
  color: #09090b;
}

.url-prefix {
  position: absolute;
  left: 16px;
  color: #71717a;
  font-size: 0.9rem;
}

textarea.premium-input {
  padding-left: 16px;
  resize: vertical;
  min-height: 80px;
}

.hint {
  font-size: 0.75rem;
  color: #a1a1aa;
  margin-top: 8px;
  margin-left: 4px;
}

/* Plans Grid */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.plan-card {
  background: white;
  border: 1.5px solid #e4e4e7;
  border-radius: 20px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.plan-card:hover {
  border-color: #a1a1aa;
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.plan-card.selected {
  border-color: #09090b;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.plan-card.featured {
  border-color: #71717a;
}

.plan-card.featured.selected {
  border-color: #09090b;
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #09090b;
  color: white;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
}

.plan-header {
  margin-bottom: 20px;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 8px;
  color: #09090b;
}

.plan-price .amount {
  font-size: 1.75rem;
  font-weight: 900;
  color: #09090b;
}

.plan-price .period {
  color: #71717a;
  font-size: 0.9rem;
}

.plan-desc {
  color: #71717a;
  font-size: 0.9rem;
  margin-bottom: 24px;
  line-height: 1.5;
}

.plan-features {
  list-style: none;
  padding: 0;
}

.plan-features li {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  font-size: 0.9rem;
  color: #52525b;
}

.check {
  color: #22c55e;
  margin-top: 3px;
}

/* Buttons */
.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

.btn-next,
.btn-submit {
  padding: 0 32px;
  height: 56px;
  background: #09090b;
  color: white;
  border-radius: 14px;
  border: none;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-submit {
  background: #09090b;
  color: white;
  width: auto;
}

.btn-next:hover,
.btn-submit:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-next:disabled,
.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-back {
  background: white;
  border: 1.5px solid #e4e4e7;
  color: #09090b;
  padding: 0 24px;
  border-radius: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
}

.btn-back:hover {
  border-color: #09090b;
  background: #fafafa;
}

.fade-in {
  animation: fadeIn 0.4s ease-out;
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
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-plans {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e4e4e7;
  border-top-color: #09090b;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .register-shop-premium {
    padding: 20px 16px;
  }

  .title {
    font-size: 1.8rem;
    line-height: 1.2;
  }

  .subtitle {
    font-size: 1rem;
  }

  .premium-form {
    padding: 24px;
    border-radius: 20px;
  }

  .register-header {
    flex-direction: column;
    gap: 24px;
    margin-bottom: 40px;
  }

  .header-steps {
    width: 100%;
    justify-content: center;
  }

  .step-name {
    display: none;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn-next,
  .btn-submit,
  .btn-back {
    width: 100%;
    justify-content: center;
  }

  .plans-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .plan-card {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.9rem;
  }

  .premium-form {
    padding: 20px;
  }

  .form-group label {
    font-size: 0.85rem;
  }

  .premium-input {
    font-size: 0.9rem;
    padding: 12px 14px 12px 40px;
  }

  .slug-wrapper .premium-input {
    padding-left: 90px;
    font-size: 0.85rem;
  }

  .url-prefix {
    font-size: 0.85rem;
  }

  .btn-next,
  .btn-submit,
  .btn-back {
    height: 48px;
    font-size: 0.9rem;
  }

  .plan-name {
    font-size: 1.25rem;
  }

  .plan-price .amount {
    font-size: 1.5rem;
  }
}
</style>
