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
      <span class="mobile-title">{{ $t('bannerPage.title') }}</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" current-route="banner" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <div>
            <h1 class="page-title">{{ $t('bannerPage.title') }}</h1>
            <p class="page-subtitle">{{ $t('bannerPage.subtitle') }}</p>
          </div>
          <button @click="openCreateModal" class="add-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            {{ $t('bannerPage.addBanner') }}
          </button>
        </div>

        <div class="banners-grid">
          <div v-for="banner in bannerList" :key="banner.id" class="banner-card">
            <div class="banner-image">
              <img :src="banner.image_url || '/placeholder.png'" alt="Banner">
              <div class="banner-overlay">
                <span class="banner-badge">{{ banner.badge_text }}</span>
              </div>
            </div>
            <div class="banner-content">
              <h3 class="banner-title">{{ banner.title }}</h3>
              <p class="banner-subtitle">{{ banner.subtitle }}</p>
              <div class="banner-actions">
                <button @click="editBanner(banner)" class="action-btn edit" :title="$t('bannerPage.tooltips.edit')">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button @click="deleteBanner(banner.id)" class="action-btn delete"
                  :title="$t('bannerPage.tooltips.delete')">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div v-if="bannerList.length === 0" class="empty-state">
            <p>{{ $t('bannerPage.noBanners') }}</p>
            <button @click="openCreateModal">{{ $t('bannerPage.createFirst') }}</button>
          </div>
        </div>

        <!-- Modal -->
        <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
          <div class="modal-content">
            <div class="modal-header">
              <h2>{{ isEditing ? $t('bannerPage.editBanner') : $t('bannerPage.createBanner') }}</h2>
              <button @click="closeModal" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
              <!-- Live Preview -->
              <div class="banner-preview-wrapper mb-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('bannerPage.preview') }}</label>
                <div class="banner-preview">
                  <div class="preview-content">
                    <div v-if="form.badge_text" class="preview-badge">{{ form.badge_text }}</div>
                    <h3 class="preview-title"
                      v-html="form[`title_${activeLang}`] ? form[`title_${activeLang}`].replace(/\\n/g, '<br/>') : $t('bannerPage.previewTitle')">
                    </h3>
                    <p class="preview-subtitle">{{ form[`subtitle_${activeLang}`] || $t('bannerPage.previewSubtitle') }}
                    </p>
                    <span class="preview-btn">{{ form[`button_text_${activeLang}`] || $t('bannerPage.previewButton')
                      }}</span>
                  </div>
                  <div class="preview-image">
                    <img :src="form.image_url || '/placeholder.png'" alt="Banner" class="object-cover w-full h-full" />
                  </div>
                </div>
              </div>

              <!-- Language Tabs -->
              <div class="tabs mb-4">
                <button v-for="lang in ['en', 'ru', 'uz']" :key="lang" @click="activeLang = lang"
                  :class="['tab-btn', { active: activeLang === lang }]">
                  {{ lang.toUpperCase() }}
                </button>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label>{{ $t('bannerPage.badgeLabel') }}</label>
                  <input v-model="form.badge_text" type="text" :placeholder="$t('bannerPage.badgePlaceholder')" />
                </div>

                <!-- Multilingual Fields -->
                <div class="form-group full-width">
                  <label>{{ $t('bannerPage.titleLabel') }} ({{ activeLang.toUpperCase() }})</label>
                  <input v-model="form[`title_${activeLang}`]" type="text"
                    :placeholder="$t('bannerPage.titlePlaceholder')" />
                </div>
                <div class="form-group full-width">
                  <label>{{ $t('bannerPage.subtitleLabel') }} ({{ activeLang.toUpperCase() }})</label>
                  <input v-model="form[`subtitle_${activeLang}`]" type="text"
                    :placeholder="$t('bannerPage.subtitlePlaceholder')" />
                </div>
                <div class="form-group full-width">
                  <label>{{ $t('bannerPage.btnTextLabel') }} ({{ activeLang.toUpperCase() }})</label>
                  <input v-model="form[`button_text_${activeLang}`]" type="text"
                    :placeholder="$t('bannerPage.btnTextPlaceholder')" />
                </div>

                <div class="form-group">
                  <label>{{ $t('bannerPage.btnLinkLabel') }}</label>
                  <input v-model="form.button_link" type="text" :placeholder="$t('bannerPage.linkPlaceholder')" />
                </div>
                <div class="form-group full-width">
                  <label>{{ $t('bannerPage.imageUrlLabel') }}</label>
                  <div class="image-upload-wrapper">
                    <input v-model="form.image_url" type="text" placeholder="https://..." class="url-input" />
                    <label class="file-upload-btn">
                      {{ $t('bannerPage.buttons.upload') }}
                      <input type="file" accept="image/*" @change="uploadImage" hidden />
                    </label>
                  </div>
                </div>
                <div class="form-group checkbox-group full-width">
                  <label>
                    <input type="checkbox" v-model="form.is_active" />
                    <span>{{ $t('bannerPage.activeLabel') }}</span>
                  </label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button @click="closeModal" class="cancel-btn">{{ $t('common.cancel') }}</button>
              <button @click="saveBanner" class="save-btn" :disabled="saving">
                <span v-if="saving" class="spinner-small"></span>
                {{ saving ? $t('common.saving') : $t('common.save') }}
              </button>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
