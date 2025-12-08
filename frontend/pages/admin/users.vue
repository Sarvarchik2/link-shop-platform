<template>
  <div class="users-page">
    <h1 class="page-title">Foydalanuvchilar</h1>
    
    <div class="users-stats">
      <div class="stat-card">
        <span class="stat-value">{{ users?.length || 0 }}</span>
        <span class="stat-label">Jami foydalanuvchilar</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">{{ adminCount }}</span>
        <span class="stat-label">Adminlar</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">{{ userCount }}</span>
        <span class="stat-label">Mijozlar</span>
      </div>
    </div>
    
    <div class="users-list">
      <div v-for="user in users" :key="user.id" class="user-card" @click="toggleUser(user.id)">
        <div class="user-avatar">
          {{ getInitials(user) }}
        </div>
        <div class="user-info">
          <div class="user-name">
            {{ user.first_name || 'Ism yo\'q' }} {{ user.last_name || '' }}
              <span class="role-badge" :class="user.role">{{ user.role }}</span>
          </div>
          <div class="user-phone">{{ user.phone }}</div>
        </div>
        <div class="user-id">ID: {{ user.id }}</div>
        <button class="expand-btn" :class="{ expanded: expandedUser === user.id }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
        
        <!-- Expanded Details -->
        <div v-if="expandedUser === user.id" class="user-details" @click.stop>
          <div class="detail-section">
            <h4 class="detail-title">Aloqa ma'lumotlari</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Telefon</span>
                <span class="detail-value">{{ user.phone }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Ism</span>
                <span class="detail-value">{{ user.first_name || '-' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Familiya</span>
                <span class="detail-value">{{ user.last_name || '-' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Rol</span>
                <span class="detail-value">{{ user.role }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-actions">
            <button v-if="user.role !== 'admin'" class="btn-action promote" @click="promoteUser(user.id)">
              Admin qilish
            </button>
            <button v-if="user.role === 'admin' && user.phone !== 'admin'" class="btn-action demote" @click="demoteUser(user.id)">
              Adminlikni olib tashlash
            </button>
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
const expandedUser = ref(null)

const { data: users, refresh } = await useFetch('http://localhost:8000/admin/users', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const adminCount = computed(() => users.value?.filter(u => u.role === 'admin').length || 0)
const userCount = computed(() => users.value?.filter(u => u.role === 'user').length || 0)

const getInitials = (user) => {
  const first = user.first_name?.[0] || user.phone?.[0] || '?'
  const last = user.last_name?.[0] || ''
  return (first + last).toUpperCase()
}

const toggleUser = (userId) => {
  expandedUser.value = expandedUser.value === userId ? null : userId
}

const promoteUser = async (userId) => {
  // This would need a backend endpoint to update user role
  useToast().info('Tez orada: Foydalanuvchini admin qilish')
}

const demoteUser = async (userId) => {
  // This would need a backend endpoint to update user role
  useToast().info('Tez orada: Admin rolini olib tashlash')
}
</script>

<style scoped>
.users-page {
  width: 100%;
}

/* Page title styles are now in admin layout */

.users-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.user-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #000000 0%, #0e0e0e 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 150px;
}

.user-name {
  font-weight: 600;
  color: #111;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.user-phone {
  font-size: 0.875rem;
  color: #6B7280;
  margin-top: 2px;
}

.role-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
}

.role-badge.admin {
  background: #DBEAFE;
  color: #1E40AF;
}

.role-badge.user {
  background: #F3F4F6;
  color: #6B7280;
}

.user-id {
  font-size: 0.875rem;
  color: #9CA3AF;
  font-weight: 500;
}

.expand-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #F3F4F6;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.expand-btn.expanded {
  transform: rotate(180deg);
}

.user-details {
  width: 100%;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E5E7EB;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #374151;
  margin-bottom: 12px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.detail-value {
  font-weight: 500;
  color: #111;
}

.detail-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-action {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-action.promote {
  background: #DBEAFE;
  color: #1E40AF;
}

.btn-action.promote:hover {
  background: #BFDBFE;
}

.btn-action.demote {
  background: #FEE2E2;
  color: #DC2626;
}

.btn-action.demote:hover {
  background: #FECACA;
}

@media (max-width: 768px) {
  .users-stats {
    grid-template-columns: 1fr;
  }
  
  .user-card {
    padding: 16px;
  }
  
  .user-id {
    display: none;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
