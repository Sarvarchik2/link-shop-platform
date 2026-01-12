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
          <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/products`)" class="back-btn">
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

              <!-- Common Fields -->
              <div class="form-group">
                <label class="label">{{ $t('productsPage.categoryLabel') }} *</label>
                <!-- Custom Category Dropdown -->
                <div class="custom-dropdown" v-click-outside="() => showCategoryDropdown = false">
                  <button type="button" class="dropdown-trigger" @click="showCategoryDropdown = !showCategoryDropdown"
                    :class="{ 'active': showCategoryDropdown, 'has-selection': selectedCategory }">
                    <span class="selected-value">{{ selectedCategory ? getField(selectedCategory, 'name') :
                      $t('productsPage.selectCategory') }}</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      class="chevron">
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>
                  <Transition name="dropdown">
                    <div v-if="showCategoryDropdown" class="dropdown-menu">
                      <div v-for="cat in categories" :key="cat.id" class="dropdown-item"
                        :class="{ 'active': selectedCategory?.id === cat.id }"
                        @click="selectedCategory = cat; showCategoryDropdown = false">
                        <span class="item-text">{{ getField(cat, 'name') }}</span>
                        <svg v-if="selectedCategory?.id === cat.id" width="18" height="18" viewBox="0 0 24 24"
                          fill="none" stroke="currentColor" stroke-width="3">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </div>
                    </div>
                  </Transition>
                </div>
              </div>

              <div class="form-group">
                <label class="label">{{ $t('productsPage.brandLabel') }} *</label>
                <!-- Custom Brand Dropdown -->
                <div class="custom-dropdown" v-click-outside="() => showBrandDropdown = false">
                  <button type="button" class="dropdown-trigger" @click="showBrandDropdown = !showBrandDropdown"
                    :class="{ 'active': showBrandDropdown, 'has-selection': selectedBrand }">
                    <span class="selected-value">{{ selectedBrand ? selectedBrand.name : $t('productsPage.selectBrand')
                      }}</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      class="chevron">
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>
                  <Transition name="dropdown">
                    <div v-if="showBrandDropdown" class="dropdown-menu">
                      <div v-for="brand in brands" :key="brand.id" class="dropdown-item"
                        :class="{ 'active': selectedBrand?.id === brand.id }"
                        @click="selectedBrand = brand; showBrandDropdown = false">
                        <span class="item-text">{{ brand.name }}</span>
                        <svg v-if="selectedBrand?.id === brand.id" width="18" height="18" viewBox="0 0 24 24"
                          fill="none" stroke="currentColor" stroke-width="3">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </div>
                    </div>
                  </Transition>
                </div>
              </div>

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
              <div class="section-header-row">
                <h2 class="section-title">{{ $t('productsPage.variantsTitle') }}</h2>
                <div class="toggle-container">
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="hasVariants">
                    <span class="toggle-slider"></span>
                  </label>
                  <span class="toggle-label">{{ $t('productsPage.hasVariantsLabel') || 'Использовать варианты (размеры и цвета)' }}</span>
                </div>
              </div>

              <p class="help-text">{{ $t('productsPage.variantsHelp') }}</p>

              <!-- Simple Product Stock -->
              <div v-if="!hasVariants" class="simple-stock-input">
                <div class="form-group mb-0">
                  <label class="label">{{ $t('productsPage.stockLabel') || 'Количество на складе' }}</label>
                  <input v-model.number="simpleStock" type="number" min="0" class="input stock-input-large"
                    :placeholder="$t('productsPage.stockPlaceholder')" />
                </div>
              </div>

              <!-- Variants List -->
              <div v-else class="variants-container">
                <div class="variants-list">
                  <div v-for="(variant, index) in variants" :key="index" class="variant-row">
                    <div class="row-inputs">
                      <div class="input-group">
                        <label class="input-hint">{{ $t('productsPage.sizeLabel') || 'Размер' }}</label>
                        <input v-model="variant.size" class="input" :placeholder="$t('productsPage.sizePlaceholder')" />
                      </div>
                      <div class="input-group">
                        <label class="input-hint">{{ $t('productsPage.colorLabel') || 'Цвет' }}</label>
                        <input v-model="variant.color" class="input"
                          :placeholder="$t('productsPage.colorPlaceholder')" />
                      </div>
                      <div class="input-group shrink">
                        <label class="input-hint">{{ $t('productsPage.colorHexLabel') || 'Hex' }}</label>
                        <input v-model="variant.colorHex" type="color" class="color-picker" />
                      </div>
                      <div class="input-group">
                        <label class="input-hint">{{ $t('productsPage.stockLabel') || 'Склад' }}</label>
                        <input v-model.number="variant.stock" type="number" min="0" class="input"
                          :placeholder="$t('productsPage.stockPlaceholder')" />
                      </div>
                    </div>
                    <button type="button" @click="removeVariant(index)" class="btn-remove" v-if="variants.length > 1">
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>
                </div>

                <button type="button" @click="addVariant" class="btn-add">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  {{ $t('productsPage.addVariantBtn') }}
                </button>
              </div>
            </div>

            <div class="form-actions">
              <NuxtLink :to="localePath(`/shop/${shopSlug}/admin/products`)" class="btn btn-secondary">{{
                $t('productsPage.cancel')
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
    <NuxtLink :to="localePath('/profile')" class="btn btn-primary">{{ $t('productsPage.backToProfile') }}</NuxtLink>
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
const hasVariants = ref(false)
const simpleStock = ref(0)

const selectedCategory = ref(null)
const selectedBrand = ref(null)
const { getField } = useMultilingual()
const localePath = useLocalePath()

const showCategoryDropdown = ref(false)
const showBrandDropdown = ref(false)

// Directive to close dropdown when clicking outside
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
}

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
        const parsedVariants = JSON.parse(product.variants)
        if (parsedVariants.length > 0) {
          // Check if variants actually have size or color
          const hasV = parsedVariants.some(v => v.size || v.color)
          if (hasV) {
            variants.value = parsedVariants
            hasVariants.value = true
          } else {
            // It's a simple product stored as a variant
            simpleStock.value = parsedVariants[0].stock || product.stock || 0
            hasVariants.value = false
            variants.value = [{ size: '', color: '', colorHex: '#000000', stock: simpleStock.value }]
          }
        }
      } catch (e) {
        hasVariants.value = false
        simpleStock.value = product.stock || 0
        variants.value = [{ size: '', color: '', colorHex: '#000000', stock: simpleStock.value }]
      }
    } else {
      hasVariants.value = false
      simpleStock.value = product.stock || 0
      variants.value = [{ size: '', color: '', colorHex: '#000000', stock: simpleStock.value }]
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

    // 3. Pre-select Category and Brand based on saved strings
    // Logic: Try to match by any language name
    if (form.category_uz || form.category_ru || form.category_en) {
      selectedCategory.value = categories.value.find(c =>
        (form.category_uz && c.name_uz === form.category_uz) ||
        (form.category_ru && c.name_ru === form.category_ru) ||
        (form.category_en && c.name_en === form.category_en)
      )
    }

    if (form.brand_uz || form.brand_ru || form.brand_en) {
      selectedBrand.value = brands.value.find(b =>
        (form.brand_uz && b.name === form.brand_uz) ||
        (form.brand_ru && b.name === form.brand_ru) ||
        (form.brand_en && b.name === form.brand_en)
      )
    }

  } catch (e) {
    console.error('[Edit Product] Ошибка загрузки:', e)
    toast.error(t('alerts.shop.errorLoadingData'))
    productLoading.value = false
  }
})

// Watch for selection changes to update form
watch(selectedCategory, (newVal) => {
  if (newVal) {
    form.category_uz = newVal.name_uz
    form.category_ru = newVal.name_ru
    form.category_en = newVal.name_en
  }
})

watch(selectedBrand, (newVal) => {
  if (newVal) {
    form.brand_uz = newVal.name
    form.brand_ru = newVal.name
    form.brand_en = newVal.name
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

  // Custom Validation for Multilingual Fields
  if (!form.name_uz || !form.name_ru || !form.name_en) {
    toast.warning(t('alerts.shop.fillAllNames') || 'Please fill product name in all languages')
    return
  }

  if (!form.description_uz || !form.description_ru || !form.description_en) {
    toast.warning(t('alerts.shop.fillAllDescriptions') || 'Please fill product description in all languages')
    return
  }

  if (!selectedCategory.value) {
    toast.warning(t('alerts.shop.selectCategory') || 'Please select a category')
    return
  }

  if (!selectedBrand.value) {
    toast.warning(t('alerts.shop.selectBrand') || 'Please select a brand')
    return
  }

  // Validation for variants: if size or color is entered, both must be present
  const incompleteVariant = variants.value.find(v => (v.size?.trim() && !v.color?.trim()) || (!v.size?.trim() && v.color?.trim()))
  if (incompleteVariant) {
    toast.warning(t('alerts.shop.incompleteVariant') || 'Если введен размер или цвет, оба поля должны быть заполнены')
    return
  }

  // Filter valid variants: either (size AND color filled) OR (only stock filled)
  const validVariants = hasVariants.value ? variants.value.filter(v => {
    const hasSizeColor = v.size?.trim() && v.color?.trim()
    return hasSizeColor
  }) : []

  const totalStock = hasVariants.value ? validVariants.reduce((acc, v) => acc + (v.stock || 0), 0) : simpleStock.value

  loading.value = true
  try {
    const productData = {
      ...form,
      image_url: uploadedImages.value[0],
      images: JSON.stringify(uploadedImages.value),
      variants: hasVariants.value && validVariants.length > 0 ? JSON.stringify(validVariants) : null,
      sizes: null,
      colors: null,
      stock: totalStock || 0
    }

    await $fetch(`${useRuntimeConfig().public.apiBase}/products/${productId.value}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })

    toast.success(t('alerts.shop.productUpdated'))
    navigateTo(localePath(`/shop/${shopSlug.value}/admin/products`))
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
  background: #f8fafc;
  color: #1e293b;
}

