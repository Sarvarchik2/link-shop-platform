<template>
  <div v-if="shopSlug" class="shop-admin-page">
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
      <span class="mobile-title">{{ $t('productsPage.titleEdit') }}</span>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" current-route="products" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="add-product-page">
        <div class="page-header">
          <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="back-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
          </NuxtLink>
          <h1 class="page-title">{{ $t('productsPage.titleEdit') }}</h1>
        </div>

        <div v-if="productLoading" class="loading-state">
          <p>{{ $t('productsPage.loading') }}</p>
        </div>

        <div v-else class="form-card">
          <form @submit.prevent="handleSubmit">
            <div class="form-section">
              <h2 class="section-title">{{ $t('productsPage.basicInfo') }}</h2>

              <!-- Language Tabs -->
              <div class="language-tabs">
                <button type="button" v-for="lang in ['uz', 'ru', 'en']" :key="lang" @click="currentLang = lang"
                  class="lang-tab" :class="{ active: currentLang === lang }">
                  {{ getLanguageLabel(lang) }}
                </button>
              </div>

              <!-- Uzbek Fields -->
              <div v-show="currentLang === 'uz'" class="lang-content">
                <div class="form-group">
                  <label class="label">{{ $t('productsPage.nameLabel') }} ({{ $t('languages.uz') }}) *</label>
                  <input v-model="form.name_uz" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ray-Ban Wayfarer'" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.descriptionLabel') }} ({{ $t('languages.uz') }}) *</label>
                  <textarea v-model="form.description_uz" rows="4" required class="input"
                    :placeholder="$t('productsPage.descriptionPlaceholder')"></textarea>
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.categoryLabel') }} ({{ $t('languages.uz') }}) *</label>
                  <input v-model="form.category_uz" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ko\'zoynak'" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.brandLabel') }} ({{ $t('languages.uz') }}) *</label>
                  <input v-model="form.brand_uz" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ray-Ban'" />
                </div>
              </div>

              <!-- Russian Fields -->
              <div v-show="currentLang === 'ru'" class="lang-content">
                <div class="form-group">
                  <label class="label">{{ $t('productsPage.nameLabel') }} ({{ $t('languages.ru') }}) *</label>
                  <input v-model="form.name_ru" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ray-Ban Wayfarer'" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.descriptionLabel') }} ({{ $t('languages.ru') }}) *</label>
                  <textarea v-model="form.description_ru" rows="4" required class="input"
                    :placeholder="$t('productsPage.descriptionPlaceholder')"></textarea>
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.categoryLabel') }} ({{ $t('languages.ru') }}) *</label>
                  <input v-model="form.category_ru" required class="input"
                    :placeholder="$t('productsPage.example') + ', Очки'" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.brandLabel') }} ({{ $t('languages.ru') }}) *</label>
                  <input v-model="form.brand_ru" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ray-Ban'" />
                </div>
              </div>

              <!-- English Fields -->
              <div v-show="currentLang === 'en'" class="lang-content">
                <div class="form-group">
                  <label class="label">{{ $t('productsPage.nameLabel') }} ({{ $t('languages.en') }}) *</label>
                  <input v-model="form.name_en" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ray-Ban Wayfarer'" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.descriptionLabel') }} ({{ $t('languages.en') }}) *</label>
                  <textarea v-model="form.description_en" rows="4" required class="input"
                    :placeholder="$t('productsPage.descriptionPlaceholder')"></textarea>
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.categoryLabel') }} ({{ $t('languages.en') }}) *</label>
                  <input v-model="form.category_en" required class="input"
                    :placeholder="$t('productsPage.example') + ', Sunglasses'" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.brandLabel') }} ({{ $t('languages.en') }}) *</label>
                  <input v-model="form.brand_en" required class="input"
                    :placeholder="$t('productsPage.example') + ', Ray-Ban'" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="label">{{ $t('productsPage.priceLabel') }}</label>
                  <input v-model.number="form.price" type="number" step="0.01" required class="input"
                    placeholder="0.00" />
                </div>

                <div class="form-group">
                  <label class="label">{{ $t('productsPage.discountLabel') }}</label>
                  <input v-model.number="form.discount" type="number" step="0.1" min="0" max="100" class="input"
                    placeholder="0" />
                  <p class="help-text-small">{{ $t('productsPage.discountHelp') }}</p>
                </div>
              </div>
            </div>

            <div class="form-section">
              <h2 class="section-title">{{ $t('productsPage.imagesTitle') }}</h2>

              <div class="images-upload-area">
                <div class="images-preview" v-if="uploadedImages.length > 0">
                  <div v-for="(img, index) in uploadedImages" :key="index" class="image-preview-item"
                    :class="{ 'main-image': index === 0 }">
                    <img :src="img" alt="Product image" />
                    <div class="image-actions">
                      <button v-if="index !== 0" type="button" @click="setMainImage(index)" class="btn-set-main"
                        :title="$t('productsPage.makeMain')">
                        ⭐
                      </button>
                      <button type="button" @click="removeImage(index)" class="btn-remove-image"
                        :title="$t('productsPage.remove')">
                        ✕
                      </button>
                    </div>
                    <span v-if="index === 0" class="main-badge">{{ $t('productsPage.mainBadge') }}</span>
                  </div>
                </div>

                <div class="upload-zone" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
                  <input ref="fileInput" type="file" accept="image/*" multiple @change="handleFileSelect"
                    class="hidden-input" />
                  <div class="upload-content">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                      stroke-width="1.5">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    <span class="upload-text">{{ $t('productsPage.uploadText') }}</span>
                    <span class="upload-hint">{{ $t('productsPage.uploadHint') }}</span>
                  </div>
                </div>

                <div class="url-input-section">
                  <span class="divider-text">{{ $t('productsPage.orUrl') }}</span>
                  <div class="url-input-row">
                    <input v-model="imageUrl" class="input" placeholder="https://example.com/image.jpg" />
                    <button type="button" @click="addImageUrl" class="btn-add-url" :disabled="!imageUrl">{{
                      $t('productsPage.addBtn') }}</button>
                  </div>
                </div>
              </div>

              <p v-if="uploadingImages" class="uploading-text">{{ $t('productsPage.uploading') }}</p>
            </div>

            <div class="form-section">
              <h2 class="section-title">{{ $t('productsPage.variantsTitle') }}</h2>
              <p class="help-text">{{ $t('productsPage.variantsHelp') }}</p>

              <div class="variants-list">
                <div v-for="(variant, index) in variants" :key="index" class="variant-row">
                  <input v-model="variant.size" class="input variant-size-input"
                    :placeholder="$t('productsPage.sizePlaceholder')" />
                  <input v-model="variant.color" class="input variant-color-input"
                    :placeholder="$t('productsPage.colorPlaceholder')" />
                  <input v-model="variant.colorHex" type="color" class="color-picker"
                    :title="$t('productsPage.colorPlaceholder')" />
                  <input v-model.number="variant.stock" type="number" min="0" class="input stock-input"
                    :placeholder="$t('productsPage.stockPlaceholder')" />
                  <button type="button" @click="removeVariant(index)" class="btn-remove">✕</button>
                </div>
              </div>

              <button type="button" @click="addVariant" class="btn-add">
                {{ $t('productsPage.addVariantBtn') }}
              </button>
            </div>

            <div class="form-actions">
              <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="btn btn-secondary">{{ $t('productsPage.cancel')
              }}</NuxtLink>
              <button type="submit" class="btn btn-primary" :disabled="loading || uploadedImages.length === 0">
                {{ loading ? $t('productsPage.saving') : $t('productsPage.saveBtn') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
  <div v-else class="error-state">
    <p>{{ $t('productsPage.shopInfoError') }}</p>
    <NuxtLink to="/profile" class="btn btn-primary">{{ $t('productsPage.backToProfile') }}</NuxtLink>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth', 'shop-owner'],
  ssr: false
})

