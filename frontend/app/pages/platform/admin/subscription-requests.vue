<template>
  <div class="platform-admin-requests">
    <PlatformAdminSidebar :current-route="'subscription-requests'" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('platformAdmin.requests.title') }}</h1>
            <p class="page-subtitle">Обработка заявок на активацию и продление подписок</p>
          </div>
        </div>

        <div class="nav-right">
          <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
            <iconify-icon icon="lucide:rotate-cw" />
            <span>{{ $t('platformAdmin.dashboard.refresh') }}</span>
          </button>
        </div>
      </header>

      <div class="admin-scroll">
        <!-- Stats summary -->
        <div class="stats-bar" v-if="requests?.length">
          <div class="mini-stat">
            <span class="ms-val">{{ pendingCount }}</span>
            <span class="ms-label">Ожидают</span>
          </div>
          <div class="ms-divider"></div>
          <div class="mini-stat">
            <span class="ms-val">{{ approvedCount }}</span>
            <span class="ms-label">Одобрено</span>
          </div>
          <div class="ms-divider"></div>
          <div class="mini-stat">
            <span class="ms-val">{{ rejectedCount }}</span>
            <span class="ms-label">Отклонено</span>
          </div>
        </div>

        <div v-if="pending" class="loading-state">
          <div class="loader"></div>
          <p>Загрузка заявок...</p>
        </div>

        <div v-else-if="!requests || requests.length === 0" class="empty-state">
          <div class="empty-icon"><iconify-icon icon="lucide:inbox" /></div>
          <h2>Заявок пока нет</h2>
          <p>Когда владельцы магазинов отправят запрос на оплату, они появятся здесь.</p>
        </div>

        <div v-else class="requests-grid">
          <div v-for="req in sortedRequests" :key="req.id" class="request-card" :class="req.status">
            <div class="card-header">
              <div class="shop-badge">
                <iconify-icon icon="lucide:store" />
                <span>{{ req.shop_name }}</span>
              </div>
              <div class="status-pill" :class="req.status">
                {{ getStatusLabel(req.status) }}
              </div>
            </div>

            <div class="card-body">
              <div class="plan-info">
                <div class="plan-main">
                  <span class="plan-name">{{ req.plan_name }}</span>
                  <span class="plan-type" :class="req.type">{{ req.type === 'new' ? 'Новая' : 'Продление' }}</span>
                </div>
                <div class="plan-duration">Срок: {{ req.duration_months }} мес.</div>
              </div>

              <div class="request-meta">
                <div class="meta-item">
                  <iconify-icon icon="lucide:calendar" />
                  <span>{{ formatDate(req.requested_at) }}</span>
                </div>
                <div class="meta-item" v-if="req.notes">
                  <iconify-icon icon="lucide:message-square" />
                  <span class="note-text" :title="req.notes">{{ req.notes }}</span>
                </div>
              </div>
            </div>

            <div class="card-footer" v-if="req.status === 'pending'">
              <button @click="handleAction(req, 'rejected')" class="btn-reject" :disabled="processingId === req.id">
                <iconify-icon icon="lucide:x-circle" /> Отклонить
              </button>
              <button @click="handleAction(req, 'approved')" class="btn-approve" :disabled="processingId === req.id">
                <span v-if="processingId === req.id" class="loader-xs"></span>
                <iconify-icon v-else icon="lucide:check-circle" />
                Одобрить
              </button>
            </div>
            <div class="card-footer processed" v-else>
              <div class="processed-msg">
                <iconify-icon :icon="req.status === 'approved' ? 'lucide:check' : 'lucide:info'" />
                Заявка {{ req.status === 'approved' ? 'была одобрена' : 'отклонена' }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t, locale } = useI18n()
const config = useRuntimeConfig()
const toast = useToast()
const { token, logout } = useAuth()

definePageMeta({ middleware: 'platform-admin' })

const sidebarOpen = ref(false)
const processingId = ref(null)

const { data: requests, pending, refresh } = await useFetch(`${config.public.apiBase}/platform/admin/subscription-requests`, {
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` })),
  watch: [token]
})

const handleLogout = () => { logout(); toast.success(t('auth.loggedOut')) }

const formatDate = (date) => new Date(date).toLocaleDateString(locale.value, {
  day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit'
})

const getStatusLabel = (s) => {
  const map = { pending: 'Ожидает', approved: 'Одобрена', rejected: 'Отклонена' }
  return map[s] || s
}

const pendingCount = computed(() => requests.value?.filter(r => r.status === 'pending').length || 0)
const approvedCount = computed(() => requests.value?.filter(r => r.status === 'approved').length || 0)
const rejectedCount = computed(() => requests.value?.filter(r => r.status === 'rejected').length || 0)

const sortedRequests = computed(() => {
  if (!requests.value) return []
  return [...requests.value].sort((a, b) => {
    if (a.status === 'pending' && b.status !== 'pending') return -1
    if (a.status !== 'pending' && b.status === 'pending') return 1
    return new Date(b.requested_at) - new Date(a.requested_at)
  })
})

const handleAction = async (req, status) => {
  processingId.value = req.id
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/subscription-requests/${req.id}/status`, {
      method: 'PUT',
      body: { status },
      headers: { Authorization: `Bearer ${token.value}` }
    })
    toast.success(status === 'approved' ? 'Подписка активирована' : 'Заявка отклонена')
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка')
  } finally {
    processingId.value = null
  }
}
</script>

