<template>
  <div class="platform-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">Планы подписки</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar 
      :current-route="currentRoute" 
      :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event"
      @logout="handleLogout" 
    />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div class="header-content">
          <div>
            <h1 class="admin-title">Управление планами подписки</h1>
            <p class="admin-subtitle">Создавайте и управляйте планами подписки для магазинов</p>
          </div>
          <button @click="openCreateModal" class="create-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span>Добавить план</span>
          </button>
        </div>
      </div>

      <div class="admin-content">
        <!-- Error State -->
        <div v-if="error" class="error-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p class="error-message">Ошибка загрузки данных: {{ error.message || 'Неизвестная ошибка' }}</p>
          <button @click="refresh" class="retry-btn">Повторить</button>
        </div>
        
        <!-- Loading State -->
        <div v-else-if="pending" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Загрузка планов...</p>
        </div>

        <!-- Plans Grid -->
        <div v-else class="plans-grid">
          <div v-for="plan in plans" :key="plan.id" class="plan-card" :class="{ 'inactive': !plan.is_active, 'trial': plan.is_trial }">
            <div class="plan-header">
              <div class="plan-title-section">
                <h3 class="plan-name">{{ plan.name }}</h3>
                <div class="plan-badges">
                  <span v-if="plan.is_trial" class="badge trial-badge">Пробный</span>
                  <span v-if="!plan.is_active" class="badge inactive-badge">Неактивен</span>
                </div>
              </div>
              <div class="plan-actions">
                <button @click="editPlan(plan)" class="icon-btn" title="Редактировать">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button @click="deletePlan(plan)" class="icon-btn delete" title="Удалить">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>

            <div class="plan-price-section">
              <div class="plan-price">
                <span v-if="plan.price === 0 || plan.is_trial" class="price-amount">Бесплатно</span>
                <span v-else class="price-amount">${{ plan.price }}</span>
                <span class="price-period">/ {{ plan.period_days }} {{ getPeriodText(plan.period_days) }}</span>
              </div>
              <div class="plan-slug">{{ plan.slug }}</div>
            </div>

            <div v-if="plan.description" class="plan-description">
              {{ plan.description }}
            </div>

            <div class="plan-features">
              <div class="features-header">
                <span class="features-title">Что входит:</span>
              </div>
              <ul class="features-list" v-if="plan.features_list && plan.features_list.length > 0">
                <li v-for="(feature, index) in plan.features_list" :key="index">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  {{ feature }}
                </li>
              </ul>
              <div v-else class="no-features">Функции не указаны</div>
            </div>

            <div class="plan-limits">
              <div class="limit-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                  <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
                <span class="limit-label">Товаров:</span>
                <span class="limit-value">
                  {{ plan.max_products === null ? 'Неограниченно' : plan.max_products }}
                </span>
              </div>
            </div>

            <div class="plan-footer">
              <div class="plan-meta">
                <span>Порядок: {{ plan.display_order }}</span>
              </div>
              <button @click="toggleActive(plan)" :class="['toggle-btn', plan.is_active ? 'active' : 'inactive']">
                {{ plan.is_active ? 'Активен' : 'Неактивен' }}
              </button>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="plans && plans.length === 0" class="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <p>Планов подписки пока нет</p>
            <p class="empty-subtitle">Создайте первый план подписки</p>
            <button @click="openCreateModal" class="create-first-btn">Создать план</button>
          </div>
        </div>

        <!-- Create/Edit Modal -->
        <div v-if="showModal" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ editingPlan ? 'Редактировать план' : 'Создать новый план' }}</h2>
              <button @click="closeModal" class="modal-close">×</button>
            </div>

            <form @submit.prevent="savePlan" class="modal-form">
              <div class="form-grid">
                <div class="form-group">
                  <label>Название плана *</label>
                  <input v-model="planForm.name" type="text" class="form-input" required placeholder="Например: Базовый" />
                </div>

                <div class="form-group">
                  <label>Slug *</label>
                  <input v-model="planForm.slug" type="text" class="form-input" required placeholder="Например: basic" />
                  <small class="form-hint">Уникальный идентификатор (латиница, без пробелов)</small>
                </div>

                <div class="form-group">
                  <label>Цена ($) *</label>
                  <input v-model.number="planForm.price" type="number" step="0.01" min="0" class="form-input" required />
                </div>

                <div class="form-group">
                  <label>Период (дней) *</label>
                  <input v-model.number="planForm.period_days" type="number" min="1" class="form-input" required />
                </div>

                <div class="form-group">
                  <label>Максимум товаров</label>
                  <input 
                    :value="planForm.max_products === null ? '' : planForm.max_products"
                    @input="planForm.max_products = $event.target.value === '' ? null : Number($event.target.value)"
                    type="number" 
                    min="0" 
                    class="form-input" 
                    placeholder="Оставьте пустым для неограниченно" 
                  />
                  <small class="form-hint">Оставьте пустым для неограниченного количества товаров</small>
                </div>

                <div class="form-group full-width">
                  <label>Описание</label>
                  <textarea v-model="planForm.description" class="form-input" rows="3" placeholder="Краткое описание плана"></textarea>
                </div>

                <div class="form-group full-width">
                  <label>
                    Функции плана
                    <button type="button" @click="addFeature" class="add-feature-btn">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                      </svg>
                      Добавить
                    </button>
                  </label>
                  <div class="features-input-list">
                    <div v-for="(feature, index) in planForm.features" :key="index" class="feature-input-row">
                      <input 
                        v-model="planForm.features[index]" 
                        type="text" 
                        class="form-input" 
                        :placeholder="`Функция ${index + 1}`"
                      />
                      <button type="button" @click="removeFeature(index)" class="remove-feature-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                    <div v-if="planForm.features.length === 0" class="no-features-input">
                      Функции не указаны. Нажмите "Добавить", чтобы добавить функцию.
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label class="checkbox-label">
                    <input v-model="planForm.is_trial" type="checkbox" class="checkbox-input" />
                    <span>Пробный период</span>
                  </label>
                </div>

                <div class="form-group">
                  <label class="checkbox-label">
                    <input v-model="planForm.is_active" type="checkbox" class="checkbox-input" />
                    <span>Активен</span>
                  </label>
                </div>

                <div class="form-group">
                  <label>Порядок отображения</label>
                  <input v-model.number="planForm.display_order" type="number" min="0" class="form-input" />
                  <small class="form-hint">Меньше число = выше в списке</small>
                </div>
              </div>

              <div class="modal-actions">
                <button type="button" @click="closeModal" class="btn-secondary">Отмена</button>
                <button type="submit" class="btn-primary" :disabled="saving">
                  {{ saving ? 'Сохранение...' : (editingPlan ? 'Сохранить' : 'Создать') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'platform-admin'
})

