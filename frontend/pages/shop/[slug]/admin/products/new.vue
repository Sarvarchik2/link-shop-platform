<template>
  <div v-if="shopSlug" class="shop-admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"></path>
          </svg>
        </div>
        <h2 class="sidebar-title">Панель управления</h2>
      </div>
      
      <nav class="sidebar-nav">
        <NuxtLink :to="`/shop/${shopSlug}/admin`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="nav-item active">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>Товары</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/orders`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>Заказы</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/categories`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
          <span>Категории</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/brands`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            <line x1="7" y1="7" x2="7.01" y2="7"></line>
          </svg>
          <span>Бренды</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/admin/banner`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span>Баннер</span>
        </NuxtLink>
        
        <NuxtLink :to="`/shop/${shopSlug}/subscription`" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <span>Подписка</span>
        </NuxtLink>
      </nav>
      
      <div class="sidebar-footer">
        <NuxtLink :to="`/${shopSlug}`" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>В магазин</span>
        </NuxtLink>
        <button @click="handleLogout" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Выйти</span>
        </button>
      </div>
    </aside>

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
          <h1 class="page-title">Добавить товар</h1>
        </div>
        
        <div class="form-card">
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
              <p v-if="brandsError" class="error-text">Ошибка загрузки брендов. Попробуйте обновить страницу.</p>
            </div>
            
            <div class="form-group">
              <label class="label">Категория</label>
              <select v-model="form.category" required class="input" :disabled="!categories || categories.length === 0">
                <option value="">{{ categories && categories.length > 0 ? 'Выберите категорию' : 'Загрузка категорий...' }}</option>
                <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}</option>
              </select>
              <p v-if="categoriesError" class="error-text">Ошибка загрузки категорий. Попробуйте обновить страницу.</p>
            </div>
          </div>

          <div class="form-group">
            <label class="label">Описание</label>
            <textarea v-model="form.description" rows="4" required class="input" placeholder="Описание товара..."></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2 class="section-title">Изображения</h2>
          
          <!-- Image Upload Area -->
          <div class="images-upload-area">
            <!-- Uploaded Images Preview -->
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
            
            <!-- Upload Button -->
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

            <!-- OR URL Input -->
            <div class="url-input-section">
              <span class="divider-text">или добавьте по URL</span>
              <div class="url-input-row">
                <input v-model="imageUrl" class="input" placeholder="https://example.com/image.jpg" />
                <button type="button" @click="addImageUrl" class="btn-add-url" :disabled="!imageUrl">Добавить</button>
              </div>
            </div>
          </div>
          
          <p v-if="uploadingImages" class="uploading-text">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            Загрузка изображений...
          </p>
        </div>

        <div class="form-section">
          <h2 class="section-title">Варианты товара</h2>
          <p class="help-text">Добавьте комбинации размера и цвета с количеством на складе</p>
          
          <div class="variants-list">
            <div v-for="(variant, index) in variants" :key="index" class="variant-row">
              <input v-model="variant.size" class="input variant-size-input" placeholder="Размер (например, M, L)" />
              <input v-model="variant.color" class="input variant-color-input" placeholder="Цвет (например, Черный)" />
              <input v-model="variant.colorHex" type="color" class="color-picker" title="Выбрать цвет" />
              <input v-model.number="variant.stock" type="number" min="0" class="input stock-input" placeholder="Склад" />
              <button type="button" @click="removeVariant(index)" class="btn-remove">✕</button>
            </div>
          </div>
          
          <button type="button" @click="addVariant" class="btn-add">
            + Добавить вариант
          </button>
          <p class="help-text">Каждый вариант = размер + цвет + количество на складе</p>
        </div>

        <div class="form-actions">
          <NuxtLink :to="`/shop/${shopSlug}/admin/products`" class="btn btn-secondary">Отмена</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading || uploadedImages.length === 0">
            {{ loading ? 'Создание...' : 'Создать товар' }}
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
  useToast().success('Вы вышли из аккаунта')
}

// Проверка что все необходимое загружено
onMounted(() => {
  console.log('[Add Product] Компонент смонтирован, shopSlug:', shopSlug.value)
  if (!shopSlug.value) {
    console.error('[Add Product] КРИТИЧЕСКАЯ ОШИБКА: shopSlug отсутствует!')
  }
})

const loading = ref(false)
const uploadingImages = ref(false)
const brands = ref([])
const categories = ref([])
const brandsError = ref(null)
const categoriesError = ref(null)
const toast = useToast()

onMounted(async () => {
  console.log('[Add Product] Компонент смонтирован, shopSlug:', shopSlug.value)
  
  if (!shopSlug.value) {
    console.error('[Add Product] ОШИБКА: shopSlug отсутствует, невозможно загрузить данные')
    return
  }
  
  // Загружаем данные после монтирования
  try {
    console.log('[Add Product] Загрузка брендов и категорий для shop:', shopSlug.value)
    const [brandsData, categoriesData] = await Promise.all([
      $fetch(`http://localhost:8000/brands?shop_slug=${shopSlug.value}`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      }).catch(e => {
        console.error('[Add Product] Ошибка загрузки брендов:', e)
        brandsError.value = e
        return []
      }),
      $fetch(`http://localhost:8000/categories?shop_slug=${shopSlug.value}`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      }).catch(e => {
        console.error('[Add Product] Ошибка загрузки категорий:', e)
        categoriesError.value = e
        return []
      })
    ])
    
    brands.value = brandsData || []
    categories.value = categoriesData || []
    console.log('[Add Product] Бренды загружены:', brands.value.length)
    console.log('[Add Product] Категории загружены:', categories.value.length)
  } catch (e) {
    console.error('[Add Product] Ошибка при загрузке данных:', e)
  }
})


