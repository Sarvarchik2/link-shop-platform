<template>
  <div class="landing-page">
    <!-- Navigation Bar -->
    <nav class="platform-navbar">
      <div class="container">
        <div class="nav-content">
          <NuxtLink to="/" class="nav-logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
            <span>Link Shop Platform</span>
          </NuxtLink>
          
          <div class="nav-links">
            <NuxtLink to="/" class="nav-link">Главная</NuxtLink>
            <NuxtLink to="/platform" class="nav-link">Магазины</NuxtLink>
            <NuxtLink to="/register-shop" class="nav-link">Создать магазин</NuxtLink>
          </div>
          
          <div class="nav-actions">
            <template v-if="token || user">
              <button @click="goToProfile" class="nav-btn profile-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Профиль
              </button>
            </template>
            
            <template v-else>
              <NuxtLink to="/login" class="nav-btn login-btn">Войти</NuxtLink>
              <NuxtLink to="/register" class="nav-btn register-btn">Зарегистрироваться</NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Создайте свой интернет-магазин за минуты</h1>
          <p class="hero-subtitle">
            Link Shop Platform - это современная платформа для создания и управления интернет-магазинами. 
            Начните продавать онлайн уже сегодня!
          </p>
          <div class="hero-actions">
            <NuxtLink to="/register-shop" class="btn-primary">
              Создать магазин
            </NuxtLink>
            <NuxtLink to="/platform" class="btn-secondary">
              Посмотреть магазины
            </NuxtLink>
          </div>
        </div>
        <div class="hero-image">
          <div class="hero-visual">
            <div class="floating-card card-1">🛍️</div>
            <div class="floating-card card-2">📦</div>
            <div class="floating-card card-3">💳</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">Почему выбирают нас?</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Быстрый старт</h3>
            <p class="feature-description">
              Создайте магазин за несколько минут. Не нужно настраивать серверы или писать код.
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">💰</div>
            <h3 class="feature-title">Гибкие подписки</h3>
            <p class="feature-description">
              Пробный период 30 дней. Выберите план, который подходит именно вам.
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3 class="feature-title">Свой домен</h3>
            <p class="feature-description">
              Ваш магазин будет доступен по уникальному адресу: link-platform-shop.uz/ваш-магазин
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Аналитика</h3>
            <p class="feature-description">
              Полная статистика продаж, заказов и клиентов в удобной админ-панели.
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">Безопасность</h3>
            <p class="feature-description">
              Все данные защищены. Регулярные резервные копии и SSL-шифрование.
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">Мобильная версия</h3>
            <p class="feature-description">
              Ваш магазин автоматически адаптируется под все устройства.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section class="pricing-section">
      <div class="container">
        <h2 class="section-title">Тарифы и подписки</h2>
        <div class="pricing-grid">
          <div class="pricing-card">
            <div class="pricing-header">
              <h3 class="pricing-name">Пробный период</h3>
              <div class="pricing-price">
                <span class="price-amount">Бесплатно</span>
                <span class="price-period">30 дней</span>
              </div>
            </div>
            <ul class="pricing-features">
              <li>✓ Полный доступ ко всем функциям</li>
              <li>✓ Неограниченное количество товаров</li>
              <li>✓ Управление заказами</li>
              <li>✓ Аналитика и статистика</li>
            </ul>
            <NuxtLink to="/register-shop" class="pricing-button">Начать бесплатно</NuxtLink>
          </div>
          
          <div class="pricing-card featured">
            <div class="pricing-badge">Популярный</div>
            <div class="pricing-header">
              <h3 class="pricing-name">Базовый</h3>
              <div class="pricing-price">
                <span class="price-amount">$29</span>
                <span class="price-period">в месяц</span>
              </div>
            </div>
            <ul class="pricing-features">
              <li>✓ Все функции пробного периода</li>
              <li>✓ Приоритетная поддержка</li>
              <li>✓ Расширенная аналитика</li>
              <li>✓ Интеграции с платежными системами</li>
            </ul>
            <NuxtLink to="/register-shop" class="pricing-button">Выбрать план</NuxtLink>
          </div>
          
          <div class="pricing-card">
            <div class="pricing-header">
              <h3 class="pricing-name">Профессиональный</h3>
              <div class="pricing-price">
                <span class="price-amount">$79</span>
                <span class="price-period">в месяц</span>
              </div>
            </div>
            <ul class="pricing-features">
              <li>✓ Все функции базового плана</li>
              <li>✓ API доступ</li>
              <li>✓ Кастомный дизайн</li>
              <li>✓ Персональный менеджер</li>
            </ul>
            <NuxtLink to="/register-shop" class="pricing-button">Выбрать план</NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Shops Section -->
    <section class="shops-section">
      <div class="container">
        <h2 class="section-title">Магазины на платформе</h2>
        <div v-if="shopsPending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Магазины загружаются...</p>
        </div>
        <div v-else-if="shops && shops.length > 0" class="shops-grid">
          <NuxtLink 
            v-for="shop in shops.slice(0, 6)" 
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
        <div v-if="shops && shops.length > 6" class="text-center mt-8">
          <NuxtLink to="/platform" class="btn-secondary">
            Посмотреть все магазины
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">Готовы начать?</h2>
          <p class="cta-subtitle">Создайте свой интернет-магазин прямо сейчас</p>
          <NuxtLink to="/register-shop" class="btn-primary large">
            Создать магазин бесплатно
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const { user, token, fetchUser } = useAuth()

