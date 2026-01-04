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
      <span class="mobile-title">{{ $t('shopSettings.title') }}</span>
      <NuxtLink :to="`/${shopSlug}`" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" current-route="info" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">{{ $t('shopSettings.infoTitle') }}</h1>
          <p class="page-subtitle">{{ $t('shopSettings.infoSubtitle') }}</p>
        </div>

        <div class="admin-content">
          <form @submit.prevent="handleSubmit" class="shop-info-form">
            <!-- Basic Info -->
            <div class="form-section">
              <h2 class="section-title">{{ $t('shopSettings.basicInfo') }}</h2>

              <div class="form-group">
                <label class="form-label">{{ $t('shopSettings.shopName') }} *</label>
                <input v-model="form.name" type="text" required class="form-input"
                  :placeholder="$t('shopSettings.placeholders.name')" />
                <p class="form-help">{{ $t('shopSettings.hints.name') }}</p>
              </div>

              <div class="form-group">
                <label class="form-label">{{ $t('shopSettings.description') }}</label>
                <textarea v-model="form.description" class="form-input" rows="4"
                  :placeholder="$t('shopSettings.placeholders.description')"></textarea>
              </div>

              <div class="form-group">
                <label class="form-label">{{ $t('shopSettings.logo') }}</label>
                <div class="logo-area">
                  <div class="logo-preview-box" :class="{ 'has-logo': form.logo_url }">
                    <template v-if="form.logo_url">
                      <img :src="form.logo_url" alt="Logo" class="logo-img" @error="logoError = true" />
                      <button type="button" class="logo-remove-btn" @click="form.logo_url = ''"
                        :title="$t('shopSettings.tooltips.remove')">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2.5">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </template>
                    <div v-else class="logo-empty" @click="$refs.logoInput.click()">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <circle cx="8.5" cy="8.5" r="1.5"></circle>
                        <polyline points="21 15 16 10 5 21"></polyline>
                      </svg>
                      <span>{{ $t('shopSettings.uploadLogo') }}</span>
                    </div>
                  </div>

                  <div class="logo-actions">
                    <div class="url-input-container">
                      <input v-model="form.logo_url" type="url" class="form-input-small"
                        :placeholder="$t('shopSettings.placeholders.logoUrl')" />
                      <button type="button" class="btn-file-upload" @click="$refs.logoInput.click()"
                        :disabled="uploading">
                        {{ uploading ? '...' : $t('shopSettings.buttons.file') }}
                      </button>
                    </div>
                    <p class="form-help">{{ $t('shopSettings.hints.logoSize') }}</p>
                  </div>
                  <input type="file" ref="logoInput" style="display: none" accept="image/*"
                    @change="handleLogoUpload" />
                </div>
                <p v-if="logoError" class="error-msg">{{ $t('shopSettings.errors.logoUpload') }}</p>
              </div>
            </div>

            <!-- Contact Info -->
            <div class="form-section">
              <h2 class="section-title">{{ $t('shopSettings.contacts') }}</h2>

              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">{{ $t('shopSettings.email') }}</label>
                  <input v-model="form.email" type="email" class="form-input" placeholder="hello@shop.com" />
                </div>

                <div class="form-group">
                  <label class="form-label">{{ $t('shopSettings.phone') }}</label>
                  <input v-model="form.phone" type="tel" class="form-input" placeholder="+998 90 123 45 67" />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">{{ $t('shopSettings.address') }}</label>
                <input v-model="form.address" type="text" class="form-input"
                  :placeholder="$t('shopSettings.placeholders.address')" />
              </div>
            </div>

            <!-- Social Media -->
            <div class="form-section last">
              <h2 class="section-title">{{ $t('shopSettings.socials') }}</h2>

              <div class="social-grid">
                <div class="social-input-group">
                  <div class="social-label">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path
                        d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.169 1.858-.896 6.728-.896 6.728s-.537 3.593-2.351 4.131c-1.815.538-3.785-1.15-4.371-1.705-.293-.278-5.185-3.266-5.185-3.266s-2.023-1.387 1.421-2.738c3.444-1.351 7.377-2.853 7.377-2.853s1.512-.956 2.895.538c1.383 1.494 2.109 3.266 2.109 3.266h.001z" />
                    </svg>
                    <span>Telegram</span>
                  </div>
                  <input v-model="form.telegram" type="url" class="form-input" placeholder="https://t.me/..." />
                </div>

                <div class="social-input-group">
                  <div class="social-label">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                    </svg>
                    <span>Instagram</span>
                  </div>
                  <input v-model="form.instagram" type="url" class="form-input"
                    placeholder="https://instagram.com/..." />
                </div>

                <div class="social-input-group">
                  <div class="social-label">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
                    </svg>
                    <span>Facebook</span>
                  </div>
                  <input v-model="form.facebook" type="url" class="form-input" placeholder="https://facebook.com/..." />
                </div>

                <div class="social-input-group">
                  <div class="social-label">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path
                        d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z" />
                    </svg>
                    <span>Twitter</span>
                  </div>
                  <input v-model="form.twitter" type="url" class="form-input" placeholder="https://twitter.com/..." />
                </div>

                <div class="social-input-group">
                  <div class="social-label">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path
                        d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                    </svg>
                    <span>WhatsApp</span>
                  </div>
                  <input v-model="form.whatsapp" type="url" class="form-input" placeholder="https://wa.me/..." />
                </div>
              </div>
            </div>

            <div class="form-footer">
              <NuxtLink :to="`/shop/${shopSlug}/admin`" class="btn-cancel">{{ $t('common.cancel') }}</NuxtLink>
              <button type="submit" class="btn-save" :disabled="loading">
                <span v-if="loading" class="btn-spinner"></span>
                {{ loading ? $t('common.saving') : $t('shopSettings.save') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t } = useI18n()
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

const { data: shop, refresh } = await useFetch(`${useRuntimeConfig().public.apiBase}/platform/shops/${shopSlug.value}`, {
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
    toast.error(t('alerts.shop.logoRequired'))
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    toast.error(t('alerts.shop.fileSize'))
    return
  }

  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await $fetch(useRuntimeConfig().public.apiBase + '/upload', {
      method: 'POST',
      body: formData
    })

    form.logo_url = response.url
    logoError.value = false
    toast.success(t('alerts.shop.logoUploaded'))
  } catch (e) {
    console.error('Upload error:', e)
    toast.error(t('alerts.shop.logoError'))
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
    await $fetch(`${useRuntimeConfig().public.apiBase}/shop/${shopSlug.value}/admin/info`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: form
    })

    toast.success(t('shopSettings.saved'))
    await refresh()
  } catch (e) {
    console.error('Error updating shop info:', e)
    toast.error(e.data?.detail || t('alerts.shop.errorSaving'))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  background: #fdfdfd;
}

