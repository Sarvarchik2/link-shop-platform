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
      <span class="mobile-title">{{ $t('productsPage.titleNew') }}</span>
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
          <h1 class="page-title">{{ $t('productsPage.titleNew') }}</h1>
        </div>

        <!-- Limit Warning -->
        <div v-if="limitReached" class="limit-warning">
          <div class="warning-icon">⚠️</div>
          <div class="warning-content">
            <h3>{{ $t('productsPage.limitReachedTitle') }}</h3>
            <p>{{ $t('productsPage.limitReachedDesc', { limit: stats?.plan_limit_products }) }}</p>
            <NuxtLink :to="localePath(`/shop/${shopSlug}/subscription`)" class="btn-upgrade">{{
              $t('productsPage.upgradePlan') }}
            </NuxtLink>
          </div>
        </div>

        <div class="form-card">
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
                  <label class="label">{{ $t('productsPage.discountLabel') }} (%)</label>
                  <input v-model.number="form.discount" type="number" step="0.1" min="0" max="100" class="input"
                    placeholder="0" />
                  <p class="help-text-small">{{ $t('productsPage.discountHelp') }}</p>
                </div>
              </div>
            </div>


            <div class="form-section">
              <h2 class="section-title">{{ $t('productsPage.imagesTitle') }}</h2>

              <!-- Image Upload Area -->
              <div class="images-upload-area">
                <!-- Uploaded Images Preview -->
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

                <!-- Upload Button -->
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

                <!-- OR URL Input -->
                <div class="url-input-section">
                  <span class="divider-text">{{ $t('productsPage.orUrl') }}</span>
                  <div class="url-input-row">
                    <input v-model="imageUrl" class="input" placeholder="https://example.com/image.jpg" />
                    <button type="button" @click="addImageUrl" class="btn-add-url" :disabled="!imageUrl">{{
                      $t('productsPage.addBtn') }}</button>
                  </div>
                </div>
              </div>

              <p v-if="uploadingImages" class="uploading-text">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                {{ $t('productsPage.uploading') }}
              </p>
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
              <button type="submit" class="btn btn-primary"
                :disabled="loading || uploadedImages.length === 0 || limitReached">
                {{ loading ? $t('productsPage.creating') : $t('productsPage.createBtn') }}
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

console.log('[Add Product] Страница загружается...')

const route = useRoute()
const shopSlug = computed(() => {
  const slug = route.params.slug
  console.log('[Add Product] Shop slug из route:', slug)
  if (!slug) {
    console.error('[Add Product] ОШИБКА: shop slug не найден в route.params')
  }
  return slug
})
console.log('[Add Product] Shop slug:', shopSlug.value)

const { token, logout } = useAuth()
console.log('[Add Product] Token:', token.value ? 'есть' : 'нет')

const handleLogout = () => {
  logout()
  useToast().success(t('alerts.shop.loggedOut'))
}

// Проверка что все необходимое загружено
onMounted(() => {
  console.log('[Add Product] Компонент смонтирован, shopSlug:', shopSlug.value)
  if (!shopSlug.value) {
    console.error('[Add Product] КРИТИЧЕСКАЯ ОШИБКА: shopSlug отсутствует!')
  }
})

const sidebarOpen = ref(false)
const loading = ref(false)
const uploadingImages = ref(false)
const stats = ref(null)
const brands = ref([])
const categories = ref([])
const brandsError = ref(null)
const categoriesError = ref(null)
const toast = useToast()
const { t } = useI18n()
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

const getLanguageLabel = (lang) => {
  switch (lang) {
    case 'uz': return '🇺🇿 ' + t('languages.uz')
    case 'ru': return '🇷🇺 ' + t('languages.ru')
    case 'en': return '🇬🇧 ' + t('languages.en')
    default: return lang
  }
}

const limitReached = computed(() => {
  if (!stats.value || stats.value.plan_limit_products === null) return false
  return stats.value.total_products >= stats.value.plan_limit_products
})

// Move config to top level so it's accessible in all functions
const config = useRuntimeConfig()

