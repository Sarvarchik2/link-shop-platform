<template>
  <div class="customer-profile-page">
    <AppHeader />
    
    <main class="profile-content">
      <div class="profile-layout">
        <!-- Left Column - Profile Card -->
        <div class="profile-left">
          <div class="profile-header">
            <div class="profile-card">
              <div class="profile-avatar">
                <span class="avatar-text">{{ getInitials }}</span>
              </div>
              <h1 class="profile-name">{{ fullName || 'User' }}</h1>
              <p class="profile-role">🛒 Покупатель</p>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="quick-actions" v-if="user">
            <NuxtLink to="/orders" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
              </div>
              <span>Buyurtmalarim</span>
            </NuxtLink>
            <NuxtLink to="/favorites" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
              </div>
              <span>Sevimlilar</span>
            </NuxtLink>
            <NuxtLink to="/cart" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="9" cy="21" r="1"></circle>
                  <circle cx="20" cy="21" r="1"></circle>
                  <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                </svg>
              </div>
              <span>Savatcha</span>
            </NuxtLink>
            <NuxtLink to="/platform" class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                  <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
              </div>
              <span>Платформа</span>
            </NuxtLink>
          </div>
        </div>

        <!-- Right Column - Info & Actions -->
        <div class="profile-right">
          <!-- User Info Section -->
          <div class="info-section">
            <h2 class="section-title">Shaxsiy ma'lumotlar</h2>
            
            <div class="info-card">
              <div class="info-item">
                <div class="info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div class="info-content">
                  <span class="info-label">Ism</span>
                  <span class="info-value">{{ user?.first_name || '—' }}</span>
                </div>
              </div>

              <div class="info-item">
                <div class="info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div class="info-content">
                  <span class="info-label">Familiya</span>
                  <span class="info-value">{{ user?.last_name || '—' }}</span>
                </div>
              </div>

              <div class="info-item">
                <div class="info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                  </svg>
                </div>
                <div class="info-content">
                  <span class="info-label">Telefon raqam</span>
                  <span class="info-value">{{ user?.phone || '—' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Create Shop Section -->
          <div class="create-shop-section">
            <div class="info-box">
              <h3>Хотите создать магазин?</h3>
              <p>Создайте свой интернет-магазин на платформе и начните продавать онлайн</p>
              <NuxtLink to="/register-shop" class="create-shop-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Создать магазин
              </NuxtLink>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <!-- Logout Button -->
            <button @click="handleLogout" class="logout-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              Chiqish
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { user, logout } = useAuth()

const fullName = computed(() => {
  if (!user.value) return ''
  return `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim()
})

const getInitials = computed(() => {
  if (!user.value) return '?'
  const first = user.value.first_name?.[0] || user.value.phone?.[0] || '?'
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase()
})

const handleLogout = () => {
  logout()
}
</script>

<style scoped>
/* Используем те же стили, что и в profile.vue */
.customer-profile-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.profile-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  margin: -20px -20px 0;
  padding: 40px 20px 60px;
  border-radius: 0 0 32px 32px;
}

.profile-card {
  background: white;
  border-radius: 24px;
  padding: 40px 24px 32px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  position: relative;
  margin-top: 30px;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #111;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -70px auto 20px;
  border: 4px solid white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.avatar-text {
  font-size: 2rem;
  font-weight: 800;
  color: white;
}

.profile-name {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
}

.profile-role {
  font-size: 0.875rem;
  color: #6B7280;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 20px 12px;
  text-align: center;
  text-decoration: none;
  color: #111;
  transition: all 0.2s;
  border: 1px solid #E5E7EB;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  border-color: #111;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  color: #111;
  transition: all 0.2s;
}

.action-card:hover .action-icon {
  background: #111;
  color: white;
}

.action-card span {
  font-size: 0.8rem;
  font-weight: 600;
}

.profile-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-section {
  flex: 1;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
  padding-left: 4px;
}

.info-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  border: 1px solid #E5E7EB;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #F3F4F6;
}

.info-item:last-child {
  border-bottom: none;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: #111;
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.info-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 0.95rem;
  color: #111;
  font-weight: 600;
}

.create-shop-section {
  margin-top: 24px;
}

.info-box {
  background: #F9FAFB;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #E5E7EB;
  text-align: center;
}

.info-box h3 {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: #111;
}

.info-box p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
  font-size: 0.875rem;
}

.create-shop-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: linear-gradient(135deg, #111 0%, #374151 100%);
  border: none;
  border-radius: 16px;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.create-shop-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px;
  background: white;
  border: 2px solid #FEE2E2;
  border-radius: 16px;
  color: #DC2626;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #FEF2F2;
  border-color: #FECACA;
  transform: translateY(-2px);
}

@media (min-width: 768px) {
  .profile-layout {
    flex-direction: row;
    gap: 32px;
  }
  
  .profile-left {
    width: 300px;
    flex-shrink: 0;
  }
  
  .profile-right {
    flex: 1;
  }
  
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

