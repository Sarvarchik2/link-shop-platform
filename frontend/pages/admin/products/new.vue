<template>
  <div class="add-product-page">
    <div class="page-header">
      <NuxtLink to="/admin/products" class="back-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </NuxtLink>
      <h1 class="page-title">Yangi mahsulot qo'shish</h1>
    </div>
    
    <div class="form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-section">
          <h2 class="section-title">Asosiy ma'lumotlar</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label class="label">Mahsulot nomi</label>
              <input v-model="form.name" required class="input" placeholder="masalan, Ray-Ban Wayfarer" />
            </div>
            
            <div class="form-group">
              <label class="label">Narx ($)</label>
              <input v-model.number="form.price" type="number" step="0.01" required class="input" placeholder="0.00" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="label">Brend</label>
              <select v-model="form.brand" required class="input">
                <option value="">Brendni tanlang</option>
                <option v-for="brand in brands" :key="brand.id" :value="brand.name">{{ brand.name }}</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="label">Kategoriya</label>
              <select v-model="form.category" required class="input">
                <option value="">Kategoriyani tanlang</option>
                <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="label">Tavsif</label>
            <textarea v-model="form.description" rows="4" required class="input" placeholder="Mahsulot tavsifi..."></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2 class="section-title">Rasmlar</h2>
          
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
                  <button v-if="index !== 0" type="button" @click="setMainImage(index)" class="btn-set-main" title="Set as main">
                    ⭐
                  </button>
                  <button type="button" @click="removeImage(index)" class="btn-remove-image" title="Remove">
                    ✕
                  </button>
                </div>
                <span v-if="index === 0" class="main-badge">Asosiy</span>
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
                <span class="upload-text">Rasmlarni yuklash uchun bosing yoki sudrab tashlang</span>
                <span class="upload-hint">PNG, JPG 5MB gacha</span>
              </div>
          </div>

            <!-- OR URL Input -->
            <div class="url-input-section">
              <span class="divider-text">yoki URL orqali qo'shing</span>
              <div class="url-input-row">
                <input v-model="imageUrl" class="input" placeholder="https://example.com/image.jpg" />
                <button type="button" @click="addImageUrl" class="btn-add-url" :disabled="!imageUrl">Qo'shish</button>
              </div>
            </div>
          </div>
          
          <p v-if="uploadingImages" class="uploading-text">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            Rasmlar yuklanmoqda...
          </p>
        </div>

        <div class="form-section">
          <h2 class="section-title">Mahsulot variantlari</h2>
          <p class="help-text">O'lcham va rang kombinatsiyalarini zaxira miqdori bilan qo'shing</p>
          
          <div class="variants-list">
            <div v-for="(variant, index) in variants" :key="index" class="variant-row">
              <input v-model="variant.size" class="input variant-size-input" placeholder="O'lcham (masalan, M, L)" />
              <input v-model="variant.color" class="input variant-color-input" placeholder="Rang (masalan, Qora)" />
              <input v-model="variant.colorHex" type="color" class="color-picker" title="Rang tanlash" />
              <input v-model.number="variant.stock" type="number" min="0" class="input stock-input" placeholder="Zaxira" />
              <button type="button" @click="removeVariant(index)" class="btn-remove">✕</button>
            </div>
          </div>
          
          <button type="button" @click="addVariant" class="btn-add">
            + Variant qo'shish
          </button>
          <p class="help-text">Har bir variant = o'lcham + rang + zaxira miqdori</p>
        </div>

        <div class="form-actions">
          <NuxtLink to="/admin/products" class="btn btn-secondary">Bekor qilish</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading || uploadedImages.length === 0">
            {{ loading ? 'Yaratilmoqda...' : 'Mahsulot yaratish' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { token } = useAuth()
const loading = ref(false)
const uploadingImages = ref(false)
const { data: brands } = await useFetch('http://localhost:8000/brands', { server: false })
const { data: categories } = await useFetch('http://localhost:8000/categories', { server: false })

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
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await $fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData
        })
        
        uploadedImages.value.push(response.url)
      } catch (e) {
        console.error('Failed to upload image:', e)
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
  description: ''
})

const toast = useToast()

const handleSubmit = async () => {
  if (uploadedImages.value.length === 0) {
    toast.warning('Iltimos, kamida bitta rasm qo\'shing')
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
    
    await $fetch('http://localhost:8000/products', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })
    
    toast.success('Mahsulot muvaffaqiyatli yaratildi!')
    navigateTo('/admin/products')
  } catch (e) {
    console.error(e)
    toast.error('Mahsulot yaratishda xatolik')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-product-page {
  width: 100%;
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

@media (max-width: 768px) {
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