onMounted(async () => {
  console.log('[Add Product] Компонент смонтирован, shopSlug:', shopSlug.value)

  if (!shopSlug.value) {
    console.error('[Add Product] ОШИБКА: shopSlug отсутствует, невозможно загрузить данные')
    return
  }

  // Загружаем данные после монтирования
  try {
    console.log('[Add Product] Загрузка данных для shop:', shopSlug.value)
    const [brandsData, categoriesData, statsData] = await Promise.all([
      $fetch(`${config.public.apiBase}/brands?shop_slug=${shopSlug.value}`, {
        headers: { 'Authorization': `Bearer ${token.value}` }
      }).catch(e => {
        console.error('[Add Product] Ошибка загрузки брендов:', e)
        brandsError.value = e
        return []
      }),
      $fetch(`${config.public.apiBase}/categories?shop_slug=${shopSlug.value}`, {
        headers: { 'Authorization': `Bearer ${token.value}` }
      }).catch(e => {
        console.error('[Add Product] Ошибка загрузки категорий:', e)
        categoriesError.value = e
        return []
      }),
      $fetch(`${config.public.apiBase}/shop/${shopSlug.value}/admin/stats`, {
        headers: { 'Authorization': `Bearer ${token.value}` }
      }).catch(e => {
        console.error('[Add Product] Ошибка загрузки статистики магазина:', e)
        return null
      })
    ])

    brands.value = brandsData || []
    categories.value = categoriesData || []
    stats.value = statsData
    console.log('[Add Product] Данные загружены:', {
      brands: brands.value.length,
      categories: categories.value.length,
      limit: stats.value?.plan_limit_products,
      current: stats.value?.total_products
    })
  } catch (e) {
    console.error('[Add Product] Ошибка при загрузке данных:', e)
  }
})


const fileInput = ref(null)
const uploadedImages = ref([])
const imageUrl = ref('')

// Selection state
const selectedCategory = ref(null)
const selectedBrand = ref(null)

// Watch for selection changes to populate form
watch(selectedCategory, (newVal) => {
  if (newVal) {
    form.category_uz = newVal.name_uz
    form.category_ru = newVal.name_ru
    form.category_en = newVal.name_en
  }
})

watch(selectedBrand, (newVal) => {
  if (newVal) {
    form.brand_uz = newVal.name // Brand name is usually universal? Check model.
    form.brand_ru = newVal.name
    form.brand_en = newVal.name
    // Wait, Product model has brand_uz/ru/en. Brand model has name?
    // Let's check brand model or just copy name to all if generic.
    // Assuming Brand model has simple 'name'.
  }
})

