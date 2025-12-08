<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1 class="login-title">Admin kirish</h1>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Foydalanuvchi nomi</label>
            <input 
              v-model="username" 
              type="text" 
              required 
              class="form-input" 
              placeholder="Foydalanuvchi nomini kiriting"
              autocomplete="username"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Parol</label>
            <input 
              v-model="password" 
              type="password" 
              required 
              class="form-input" 
              placeholder="Parolni kiriting"
              autocomplete="current-password"
            />
          </div>
          
          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading">Boshqaruv paneliga kirish</span>
            <span v-else class="loading-spinner">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              </svg>
            </span>
          </button>
        </form>
        
        <div class="form-footer">
          <NuxtLink to="/" class="footer-link">
            ← Do'konga qaytish
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})

const username = ref('')
const password = ref('')
const loading = ref(false)
const { login, user, token } = useAuth()

const handleLogin = async () => {
  loading.value = true
  try {
    await login(username.value, password.value, false)
    
    if (user.value && user.value.role === 'admin') {
      useToast().success('Xush kelibsiz!')
      navigateTo('/admin')
    } else {
      useToast().error('Kirish rad etildi. Admin huquqlari talab qilinadi.')
      token.value = null
      user.value = null
    }
  } catch (e) {
    console.error(e)
    useToast().error('Noto\'g\'ri foydalanuvchi nomi yoki parol')
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
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
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.form-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #E5E7EB;
}

.footer-link {
  color: #111;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.2s;
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
