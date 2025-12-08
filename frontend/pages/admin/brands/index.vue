<template>
  <div class="brands-page">
    <div class="page-header">
      <h1 class="page-title">Brendlar</h1>
      <NuxtLink to="/admin/brands/new" class="btn btn-primary">
        + Brend qo'shish
      </NuxtLink>
    </div>
    
    <div v-if="!brands || brands.length === 0" class="empty-state">
      <p>Brendlar topilmadi</p>
    </div>
    
    <div v-else class="brands-grid">
      <div v-for="brand in brands" :key="brand.id" class="brand-card">
        <div class="brand-logo-wrapper">
          <img :src="brand.logo_url" :alt="brand.name" class="brand-logo" />
        </div>
        <div class="brand-info">
          <h3 class="brand-name">{{ brand.name }}</h3>
          <button @click="deleteBrand(brand.id)" class="btn-delete">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            O'chirish
          </button>
        </div>
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
const { data: brands, refresh } = await useFetch('http://localhost:8000/brands', {
  server: false
})

const deleteBrand = async (id) => {
  if (!confirm('Haqiqatan ham bu brendni o\'chirmoqchimisiz?')) return
  try {
    await $fetch(`http://localhost:8000/brands/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    refresh()
  } catch (e) {
    useToast().error('Brendni o\'chirishda xatolik')
  }
}
</script>

<style scoped>
/* Page title styles are now in admin layout */

.btn {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #000;
  transform: translateY(-1px);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #9CA3AF;
  font-size: 1.125rem;
}

.brands-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
}

.brand-card {
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.brand-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.brand-logo-wrapper {
  width: 120px;
  height: 120px;
  background: #F9FAFB;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  margin-bottom: 20px;
}

.brand-logo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.brand-info {
  width: 100%;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 16px;
}

.btn-delete {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  background: #FEF2F2;
  color: #EF4444;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-delete:hover {
  background: #EF4444;
  color: white;
}

@media (max-width: 768px) {
  .brands-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .brand-card {
    padding: 24px 16px;
  }
  
  .brand-logo-wrapper {
    width: 100px;
    height: 100px;
  }
}

@media (min-width: 1200px) {
  .brands-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
</style>