// Загружаем пользователя при монтировании, если есть токен
onMounted(async () => {
  if (token.value && !user.value) {
    await fetchUser()
  }
})

// Получаем магазины пользователя для навигационной панели
const { data: myShops, refresh: refreshShops } = await useFetch('http://localhost:8000/platform/shops/me', {
  server: false,
  headers: token.value ? {
    'Authorization': `Bearer ${token.value}`
  } : {},
  watch: [token],
  immediate: false
})

// Обновляем список магазинов при изменении токена
watch(token, async (newToken) => {
  if (newToken) {
    await refreshShops()
  }
}, { immediate: true })

// Функция для перехода в профиль с автоматическим перенаправлением
const goToProfile = async () => {
  // Если пользователь не загружен, загружаем
  if (token.value && !user.value) {
    await fetchUser()
  }
  
  // Если нет токена - на страницу входа
  if (!token.value) {
    await navigateTo('/login')
    return
  }
  
  // Если админ платформы - сразу в админку платформы
  if (user.value?.role === 'platform_admin') {
    await navigateTo('/platform/admin')
    return
  }
  
  // Обновляем список магазинов перед проверкой
  if (token.value) {
    await refreshShops()
  }
  
  // Если владелец магазина - в админку первого магазина
  if (myShops.value && myShops.value.length > 0) {
    await navigateTo(`/shop/${myShops.value[0].slug}/admin`)
    return
  }
  
  // Иначе в профиль
  await navigateTo('/profile')
}

const { data: shops, pending: shopsPending } = await useFetch('http://localhost:8000/platform/shops', { server: false })

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
.landing-page {
  min-height: 100vh;
  background: #FAFAFA;
}

/* Platform Navigation Bar */
.platform-navbar {
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 900;
  font-size: 1.125rem;
  color: #111;
  text-decoration: none;
  transition: opacity 0.2s;
}

.nav-logo:hover {
  opacity: 0.8;
}

.nav-logo svg {
  color: #111;
}

.nav-links {
  display: flex;
  gap: 32px;
  align-items: center;
  flex: 1;
  justify-content: center;
}

.nav-link {
  font-weight: 600;
  font-size: 0.95rem;
  color: #666;
  text-decoration: none;
  transition: color 0.2s;
  position: relative;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #111;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background: #111;
}

