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
          <h1 class="register-title">Регистрация</h1>
          <p class="register-subtitle">Создайте аккаунт и начните делать покупки</p>
          <p class="register-note">Хотите создать магазин? <NuxtLink to="/register-shop" class="register-link">Создать магазин</NuxtLink></p>
        </div>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Имя</label>
              <input 
                v-model="firstName" 
                type="text" 
                required 
                class="form-input" 
                placeholder="Иван" 
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Фамилия</label>
              <input 
                v-model="lastName" 
                type="text" 
                required 
                class="form-input" 
                placeholder="Иванов" 
              />
            </div>
          </div>
          
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
            <span v-if="loading">Регистрация...</span>
            <span v-else>Зарегистрироваться</span>
          </button>
          
          <div class="form-footer">
            <span class="footer-text">Уже есть аккаунт?</span>
            <NuxtLink to="/login" class="footer-link">Войти</NuxtLink>
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

const firstName = ref('')
const lastName = ref('')
const phone = ref('')
const password = ref('')
const loading = ref(false)
const { register } = useAuth()

const handleRegister = async () => {
  if (loading.value) return
  
  if (!phone.value || !password.value || !firstName.value || !lastName.value) {
    useToast().error('Заполните все поля')
    return
  }
  
  loading.value = true
  try {
  await register(phone.value, password.value, firstName.value, lastName.value)
  } catch (e) {
    console.error('Register error details:', e)
    let errorMessage = 'Ошибка при регистрации. Этот номер телефона уже зарегистрирован.'
    
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
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
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