const route = useRoute()
const shopSlug = computed(() => route.params.slug)
const productId = computed(() => route.params.id)
const { token, logout } = useAuth()
const toast = useToast()
const { t } = useI18n()

const getLanguageLabel = (lang) => {
  switch (lang) {
    case 'uz': return '🇺🇿 ' + t('languages.uz')
    case 'ru': return '🇷🇺 ' + t('languages.ru')
    case 'en': return '🇬🇧 ' + t('languages.en')
    default: return lang
  }
}

const sidebarOpen = ref(false)
const loading = ref(false)
const productLoading = ref(true)
const uploadingImages = ref(false)
const brands = ref([])
const categories = ref([])
const brandsError = ref(null)
const categoriesError = ref(null)

const fileInput = ref(null)
const uploadedImages = ref([])
const imageUrl = ref('')
const variants = ref([{ size: '', color: '', colorHex: '#000000', stock: 0 }])

const currentLang = ref('uz')

const form = reactive({
  name_uz: '',
  name_ru: '',
  name_en: '',
  description_uz: '',
  description_ru: '',
  description_en: '',
  category_uz: '',
  category_ru: '',
  category_en: '',
  brand_uz: '',
  brand_ru: '',
  brand_en: '',
  price: 0,
  discount: 0
})

const handleLogout = () => {
  logout()
  toast.success(t('alerts.shop.loggedOut'))
}

