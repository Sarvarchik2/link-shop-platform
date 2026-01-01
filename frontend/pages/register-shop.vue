<template>
  <div class="register-shop-page">
    <div class="container py-8">
      <div class="register-card">
        <div class="register-header">
          <h1 class="page-title">{{ $t('shopRegistration.title') }}</h1>
          <p class="page-subtitle">{{ $t('shopRegistration.subtitle') }}</p>
        </div>

        <div v-if="!user" class="auth-notice">
          <p>{{ $t('shopRegistration.authNotice.text') }}</p>
          <div class="auth-actions">
            <NuxtLink to="/login" class="btn-primary">{{ $t('shopRegistration.authNotice.login') }}</NuxtLink>
            <NuxtLink to="/register" class="btn-secondary">{{ $t('shopRegistration.authNotice.register') }}</NuxtLink>
          </div>
        </div>

        <div v-else-if="checkingShops" class="auth-notice">
          <p>{{ $t('platformAdmin.dashboard.loading') }}</p>
        </div>

        <div v-else-if="myShops && myShops.length > 0" class="auth-notice already-has-shop">
          <div class="notice-icon">⚠️</div>
          <h3>{{ $t('shopRegistration.existingShop.title') }}</h3>
          <p>{{ $t('shopRegistration.existingShop.desc') }}</p>
          <div class="auth-actions">
            <NuxtLink :to="`/shop/${myShops[0].slug}/admin`" class="btn-primary">{{
              $t('shopRegistration.existingShop.admin') }}</NuxtLink>
            <NuxtLink to="/profile" class="btn-secondary">{{ $t('shopRegistration.existingShop.profile') }}</NuxtLink>
          </div>
        </div>

        <form v-else @submit.prevent="registerShop" class="register-form">
          <div class="form-group">
            <label for="name">{{ $t('shopRegistration.form.name') }} *</label>
            <input id="name" v-model="form.name" type="text" required
              :placeholder="$t('shopRegistration.form.namePlaceholder')" class="form-input" />
          </div>

          <div class="form-group">
            <label for="slug">{{ $t('shopRegistration.form.slug') }} *</label>
            <div class="slug-input-wrapper">
              <span class="slug-prefix">link-platform-shop.uz/</span>
              <input id="slug" v-model="form.slug" type="text" required
                :placeholder="$t('shopRegistration.form.slugPlaceholder')" class="form-input slug-input"
                @input="formatSlug" />
            </div>
            <p class="form-hint">{{ $t('shopRegistration.form.slugHint') }}</p>
          </div>

          <div class="form-group">
            <label for="description">{{ $t('shopRegistration.form.desc') }} ({{ $t('common.optional') }})</label>
            <textarea id="description" v-model="form.description" rows="4"
              :placeholder="$t('shopRegistration.form.descPlaceholder')" class="form-input" />
          </div>

          <div class="form-group">
            <label>{{ $t('shopRegistration.form.logo') }}</label>
            <div class="logo-upload-container">
              <div class="logo-input-wrapper">
                <input v-model="form.logo_url" type="url" class="form-input"
                  :placeholder="$t('shopRegistration.form.logoUrlPlaceholder')" />
                <span class="input-divider">{{ $t('common.or') }}</span>
                <button type="button" class="btn-upload" @click="$refs.logoInput.click()" :disabled="uploading">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                  {{ uploading ? '...' : $t('common.upload') }}
                </button>
                <input type="file" ref="logoInput" style="display: none" accept="image/*" @change="handleLogoUpload" />
              </div>
              <small class="form-hint">{{ $t('shopRegistration.form.logoHint') }}</small>

              <div v-if="form.logo_url" class="logo-preview">
                <div class="preview-header">
                  <span class="preview-label">{{ $t('shopRegistration.form.preview') }}:</span>
                  <button type="button" class="btn-remove-logo" @click="form.logo_url = ''">{{ $t('common.delete')
                    }}</button>
                </div>
                <img :src="form.logo_url" alt="Logo" class="preview-image" @error="logoError = true" />
                <p v-if="logoError" class="preview-error">{{ $t('shopRegistration.form.uploadError') }}</p>
              </div>
            </div>
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" :disabled="loading" class="submit-button">
            <span v-if="loading">{{ $t('shopRegistration.form.creating') }}</span>
            <span v-else>{{ $t('shopRegistration.form.submit') }}</span>
          </button>
        </form>

        <div class="info-box">
          <h3>{{ $t('shopRegistration.info.title') }}</h3>
          <ul>
            <li>{{ $t('shopRegistration.info.point1') }}</li>
            <li>{{ $t('shopRegistration.info.point2') }} <strong>link-platform-shop.uz/{{ form.slug || 'your-slug'
                }}</strong></li>
            <li>{{ $t('shopRegistration.info.point3') }}</li>
            <li>{{ $t('shopRegistration.info.point4') }}</li>
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

