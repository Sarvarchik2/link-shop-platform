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
      <span class="mobile-title">О магазине</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar 
      :shop-slug="shopSlug" 
      current-route="info"
      :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event"
    />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div>
          <h1 class="admin-title">Информация о магазине</h1>
          <p class="admin-subtitle">Управление контактами и социальными сетями</p>
        </div>
      </div>

      <div class="admin-content">
        <form @submit.prevent="handleSubmit" class="shop-info-form">
          <!-- Basic Info -->
          <div class="form-section">
            <h2 class="section-title">Основная информация</h2>
            <p class="section-description">Название магазина всегда отображается. Если добавлен логотип, он будет показан в навбаре вместо названия.</p>
            
            <div class="form-group">
              <label>Название магазина *</label>
              <input v-model="form.name" type="text" required class="input" placeholder="Название магазина" />
              <small class="help-text">Название магазина отображается, если логотип не загружен</small>
            </div>

            <div class="form-group">
              <label>Описание</label>
              <textarea v-model="form.description" class="input" rows="4" placeholder="Описание магазина"></textarea>
            </div>

            <div class="form-group">
              <label>Логотип магазина</label>
              <div class="logo-upload-container">
                <div class="logo-input-wrapper">
                  <input v-model="form.logo_url" type="url" class="input" placeholder="https://example.com/logo.png" />
                  <span class="input-divider">или</span>
                  <button type="button" class="btn-upload" @click="$refs.logoInput.click()" :disabled="uploading">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    {{ uploading ? 'Загрузка...' : 'Загрузить файл' }}
                  </button>
                  <input 
                    type="file" 
                    ref="logoInput" 
                    style="display: none" 
                    accept="image/*"
                    @change="handleLogoUpload"
                  />
                </div>
                <small class="help-text">Рекомендуемый размер: до 200px по ширине, высота автоматическая.</small>
                
                <div v-if="form.logo_url" class="logo-preview">
                  <div class="preview-header">
                    <span class="preview-label">Предпросмотр:</span>
                    <button type="button" class="btn-remove-logo" @click="form.logo_url = ''">Удалить</button>
                  </div>
                  <img :src="form.logo_url" alt="Логотип" class="preview-image" @error="logoError = true" />
                  <p v-if="logoError" class="preview-error">Ошибка загрузки изображения. Проверьте URL или файл.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Info -->
          <div class="form-section">
            <h2 class="section-title">Контакты</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label>Email</label>
                <input v-model="form.email" type="email" class="input" placeholder="shop@example.com" />
              </div>
              
              <div class="form-group">
                <label>Телефон</label>
                <input v-model="form.phone" type="tel" class="input" placeholder="+998901234567" />
              </div>
            </div>

            <div class="form-group">
              <label>Адрес</label>
              <input v-model="form.address" type="text" class="input" placeholder="Город, улица, дом" />
            </div>
          </div>

          <!-- Social Media -->
          <div class="form-section">
            <h2 class="section-title">Социальные сети</h2>
            <p class="help-text">Введите полные URL-адреса ваших страниц в социальных сетях</p>
            
            <div class="form-group">
              <label>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.169 1.858-.896 6.728-.896 6.728s-.537 3.593-2.351 4.131c-1.815.538-3.785-1.15-4.371-1.705-.293-.278-5.185-3.266-5.185-3.266s-2.023-1.387 1.421-2.738c3.444-1.351 7.377-2.853 7.377-2.853s1.512-.956 2.895.538c1.383 1.494 2.109 3.266 2.109 3.266h.001z"/>
                </svg>
                Telegram
              </label>
              <input v-model="form.telegram" type="url" class="input" placeholder="https://t.me/yourchannel" />
            </div>

            <div class="form-group">
              <label>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 8px;">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                  <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                </svg>
                Instagram
              </label>
              <input v-model="form.instagram" type="url" class="input" placeholder="https://instagram.com/yourpage" />
            </div>

            <div class="form-group">
              <label>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                  <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
                </svg>
                Facebook
              </label>
              <input v-model="form.facebook" type="url" class="input" placeholder="https://facebook.com/yourpage" />
            </div>

            <div class="form-group">
              <label>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                  <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
                </svg>
                Twitter
              </label>
              <input v-model="form.twitter" type="url" class="input" placeholder="https://twitter.com/yourpage" />
            </div>

            <div class="form-group">
              <label>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                WhatsApp
              </label>
              <input v-model="form.whatsapp" type="url" class="input" placeholder="https://wa.me/998901234567" />
            </div>
          </div>

          <div class="form-actions">
            <NuxtLink :to="`/shop/${shopSlug}/admin`" class="btn btn-secondary">Отмена</NuxtLink>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth', 'shop-owner'],
  ssr: false
})

const route = useRoute()
const shopSlug = computed(() => route.params.slug)
const sidebarOpen = ref(false)
const loading = ref(false)
const toast = useToast()
const { token } = useAuth()

