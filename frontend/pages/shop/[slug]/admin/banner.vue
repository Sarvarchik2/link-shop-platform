<template>
  <div class="shop-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">Баннер</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar 
      :shop-slug="shopSlug"
      current-route="banner"
      v-model="sidebarOpen"
    />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">Баннер</h1>
          <p class="page-subtitle">Настройка баннера магазина</p>
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
const { token } = useAuth()
const saving = ref(false)
const sidebarOpen = ref(false)

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

/* Mobile Header */
.mobile-header {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
  z-index: 1000;
}

.menu-btn,
.home-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  color: #111;
  transition: all 0.2s;
}

.menu-btn:hover,
.home-btn:hover {
  background: #111;
  color: white;
}

.mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 280px;
  padding: 40px;
  min-height: 100vh;
  background: #fafafa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.95rem;
  color: #6B7280;
  margin: 0;
}

.admin-content {
  padding: 0;
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
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 40px rgba(0,0,0,0.02);
  border: 1px solid #f1f1f1;
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
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 40px rgba(0,0,0,0.02);
  border: 1px solid #f1f1f1;
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
  .admin-main {
    margin-left: 0;
    padding: 64px 0 0 0;
    width: 100%;
    min-width: 0;
  }
  
  .container {
    padding: 0;
  }

  .page-header {
    background: white;
    padding: 12px 16px;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
  }

  .page-title, 
  .page-subtitle {
    display: none;
  }

  .mobile-header {
    display: flex;
  }
  
  .banner-editor {
    grid-template-columns: 1fr;
    padding: 0 16px 40px;
    gap: 20px;
  }

  .preview-section {
    order: 2;
  }

  .form-section {
    order: 1;
  }
}

@media (max-width: 768px) {
  .admin-content {
    padding: 0;
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
@keyframes spin { to { transform: rotate(360deg); } }
.btn-spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}
</style>