const { t } = useI18n()
definePageMeta({
  middleware: ['auth', 'shop-owner'],
  layout: false
})

const route = useRoute()
const shopSlug = route.params.slug
const { token } = useAuth()
const saving = ref(false)
const sidebarOpen = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const toast = useToast()
const activeLang = ref('en')

const form = ref({
  badge_text: '',
  title: '',
  subtitle: '',
  button_text: '',
  button_link: '',
  image_url: '',
  is_active: true
})

// Fetch banners
const { data: banners, refresh } = await useFetch(`${useRuntimeConfig().public.apiBase}/banner?shop_slug=${shopSlug}`, {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

// Ensure banners is always an array
const bannerList = computed(() => banners.value || [])

const openCreateModal = () => {
  isEditing.value = false
  editingId.value = null
  form.value = {
    badge_text: '',
    title: '',
    subtitle: '',
    button_text: '',
    button_link: '',
    image_url: '',
    is_active: true
  }
  showModal.value = true
}

const editBanner = (banner) => {
  isEditing.value = true
  editingId.value = banner.id
  form.value = { ...banner }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const uploadImage = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const result = await $fetch(useRuntimeConfig().public.apiBase + '/upload', {
      method: 'POST',
      body: formData
    })
    form.value.image_url = result.url
    toast.success(t('alerts.shop.imageUploaded'))
  } catch (e) {
    toast.error(t('alerts.shop.imageError'))
  }
}

const saveBanner = async () => {
  saving.value = true
  try {
    if (isEditing.value) {
      // Update
      await $fetch(`${useRuntimeConfig().public.apiBase}/banner/${editingId.value}?shop_slug=${shopSlug}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token.value}` },
        body: form.value
      })
    } else {
      // Create
      await $fetch(`${useRuntimeConfig().public.apiBase}/banner?shop_slug=${shopSlug}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token.value}` },
        body: form.value
      })
    }
    toast.success(t('bannerPage.saved'))
    closeModal()
    refresh()
  } catch (e) {
    if (e.response && e.response.status === 400 && e.response._data.detail.includes('limit reached')) {
      toast.error(t('bannerPage.limitReached'))
    } else {
      toast.error(t('alerts.shop.errorSaving'))
    }
  } finally {
    saving.value = false
  }
}

const deleteBanner = async (id) => {
  if (!confirm(t('bannerPage.confirmDelete'))) return

  try {
    await $fetch(`${useRuntimeConfig().public.apiBase}/banner/${id}?shop_slug=${shopSlug}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    toast.success('Deleted')
    refresh()
  } catch (e) {
    toast.error('Error deleting')
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

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding-top: 80px;
  }

  .mobile-header {
    display: flex;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 6px 0;
}

.page-subtitle {
  color: #6B7280;
  margin: 0;
}

.add-btn {
  background: #111;
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Banners Grid */
.banners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.banner-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #E5E7EB;
  transition: all 0.2s;
}

.banner-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.banner-image {
  height: 160px;
  position: relative;
  background: #f3f4f6;
}

.banner-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-overlay {
  position: absolute;
  top: 12px;
  left: 12px;
}

.banner-badge {
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.banner-content {
  padding: 20px;
}

.banner-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 4px;
  color: #111;
}

.banner-subtitle {
  color: #6B7280;
  font-size: 0.9rem;
  margin-bottom: 16px;
}

.banner-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.edit {
  background: #F3F4F6;
  color: #374151;
}

.action-btn.edit:hover {
  background: #E5E7EB;
}

.action-btn.delete {
  background: #FEE2E2;
  color: #EF4444;
}

.action-btn.delete:hover {
  background: #FECACA;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  grid-column: 1 / -1;
  color: #6B7280;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6B7280;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 0.95rem;
}

.form-group input[type="text"]:focus {
  border-color: #111;
  outline: none;
}

.image-upload-wrapper {
  display: flex;
  gap: 8px;
}

.file-upload-btn {
  background: #F3F4F6;
  border: 2px solid #E5E7EB;
  padding: 0 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
}

.cancel-btn {
  padding: 10px 20px;
  border: none;
  background: transparent;
  font-weight: 600;
  cursor: pointer;
}

.save-btn {
  padding: 10px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-btn:disabled {
  opacity: 0.7;
}

.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

<style scoped>
/* Preview Styles in Modal */
.banner-preview-wrapper {
  margin-bottom: 24px;
}

.banner-preview {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 16px;
  padding: 24px;
  color: white;
  position: relative;
  overflow: hidden;
  height: 200px;
  display: flex;
  align-items: center;
}

.preview-content {
  z-index: 2;
  max-width: 65%;
  position: relative;
}

.preview-badge {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.preview-title {
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 6px;
}

.preview-subtitle {
  font-size: 0.85rem;
  opacity: 0.9;
  margin-bottom: 12px;
}

.preview-btn {
  display: inline-block;
  background: white;
  color: #111;
  padding: 8px 20px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.75rem;
}

.preview-image {
  position: absolute;
  right: -20px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 50%;
  height: 120%;
  opacity: 0.5;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Form Grid */
.tabs {
  display: flex;
  gap: 8px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
}

.tab-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  background: transparent;
  transition: all 0.2s;
}

.tab-btn:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.tab-btn.active {
  background-color: #000;
  color: #fff;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.full-width {
  grid-column: span 2;
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: span 1;
  }
}
</style>
