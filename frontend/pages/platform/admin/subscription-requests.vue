<template>
  <div class="requests-page">
    <div class="page-header">
      <h1 class="page-title">{{ $t('platformAdmin.requests.title') }}</h1>
    </div>

    <div v-if="pending" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else class="requests-list">
      <div v-if="requests.length === 0" class="empty-state">
        {{ $t('platformAdmin.requests.empty') }}
      </div>

      <div v-for="req in requests" :key="req.id" class="request-card">
        <div class="request-header">
          <div>
            <h3 class="shop-name">{{ req.shop_name }}</h3>
            <span class="request-type" :class="req.type">{{ req.type }}</span>
          </div>
          <span class="date">{{ formatDate(req.requested_at) }}</span>
        </div>

        <div class="request-details">
          <div class="detail-row">
            <span class="label">{{ $t('platformAdmin.requests.plan') }}:</span>
            <span class="value">{{ req.plan_name }}</span>
          </div>
          <div class="detail-row">
            <span class="label">{{ $t('platformAdmin.requests.duration') }}:</span>
            <span class="value">{{ req.duration_months }} {{ $t('shopSettings.subscription.months') }}</span>
          </div>
          <div class="detail-row" v-if="req.notes">
            <span class="label">{{ $t('platformAdmin.requests.notes') }}:</span>
            <span class="value">{{ req.notes }}</span>
          </div>
        </div>

        <div class="request-actions" v-if="req.status === 'pending'">
          <button class="btn-reject" @click="handleAction(req, 'rejected')">
            {{ $t('common.reject') }}
          </button>
          <button class="btn-approve" @click="handleAction(req, 'approved')">
            {{ $t('common.approve') }}
          </button>
        </div>
        <div v-else class="request-status">
          <span class="status-badge" :class="req.status">{{ req.status }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'platform-admin'
})

const { t } = useI18n()
const config = useRuntimeConfig()
const toast = useToast()
const { token } = useAuth()

const { data: requests, pending, refresh } = await useFetch(`${config.public.apiBase}/platform/admin/subscription-requests`, {
  headers: { Authorization: `Bearer ${token.value}` }
})

const formatDate = (date) => new Date(date).toLocaleDateString()

const handleAction = async (req, status) => {
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/subscription-requests/${req.id}/status`, {
      method: 'PUT',
      body: { status },
      headers: { Authorization: `Bearer ${token.value}` }
    })
    toast.success(status === 'approved' ? t('platformAdmin.requests.approved') : t('platformAdmin.requests.rejected'))
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Error')
  }
}
</script>

<style scoped>
.requests-page {
  padding: 24px;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 800;
  margin-bottom: 24px;
}

.requests-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.request-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.request-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  align-items: flex-start;
}

.shop-name {
  font-weight: 700;
  font-size: 1.125rem;
}

.request-type {
  display: inline-block;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  margin-top: 4px;
  text-transform: uppercase;
  font-weight: 600;
}

.request-type.new {
  background: #DBEAFE;
  color: #1E40AF;
}

.request-type.renew {
  background: #D1FAE5;
  color: #065F46;
}

.request-type.change {
  background: #FEF3C7;
  color: #92400E;
}

.request-details {
  margin-bottom: 24px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.875rem;
}

.label {
  color: #6B7280;
}

.value {
  font-weight: 500;
}

.request-actions {
  display: flex;
  gap: 12px;
}

button {
  flex: 1;
  padding: 8px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.btn-reject {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-approve {
  background: #111;
  color: white;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.approved {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.rejected {
  background: #FEE2E2;
  color: #991B1B;
}
</style>