.admin-main {
  flex: 1;
  margin-left: 280px;
  padding: 40px;
  max-width: 1400px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: white;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  text-decoration: none;
}

.back-btn:hover {
  background: #111;
  color: white;
  border-color: #111;
  transform: translateX(-4px);
}

.page-title {
  font-size: 1.875rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.025em;
  margin: 0;
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
    display: grid;
    grid-template-columns: 1fr 1fr 44px;
    grid-template-rows: auto auto;
    gap: 10px;
    padding: 12px;
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    align-items: center;
  }

  .variant-size-input {
    grid-column: 1;
    grid-row: 1;
    width: 100%;
  }

  .variant-color-input {
    grid-column: 2;
    grid-row: 1;
    width: 100%;
  }

  .color-picker {
    grid-column: 1;
    grid-row: 2;
    width: 100%;
    height: 48px;
    margin: 0;
  }

  .stock-input {
    grid-column: 2;
    grid-row: 2;
    width: 100%;
    margin: 0;
  }

  .btn-remove {
    grid-column: 3;
    grid-row: 1 / span 2;
    height: 100%;
    width: 44px;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #FEE2E2;
    color: #DC2626;
    border: none;
    border-radius: 10px;
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
  box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
}

.form-section {
  margin-bottom: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid #f1f5f9;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0px;
  padding-bottom: 0px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 24px;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #F3F4F6;
  padding: 8px 16px;
  border-radius: 12px;
}