const { token, user } = useAuth()
const { t } = useI18n()
const router = useRouter()
const toast = useToast()
const config = useRuntimeConfig()

const form = reactive({
  name: '',
  slug: '',
  description: '',
  logo_url: ''
})

const loading = ref(false)
const uploading = ref(false)
const logoError = ref(false)
const error = ref('')

const handleLogoUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    toast.error(t('shopRegistration.validation.imageRequired'))
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    toast.error(t('shopRegistration.validation.sizeLimit'))
    return
  }

  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await $fetch(`${config.public.apiBase}/upload`, {
      method: 'POST',
      body: formData
    })

    form.logo_url = response.url
    logoError.value = false
    toast.success(t('shopRegistration.success.logoUploaded'))
  } catch (e) {
    console.error('Upload error:', e)
    toast.error(t('shopRegistration.error.uploadFailed'))
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}
const myShops = ref([])
const checkingShops = ref(true)

const formatSlug = () => {
  form.slug = form.slug
    .toLowerCase()
    .replace(/[^a-z0-9-]/g, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

// Check if user already has a shop
const checkExistingShop = async () => {
  if (!token.value || !user.value) {
    checkingShops.value = false
    return
  }

  // Check user role
  const userRole = user.value?.role || (user.value?.roles?.includes('shop_owner') ? 'shop_owner' : 'user')

  if (userRole === 'shop_owner' || userRole === 'platform_admin' || user.value?.roles?.includes('admin')) {
    try {
      const shops = await $fetch(`${config.public.apiBase}/platform/shops/me`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      myShops.value = shops || []
    } catch (e) {
      if (e?.statusCode !== 404 && e?.statusCode !== 401) {
        console.error('[Register Shop] Error checking shops:', e)
      }
      myShops.value = []
    }
  }
  checkingShops.value = false
}

// Check on mount
onMounted(async () => {
  if (user.value) {
    await checkExistingShop()
  }
})

// Check on user change
watch(() => user.value, async (newUser) => {
  if (newUser) {
    await checkExistingShop()
  } else {
    checkingShops.value = false
    myShops.value = []
  }
}, { immediate: true })

const registerShop = async () => {
  if (!token.value) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = ''

  try {
    const data = await $fetch(`${config.public.apiBase}/platform/shops/register`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: form
    })

    toast.success(t('shopRegistration.success.created'))

    // Small delay for processing
    await new Promise(resolve => setTimeout(resolve, 500))

    // Navigate to subscription page
    await navigateTo(`/shop/${data.slug}/subscription`)
  } catch (e) {
    error.value = e.data?.detail || t('shopRegistration.error.createFailed')
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
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
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
}

.auth-notice {
  text-align: center;
  padding: 40px 20px;
  background: #F9FAFB;
  border-radius: 16px;
  margin-bottom: 32px;
  border: 2px solid #E5E7EB;
}

.auth-notice p {
  font-size: 1.125rem;
  margin-bottom: 24px;
  color: #111;
}

.already-has-shop {
  background: #FEF3C7;
  border-color: #FCD34D;
}

.already-has-shop h3 {
  color: #92400E;
  margin-bottom: 12px;
  font-size: 1.25rem;
  font-weight: 700;
}

.already-has-shop p {
  color: #78350F;
  margin-bottom: 24px;
}

.notice-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.auth-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
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

.logo-upload-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.logo-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.input-divider {
  color: #666;
  font-size: 0.875rem;
  font-weight: 500;
}

.btn-upload {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  color: #111;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  font-size: 0.875rem;
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
  margin-top: 12px;
  padding: 16px;
  background: #F9FAFB;
  border-radius: 16px;
  border: 2px dashed #E5E7EB;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.preview-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-label {
  font-size: 0.75rem;
  color: #666;
  font-weight: 600;
}

.btn-remove-logo {
  background: none;
  border: none;
  color: #DC2626;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
}

.btn-remove-logo:hover {
  background: #FEE2E2;
}

.preview-image {
  max-height: 60px;
  max-width: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  background: white;
  padding: 8px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.preview-error {
  font-size: 0.75rem;
  color: #DC2626;
  margin-top: 0;
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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

.btn-primary,
.btn-secondary {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #000;
}

.btn-secondary {
  background: white;
  color: #111;
  border: 2px solid #E5E7EB;
}

.btn-secondary:hover {
  border-color: #111;
}

@media (max-width: 768px) {
  .register-card {
    padding: 32px 24px;
    border-radius: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .auth-actions {
    flex-direction: column;
  }
}
</style>