.admin-main {
  margin-left: 280px;
  padding: 40px;
  min-height: 100vh;
  background: #fafafa;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 8px 0;
  letter-spacing: -0.03em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.admin-content {
  background: white;
  border-radius: 24px;
  padding: 40px;
  max-width: 960px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.02);
  border: 1px solid #f1f1f1;
}

.form-section {
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid #f3f4f6;
}

.form-section.last {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #111;
  margin: 0 0 24px 0;
}

.form-group {
  margin-bottom: 32px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #111;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f9f9f9;
}

.form-input:focus {
  outline: none;
  border-color: #111;
  background: white;
  box-shadow: 0 0 0 4px rgba(17, 17, 17, 0.05);
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
  line-height: 1.5;
}

.form-help {
  font-size: 0.8rem;
  color: #6B7280;
  margin-top: 6px;
}

/* Logo Area */
.logo-area {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.logo-preview-box {
  width: 110px;
  height: 110px;
  background: #f3f4f6;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: visible;
  transition: all 0.2s;
  cursor: pointer;
  flex-shrink: 0;
}

.logo-preview-box:hover {
  border-color: #111;
  background: #f0f0f0;
}

.logo-preview-box.has-logo {
  border-style: solid;
  background: white;
  border-color: #f1f1f1;
}

.logo-img {
  width: 80%;
  height: 80%;
  object-fit: contain;
}

.logo-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: #9ca3af;
  font-size: 0.75rem;
  font-weight: 600;
}

.logo-remove-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.logo-remove-btn:hover {
  transform: scale(1.1);
}

.logo-actions {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 110px;
}

.url-input-container {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.form-input-small {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.85rem;
  background: #f9f9f9;
}

.form-input-small:focus {
  outline: none;
  border-color: #111;
  background: white;
}

.btn-file-upload {
  padding: 0 16px;
  background: #111;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-file-upload:hover {
  background: #333;
}

/* Grids */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.social-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.social-input-group {
  background: white;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 20px;
  transition: all 0.2s;
}

.social-input-group:focus-within {
  border-color: #111;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.social-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 12px;
}

.social-input-group .form-input {
  height: 40px;
  padding: 8px 12px;
  font-size: 0.85rem;
  background: white;
  border-color: #e5e7eb;
}

/* Footer & Buttons */
.form-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

.btn-cancel {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6B7280;
  text-decoration: none;
  transition: color 0.2s;
}

.btn-cancel:hover {
  color: #111;
}

.btn-save {
  padding: 12px 32px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: #000;
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-msg {
  color: #ef4444;
  font-size: 0.8rem;
  margin-top: 8px;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.mobile-header {
  display: none;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 0px;
    padding-top: 84px;
  }

  .mobile-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: white;
    z-index: 1000;
    border-bottom: 1px solid #f3f4f6;
    height: 64px;
    padding: 0 20px;
  }

  .menu-btn {
    background: none;
    border: none;
    padding: 8px;
    color: #111;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  .mobile-title {
    font-weight: 700;
    font-size: 1rem;
    color: #111;
  }

  .home-btn {
    color: #111;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .admin-content {
    padding: 24px 16px;
    border-radius: 16px;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .logo-area {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .logo-preview-box {
    width: 100%;
    max-width: 200px;
    height: 140px;
  }
}
</style>