const { data: shop, refresh } = await useFetch(`http://localhost:8000/platform/shops/${shopSlug.value}`, {
  key: `shop-data-${shopSlug.value}`,
  server: false
})

const logoError = ref(false)
const uploading = ref(false)

const handleLogoUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validation
  if (!file.type.startsWith('image/')) {
    toast.error('Пожалуйста, выберите изображение')
    return
  }
  
  if (file.size > 2 * 1024 * 1024) {
    toast.error('Размер файла не должен превышать 2МБ')
    return
  }
  
  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await $fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    
    form.logo_url = response.url
    logoError.value = false
    toast.success('Логотип успешно загружен')
  } catch (e) {
    console.error('Upload error:', e)
    toast.error('Ошибка при загрузке логотипа')
  } finally {
    uploading.value = false
    // Clear input
    event.target.value = ''
  }
}

const form = reactive({
  name: '',
  description: '',
  logo_url: '',
  email: '',
  phone: '',
  address: '',
  telegram: '',
  instagram: '',
  facebook: '',
  twitter: '',
  whatsapp: ''
})

// Populate form when shop data loads
watch(shop, (newShop) => {
  if (newShop) {
    form.name = newShop.name || ''
    form.description = newShop.description || ''
    form.logo_url = newShop.logo_url || ''
    form.email = newShop.email || ''
    form.phone = newShop.phone || ''
    form.address = newShop.address || ''
    form.telegram = newShop.telegram || ''
    form.instagram = newShop.instagram || ''
    form.facebook = newShop.facebook || ''
    form.twitter = newShop.twitter || ''
    form.whatsapp = newShop.whatsapp || ''
    logoError.value = false
  }
}, { immediate: true })

// Watch logo_url to reset error state
watch(() => form.logo_url, () => {
  logoError.value = false
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await $fetch(`http://localhost:8000/shop/${shopSlug.value}/admin/info`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: form
    })
    
    toast.success('Информация о магазине успешно обновлена!')
    await refresh()
  } catch (e) {
    console.error('Error updating shop info:', e)
    toast.error(e.data?.detail || 'Ошибка при сохранении информации')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  background: #FAFAFA;
}

.mobile-header {
  display: none;
}

.admin-main {
  margin-left: 280px;
  padding: 40px;
  min-height: 100vh;
}

.admin-header {
  margin-bottom: 32px;
}

.admin-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 8px 0;
}

.admin-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.admin-content {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.shop-info-form {
  max-width: 800px;
}

.form-section {
  margin-bottom: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid #E5E7EB;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
  margin: 0 0 8px 0;
}

.section-description {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #111;
  margin-bottom: 8px;
  font-size: 0.875rem;
}

.form-group label svg {
  display: inline-block;
  vertical-align: middle;
}

.input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  font-family: inherit;
}

.input:focus {
  outline: none;
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

textarea.input {
  resize: vertical;
  min-height: 100px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.help-text {
  font-size: 0.875rem;
  color: #6B7280;
  margin-top: 8px;
  display: block;
}

.logo-upload-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.logo-input-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-direction: column;
}

.input-divider {
  color: #9CA3AF;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

.btn-upload {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  color: #111;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-upload:hover:not(:disabled) {
  border-color: #111;
  background: #F9FAFB;
}

.btn-upload:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.logo-preview {
  margin-top: 16px;
  padding: 20px;
  background: #F9FAFB;
  border-radius: 16px;
  border: 2px dashed #E5E7EB;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.preview-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-remove-logo {
  background: none;
  border: none;
  color: #DC2626;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
}

.btn-remove-logo:hover {
  background: #FEE2E2;
}

.preview-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 600;
}

.preview-image {
  max-height: 80px;
  max-width: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  background: white;
  padding: 12px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.preview-error {
  font-size: 0.75rem;
  color: #DC2626;
  margin-top: 0;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 40px;
  padding-top: 40px;
  border-top: 1px solid #E5E7EB;
}

.btn {
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
  font-size: 1rem;
  text-align: center;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #000;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #F3F4F6;
  color: #111;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

 .form-actions{
    flex-direction: column;
  }
@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 20px;
  }
  
  .mobile-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: white;
    border-bottom: 1px solid #E5E7EB;
    position: sticky;
    top: 0;
    z-index: 1000;
  }
  
  .menu-btn {
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    color: #111;
  }
  
  .mobile-title {
    font-weight: 700;
    font-size: 1.125rem;
  }
  
  .home-btn {
    color: #111;
  }
  
  .admin-content {
    padding: 24px 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 768px) {
  .form-actions{
    flex-direction: row;
  }
  .form-row {
    grid-template-columns: repeat(2, 1fr);
  }
  .logo-input-wrapper{
    flex-direction: row;
  }
}
</style>
