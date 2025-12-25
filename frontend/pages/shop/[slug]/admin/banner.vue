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
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <line x1="7" y1="7" x2="7.01" y2="7"></line>
          </svg>
          <span>Бренды</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/banner`" class="nav-item active">
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
      <div class="admin-header">
        <div>
          <h1 class="admin-title">Баннер</h1>
          <p class="admin-subtitle">Настройка баннера магазина</p>
        </div>
      </div>

      <div class="admin-content">
        <div class="banner-editor">
          <!-- Preview -->
          <div class="preview-section">
            <h2 class="section-title">Предпросмотр</h2>
            <div class="banner-preview">
              <div class="preview-content">
                <div class="preview-badge">{{ form.badge_text }}</div>
                <h3 class="preview-title" v-html="form.title.replace(/\\n/g, '<br/>')"></h3>
                <p class="preview-subtitle">{{ form.subtitle }}</p>
                <span class="preview-btn">{{ form.button_text }}</span>
              </div>
              <div class="preview-image">
                <img :src="form.image_url || '/placeholder.png'" alt="Banner" />
              </div>
            </div>
          </div>

          <!-- Form -->
          <div class="form-section">
            <h2 class="section-title">Редактирование баннера</h2>
            
            <div class="form-group">
              <label>Текст бейджа</label>
              <input v-model="form.badge_text" type="text" placeholder="НОВИНКА" />
            </div>

            <div class="form-group">
              <label>Заголовок (\n для новой строки)</label>
              <input v-model="form.title" type="text" placeholder="Ray-Ban Meta Smart Glasses" />
            </div>

            <div class="form-group">
              <label>Подзаголовок</label>
              <input v-model="form.subtitle" type="text" placeholder="$299 от" />
            </div>

            <div class="form-group">
              <label>Текст кнопки</label>
              <input v-model="form.button_text" type="text" placeholder="Купить" />
            </div>

            <div class="form-group">
              <label>Ссылка кнопки</label>
              <input v-model="form.button_link" type="text" placeholder="/products" />
            </div>

            <div class="form-group">
              <label>URL изображения</label>
              <input v-model="form.image_url" type="text" placeholder="https://..." />
            </div>

            <div class="form-group">
              <label>Или загрузите изображение</label>
              <input type="file" accept="image/*" @change="uploadImage" />
            </div>

            <div class="form-group checkbox-group">
              <label>
                <input type="checkbox" v-model="form.is_active" />
                <span>Баннер активен</span>
              </label>
            </div>

            <button @click="saveBanner" class="save-btn" :disabled="saving">
              {{ saving ? 'Сохранение...' : 'Сохранить баннер' }}
            </button>
          </div>
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
const { token, logout } = useAuth()
const saving = ref(false)

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const form = ref({
  badge_text: '',
  title: '',
  subtitle: '',
  button_text: '',
  button_link: '',
  image_url: '',
  is_active: true
})

// Fetch current banner
const { data: banner } = await useFetch(`http://localhost:8000/banner?shop_slug=${shopSlug}`, {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

watch(banner, (newBannerArray) => {
  if (newBannerArray && newBannerArray.length > 0) {
    const newBanner = newBannerArray[0]
    form.value = {
      badge_text: newBanner.badge_text || '',
      title: newBanner.title || '',
      subtitle: newBanner.subtitle || '',
      button_text: newBanner.button_text || '',
      button_link: newBanner.button_link || '',
      image_url: newBanner.image_url || '',
      is_active: newBanner.is_active ?? true
    }
  }
}, { immediate: true })

const uploadImage = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const result = await $fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    form.value.image_url = result.url
    useToast().success('Изображение загружено!')
  } catch (e) {
    useToast().error('Ошибка при загрузке изображения')
  }
}

const saveBanner = async () => {
  saving.value = true
  try {
    await $fetch(`http://localhost:8000/banner?shop_slug=${shopSlug}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: form.value
    })
    useToast().success('Баннер сохранен!')
  } catch (e) {
    useToast().error('Ошибка при сохранении баннера')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

/* Sidebar - same as orders.vue */
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

.admin-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 48px 40px;
}

.admin-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 8px;
}

.admin-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
}

.admin-content {
  padding: 40px;
}

.banner-editor {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #374151;
}

/* Preview Section */
.preview-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
}

.banner-preview {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 24px;
  padding: 40px;
  color: white;
  position: relative;
  overflow: hidden;
  min-height: 300px;
  display: flex;
  align-items: center;
}

.preview-content {
  z-index: 2;
  max-width: 60%;
}

.preview-badge {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 16px;
  border: 1px solid rgba(255,255,255,0.2);
  letter-spacing: 1px;
}

.preview-title {
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 12px;
}

.preview-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 24px;
}

.preview-btn {
  display: inline-block;
  background: white;
  color: #111;
  padding: 14px 32px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.875rem;
}

.preview-image {
  position: absolute;
  right: -30px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 45%;
  height: 110%;
  opacity: 0.4;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Form Section */
.form-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-group input[type="text"],
.form-group input[type="file"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.form-group input[type="text"]:focus {
  outline: none;
  border-color: #111;
}

.form-group input[type="file"] {
  padding: 10px;
  background: #F9FAFB;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #111;
}

.save-btn {
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

.save-btn:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .admin-sidebar {
    width: 240px;
  }
  
  .admin-main {
    margin-left: 240px;
  }
  
  .banner-editor {
    grid-template-columns: 1fr;
  }

  .preview-section {
    order: 2;
  }

  .form-section {
    order: 1;
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
  
  .admin-title {
    font-size: 1.5rem;
  }

  .banner-preview {
    padding: 24px;
    min-height: 220px;
  }

  .preview-content {
    max-width: 70%;
  }

  .preview-title {
    font-size: 1.5rem;
  }

  .preview-subtitle {
    font-size: 0.875rem;
  }

  .preview-btn {
    padding: 10px 24px;
    font-size: 0.75rem;
  }

  .preview-image {
    opacity: 0.2;
  }
}
</style>