onMounted(async () => {
  if (!shopSlug.value || !productId.value) return

  try {
    // 1. Fetch product data
    const product = await $fetch(`${useRuntimeConfig().public.apiBase}/products/${productId.value}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })

    // Fill form with multilingual fields
    form.name_uz = product.name_uz || product.name || ''
    form.name_ru = product.name_ru || product.name || ''
    form.name_en = product.name_en || product.name || ''

    form.description_uz = product.description_uz || product.description || ''
    form.description_ru = product.description_ru || product.description || ''
    form.description_en = product.description_en || product.description || ''

    form.category_uz = product.category_uz || product.category || ''
    form.category_ru = product.category_ru || product.category || ''
    form.category_en = product.category_en || product.category || ''

    form.brand_uz = product.brand_uz || product.brand || ''
    form.brand_ru = product.brand_ru || product.brand || ''
    form.brand_en = product.brand_en || product.brand || ''

    form.price = product.price
    form.discount = product.discount

    // Handle images
    if (product.images) {
      try {
        uploadedImages.value = JSON.parse(product.images)
      } catch (e) {
        uploadedImages.value = [product.image_url]
      }
    } else {
      uploadedImages.value = [product.image_url]
    }

    // Handle variants
    if (product.variants) {
      try {
        variants.value = JSON.parse(product.variants)
      } catch (e) {
        variants.value = [{ size: '', color: '', colorHex: '#000000', stock: product.stock || 0 }]
      }
    } else {
      variants.value = [{ size: '', color: '', colorHex: '#000000', stock: product.stock || 0 }]
    }

    productLoading.value = false

    // 2. Fetch brands and categories
    const [brandsData, categoriesData] = await Promise.all([
      $fetch(`${useRuntimeConfig().public.apiBase}/brands?shop_slug=${shopSlug.value}`, {
        headers: { Authorization: `Bearer ${token.value}` }
      }),
      $fetch(`${useRuntimeConfig().public.apiBase}/categories?shop_slug=${shopSlug.value}`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
    ])

    brands.value = brandsData || []
    categories.value = categoriesData || []
  } catch (e) {
    console.error('[Edit Product] Ошибка загрузки:', e)
    toast.error(t('alerts.shop.errorLoadingData'))
    productLoading.value = false
  }
})

// Variant functions
const addVariant = () => {
  variants.value.push({ size: '', color: '', colorHex: '#000000', stock: 0 })
}

const removeVariant = (index) => {
  variants.value.splice(index, 1)
}

// Image functions
const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = async (event) => {
  const files = event.target.files
  if (files.length > 0) {
    await uploadFiles(files)
  }
}

const handleDrop = async (event) => {
  const files = event.dataTransfer.files
  if (files.length > 0) {
    await uploadFiles(files)
  }
}

const uploadFiles = async (files) => {
  uploadingImages.value = true
  for (const file of files) {
    if (file.type.startsWith('image/')) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const response = await $fetch(useRuntimeConfig().public.apiBase + '/upload', {
          method: 'POST',
          body: formData
        })
        uploadedImages.value.push(response.url)
        toast.success(t('alerts.shop.imageUploaded'))
      } catch (e) {
        toast.error(t('alerts.shop.imageError'))
      }
    }
  }
  uploadingImages.value = false
}

const addImageUrl = () => {
  if (imageUrl.value.trim()) {
    uploadedImages.value.push(imageUrl.value.trim())
    imageUrl.value = ''
  }
}

const removeImage = (index) => {
  uploadedImages.value.splice(index, 1)
}

const setMainImage = (index) => {
  const [img] = uploadedImages.value.splice(index, 1)
  uploadedImages.value.unshift(img)
}

const handleSubmit = async () => {
  if (uploadedImages.value.length === 0) {
    toast.warning(t('alerts.shop.addOneImage'))
    return
  }

  const validVariants = variants.value.filter(v => v.size?.trim() && v.color?.trim())
  const totalStock = validVariants.reduce((acc, v) => acc + (v.stock || 0), 0)

  loading.value = true
  try {
    const productData = {
      ...form,
      image_url: uploadedImages.value[0],
      images: JSON.stringify(uploadedImages.value),
      variants: validVariants.length > 0 ? JSON.stringify(validVariants) : null,
      sizes: null,
      colors: null,
      stock: validVariants.length > 0 ? totalStock : variants.value[0].stock || 0
    }

    await $fetch(`${useRuntimeConfig().public.apiBase}/products/${productId.value}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })

    toast.success(t('alerts.shop.productUpdated'))
    navigateTo(`/shop/${shopSlug.value}/admin/products`)
  } catch (e) {
    console.error('[Edit Product] Ошибка при обновлении:', e)
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

/* Sidebar styles handled by ShopAdminSidebar component */

.admin-main {
  flex: 1;
  margin-left: 280px;
  padding: 40px;
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
  justify-content: center;
  z-index: 1000;
}

.menu-btn {
  position: absolute;
  left: 16px;
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
}

.mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }

  .admin-main {
    margin-left: 0;
    padding: 70px 12px 20px;
    width: 100%;
    min-width: 0;
  }

  /* Hide huge title since we have it in mobile-header */
  .page-header {
    display: none;
  }

  .form-card {
    padding: 20px;
    border-radius: 16px;
  }

  .form-section {
    margin-bottom: 24px;
    padding-bottom: 24px;
  }

  .form-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .variant-row {
    grid-template-columns: 1fr 1fr 60px;
    gap: 8px;
  }

  .stock-input {
    grid-column: 1 / span 2;
  }

  .btn-remove {
    grid-column: 3;
    grid-row: 1 / span 2;
    height: 100%;
    background: #FEE2E2;
    color: #DC2626;
    border: none;
    border-radius: 8px;
    font-size: 1.2rem;
  }

  .url-input-row {
    flex-direction: column;
  }

  .btn-add-url {
    padding: 12px;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
    text-align: center;
  }
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: white;
  border: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
}

