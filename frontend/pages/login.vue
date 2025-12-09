<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-wrapper">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
          </div>
          <h1 class="login-title">Вход в систему</h1>
          <p class="login-subtitle">Войдите в свой аккаунт</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Номер телефона</label>
            <input 
              v-model="phone" 
              type="tel" 
              required 
              class="form-input" 
              placeholder="+998901234567" 
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Пароль</label>
            <input 
              v-model="password" 
              type="password" 
              required 
              class="form-input" 
              placeholder="••••••••" 
            />
          </div>
          
          <button type="submit" :disabled="loading" class="btn-submit">
            <span v-if="loading">Вход...</span>
            <span v-else>Войти</span>
          </button>
          
          <div class="form-footer">
            <span class="footer-text">Нет аккаунта?</span>
            <NuxtLink to="/register" class="footer-link">Зарегистрироваться</NuxtLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})

const phone = ref('')
const password = ref('')
const loading = ref(false)
const { login } = useAuth()

const handleLogin = async () => {
  if (loading.value) return
  
  if (!phone.value || !password.value) {
    useToast().error('Заполните все поля')
    return
  }
  
  loading.value = true
  try {
  await login(phone.value, password.value)
  } catch (e) {
    console.error('Login error details:', e)
    let errorMessage = 'Неверный номер телефона или пароль'
    
    if (e?.data?.detail) {
      errorMessage = e.data.detail
    } else if (e?.message) {
      errorMessage = e.message
    } else if (e?.statusMessage) {
      errorMessage = e.statusMessage
    }
    
    useToast().error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
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
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.login-header {
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

.login-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0;
  letter-spacing: -0.02em;
}

.login-subtitle {
  font-size: 0.875rem;
  color: #6B7280;
  margin-top: 8px;
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

.btn-submit:hover:not(:disabled) {
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
  .login-card {
    padding: 32px 24px;
  }
  
  .login-title {
    font-size: 2rem;
  }
}
</style>
