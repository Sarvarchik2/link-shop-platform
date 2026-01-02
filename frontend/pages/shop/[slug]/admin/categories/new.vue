<template>
  <div class="shop-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">{{ $t('categoriesPage.add') }}</span>
      <NuxtLink :to="`/shop/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" current-route="categories" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="add-category-page">
        <div class="page-header">
          <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="back-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            {{ $t('common.back') }}
          </NuxtLink>
          <h1 class="page-title">{{ $t('categoriesPage.add') }}</h1>
        </div>

        <div class="form-card">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label class="label">{{ $t('categoriesPage.nameLabel') }}</label>
              <input v-model="form.name" required class="input" :placeholder="$t('categoriesPage.namePlaceholder')" />
            </div>

            <div class="form-group">
              <label class="label">{{ $t('categoriesPage.imageLabel') }}</label>

              <!-- Image Preview -->
              <div v-if="imageUrl" class="image-preview">
                <img :src="imageUrl" alt="Category preview" />
                <button type="button" @click="imageUrl = ''" class="remove-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>

              <!-- Upload Area -->
              <div v-else class="upload-area">
                <div class="drop-zone" :class="{ 'drag-over': isDragging }" @dragover.prevent="isDragging = true"
                  @dragleave.prevent="isDragging = false" @drop.prevent="handleDrop" @click="$refs.fileInput.click()">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                  <p>{{ $t('categoriesPage.imageHelp') }}</p>
                  <span class="upload-hint">{{ $t('admin.uploadHint') }}</span>
                </div>
                <input ref="fileInput" type="file" accept="image/*" @change="handleFileChange" hidden />

                <div class="url-input">
                  <span class="or-divider">{{ $t('categoriesPage.orUrl') }}</span>
                  <input v-model="imageUrl" class="input" placeholder="https://example.com/category.png" />
                </div>
              </div>
            </div>

            <div class="form-actions">
              <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="btn btn-outline">{{ $t('common.cancel') }}
              </NuxtLink>
              <button type="submit" class="btn btn-primary" :disabled="loading || !form.name || !imageUrl">
                {{ loading ? $t('admin.creating') : $t('categoriesPage.createBtn') }}
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

console.log('[Add Category] Страница загружается...')

const route = useRoute()
const shopSlug = route.params.slug
console.log('[Add Category] Shop slug:', shopSlug)

const { token } = useAuth()
console.log('[Add Category] Token:', token.value ? 'есть' : 'нет')

const sidebarOpen = ref(false)

const { t } = useI18n()
const toast = useToast()
const loading = ref(false)
const isDragging = ref(false)
const imageUrl = ref('')
const fileInput = ref(null)

onMounted(() => {
  console.log('[Add Category] Компонент смонтирован')
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
    toast.error(t('alerts.shop.imageRequired'))
  }
}

const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  try {
    console.log('[Add Category] Загрузка изображения:', file.name)
    const response = await $fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    console.log('[Add Category] Изображение загружено:', response.url)
    imageUrl.value = response.url
    toast.success(t('alerts.shop.imageUploaded'))
  } catch (e) {
    console.error('[Add Category] Ошибка загрузки изображения:', e)
    console.error('[Add Category] Детали ошибки:', {
      message: e.message,
      statusCode: e.statusCode,
      data: e.data
    })
    toast.error(t('alerts.shop.imageError'))
  }
}

const handleSubmit = async () => {
  if (!form.name || !imageUrl.value) {
    toast.warning(t('alerts.shop.fillAll'))
    return
  }

  loading.value = true
  try {
    console.log('[Add Category] Отправка данных:', { name: form.name, image_url: imageUrl.value, shop_slug: shopSlug })

    const response = await $fetch(`http://localhost:8000/categories?shop_slug=${shopSlug}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        name: form.name,
        image_url: imageUrl.value
      }
    })

    console.log('[Add Category] Категория создана успешно:', response)
    toast.success(t('alerts.shop.categoryCreated'))
    navigateTo(`/shop/${shopSlug}/admin/categories`)
  } catch (e) {
    console.error('[Add Category] Ошибка при создании категории:', e)
    console.error('[Add Category] Детали ошибки:', {
      message: e.message,
      statusCode: e.statusCode,
      statusMessage: e.statusMessage,
      data: e.data
    })
    toast.error(e.data?.detail || e.message || t('common.error'))
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



/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
}

.add-category-page {
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
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
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.7);
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

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }

  .mobile-header {
    display: flex;
  }
}

@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
  }

  .add-category-page {
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
