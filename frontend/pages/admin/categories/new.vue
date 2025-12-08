<template>
  <div class="add-category-page">
    <div class="page-header">
      <NuxtLink to="/admin/categories" class="back-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        Orqaga
      </NuxtLink>
      <h1 class="page-title">Yangi kategoriya qo'shish</h1>
    </div>
    
    <div class="form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="label">Kategoriya nomi</label>
          <input v-model="form.name" required class="input" placeholder="masalan, Quyoshdan himoya ko'zoynaklari" />
        </div>

        <div class="form-group">
          <label class="label">Kategoriya rasmi</label>
          
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
            <div 
              class="drop-zone"
              :class="{ 'drag-over': isDragging }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p>Rasmni sudrab tashlang yoki yuklash uchun bosing</p>
              <span class="upload-hint">PNG, JPG 5MB gacha</span>
            </div>
            <input 
              ref="fileInput" 
              type="file" 
              accept="image/*" 
              @change="handleFileChange" 
              hidden 
            />
            
            <div class="url-input">
              <span class="or-divider">yoki URL kiriting</span>
              <input 
                v-model="imageUrl" 
                class="input" 
                placeholder="https://example.com/category.png" 
              />
            </div>
          </div>
        </div>

        <div class="form-actions">
          <NuxtLink to="/admin/categories" class="btn btn-outline">Bekor qilish</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading || !form.name || !imageUrl">
            {{ loading ? 'Yaratilmoqda...' : 'Kategoriya yaratish' }}
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
const toast = useToast()
const loading = ref(false)
const isDragging = ref(false)
const imageUrl = ref('')
const fileInput = ref(null)

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
    toast.error('Iltimos, rasm faylini yuklang')
  }
}

const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await $fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    imageUrl.value = response.url
    toast.success('Rasm yuklandi!')
  } catch (e) {
    console.error(e)
    toast.error('Rasmni yuklashda xatolik')
  }
}

const handleSubmit = async () => {
  if (!form.name || !imageUrl.value) {
    toast.warning('Iltimos, barcha maydonlarni to\'ldiring')
    return
  }
  
  loading.value = true
  try {
    await $fetch('http://localhost:8000/categories', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        name: form.name,
        image_url: imageUrl.value
      }
    })
    toast.success('Kategoriya muvaffaqiyatli yaratildi!')
    navigateTo('/admin/categories')
  } catch (e) {
    toast.error('Kategoriyani yaratishda xatolik')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-category-page {
  width: 100%;
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
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
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
  background: rgba(0,0,0,0.7);
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

@media (max-width: 640px) {
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
