<template>
  <div class="shop-admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
          </svg>
        </div>
        <h2 class="sidebar-title">Панель управления</h2>
      </div>
      
      <nav class="sidebar-nav">
        <NuxtLink :to="`/shop/${shopSlug}/admin`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>Товары</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/orders`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Заказы</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
          <span>Категории</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="nav-item active">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <line x1="7" y1="7" x2="7.01" y2="7"></line>
          </svg>
          <span>Бренды</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/banner`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span>Баннер</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/subscription`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <span>Подписка</span>
        </NuxtLink>
      </nav>
      
      <div class="sidebar-footer">
        <NuxtLink :to="`/${shopSlug}`" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>В магазин</span>
        </NuxtLink>
        <button @click="handleLogout" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Выйти</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="admin-main">
      <div class="add-brand-page">
        <div class="page-header">
          <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="back-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Назад
          </NuxtLink>
          <h1 class="page-title">Добавить бренд</h1>
        </div>
        
        <div class="form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="label">Название бренда</label>
          <input v-model="form.name" required class="input" placeholder="например, Ray-Ban" />
        </div>

        <div class="form-group">
          <label class="label">Логотип бренда</label>
          
          <!-- Image Preview -->
          <div v-if="logoUrl" class="image-preview">
            <img :src="logoUrl" alt="Logo preview" />
            <button type="button" @click="logoUrl = ''" class="remove-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- Upload Area -->
          <div v-else class="upload-area">
            <div 
              class="drop-zone"
              :class="{ 'drag-over': isDragging }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p>Перетащите изображение или нажмите для загрузки</p>
              <span class="upload-hint">PNG, JPG до 5MB</span>
            </div>
            <input 
              ref="fileInput" 
              type="file" 
              accept="image/*" 
              @change="handleFileChange" 
              hidden 
            />
            
            <div class="url-input">
              <span class="or-divider">или введите URL</span>
              <input 
                v-model="logoUrl" 
                class="input" 
                placeholder="https://example.com/logo.png" 
              />
            </div>
          </div>
        </div>

        <div class="form-actions">
          <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="btn btn-outline">Отмена</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading || !form.name || !logoUrl">
            {{ loading ? 'Создание...' : 'Создать бренд' }}
          </button>
        </div>
      </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth', 'shop-owner'],
  ssr: false
})

console.log('[Add Brand] Страница загружается...')

const route = useRoute()
const shopSlug = route.params.slug
console.log('[Add Brand] Shop slug:', shopSlug)

const { token, logout } = useAuth()
console.log('[Add Brand] Token:', token.value ? 'есть' : 'нет')

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const toast = useToast()
const loading = ref(false)
const isDragging = ref(false)
const logoUrl = ref('')
const fileInput = ref(null)

onMounted(() => {
  console.log('[Add Brand] Компонент смонтирован')
})

const form = reactive({
  name: ''
})

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (file) {
    await uploadFile(file)
  }
}

const handleDrop = async (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    await uploadFile(file)
  } else {
    toast.error('Пожалуйста, загрузите изображение')
  }
}

const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    console.log('[Add Brand] Загрузка изображения:', file.name)
    const response = await $fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    console.log('[Add Brand] Изображение загружено:', response.url)
    logoUrl.value = response.url
    toast.success('Изображение загружено!')
  } catch (e) {
    console.error('[Add Brand] Ошибка загрузки изображения:', e)
    console.error('[Add Brand] Детали ошибки:', {
      message: e.message,
      statusCode: e.statusCode,
      data: e.data
    })
    toast.error('Ошибка при загрузке изображения')
  }
}

const handleSubmit = async () => {
  if (!form.name || !logoUrl.value) {
    toast.warning('Пожалуйста, заполните все поля')
    return
  }
  
  loading.value = true
  try {
    console.log('[Add Brand] Отправка данных:', { name: form.name, logo_url: logoUrl.value, shop_slug: shopSlug })
    
    const response = await $fetch(`http://localhost:8000/brands?shop_slug=${shopSlug}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        name: form.name,
        logo_url: logoUrl.value
      }
    })
    
    console.log('[Add Brand] Бренд создан успешно:', response)
    toast.success('Бренд успешно создан!')
    navigateTo(`/shop/${shopSlug}/admin/brands`)
  } catch (e) {
    console.error('[Add Brand] Ошибка при создании бренда:', e)
    console.error('[Add Brand] Детали ошибки:', {
      message: e.message,
      statusCode: e.statusCode,
      statusMessage: e.statusMessage,
      data: e.data
    })
    toast.error(e.data?.detail || e.message || 'Ошибка при создании бренда')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

/* Sidebar */
.admin-sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-logo {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.sidebar-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #6B7280;
  text-decoration: none;
  transition: all 0.2s;
  font-weight: 500;
}

.nav-item:hover {
  background: #F9FAFB;
  color: #111;
}

.nav-item.active {
  background: #111;
  color: white;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: #111;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #EF4444;
  background: none;
  border: none;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
  font-family: inherit;
}

.logout-btn:hover {
  color: #DC2626;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
}

.add-brand-page {
  width: 100%;
  padding: 40px;
  background: #FAFAFA;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 32px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  text-decoration: none;
  font-weight: 500;
  margin-bottom: 16px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #111;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.form-card {
  background: white;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

.form-group {
  margin-bottom: 24px;
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  background: #F9FAFB;
  font-size: 1rem;
  transition: all 0.2s;
}

.input:focus {
  outline: none;
  border-color: #111;
  background: white;
}

.upload-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.drop-zone {
  border: 2px dashed #D1D5DB;
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #FAFAFA;
}

.drop-zone:hover {
  border-color: #9CA3AF;
  background: #F3F4F6;
}

.drop-zone.drag-over {
  border-color: #111;
  background: #F0F0F0;
}

.drop-zone svg {
  color: #9CA3AF;
  margin-bottom: 12px;
}

.drop-zone p {
  color: #6B7280;
  font-weight: 500;
  margin: 0 0 4px 0;
}

.upload-hint {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.url-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.or-divider {
  text-align: center;
  color: #9CA3AF;
  font-size: 0.875rem;
}

.image-preview {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 16px;
  overflow: hidden;
  background: #F3F4F6;
  border: 2px solid #E5E7EB;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 16px;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(0,0,0,0.7);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-btn:hover {
  background: #EF4444;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #E5E7EB;
}

.btn {
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #000;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-outline {
  background: transparent;
  border: 2px solid #E5E7EB;
  color: #6B7280;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.btn-outline:hover {
  border-color: #111;
  color: #111;
}

@media (max-width: 1024px) {
  .admin-sidebar {
    width: 240px;
  }
  
  .admin-main {
    margin-left: 240px;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  
  .admin-main {
    margin-left: 0;
  }
  
  .add-brand-page {
    padding: 20px;
  }
  
  .form-card {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
}

</style>