.toggle-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #D1D5DB;
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked+.toggle-slider {
  background-color: #111;
}

input:checked+.toggle-slider:before {
  transform: translateX(20px);
}

.stock-input-large {
  max-width: 200px;
  font-size: 1.25rem;
  font-weight: 700;
  text-align: center;
}

.variant-row {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  padding: 16px;
  border-radius: 20px;
  margin-bottom: 12px;
}

.row-inputs {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr 60px 100px;
  gap: 12px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input-hint {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6B7280;
  margin-left: 4px;
}

.color-picker {
  height: 46px;
  width: 100%;
  padding: 4px;
  border-radius: 10px;
}

.btn-remove {
  width: 46px;
  height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #FEE2E2;
  color: #DC2626;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #FECACA;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add:hover {
  background: #333;
}

@media (max-width: 768px) {
  .row-inputs {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
  }
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  color: #1e293b;
  font-size: 0.9375rem;
  transition: all 0.2s;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: #111;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.03);
}

.form-group {
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

/* Custom Dropdown Stylings */
.custom-dropdown {
  position: relative;
}

.dropdown-trigger {
  width: 100%;
  height: 52px;
  padding: 0 16px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  color: #374151;
}

.dropdown-trigger:hover {
  border-color: #cbd5e1;
}

.dropdown-trigger.active {
  background: white;
  border-color: #111;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.03);
}

.dropdown-trigger.has-selection {
  color: #0f172a;
  font-weight: 500;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  padding: 6px;
  z-index: 100;
  max-height: 300px;
  overflow-y: auto;
}

.dropdown-item {
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9375rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dropdown-item:hover {
  background: #f1f5f9;
}

.dropdown-item.active {
  background: #111;
  color: white;
}

.variants-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.variant-row {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  background: white;
  padding: 16px;
  border: 1px solid #F3F4F6;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
}

.row-inputs {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr auto 100px;
  gap: 16px;
}

.variant-row:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-color: #E5E7EB;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-hint {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.color-picker {
  width: 44px;
  height: 44px;
  padding: 0;
  border-radius: 10px;
  border: 2px solid #E5E7EB;
  cursor: pointer;
  background: white;
  overflow: hidden;
}

.color-picker::-webkit-color-swatch-wrapper {
  padding: 0;
}

.color-picker::-webkit-color-swatch {
  border: none;
}

.btn-add {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  border-radius: 12px;
  border: 2px dashed #E5E7EB;
  background: #F9FAFB;
  width: 100%;
  cursor: pointer;
  color: #4B5563;
  font-weight: 600;
  font-size: 0.9375rem;
  transition: all 0.3s ease;
}

.btn-add:hover {
  background: #F3F4F6;
  border-color: #D1D5DB;
  color: #111;
}

.btn-remove {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  border: none;
  background: #FEE2E2;
  color: #DC2626;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 2px;
}

.btn-remove:hover {
  background: #FECACA;
  transform: scale(1.05);
}

/* Language Tabs Styling */
.language-tabs {
  display: flex;
  gap: 6px;
  padding: 6px;
  background: #f1f5f9;
  border-radius: 14px;
  margin-bottom: 32px;
  width: fit-content;
}

.lang-tab {
  padding: 8px 18px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.875rem;
  color: #64748b;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.lang-tab:hover {
  color: #0f172a;
}

.lang-tab.active {
  background: white;
  color: #0f172a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Image Upload Styling */
.images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.image-preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 16px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  overflow: hidden;
  transition: all 0.3s;
}

.image-preview-item.main-image {
  border-color: #10b981;
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 6px;
}

.btn-remove-image,
.btn-set-main {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-remove-image {
  background: #fee2e2;
  color: #ef4444;
}

.btn-set-main {
  background: #fef9c3;
  color: #854d0e;
}

.upload-zone {
  border: 2.5px dashed #e2e8f0;
  border-radius: 20px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f8fafc;
  color: #64748b;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-zone:hover {
  border-color: #111;
  background: white;
  color: #111;
  box-shadow: 0 10px 20px -10px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

/* Toggle Switch Premium Styling */
.toggle-container {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 8px 16px;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
}

.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e2e8f0;
  transition: .3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input:checked+.toggle-slider {
  background-color: #111;
}

.hidden-input {
  display: none !important;
}

.url-input-section {
  margin-top: 32px;
}

.divider-text {
  display: flex;
  align-items: center;
  text-align: center;
  color: #94a3b8;
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 20px;
}

.divider-text::before,
.divider-text::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}

.divider-text::before {
  margin-right: 16px;
}

.divider-text::after {
  margin-left: 16px;
}

.url-input-row {
  display: flex;
  gap: 12px;
  background: #f8fafc;
  padding: 8px;
  border-radius: 16px;
  border: 1.5px solid #e2e8f0;
  transition: all 0.2s;
}

.url-input-row:focus-within {
  border-color: #111;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.03);
}

.url-input-row .input {
  flex: 1;
  background: transparent !important;
  border: none !important;
  padding: 10px 12px !important;
  box-shadow: none !important;
}

.btn-add-url {
  padding: 10px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-add-url:hover:not(:disabled) {
  background: #2d2d2d;
  transform: scale(1.02);
}

.btn-add-url:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}

/* Variants Redesign */
.variants-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 28px;
}

.variant-row {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  padding: 20px;
  border-radius: 18px;
  transition: all 0.3s;
}

.variant-row:hover {
  border-color: #cbd5e1;
  background: white;
}

.row-inputs {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr auto 100px;
  gap: 16px;
}

.btn-remove {
  width: 46px;
  height: 46px;
  background: #fee2e2;
  color: #ef4444;
  border: none;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #fecaca;
  transform: scale(1.05);
}

.btn-add {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 16px;
  background: white;
  border: 2px dashed #e2e8f0;
  color: #64748b;
  border-radius: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add:hover {
  border-color: #111;
  color: #111;
  background: #f8fafc;
}

/* Action Buttons */
.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 40px;
}

.btn {
  padding: 14px 32px;
  border-radius: 14px;
  font-weight: 700;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #2d2d2d;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
  color: #0f172a;
}

/* Mobile Adjustments */
.mobile-header {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 16px;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.menu-btn {
  position: absolute;
  left: 16px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.mobile-title {
  font-weight: 700;
  color: #0f172a;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 84px 16px 40px;
  }

  .mobile-header {
    display: flex;
  }

  .page-header {
    display: none;
  }
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .row-inputs {
    grid-template-columns: 1fr 1fr;
  }

  .form-card {
    padding: 24px;
  }

  .variant-row {
    display: grid;
    grid-template-columns: 1fr 1fr 44px;
    grid-template-rows: auto auto;
  }
}

.lang-content {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