const variants = ref([{ size: '', color: '', colorHex: '#000000', stock: 0 }])
const hasVariants = ref(false)
const simpleStock = ref(0)

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
        console.log('[Add Product] Загрузка изображения:', file.name)
        const formData = new FormData()
        formData.append('file', file)

        const response = await $fetch(config.public.apiBase + '/upload', {
          method: 'POST',
          body: formData
        })

        console.log('[Add Product] Изображение загружено:', response.url)
        uploadedImages.value.push(response.url)
        toast.success(t('alerts.shop.imageUploaded'))
      } catch (e) {
        console.error('[Add Product] Ошибка загрузки изображения:', e)
        console.error('[Add Product] Детали ошибки:', {
          message: e.message,
          statusCode: e.statusCode,
          data: e.data
        })
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

  // Filter valid variants: either (size AND color filled) OR (only stock filled)
  const validVariants = hasVariants.value ? variants.value.filter(v => {
    const hasSizeColor = v.size.trim() && v.color.trim()
    return hasSizeColor
  }) : []

  // Calculate total stock from variants
  const totalStock = hasVariants.value ? validVariants.reduce((acc, v) => acc + (v.stock || 0), 0) : simpleStock.value

  loading.value = true
  try {
    const productData = {
      ...form,
      image_url: uploadedImages.value[0],
      images: JSON.stringify(uploadedImages.value),
      variants: hasVariants.value && validVariants.length > 0 ? JSON.stringify(validVariants) : null,
      sizes: null, // Legacy field
      colors: null, // Legacy field
      stock: totalStock || 0
    }

    console.log('[Add Product] Отправка данных:', productData)
    console.log('[Add Product] Shop slug:', shopSlug.value)

    if (!shopSlug.value) {
      toast.error(t('common.error'))
      return
    }

    const response = await $fetch(`${config.public.apiBase}/products?shop_slug=${shopSlug.value}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })

    console.log('[Add Product] Товар создан успешно:', response)
    toast.success(t('alerts.shop.productCreated'))
    navigateTo(localePath(`/shop/${shopSlug.value}/admin/products`))
  } catch (e) {
    console.error('[Add Product] Ошибка при создании товара:', e)
    console.error('[Add Product] Детали ошибки:', {
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
  background: #f8fafc;
  color: #1e293b;
}

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
    padding-top: 60px;
    padding: 20px;
  }
}

.add-product-page {
  width: 100%;
  padding: 40px;
  background: #FAFAFA;
  min-height: 100vh;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
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
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: #111;
}

.back-btn:hover {
  background: #111;
  color: white;
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

.form-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
}

.form-section {
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid #E5E7EB;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 0;
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

.form-group {
  margin-bottom: 20px;
}

.error-text {
  color: #EF4444;
  font-size: 0.875rem;
  margin-top: 8px;
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

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease-out;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.help-text-small {
  font-size: 0.7rem;
  color: #9CA3AF;
  margin-top: 4px;
}

/* Images Upload */
.images-upload-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
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
  top: 6px;
  right: 6px;
  display: flex;
  gap: 4px;
}

.btn-set-main,
.btn-remove-image {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-set-main {
  background: #FEF3C7;
}

.btn-remove-image {
  background: #FEE2E2;
  color: #DC2626;
}

.main-badge {
  position: absolute;
  bottom: 6px;
  left: 6px;
  background: #10B981;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
}

.upload-zone {
  border: 2px dashed #e2e8f0;
  border-radius: 20px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-zone:hover {
  border-color: #111;
  background: white;
  box-shadow: 0 10px 20px -10px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.hidden-input {
  display: none !important;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #6B7280;
}

.upload-text {
  font-weight: 700;
  color: #0f172a;
  font-size: 1rem;
}

.upload-hint {
  font-size: 0.875rem;
  color: #64748b;
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
  background: transparent;
  border: none;
  padding: 10px 12px;
}

.url-input-row .input:focus {
  box-shadow: none;
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

.uploading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-align: center;
  color: #6B7280;
  font-size: 0.875rem;
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

input:checked+.toggle-slider {
  background-color: #111;
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

.btn-primary:hover:not(:disabled) {
  background: #2d2d2d;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 40px;
  text-align: center;
}

.error-state p {
  font-size: 1.25rem;
  color: #EF4444;
  margin-bottom: 24px;
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

  .page-header {
    display: none;
  }

  .add-product-page {
    padding: 0;
  }

  .form-card {
    padding: 20px;
    border-radius: 16px;
  }

  .form-section {
    margin-bottom: 24px;
    padding-bottom: 24px;
  }

  .images-preview {
    grid-template-columns: repeat(3, 1fr);
  }
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

.limit-warning {
  display: flex;
  gap: 16px;
  background: #FFFBEB;
  border: 1px solid #FEF3C7;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 24px;
}

.warning-icon {
  font-size: 2rem;
}

.warning-content h3 {
  color: #92400E;
  margin-bottom: 4px;
}

.warning-content p {
  color: #B45309;
  font-size: 0.9375rem;
  margin-bottom: 16px;
}

.btn-upgrade {
  display: inline-block;
  background: #92400E;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  font-size: 0.875rem;
}

.btn-upgrade:hover {
  background: #78350F;
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
  }

  .url-input-row {
    flex-direction: column;
  }

  .btn-add-url {
    width: 100%;
  }

  .form-actions {
    flex-direction: column;
    gap: 12px;
  }

  .form-actions .btn {
    width: 100%;
    text-align: center;
    margin: 0;
  }
}
</style>
