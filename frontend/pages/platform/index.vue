<template>
  <div class="platform-page">
    <div class="platform-header">
      <div class="container">
        <h1 class="platform-title">Link Shop Platform</h1>
        <p class="platform-subtitle">Создайте свой интернет-магазин за минуты</p>
        <NuxtLink to="/platform/register" class="cta-button">
          Создать магазин
        </NuxtLink>
      </div>
    </div>

    <main class="container py-8">
      <section class="mb-8">
        <div class="section-header">
          <h2 class="section-title">Все магазины</h2>
        </div>
        
        <div v-if="pending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Магазины загружаются...</p>
        </div>
        
        <div v-else-if="shops && shops.length > 0" class="shops-grid">
          <NuxtLink 
            v-for="shop in shops" 
            :key="shop.id"
            :to="`/${shop.slug}`"
            class="shop-card"
          >
            <div class="shop-logo-wrapper">
              <img 
                v-if="shop.logo_url" 
                :src="shop.logo_url" 
                :alt="shop.name" 
                class="shop-logo-img" 
              />
              <div v-else class="shop-logo-placeholder">
                {{ shop.name.charAt(0).toUpperCase() }}
              </div>
            </div>
            <h3 class="shop-name">{{ shop.name }}</h3>
            <p v-if="shop.description" class="shop-description">{{ shop.description }}</p>
            <div class="shop-status">
              <span :class="['status-badge', getStatusClass(shop.subscription_status)]">
                {{ getStatusText(shop.subscription_status) }}
              </span>
            </div>
          </NuxtLink>
        </div>
        
        <div v-else class="text-center py-12 text-gray-400">
          <p>Пока нет зарегистрированных магазинов</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const { data: shops, pending } = await useFetch(useRuntimeConfig().public.apiBase + '/platform/shops', { server: false })

const getStatusClass = (status) => {
  const statusMap = {
    'trial': 'status-trial',
    'active': 'status-active',
    'expired': 'status-expired',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || 'status-trial'
}

const getStatusText = (status) => {
  const statusMap = {
    'trial': 'Пробный период',
    'active': 'Активен',
    'expired': 'Истек',
    'cancelled': 'Отменен'
  }
  return statusMap[status] || status
}
</script>

<style scoped>
.platform-page {
  min-height: 100vh;
  background: #FAFAFA;
}

.platform-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
}

.platform-title {
  font-size: 3.5rem;
  font-weight: 900;
  margin-bottom: 16px;
  letter-spacing: -1px;
}

.platform-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 32px;
}

.cta-button {
  display: inline-block;
  background: white;
  color: #111;
  padding: 16px 40px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255,255,255,0.2);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255,255,255,0.3);
}

.section-header {
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  letter-spacing: -0.5px;
}

.shops-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.shop-card {
  background: white;
  border: 2px solid #f0f0f0;
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  color: #111;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.shop-card:hover {
  border-color: #111;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.shop-logo-wrapper {
  width: 100px;
  height: 100px;
  background: #f9f9f9;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.shop-logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.shop-logo-placeholder {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
}

.shop-name {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0;
}

.shop-description {
  font-size: 0.875rem;
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.shop-status {
  margin-top: auto;
}

.status-badge {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .platform-title {
    font-size: 2rem;
  }
  
  .platform-subtitle {
    font-size: 1rem;
  }
  
  .shops-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .shop-card {
    padding: 24px;
  }
}
</style>