.nav-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.2s;
  border: 2px solid transparent;
  cursor: pointer;
  background: transparent;
  color: #111;
}

.nav-btn.profile-btn {
  background: #F3F4F6;
  color: #111;
}

.nav-btn.profile-btn:hover {
  background: #E5E7EB;
  transform: translateY(-2px);
}

.nav-btn.login-btn {
  background: transparent;
  color: #111;
  border-color: #E5E7EB;
}

.nav-btn.login-btn:hover {
  border-color: #111;
  background: #F9FAFB;
}

.nav-btn.register-btn {
  background: #111;
  color: white;
}

.nav-btn.register-btn:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

@media (max-width: 768px) {
  .nav-content {
    flex-wrap: wrap;
  }
  
  .nav-links {
    order: 3;
    width: 100%;
    justify-content: center;
    gap: 16px;
    padding-top: 12px;
    border-top: 1px solid #E5E7EB;
  }
  
  .nav-actions {
    gap: 8px;
  }
  
  .nav-btn {
    padding: 8px 16px;
    font-size: 0.75rem;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 100px 0;
  position: relative;
  overflow: hidden;
}

.hero-section .container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-content {
  z-index: 2;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-block;
  background: white;
  color: #111;
  padding: 16px 32px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255,255,255,0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255,255,255,0.3);
}

.btn-primary.large {
  padding: 20px 40px;
  font-size: 1.125rem;
}

.btn-secondary {
  display: inline-block;
  background: transparent;
  color: white;
  padding: 16px 32px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.1);
  border-color: white;
}

.hero-image {
  position: relative;
  height: 400px;
}

.hero-visual {
  position: relative;
  width: 100%;
  height: 100%;
}

.floating-card {
  position: absolute;
  width: 120px;
  height: 120px;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  animation: float 3s ease-in-out infinite;
}

.card-1 {
  top: 0;
  left: 0;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  animation-delay: 1s;
}

.card-3 {
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Features Section */
.features-section {
  padding: 80px 0;
  background: white;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 900;
  text-align: center;
  margin-bottom: 60px;
  color: #111;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.feature-card {
  background: #F9FAFB;
  border-radius: 24px;
  padding: 40px;
  text-align: center;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 12px;
  color: #111;
}

.feature-description {
  color: #666;
  line-height: 1.6;
}

/* Pricing Section */
.pricing-section {
  padding: 80px 0;
  background: #FAFAFA;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1100px;
  margin: 0 auto;
}

.pricing-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  position: relative;
  transition: all 0.3s;
}

.pricing-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.pricing-card.featured {
  border: 3px solid #111;
  transform: scale(1.05);
}

.pricing-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #111;
  color: white;
  padding: 6px 20px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.pricing-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 2px solid #F3F4F6;
}

.pricing-name {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 16px;
  color: #111;
}

.pricing-price {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.price-amount {
  font-size: 3rem;
  font-weight: 900;
  color: #111;
}

.price-period {
  font-size: 0.875rem;
  color: #666;
}

.pricing-features {
  list-style: none;
  padding: 0;
  margin: 0 0 32px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pricing-features li {
  color: #666;
  line-height: 1.6;
}

.pricing-button {
  display: block;
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border-radius: 12px;
  text-align: center;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
}

.pricing-button:hover {
  background: #000;
  transform: translateY(-2px);
}

/* Shops Section */
.shops-section {
  padding: 80px 0;
  background: white;
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
  transition: all 0.3s;
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

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
}

.cta-content {
  text-align: center;
}

.cta-title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 16px;
}

.cta-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 40px;
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

@media (max-width: 1024px) {
  .hero-section .container {
    grid-template-columns: 1fr;
  }
  
  .features-grid,
  .pricing-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .pricing-card.featured {
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .features-grid,
  .pricing-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
    text-align: center;
  }
}
</style>
