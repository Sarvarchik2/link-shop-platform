<template>
  <div class="banner-page">
    <h1 class="page-title">Banner sozlamalari</h1>

    <div class="banner-editor">
      <!-- Preview -->
      <div class="preview-section">
        <h2 class="section-title">Ko'rinish</h2>
        <div class="banner-preview">
          <div class="preview-content">
            <div class="preview-badge">{{ form.badge_text }}</div>
            <h3 class="preview-title" v-html="form.title.replace(/\\n/g, '<br/>')"></h3>
            <p class="preview-subtitle">{{ form.subtitle }}</p>
            <span class="preview-btn">{{ form.button_text }}</span>
          </div>
          <div class="preview-image">
            <img :src="form.image_url" alt="Banner" />
          </div>
        </div>
      </div>

      <!-- Form -->
      <div class="form-section">
        <h2 class="section-title">Bannerni tahrirlash</h2>
        
        <div class="form-group">
          <label>Badge matni</label>
          <input v-model="form.badge_text" type="text" placeholder="YANGI KELDI" />
        </div>

        <div class="form-group">
          <label>Sarlavha (\n yangi qator uchun)</label>
          <input v-model="form.title" type="text" placeholder="Ray-Ban Meta Smart Glasses" />
        </div>

        <div class="form-group">
          <label>Qo'shimcha matn</label>
          <input v-model="form.subtitle" type="text" placeholder="$299 dan boshlab" />
        </div>

        <div class="form-group">
          <label>Tugma matni</label>
          <input v-model="form.button_text" type="text" placeholder="Xarid qilish" />
        </div>

        <div class="form-group">
          <label>Tugma havolasi</label>
          <input v-model="form.button_link" type="text" placeholder="/products" />
        </div>

        <div class="form-group">
          <label>Rasm URL</label>
          <input v-model="form.image_url" type="text" placeholder="https://..." />
        </div>

        <div class="form-group">
          <label>Yoki rasm yuklang</label>
          <input type="file" accept="image/*" @change="uploadImage" />
        </div>

        <div class="form-group checkbox-group">
          <label>
            <input type="checkbox" v-model="form.is_active" />
            <span>Banner faol</span>
          </label>
        </div>

        <button @click="saveBanner" class="save-btn" :disabled="saving">
          {{ saving ? 'Saqlanmoqda...' : 'Bannerni saqlash' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { token } = useAuth()
const saving = ref(false)

const form = ref({
  badge_text: '',
  title: '',
  subtitle: '',
  button_text: '',
  button_link: '',
  image_url: '',
  is_active: true
})

// Fetch current banner
const { data: banner } = await useFetch('http://localhost:8000/admin/banner', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

watch(banner, (newBanner) => {
  if (newBanner) {
    form.value = {
      badge_text: newBanner.badge_text || '',
      title: newBanner.title || '',
      subtitle: newBanner.subtitle || '',
      button_text: newBanner.button_text || '',
      button_link: newBanner.button_link || '',
      image_url: newBanner.image_url || '',
      is_active: newBanner.is_active ?? true
    }
  }
}, { immediate: true })

const uploadImage = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const result = await $fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    form.value.image_url = result.url
    useToast().success('Rasm yuklandi!')
  } catch (e) {
    useToast().error('Rasmni yuklashda xatolik')
  }
}

const saveBanner = async () => {
  saving.value = true
  try {
    await $fetch('http://localhost:8000/admin/banner', {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: form.value
    })
    useToast().success('Banner saqlandi!')
  } catch (e) {
    useToast().error('Bannerni saqlashda xatolik')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.banner-page {
  /* Layout handled by admin.vue */
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 24px;
}

.banner-editor {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #374151;
}

/* Preview Section */
.preview-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
}

.banner-preview {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 24px;
  padding: 40px;
  color: white;
  position: relative;
  overflow: hidden;
  min-height: 300px;
  display: flex;
  align-items: center;
}

.preview-content {
  z-index: 2;
  max-width: 60%;
}

.preview-badge {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 16px;
  border: 1px solid rgba(255,255,255,0.2);
  letter-spacing: 1px;
}

.preview-title {
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 12px;
}

.preview-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 24px;
}

.preview-btn {
  display: inline-block;
  background: white;
  color: #111;
  padding: 14px 32px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.875rem;
}

.preview-image {
  position: absolute;
  right: -30px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 45%;
  height: 110%;
  opacity: 0.4;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Form Section */
.form-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-group input[type="text"],
.form-group input[type="file"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.form-group input[type="text"]:focus {
  outline: none;
  border-color: #111;
}

.form-group input[type="file"] {
  padding: 10px;
  background: #F9FAFB;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #111;
}

.save-btn {
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

.save-btn:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .banner-editor {
    grid-template-columns: 1fr;
  }

  .preview-section {
    order: 2;
  }

  .form-section {
    order: 1;
  }
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.5rem;
  }

  .banner-preview {
    padding: 24px;
    min-height: 220px;
  }

  .preview-content {
    max-width: 70%;
  }

  .preview-title {
    font-size: 1.5rem;
  }

  .preview-subtitle {
    font-size: 0.875rem;
  }

  .preview-btn {
    padding: 10px 24px;
    font-size: 0.75rem;
  }

  .preview-image {
    opacity: 0.2;
  }
}
</style>