.form-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.form-section {
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid #E5E7EB;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  background: #F9FAFB;
}

.variants-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.variant-row {
  display: grid;
  grid-template-columns: 2fr 2fr 60px 1fr 40px;
  gap: 12px;
  align-items: center;
}

.color-picker {
  width: 100%;
  height: 44px;
  padding: 2px;
  border-radius: 8px;
  border: 1px solid #ddd;
  cursor: pointer;
}

.btn-add {
  padding: 10px 16px;
  border-radius: 10px;
  border: 2px dashed #E5E7EB;
  background: transparent;
  width: 100%;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

.btn {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  text-decoration: none;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-secondary {
  background: #F3F4F6;
  color: #111;
}

.images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.image-preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #E5E7EB;
}

.image-preview-item.main-image {
  border-color: #10B981;
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-actions {
  position: absolute;
  top: 5px;
  right: 5px;
  display: flex;
  gap: 5px;
}

.btn-remove-image,
.btn-set-main {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove-image {
  background: #FEE2E2;
  color: #DC2626;
}

.btn-set-main {
  background: #FEF3C7;
}

.upload-zone {
  border: 2px dashed #E5E7EB;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  margin-bottom: 20px;
}

.hidden-input {
  display: none;
}

.url-input-row {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.btn-add-url {
  background: #111;
  color: white;
  border: none;
  padding: 0 20px;
  border-radius: 12px;
  cursor: pointer;
}

.main-badge {
  position: absolute;
  bottom: 5px;
  left: 5px;
  background: #10B981;
  color: white;
  font-size: 0.6rem;
  padding: 2px 6px;
  border-radius: 4px;
}

/* Language Tabs */
.language-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 2px solid #E5E7EB;
  padding-bottom: 0;
}

.lang-tab {
  padding: 12px 20px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 600;
  color: #9CA3AF;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.lang-tab:hover {
  color: #111;
  background: #F9FAFB;
}

.lang-tab.active {
  color: #111;
  border-bottom-color: #111;
}

.lang-content {
  animation: fadeIn 0.2s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
