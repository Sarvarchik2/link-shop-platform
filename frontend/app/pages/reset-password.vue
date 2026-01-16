<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1 class="login-title">{{ $t('auth.reset_password_title') }}</h1>
        </div>

        <form @submit.prevent="handleResetPassword" class="login-form">
          <div class="form-group">
            <label class="form-label">{{ $t('auth.password_label') }}</label>
            <input v-model="password" type="password" required class="form-input"
              :placeholder="$t('auth.password_placeholder')" />
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('auth.reset_password_confirm_placeholder') }}</label>
            <input v-model="confirmPassword" type="password" required class="form-input"
              :placeholder="$t('auth.reset_password_confirm_placeholder')" />
          </div>

          <button type="submit" :disabled="loading" class="btn-submit">
            <span v-if="loading">{{ $t('common.saving') }}</span>
            <span v-else>{{ $t('auth.reset_password_button') }}</span>
          </button>
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
const router = useRouter()
const localePath = useLocalePath()
const toast = useToast()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)

const handleResetPassword = async () => {
  if (loading.value) return
  if (password.value !== confirmPassword.value) {
    toast.error(t('common.error')) // Or a more specific message
    return
  }

  const token = route.query.token as string
  if (!token) {
    toast.error(t('common.error'))
    return
  }

  loading.value = true
  try {
    const config = useRuntimeConfig()
    await $fetch(`${config.public.apiBase}/password-reset/confirm`, {
      method: 'POST',
      body: {
        token: token,
        new_password: password.value
      }
    })
    toast.success(t('auth.reset_password_success'))
    setTimeout(() => {
      router.push(localePath('/login'))
    }, 2000)
  } catch (e: any) {
    console.error('Reset password error:', e)
    let errorMessage = t('common.error')
    if (e?.data?.detail) {
      errorMessage = e.data.detail
    }
    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Same styles as forgot-password or login */
.login-page {
  min-height: 100vh;
  background: #FAFAFA;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 440px;
}

.login-card {
  background: white;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0;
  letter-spacing: -0.02em;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
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

.btn-submit:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
