<template>
  <div class="subscription-requests-page">
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
      <span class="mobile-title">Запросы</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar 
      current-route="subscription-requests" 
      :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event"
    />
    
    <main class="admin-main">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">Запросы на подписку</h1>
          <p class="page-subtitle">Управление запросами на активацию подписки от магазинов</p>
        </div>

        <!-- Filters -->
        <div class="filters">
          <button 
            v-for="statusFilter in statusFilters" 
            :key="statusFilter.value"
            @click="selectedStatus = statusFilter.value"
            :class="['filter-btn', { active: selectedStatus === statusFilter.value }]"
          >
            {{ statusFilter.label }}
            <span v-if="statusFilter.count !== undefined" class="filter-count">{{ statusFilter.count }}</span>
          </button>
        </div>

        <!-- Loading -->
        <div v-if="pending" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Загрузка запросов...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="!requests || requests.length === 0" class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            <polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline>
            <polyline points="7.5 19.79 7.5 14.6 3 12"></polyline>
            <polyline points="21 12 16.5 14.6 16.5 19.79"></polyline>
          </svg>
          <h3>Нет запросов</h3>
          <p>Пока нет запросов на подписку</p>
        </div>

        <!-- Requests List -->
        <div v-else class="requests-list">
          <div 
            v-for="request in filteredRequests" 
            :key="request.id" 
            class="request-card"
            :class="`request-${request.status}`"
          >
            <div class="request-header">
              <div class="request-info">
                <h3 class="request-shop-name">{{ request.shop_name || 'Неизвестный магазин' }}</h3>
                <p class="request-plan">План: <strong>{{ request.plan_name }}</strong></p>
                <p class="request-duration">Длительность: <strong>{{ request.duration_months }} {{ getMonthsLabel(request.duration_months) }}</strong></p>
              </div>
              <div class="request-status-badge" :class="`status-${request.status}`">
                {{ getStatusText(request.status) }}
              </div>
            </div>

            <div class="request-details">
              <div class="detail-item">
                <span class="detail-label">Дата запроса:</span>
                <span class="detail-value">{{ formatDate(request.requested_at) }}</span>
              </div>
              <div v-if="request.approved_at" class="detail-item">
                <span class="detail-label">{{ request.status === 'approved' ? 'Одобрено:' : 'Отклонено:' }}</span>
                <span class="detail-value">{{ formatDate(request.approved_at) }}</span>
              </div>
              <div v-if="request.notes" class="detail-item notes">
                <span class="detail-label">Заметки:</span>
                <span class="detail-value">{{ request.notes }}</span>
              </div>
            </div>

            <!-- Actions for pending requests -->
            <div v-if="request.status === 'pending'" class="request-actions">
              <button 
                @click="openApproveModal(request)"
                class="action-btn approve-btn"
                :disabled="processing"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                Одобрить
              </button>
              <button 
                @click="openRejectModal(request)"
                class="action-btn reject-btn"
                :disabled="processing"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
                Отклонить
              </button>
              <NuxtLink 
                v-if="request.shop_slug"
                :to="`/platform/admin/shops`"
                class="action-btn view-btn"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Магазин
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Approve Modal -->
    <div v-if="showApproveModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Одобрить запрос на подписку</h2>
          <button @click="closeModals" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p>Вы уверены, что хотите одобрить запрос на подписку?</p>
          <div class="request-summary">
            <p><strong>Магазин:</strong> {{ selectedRequest?.shop_name }}</p>
            <p><strong>План:</strong> {{ selectedRequest?.plan_name }}</p>
            <p><strong>Длительность:</strong> {{ selectedRequest?.duration_months }} {{ getMonthsLabel(selectedRequest?.duration_months) }}</p>
          </div>
          <div class="form-group">
            <label for="approve-notes">Заметки (необязательно):</label>
            <textarea 
              id="approve-notes"
              v-model="approveNotes"
              rows="3"
              placeholder="Добавьте заметки..."
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModals" class="btn-secondary">Отмена</button>
          <button @click="approveRequest" class="btn-primary" :disabled="processing">
            {{ processing ? 'Одобрение...' : 'Одобрить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Отклонить запрос на подписку</h2>
          <button @click="closeModals" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p>Вы уверены, что хотите отклонить запрос на подписку?</p>
          <div class="request-summary">
            <p><strong>Магазин:</strong> {{ selectedRequest?.shop_name }}</p>
            <p><strong>План:</strong> {{ selectedRequest?.plan_name }}</p>
            <p><strong>Длительность:</strong> {{ selectedRequest?.duration_months }} {{ getMonthsLabel(selectedRequest?.duration_months) }}</p>
          </div>
          <div class="form-group">
            <label for="reject-notes">Причина отклонения (рекомендуется):</label>
            <textarea 
              id="reject-notes"
              v-model="rejectNotes"
              rows="3"
              placeholder="Укажите причину отклонения..."
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModals" class="btn-secondary">Отмена</button>
          <button @click="rejectRequest" class="btn-danger" :disabled="processing">
            {{ processing ? 'Отклонение...' : 'Отклонить' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'platform-admin'
})

const toast = useToast()
const { token } = useAuth()
const route = useRoute()

const sidebarOpen = ref(false)

const selectedStatus = ref('pending')
const processing = ref(false)
const selectedRequest = ref(null)
const showApproveModal = ref(false)
const showRejectModal = ref(false)
const approveNotes = ref('')
const rejectNotes = ref('')

const statusFilters = computed(() => {
  const allRequests = requests.value || []
  return [
    { value: null, label: 'Все', count: allRequests.length },
    { value: 'pending', label: 'На рассмотрении', count: allRequests.filter(r => r.status === 'pending').length },
    { value: 'approved', label: 'Одобренные', count: allRequests.filter(r => r.status === 'approved').length },
    { value: 'rejected', label: 'Отклоненные', count: allRequests.filter(r => r.status === 'rejected').length }
  ]
})

const filteredRequests = computed(() => {
  if (!requests.value) return []
  if (selectedStatus.value === null) return requests.value
  return requests.value.filter(r => r.status === selectedStatus.value)
})

// Fetch subscription requests
const { data: requests, pending, refresh } = useFetch('http://localhost:8000/platform/admin/subscription-requests', {
  server: false,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  })),
  transform: (data) => {
    if (!data) return []
    return data.map(req => ({
      ...req,
      requested_at: new Date(req.requested_at),
      approved_at: req.approved_at ? new Date(req.approved_at) : null
    }))
  }
})