const route = useRoute()
const { token, logout } = useAuth()
const toast = useToast()

const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success('Вы вышли из аккаунта')
}

const currentRoute = computed(() => {
  if (route.path.includes('/subscription-plans')) return 'subscription-plans'
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

const { data: plans, pending, refresh, error } = await useFetch('http://localhost:8000/platform/admin/subscription-plans', {
  server: false,
  lazy: true,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Modal state
const showModal = ref(false)
const editingPlan = ref(null)
const saving = ref(false)

const planForm = reactive({
  name: '',
  slug: '',
  price: 0,
  period_days: 30,
  description: '',
  features: [],
  is_active: true,
  is_trial: false,
  display_order: 0,
  max_products: null
})

const openCreateModal = () => {
  editingPlan.value = null
  resetForm()
  showModal.value = true
}

const editPlan = (plan) => {
  editingPlan.value = plan
  planForm.name = plan.name
  planForm.slug = plan.slug
  planForm.price = plan.price
  planForm.period_days = plan.period_days
  planForm.description = plan.description || ''
  planForm.features = plan.features_list ? [...plan.features_list] : []
  planForm.is_active = plan.is_active
  planForm.is_trial = plan.is_trial
  planForm.display_order = plan.display_order
  planForm.max_products = plan.max_products ?? null
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingPlan.value = null
  resetForm()
}

const resetForm = () => {
  planForm.name = ''
  planForm.slug = ''
  planForm.price = 0
  planForm.period_days = 30
  planForm.description = ''
  planForm.features = []
  planForm.is_active = true
  planForm.is_trial = false
  planForm.display_order = 0
  planForm.max_products = null
}

const addFeature = () => {
  planForm.features.push('')
}

const removeFeature = (index) => {
  planForm.features.splice(index, 1)
}

const getPeriodText = (days) => {
  if (days === 1) return 'день'
  if (days >= 2 && days <= 4) return 'дня'
  if (days >= 5 && days <= 20) return 'дней'
  const lastDigit = days % 10
  if (lastDigit === 1) return 'день'
  if (lastDigit >= 2 && lastDigit <= 4) return 'дня'
  return 'дней'
}

const savePlan = async () => {
  saving.value = true
  try {
    const payload = {
      ...planForm,
      features: planForm.features.filter(f => f.trim() !== '').join(','),
      max_products: planForm.max_products === null || planForm.max_products === '' ? null : Number(planForm.max_products)
    }

    if (editingPlan.value) {
      await $fetch(`http://localhost:8000/platform/admin/subscription-plans/${editingPlan.value.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token.value}`
        },
        body: payload
      })
      toast.success('План обновлен')
    } else {
      await $fetch('http://localhost:8000/platform/admin/subscription-plans', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`
        },
        body: payload
      })
      toast.success('План создан')
    }

    closeModal()
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при сохранении плана')
  } finally {
    saving.value = false
  }
}

const toggleActive = async (plan) => {
  try {
    await $fetch(`http://localhost:8000/platform/admin/subscription-plans/${plan.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: {
        is_active: !plan.is_active
      }
    })
    toast.success(`План ${!plan.is_active ? 'активирован' : 'деактивирован'}`)
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при изменении статуса')
  }
}

const deletePlan = async (plan) => {
  if (!confirm(`Вы уверены, что хотите удалить план "${plan.name}"?`)) {
    return
  }

  try {
    await $fetch(`http://localhost:8000/platform/admin/subscription-plans/${plan.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })
    toast.success('План удален')
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при удалении плана')
  }
}
</script>

<style scoped>
.platform-admin-page {
  min-height: 100vh;
  display: flex;
  background: #F5F7FA;
  width: 100%;
}

/* Mobile Header */
.mobile-header {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
  z-index: 1000;
}

.menu-btn,
.home-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  color: #111;
  transition: all 0.2s;
}

.menu-btn:hover,
.home-btn:hover {
  background: #111;
  color: white;
}

.mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
}

@media (max-width: 640px) {
  .admin-title {
    font-size: 1.5rem !important;
    line-height: 1.2 !important;
  }
  
  .admin-header {
    padding: 20px !important;
  }
}

.admin-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 40px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.admin-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.admin-subtitle {
  font-size: 1rem;
  opacity: 0.85;
  font-weight: 400;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.create-btn:hover {
  background: #F9FAFB;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.admin-content {
  padding: 32px;
}

/* Plans Grid */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

@media (max-width: 640px) {
  .plans-grid {
    grid-template-columns: 1fr;
  }
}

.plan-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 2px solid #E5E7EB;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}

.plan-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.plan-card.inactive {
  opacity: 0.7;
  border-color: #D1D5DB;
}

.plan-card.trial {
  border-color: #FCD34D;
  background: linear-gradient(to bottom, #FEF9C3 0%, white 20%);
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 2px solid #F3F4F6;
}

.plan-title-section {
  flex: 1;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 8px 0;
}

.plan-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
}

.trial-badge {
  background: #FEF3C7;
  color: #92400E;
}

.inactive-badge {
  background: #F3F4F6;
  color: #4B5563;
}

.plan-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #6B7280;
}

.icon-btn:hover {
  background: #F3F4F6;
  color: #111;
}

.icon-btn.delete:hover {
  background: #FEE2E2;
  color: #991B1B;
  border-color: #FCA5A5;
}

.plan-price-section {
  margin-bottom: 20px;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
}

.price-amount {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
}

.price-period {
  font-size: 1rem;
  color: #6B7280;
  font-weight: 500;
}

.plan-slug {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-family: monospace;
  background: #F9FAFB;
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;
}

.plan-description {
  color: #6B7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 20px;
}

.plan-features {
  flex: 1;
  margin-bottom: 20px;
}

.features-header {
  margin-bottom: 12px;
}

.features-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.features-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
}

.features-list li svg {
  color: #10B981;
  flex-shrink: 0;
  margin-top: 2px;
}

.no-features {
  color: #9CA3AF;
  font-size: 0.875rem;
  font-style: italic;
}

.plan-limits {
  margin-top: 16px;
  padding: 16px;
  background: #F9FAFB;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
}

.limit-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  font-size: 0.875rem;
}

.limit-item svg {
  color: #9CA3AF;
  flex-shrink: 0;
}

.limit-label {
  font-weight: 500;
}

.limit-value {
  font-weight: 700;
  color: #111;
  margin-left: auto;
}

.plan-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 2px solid #F3F4F6;
}

.plan-meta {
  font-size: 0.75rem;
  color: #6B7280;
}

.toggle-btn {
  padding: 6px 16px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active {
  background: #D1FAE5;
  color: #065F46;
}

.toggle-btn.inactive {
  background: #F3F4F6;
  color: #4B5563;
}

.toggle-btn:hover {
  opacity: 0.8;
}

/* Empty State */
.empty-state {
  grid-column: 1 / -1;
  padding: 80px 20px;
  text-align: center;
  background: white;
  border-radius: 20px;
  border: 2px dashed #E5E7EB;
}

.empty-state svg {
  margin-bottom: 16px;
  color: #9CA3AF;
}

.empty-state p {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 8px 0;
  color: #111;
}

.empty-subtitle {
  font-size: 0.875rem;
  font-weight: 400;
  color: #6B7280;
}

.create-first-btn {
  margin-top: 20px;
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.create-first-btn:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Loading & Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #E5E7EB;
}

.error-state {
  color: #EF4444;
}

.error-state svg {
  margin-bottom: 16px;
  color: #EF4444;
}

.error-message {
  margin: 16px 0;
  font-size: 1rem;
}

.retry-btn {
  margin-top: 16px;
  padding: 10px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #2d2d2d;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid #F3F4F6;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 900;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6B7280;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #F3F4F6;
  color: #111;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

@media (max-width: 640px) {
  .modal-content {
    width: 95%;
    padding: 20px;
    border-radius: 16px;
  }
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #111;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-hint {
  font-size: 0.75rem;
  color: #6B7280;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.9375rem;
  outline: none;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-input:focus {
  border-color: #111;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: 500;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.features-input-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feature-input-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.feature-input-row .form-input {
  flex: 1;
}

.remove-feature-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #FEE2E2;
  border: 1px solid #FCA5A5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #991B1B;
  flex-shrink: 0;
}

.remove-feature-btn:hover {
  background: #FECACA;
  border-color: #F87171;
}

.add-feature-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.add-feature-btn:hover {
  background: #E5E7EB;
  border-color: #D1D5DB;
}

.no-features-input {
  padding: 16px;
  background: #F9FAFB;
  border-radius: 8px;
  text-align: center;
  color: #6B7280;
  font-size: 0.875rem;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 2px solid #F3F4F6;
}

.btn-secondary {
  padding: 12px 24px;
  background: #F3F4F6;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

.btn-primary {
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #000;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }
  
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
  
  .plans-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
  
  .plans-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
  }
  
  .admin-title {
    font-size: 2rem;
  }
  
  .admin-content {
    padding: 20px;
  }
}
</style>

