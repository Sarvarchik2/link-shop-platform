<template>
  <div class="register-shop-page">
    <div class="container py-8">
      <div class="register-card">
        <h1 class="page-title">Создать магазин</h1>
        <p class="page-subtitle">Зарегистрируйте свой магазин на платформе</p>

        <form @submit.prevent="registerShop" class="register-form">
          <div class="form-group">
            <label for="name">Название магазина *</label>
            <input 
              id="name"
              v-model="form.name" 
              type="text" 
              required
              placeholder="Например: Nike Store"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="slug">URL магазина (slug) *</label>
            <div class="slug-input-wrapper">
              <span class="slug-prefix">link-platform-shop.uz/</span>
              <input 
                id="slug"
                v-model="form.slug" 
                type="text" 
                required
                pattern="[a-z0-9-]+"
                placeholder="nike"
                class="form-input slug-input"
                @input="formatSlug"
              />
            </div>
            <p class="form-hint">Только латинские буквы, цифры и дефисы. Например: nike, adidas-store</p>
          </div>

          <div class="form-group">
            <label for="description">Описание (необязательно)</label>
            <textarea 
              id="description"
              v-model="form.description" 
              rows="4"
              placeholder="Краткое описание вашего магазина"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="logo_url">URL логотипа (необязательно)</label>
            <input 
              id="logo_url"
              v-model="form.logo_url" 
              type="url" 
              placeholder="https://example.com/logo.png"
              class="form-input"
            />
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" :disabled="loading" class="submit-button">
            <span v-if="loading">Создание...</span>
            <span v-else>Создать магазин</span>
          </button>
        </form>

        <div class="info-box">
          <h3>Что дальше?</h3>
          <ul>
            <li>После регистрации вы получите пробный период на 30 дней</li>
            <li>Ваш магазин будет доступен по адресу: <strong>link-platform-shop.uz/{{ form.slug || 'your-slug' }}</strong></li>
            <li>Вы сможете добавлять товары, категории и управлять заказами</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { token, fetchUser } = useAuth()
const router = useRouter()
const toast = useToast()

const form = reactive({
  name: '',
  slug: '',
  description: '',
  logo_url: ''
})

const loading = ref(false)
const error = ref('')

const formatSlug = () => {
  form.slug = form.slug
    .toLowerCase()
    .replace(/[^a-z0-9-]/g, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

const registerShop = async () => {
  if (!token.value) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = ''

  try {
    const data = await $fetch('http://localhost:8000/platform/shops/register', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: form
    })

    // Обновить данные пользователя после создания магазина
    await fetchUser()
    
    // Небольшая задержка для обновления данных на сервере
    await new Promise(resolve => setTimeout(resolve, 500))

    toast.success('Магазин успешно создан!')
    router.push(`/shop/${data.slug}/admin`)
  } catch (e) {
    error.value = e.data?.detail || 'Ошибка при создании магазина'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-shop-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.register-card {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 24px;
  padding: 48px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.page-title {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 8px;
  color: #111;
}

.page-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 32px;
}

.register-form {
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #111;
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #111;
}

.slug-input-wrapper {
  display: flex;
  align-items: center;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  overflow: hidden;
}

.slug-prefix {
  padding: 12px 16px;
  background: #F9FAFB;
  color: #666;
  font-size: 0.875rem;
  white-space: nowrap;
}

.slug-input {
  border: none;
  flex: 1;
  border-radius: 0;
}

.slug-input-wrapper:focus-within {
  border-color: #111;
}

.form-hint {
  font-size: 0.75rem;
  color: #666;
  margin-top: 4px;
}

.error-message {
  background: #FEE2E2;
  color: #991B1B;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 16px;
  font-size: 0.875rem;
}

.submit-button {
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-button:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.info-box {
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
  content: '✓';
  position: absolute;
  left: 0;
  color: #10B981;
  font-weight: 700;
}

.info-box strong {
  color: #111;
  font-weight: 700;
}

@media (max-width: 768px) {
  .register-card {
    padding: 32px 24px;
    border-radius: 16px;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>

