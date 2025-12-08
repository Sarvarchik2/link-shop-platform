<template>
  <div class="products-page">
    <div class="page-header">
      <h1 class="page-title">Mahsulotlar</h1>
      <NuxtLink to="/admin/products/new" class="btn btn-primary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        <span class="btn-text">Mahsulot qo'shish</span>
      </NuxtLink>
    </div>
    
    <div v-if="!products || products.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
      </div>
      <h3>Hozircha mahsulotlar yo'q</h3>
      <p>Boshlash uchun birinchi mahsulotingizni qo'shing</p>
      <NuxtLink to="/admin/products/new" class="btn btn-primary">Mahsulot qo'shish</NuxtLink>
    </div>
    
    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="product-image">
          <img :src="product.image_url" :alt="product.name" />
          <div class="product-actions">
            <NuxtLink :to="`/admin/products/edit/${product.id}`" class="btn-action btn-edit">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </NuxtLink>
            <button @click="deleteProduct(product.id)" class="btn-action btn-delete">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
        <div class="product-info">
          <div class="product-category">{{ product.category }}</div>
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-brand">{{ product.brand }}</div>
          <div class="product-footer">
            <div class="product-price">${{ product.price.toFixed(2) }}</div>
            <div class="product-stock" :class="{ 'out-of-stock': product.stock === 0 }">
              {{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}
            </div>
          </div>
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
const { data: products, refresh } = await useFetch('http://localhost:8000/products', {
  server: false
})

const deleteProduct = async (id) => {
  if (!confirm('Are you sure you want to delete this product?')) return
  try {
    await $fetch(`http://localhost:8000/products/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    refresh()
  } catch (e) {
    useToast().error('Failed to delete product')
  }
}
</script>

<style scoped>
.products-page {
  width: 100%;
}

/* Page header and title styles are now in admin layout */

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
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
  background: white;
  border-radius: 20px;
  border: 1px solid #E5E7EB;
}

.empty-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  color: #D1D5DB;
}

.empty-icon svg {
  width: 64px;
  height: 64px;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.empty-state p {
  color: #6B7280;
  margin-bottom: 24px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.product-image {
  position: relative;
  background: #F9FAFB;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.product-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.2s;
}

.product-card:hover .product-actions {
  opacity: 1;
}

.btn-action {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-edit {
  background: white;
  color: #3B82F6;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.btn-edit:hover {
  background: #3B82F6;
  color: white;
}

.btn-delete {
  background: white;
  color: #EF4444;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.btn-delete:hover {
  background: #EF4444;
  color: white;
}

.product-info {
  padding: 16px;
}

.product-category {
  font-size: 0.65rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.product-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 2px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-brand {
  font-size: 0.8rem;
  color: #6B7280;
  margin-bottom: 12px;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 800;
  color: #111;
}

.product-stock {
  font-size: 0.7rem;
  font-weight: 600;
  color: #10B981;
  background: #ECFDF5;
  padding: 4px 8px;
  border-radius: 6px;
}

.product-stock.out-of-stock {
  color: #EF4444;
  background: #FEF2F2;
}

/* Mobile always show actions */
@media (max-width: 768px) {
  .page-header {
    flex-wrap: wrap;
  }
  
  .btn-text {
    display: none;
  }
  
  .btn {
    padding: 12px;
  }
  
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .product-card {
    border-radius: 12px;
  }
  
  .product-image {
    padding: 12px;
  }
  
  .product-actions {
    opacity: 1;
  }
  
  .product-info {
    padding: 12px;
  }
  
  .product-name {
    font-size: 0.85rem;
  }
  
  .product-price {
    font-size: 1rem;
  }
  
  .product-stock {
    display: none;
  }
}

@media (min-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
}

@media (min-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
  
  .product-card {
    border-radius: 20px;
  }
  
  .product-image {
    padding: 24px;
  }
  
  .product-info {
    padding: 20px;
  }
  
  .product-name {
    font-size: 1rem;
  }
}
</style>