<style scoped>
.platform-admin-requests {
  background: #f8fafc;
  min-height: 100vh;
  display: flex;
}

.admin-main {
  flex: 1;
  margin-left: 280px;
  display: flex;
  flex-direction: column;
  transition: all 0.4s;
}

.top-nav {
  padding: 32px;
  background: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mobile-menu-btn {
  display: none;
  width: 44px;
  height: 44px;
  background: #f1f5f9;
  border: none;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 950;
  margin: 0;
  letter-spacing: -1px;
}

.page-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin-top: 4px;
  font-weight: 600;
}

.refresh-btn {
  padding: 10px 18px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1.5px solid #e2e8f0;
  background: white;
}

.refresh-btn:hover {
  border-color: #111;
}

.refresh-btn.loading iconify-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.admin-scroll {
  padding: 32px;
  flex: 1;
  overflow-y: auto;
}

.stats-bar {
  display: flex;
  align-items: center;
  gap: 32px;
  background: white;
  padding: 20px 32px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
  margin-bottom: 32px;
  width: fit-content;
}

.mini-stat {
  display: flex;
  flex-direction: column;
}

.ms-val {
  font-size: 1.5rem;
  font-weight: 950;
  color: #111;
  line-height: 1;
}

.ms-label {
  font-size: 0.7rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  margin-top: 4px;
}

.ms-divider {
  width: 1.5px;
  height: 32px;
  background: #f1f5f9;
}

.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

.request-card {
  background: white;
  border-radius: 28px;
  padding: 28px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  border: 1.5px solid transparent;
  transition: all 0.3s;
  position: relative;
}

.request-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.05);
}

.request-card.pending {
  border-color: #e0f2fe;
}

.request-card.pending::before {
  content: '';
  position: absolute;
  top: 28px;
  left: 0;
  width: 4px;
  height: 40px;
  background: #0ea5e9;
  border-radius: 0 4px 4px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.shop-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  font-size: 1rem;
  color: #111;
}

.shop-badge iconify-icon {
  font-size: 1.4rem;
  color: #64748b;
}

.status-pill {
  padding: 6px 14px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-pill.pending {
  background: #e0f2fe;
  color: #0369a1;
}

.status-pill.approved {
  background: #dcfce7;
  color: #15803d;
}

.status-pill.rejected {
  background: #fee2e2;
  color: #b91c1c;
}

.card-body {
  margin-bottom: 28px;
}

.plan-info {
  background: #f8fafc;
  padding: 16px;
  border-radius: 16px;
  margin-bottom: 16px;
}

.plan-main {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}

.plan-name {
  font-weight: 900;
  font-size: 1.1rem;
  color: #111;
}

.plan-type {
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 850;
  text-transform: uppercase;
}

.plan-type.new {
  background: #ef4444;
  color: white;
}

.plan-type.renew {
  background: #111;
  color: white;
}

.plan-duration {
  font-size: 0.85rem;
  font-weight: 700;
  color: #64748b;
}

.request-meta {
  display: grid;
  gap: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
}

.note-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.card-footer {
  display: flex;
  gap: 12px;
}

.card-footer button {
  flex: 1;
  padding: 14px;
  border-radius: 16px;
  font-weight: 900;
  font-size: 0.85rem;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-reject {
  background: #f1f5f9;
  color: #475569;
}

.btn-reject:hover {
  background: #fee2e2;
  color: #ef4444;
}

.btn-approve {
  background: #111;
  color: white;
}

.btn-approve:hover {
  transform: scale(1.02);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.processed-msg {
  width: 100%;
  padding: 12px;
  background: #f8fafc;
  border-radius: 12px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 750;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.empty-state {
  padding: 80px 0;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  color: #cbd5e1;
  margin-bottom: 24px;
}

.empty-state h2 {
  font-weight: 950;
  font-size: 1.75rem;
  color: #1e293b;
  margin-bottom: 12px;
}

.empty-state p {
  color: #64748b;
  font-weight: 600;
  max-width: 400px;
  margin: 0 auto;
}

.loader {
  width: 40px;
  height: 40px;
  border: 4px solid #f1f5f9;
  border-top-color: #111;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

.loader-xs {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
  }

  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .requests-grid {
    grid-template-columns: 1fr;
  }

  .stats-bar {
    width: 100%;
    justify-content: space-around;
    padding: 20px;
  }
}
</style>
