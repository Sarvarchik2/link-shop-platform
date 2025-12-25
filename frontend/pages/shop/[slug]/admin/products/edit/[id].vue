<template>
  <div v-if="shopSlug" class="shop-admin-page">
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
      <span class="mobile-title">Редактировать товар</span>
    </header>

    <ShopAdminSidebar 
      :shop-slug="shopSlug" 
      current-route="products"
      v-model="sidebarOpen"
    />

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
          <h1 class="page-title">Редактировать товар</h1>
        </div>
        
        <div v-if="productLoading" class="loading-state">
          <p>Загрузка данных товара...</p>
        </div>
        
        <div v-else class="form-card">
          <form @submit.prevent="handleSubmit">
            <div class="form-section">
              <h2 class="section-title">Основная информация</h2>
              
              <div class="form-row">
                <div class="form-group">
                  <label class="label">Название товара</label>
                  <input v-model="form.name" required class="input" placeholder="например, Ray-Ban Wayfarer" />
                </div>
                
                <div class="form-group">
                  <label class="label">Цена ($)</label>
                  <input v-model.number="form.price" type="number" step="0.01" required class="input" placeholder="0.00" />
                </div>
                
                <div class="form-group">
                  <label class="label">Скидка (%)</label>
                  <input v-model.number="form.discount" type="number" step="0.1" min="0" max="100" class="input" placeholder="0" />
                  <p class="help-text-small">Введите процент скидки (0-100)</p>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="label">Бренд</label>
                  <select v-model="form.brand" required class="input" :disabled="!brands || brands.length === 0">
                    <option value="">{{ brands && brands.length > 0 ? 'Выберите бренд' : 'Загрузка брендов...' }}</option>
                    <option v-for="brand in brands" :key="brand.id" :value="brand.name">{{ brand.name }}</option>
                  </select>
                  <p v-if="brandsError" class="error-text">Ошибка загрузки брендов.</p>
                </div>
                
                <div class="form-group">
                  <label class="label">Категория</label>
                  <select v-model="form.category" required class="input" :disabled="!categories || categories.length === 0">
                    <option value="">{{ categories && categories.length > 0 ? 'Выберите категорию' : 'Загрузка категорий...' }}</option>
                    <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}</option>
                  </select>
                  <p v-if="categoriesError" class="error-text">Ошибка загрузки категорий.</p>
                </div>
              </div>

              <div class="form-group">
                <label class="label">Описание</label>
                <textarea v-model="form.description" rows="4" required class="input" placeholder="Описание товара..."></textarea>
              </div>
            </div>

            <div class="form-section">
              <h2 class="section-title">Изображения</h2>
              
              <div class="images-upload-area">
                <div class="images-preview" v-if="uploadedImages.length > 0">
                  <div 
                    v-for="(img, index) in uploadedImages" 
                    :key="index" 
                    class="image-preview-item"
                    :class="{ 'main-image': index === 0 }"
                  >
                    <img :src="img" alt="Product image" />
                    <div class="image-actions">
                      <button v-if="index !== 0" type="button" @click="setMainImage(index)" class="btn-set-main" title="Сделать главным">
                        ⭐
                      </button>
                      <button type="button" @click="removeImage(index)" class="btn-remove-image" title="Удалить">
                        ✕
                      </button>
                    </div>
                    <span v-if="index === 0" class="main-badge">Главное</span>
                  </div>
                </div>
                
                <div class="upload-zone" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
                  <input 
                    ref="fileInput" 
                    type="file" 
                    accept="image/*" 
                    multiple 
                    @change="handleFileSelect" 
                    class="hidden-input" 
                  />
                  <div class="upload-content">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    <span class="upload-text">Нажмите или перетащите изображения</span>
                    <span class="upload-hint">PNG, JPG до 5MB</span>
                  </div>
                </div>

                <div class="url-input-section">
                  <span class="divider-text">или добавьте по URL</span>
                  <div class="url-input-row">
                    <input v-model="imageUrl" class="input" placeholder="https://example.com/image.jpg" />
                    <button type="button" @click="addImageUrl" class="btn-add-url" :disabled="!imageUrl">Добавить</button>
                  </div>
                </div>
              </div>
              
              <p v-if="uploadingImages" class="uploading-text">Загрузка изображений...</p>
            </div>

            <div class="form-section">
              <h2 class="section-title">Варианты товара</h2>
              <p class="help-text">Добавьте комбинации размера и цвета с количеством на складе</p>
              
              <div class="variants-list">
                <div v-for="(variant, index) in variants" :key="index" class="variant-row">
                  <input v-model="variant.size" class="input variant-size-input" placeholder="Размер" />
                  <input v-model="variant.color" class="input variant-color-input" placeholder="Цвет" />
                  <input v-model="variant.colorHex" type="color" class="color-picker" title="Выбрать цвет" />
                  <input v-model.number="variant.stock" type="number" min="0" class="input stock-input" placeholder="Склад" />
                  <button type="button" @click="removeVariant(index)" class="btn-remove">✕</button>
                </div>
              </div>
              
              <button type="button" @click="addVariant" class="btn-add">
                + Добавить вариант
              </button>
            </div>

            <div class="form-actions">
              <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="btn btn-secondary">Отмена</NuxtLink>
              <button type="submit" class="btn btn-primary" :disabled="loading || uploadedImages.length === 0">
                {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
  <div v-else class="error-state">
    <p>Ошибка: не удалось загрузить информацию о магазине</p>
    <NuxtLink to="/profile" class="btn btn-primary">Вернуться в профиль</NuxtLink>
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

const form = reactive({
  name: '',
  brand: '',
  category: '',
  price: 0,
  discount: 0,
  description: ''
})

const handleLogout = () => {
  logout()
  toast.success('Вы вышли из аккаунта')
}

onMounted(async () => {
  if (!shopSlug.value || !productId.value) return
  
  try {
    // 1. Fetch product data
    const product = await $fetch(`http://localhost:8000/products/${productId.value}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    
    // Fill form
    form.name = product.name
    form.brand = product.brand
    form.category = product.category
    form.price = product.price
    form.discount = product.discount
    form.description = product.description
    
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
      $fetch(`http://localhost:8000/brands?shop_slug=${shopSlug.value}`, {
        headers: { Authorization: `Bearer ${token.value}` }
      }),
      $fetch(`http://localhost:8000/categories?shop_slug=${shopSlug.value}`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
    ])
    
    brands.value = brandsData || []
    categories.value = categoriesData || []
  } catch (e) {
    console.error('[Edit Product] Ошибка загрузки:', e)
    toast.error('Ошибка при загрузке данных товара')
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
        const response = await $fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData
        })
        uploadedImages.value.push(response.url)
        toast.success(`Изображение "${file.name}" загружено`)
      } catch (e) {
        toast.error(`Ошибка при загрузке "${file.name}"`)
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
    toast.warning('Пожалуйста, добавьте хотя бы одно изображение')
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
    
    await $fetch(`http://localhost:8000/products/${productId.value}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })
    
    toast.success('Товар успешно обновлен!')
    navigateTo(`/shop/${shopSlug.value}/admin/products`)
  } catch (e) {
    console.error('[Edit Product] Ошибка при обновлении:', e)
    toast.error(e.data?.detail || e.message || 'Ошибка при обновлении товара')
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

.admin-sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
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
  font-weight: 500;
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
    padding-top: 80px;
    padding: 20px;
  }
}

@media (max-width: 640px) {
  .form-card {
    padding: 24px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .variant-row {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  
  .stock-input, .btn-remove {
    grid-column: span 1;
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
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

.btn-remove-image, .btn-set-main {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove-image { background: #FEE2E2; color: #DC2626; }
.btn-set-main { background: #FEF3C7; }

.upload-zone {
  border: 2px dashed #E5E7EB;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  margin-bottom: 20px;
}

.hidden-input { display: none; }

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
</style>