const openApproveModal = (request) => {
  selectedRequest.value = request
  approveNotes.value = ''
  showApproveModal.value = true
}

const openRejectModal = (request) => {
  selectedRequest.value = request
  rejectNotes.value = ''
  showRejectModal.value = true
}

const closeModals = () => {
  showApproveModal.value = false
  showRejectModal.value = false
  selectedRequest.value = null
  approveNotes.value = ''
  rejectNotes.value = ''
}

const approveRequest = async () => {
  if (!selectedRequest.value) return
  
  processing.value = true
  try {
    await $fetch(`http://localhost:8000/platform/admin/subscription-requests/${selectedRequest.value.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': token.value ? `Bearer ${token.value}` : '',
        'Content-Type': 'application/json'
      },
      body: {
        status: 'approved',
        notes: approveNotes.value || null
      }
    })
    
    toast.success('Запрос успешно одобрен')
    await refresh()
    closeModals()
  } catch (error) {
    console.error('Error approving request:', error)
    toast.error('Ошибка при одобрении запроса')
  } finally {
    processing.value = false
  }
}

const rejectRequest = async () => {
  if (!selectedRequest.value) return
  
  processing.value = true
  try {
    await $fetch(`http://localhost:8000/platform/admin/subscription-requests/${selectedRequest.value.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': token.value ? `Bearer ${token.value}` : '',
        'Content-Type': 'application/json'
      },
      body: {
        status: 'rejected',
        notes: rejectNotes.value || null
      }
    })
    
    toast.success('Запрос отклонен')
    await refresh()
    closeModals()
  } catch (error) {
    console.error('Error rejecting request:', error)
    toast.error('Ошибка при отклонении запроса')
  } finally {
    processing.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': 'На рассмотрении',
    'approved': 'Одобрено',
    'rejected': 'Отклонено'
  }
  return statusMap[status] || status
}