const fileInput = ref(null)
const uploadedImages = ref([])
const imageUrl = ref('')

const variants = ref([{ size: '', color: '', colorHex: '#000000', stock: 0 }])

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
        
        const response = await $fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData
        })
        
        console.log('[Add Product] Изображение загружено:', response.url)
        uploadedImages.value.push(response.url)
        toast.success(`Изображение "${file.name}" загружено`)
      } catch (e) {
        console.error('[Add Product] Ошибка загрузки изображения:', e)
        console.error('[Add Product] Детали ошибки:', {
          message: e.message,
          statusCode: e.statusCode,
          data: e.data
        })
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

const form = reactive({
  name: '',
  brand: '',
  category: '',
  price: 0,
  discount: 0,
  description: ''
})

const handleSubmit = async () => {
  if (uploadedImages.value.length === 0) {
    toast.warning('Пожалуйста, добавьте хотя бы одно изображение')
    return
  }
  
  // Filter valid variants (both size and color must be filled)
  const validVariants = variants.value.filter(v => v.size.trim() && v.color.trim())
  
  // Calculate total stock from variants
  const totalStock = validVariants.reduce((acc, v) => acc + (v.stock || 0), 0)
  
  loading.value = true
  try {
    const productData = {
      ...form,
      image_url: uploadedImages.value[0],
      images: JSON.stringify(uploadedImages.value),
      variants: validVariants.length > 0 ? JSON.stringify(validVariants) : null,
      sizes: null, // Legacy field
      colors: null, // Legacy field
      stock: totalStock || 0
    }
    
    console.log('[Add Product] Отправка данных:', productData)
    console.log('[Add Product] Shop slug:', shopSlug.value)
    
    if (!shopSlug.value) {
      toast.error('Ошибка: не указан магазин')
      return
    }
    
    const response = await $fetch(`http://localhost:8000/products?shop_slug=${shopSlug.value}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })
    
    console.log('[Add Product] Товар создан успешно:', response)
    toast.success('Товар успешно создан!')
    navigateTo(`/shop/${shopSlug.value}/admin/products`)
  } catch (e) {
    console.error('[Add Product] Ошибка при создании товара:', e)
    console.error('[Add Product] Детали ошибки:', {
      message: e.message,
      statusCode: e.statusCode,
      statusMessage: e.statusMessage,
      data: e.data
    })
    toast.error(e.data?.detail || e.message || 'Ошибка при создании товара')
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

/* Sidebar */
.admin-sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
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
  color: #111;
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
  transition: all 0.2s;
  font-weight: 500;
}

.nav-item:hover {
  background: #F9FAFB;
  color: #111;
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

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: #111;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #EF4444;
  background: none;
  border: none;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
  font-family: inherit;
}

.logout-btn:hover {
  color: #DC2626;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
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

.page-title {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  margin: 0;
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

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
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
  color: #374151;
  margin-bottom: 8px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #F9FAFB;
}

.input:focus {
  outline: none;
  border-color: #111;
  background: white;
}

.help-text {
  font-size: 0.75rem;
  color: #9CA3AF;
  margin-top: 8px;
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
  border: 2px dashed #D1D5DB;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #FAFAFA;
}

.upload-zone:hover {
  border-color: #111;
  background: #F5F5F5;
}

.hidden-input {
  display: none;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #6B7280;
}

.upload-text {
  font-weight: 600;
}

.upload-hint {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.url-input-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.divider-text {
  text-align: center;
  font-size: 0.875rem;
  color: #9CA3AF;
}

.url-input-row {
  display: flex;
  gap: 12px;
}

.url-input-row .input {
  flex: 1;
}

.btn-add-url {
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-url:disabled {
  background: #D1D5DB;
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

/* Variants */
.variants-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.variant-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.variant-size-input,
.variant-color-input {
  flex: 1;
}

.color-picker {
  width: 50px;
  height: 44px;
  padding: 4px;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
}

.stock-input {
  width: 100px;
}

.btn-remove {
  width: 44px;
  height: 44px;
  background: #FEE2E2;
  border: none;
  border-radius: 8px;
  color: #DC2626;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #FECACA;
}

.btn-add {
  padding: 12px 20px;
  background: #F3F4F6;
  border: 2px dashed #D1D5DB;
  border-radius: 12px;
  color: #6B7280;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  width: 100%;
}

.btn-add:hover {
  background: #E5E7EB;
  border-color: #9CA3AF;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 32px;
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
  .admin-sidebar {
    width: 240px;
  }
  
  .admin-main {
    margin-left: 240px;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  
  .admin-main {
    margin-left: 0;
  }
  
  .add-product-page {
    padding: 20px;
  }
  
  .form-card {
    padding: 24px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .images-preview {
    grid-template-columns: repeat(3, 1fr);
  }
}

</style>
