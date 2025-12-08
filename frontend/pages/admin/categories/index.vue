<template>
  <div class="categories-page">
    <div class="page-header">
      <h1 class="page-title">Kategoriyalar</h1>
      <NuxtLink to="/admin/categories/new" class="btn btn-primary">
        + Kategoriya qo'shish
      </NuxtLink>
    </div>
    
    <div v-if="!categories || categories.length === 0" class="empty-state">
      <p>Kategoriyalar topilmadi</p>
    </div>
    
    <div v-else class="categories-grid">
      <div v-for="category in categories" :key="category.id" class="category-card">
        <div class="category-image-wrapper">
          <img :src="category.image_url" :alt="category.name" class="category-image" />
        </div>
        <div class="category-info">
          <h3 class="category-name">{{ category.name }}</h3>
          <button @click="deleteCategory(category.id)" class="btn-delete">
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
const { data: categories, refresh } = await useFetch('http://localhost:8000/categories', {
  server: false
})

const deleteCategory = async (id) => {
  if (!confirm('Haqiqatan ham bu kategoriyani o\'chirmoqchimisiz?')) return
  try {
    await $fetch(`http://localhost:8000/categories/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    refresh()
  } catch (e) {
    useToast().error('Kategoriyani o\'chirishda xatolik')
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

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
}

.category-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.category-image-wrapper {
  width: 100%;
  height: 180px;
  background: #F9FAFB;
  overflow: hidden;
}

.category-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-info {
  padding: 20px;
}

.category-name {
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
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .category-card {
    border-radius: 16px;
  }
  
  .category-image-wrapper {
    height: 140px;
  }
  
  .category-info {
    padding: 16px;
  }
}

@media (min-width: 1200px) {
  .categories-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