const getMonthsLabel = (months) => {
  if (months === 1) return 'месяц'
  if (months >= 2 && months <= 4) return 'месяца'
  return 'месяцев'
}

const formatDate = (date) => {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleDateString('ru-RU', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.subscription-requests-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
  width: 100%;
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.75rem;
  }
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

.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
  padding: 32px;
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }

  .admin-main {
    margin-left: 0;
    padding-top: 80px; /* 60px header + 20px padding */
    padding-left: 16px;
    padding-right: 16px;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-btn:hover {
  border-color: #111;
  color: #111;
}

.filter-btn.active {
  background: #111;
  border-color: #111;
  color: white;
}

.filter-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.875rem;
}

.filter-btn.active .filter-count {
  background: rgba(255, 255, 255, 0.3);
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 24px;
  border: 2px dashed #E5E7EB;
}

.empty-state svg {
  color: #9CA3AF;
  margin-bottom: 24px;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
}

.empty-state p {
  color: #6B7280;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.request-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  border: 2px solid #E5E7EB;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s;
}

.request-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  border-color: #D1D5DB;
}

.request-card.request-pending {
  border-left: 4px solid #F59E0B;
}

.request-card.request-approved {
  border-left: 4px solid #10B981;
}

.request-card.request-rejected {
  border-left: 4px solid #EF4444;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid #F3F4F6;
}

.request-info {
  flex: 1;
}

.request-shop-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 12px;
}

.request-plan,
.request-duration {
  font-size: 0.9375rem;
  color: #6B7280;
  margin: 4px 0;
}

.request-plan strong,
.request-duration strong {
  color: #111;
  font-weight: 700;
}

.request-status-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  white-space: nowrap;
}

.request-status-badge.status-pending {
  background: #FEF3C7;
  color: #92400E;
}

.request-status-badge.status-approved {
  background: #D1FAE5;
  color: #065F46;
}

.request-status-badge.status-rejected {
  background: #FEE2E2;
  color: #991B1B;
}

.request-details {
  margin-bottom: 24px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.9375rem;
}

.detail-item.notes {
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  color: #6B7280;
  font-weight: 500;
}

.detail-value {
  color: #111;
  font-weight: 600;
}

.request-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9375rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.approve-btn {
  background: #10B981;
  color: white;
}

.approve-btn:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-2px);
}

.reject-btn {
  background: #EF4444;
  color: white;
}

.reject-btn:hover:not(:disabled) {
  background: #DC2626;
  transform: translateY(-2px);
}

.view-btn {
  background: #F3F4F6;
  color: #111;
  text-decoration: none;
}

.view-btn:hover {
  background: #E5E7EB;
  transform: translateY(-2px);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #F3F4F6;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.modal-close {
  width: 40px;
  height: 40px;
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

.modal-close:hover {
  background: #E5E7EB;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  color: #4B5563;
  margin-bottom: 24px;
}

.request-summary {
  background: #F9FAFB;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.request-summary p {
  margin: 8px 0;
  color: #111;
  font-size: 0.9375rem;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #111;
  margin-bottom: 8px;
  font-size: 0.9375rem;
}

.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.9375rem;
  resize: vertical;
  transition: border-color 0.2s;
}

.form-group textarea:focus {
  outline: none;
  border-color: #111;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 2px solid #F3F4F6;
}

.btn-secondary {
  padding: 12px 24px;
  background: #F3F4F6;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

.btn-primary {
  padding: 12px 24px;
  background: #10B981;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #059669;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-danger {
  padding: 12px 24px;
  background: #EF4444;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-danger:hover:not(:disabled) {
  background: #DC2626;
}

.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding: 24px 16px;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }

  .request-header {
    flex-direction: column;
    gap: 16px;
  }

  .request-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .filters {
    gap: 8px;
  }

  .filter-btn {
    padding: 8px 16px;
    font-size: 0.875rem;
  }
}
@media (max-width: 640px) {
  .request-header {
    flex-direction: column;
    gap: 12px;
  }
  
  .request-status-badge {
    align-self: flex-start;
  }
  
  .detail-item {
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
  }
  
  .request-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
