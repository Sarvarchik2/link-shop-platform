<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <div class="logo-wrapper">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
          </div>
          <h1 class="register-title">{{ $t('auth.register_title') }}</h1>
          <p class="register-subtitle">{{ $t('auth.register_subtitle') }}</p>
          <p class="register-note">{{ $t('auth.shop_promo') }} <NuxtLink to="/register-shop" class="register-link">{{
            $t('auth.create_shop_link') }}</NuxtLink>
          </p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">{{ $t('auth.first_name_label') }}</label>
              <input v-model="firstName" type="text" required class="form-input"
                :placeholder="$t('auth.name_placeholder')" />
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('auth.last_name_label') }}</label>
              <input v-model="lastName" type="text" required class="form-input"
                :placeholder="$t('auth.lastname_placeholder')" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('auth.phone_label') }}</label>
            <input v-model="phone" type="tel" required class="form-input" :placeholder="$t('auth.phone_placeholder')" />
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('auth.password_label') }}</label>
            <input v-model="password" type="password" required class="form-input"
              :placeholder="$t('auth.password_placeholder')" />
          </div>

          <button type="submit" :disabled="loading" class="btn-submit">
            <span v-if="loading">{{ $t('auth.registering') }}</span>
            <span v-else>{{ $t('auth.register_button') }}</span>
          </button>

          <div class="form-footer">
            <span class="footer-text">{{ $t('auth.have_account') }}</span>
            <NuxtLink :to="loginLink" class="footer-link">{{ $t('auth.login_link_text') }}</NuxtLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
})

const { t } = useI18n()
const route = useRoute()
const firstName = ref('')
const lastName = ref('')
const phone = ref('')
const password = ref('')
const loading = ref(false)
const { register } = useAuth()
const toast = useToast()

const storageReturnUrl = ref<string | null>(null)

// Save returnUrl when page loads
onMounted(() => {
  let returnUrl: string | null = null;

  if (Array.isArray(route.query.returnUrl)) {
    returnUrl = route.query.returnUrl[0] || null
  } else if (typeof route.query.returnUrl === 'string') {
    returnUrl = route.query.returnUrl
  }

  if (returnUrl) {
    localStorage.setItem('returnUrl', returnUrl)
  } else {
    // If no returnUrl in query, check if we came from a shop page
    // by checking saved shop context
    const { getShopSlug } = useShopContext()
    const shopSlug = getShopSlug()
    if (shopSlug) {
      // User came from a shop, save shop home as returnUrl
      localStorage.setItem('returnUrl', `/${shopSlug}`)
    } else {
      // User came from platform, save platform home
      localStorage.setItem('returnUrl', '/')
    }
  }

  // Update reactive state from localStorage after mount
  storageReturnUrl.value = localStorage.getItem('returnUrl')
})

// Preserve returnUrl when linking to login
const loginLink = computed(() => {
  let queryReturnUrl: string | null = null;

  if (Array.isArray(route.query.returnUrl)) {
    queryReturnUrl = route.query.returnUrl[0] || null
  } else if (typeof route.query.returnUrl === 'string') {
    queryReturnUrl = route.query.returnUrl
  }

  const returnUrl = queryReturnUrl || storageReturnUrl.value
  if (returnUrl) {
    return `/login?returnUrl=${encodeURIComponent(returnUrl)}`
  }
  return '/login'
})

const handleRegister = async () => {
  if (loading.value) return

  if (!phone.value || !password.value || !firstName.value || !lastName.value) {
    toast.error(t('auth.validation.required'))
    return
  }

  loading.value = true
  try {
    await register(phone.value, password.value, firstName.value, lastName.value)
  } catch (e: any) {
    console.error('Register error details:', e)
    let errorMessage = t('auth.validation.register_error')

    if (e?.data?.detail) {
      errorMessage = e.data.detail
    } else if (e?.message) {
      errorMessage = e.message
    } else if (e?.statusMessage) {
      errorMessage = e.statusMessage
    }

    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: #FAFAFA;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 540px;
}

.register-card {
  background: white;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-wrapper {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
}

.register-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.register-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0 0 8px 0;
}

.register-note {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0;
}

.register-link {
  color: #111;
  font-weight: 600;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  letter-spacing: 0.025em;
}

.form-input {
  padding: 16px 20px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #F9FAFB;
  color: #111;
}

.form-input::placeholder {
  color: #9CA3AF;
}

.form-input:focus {
  outline: none;
  border-color: #111;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

.btn-submit {
  padding: 18px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 8px;
}

.btn-submit:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  text-align: center;
  margin-top: 8px;
}

.footer-text {
  color: #6B7280;
  font-size: 0.875rem;
}

.footer-link {
  color: #111;
  font-weight: 600;
  margin-left: 4px;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .register-card {
    padding: 32px 24px;
  }

  .register-title {
    font-size: 2rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
