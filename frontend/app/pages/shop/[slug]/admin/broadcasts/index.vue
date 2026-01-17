<template>
  <div class="shop-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">{{ $t('admin.broadcasts.title') }}</span>
      <NuxtLink :to="localePath(`/${slug}`)" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="slug" current-route="broadcasts" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="page-header">
        <div class="header-text">
          <h1 class="page-title">{{ $t('admin.broadcasts.pageTitle') }}</h1>
          <p class="page-subtitle">{{ $t('admin.broadcasts.pageSubtitle') }}</p>
        </div>
        <button @click="openCreateModal" class="add-btn mobile-hidden">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          {{ $t('admin.broadcasts.createNew') }}
        </button>
      </div>

      <!-- Mobile Add FAB -->
      <button @click="openCreateModal" class="mobile-fab">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>

      <!-- Stats Cards -->
      <div class="stats-grid mb-8">
        <div class="stat-card glass-card">
          <div class="stat-icon sent">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 2L11 13"></path>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-label">Total Sent</span>
            <span class="stat-value">{{ totalSent }}</span>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon campaigns">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-label">Campaigns</span>
            <span class="stat-value">{{ broadcasts?.length || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Broadcast List -->
      <div class="broadcasts-section" v-if="broadcasts?.length">
        <h2 class="section-title mb-4">{{ $t('admin.broadcasts.history') }}</h2>
        <div class="broadcasts-grid">
          <TransitionGroup name="list">
            <div v-for="b in broadcasts" :key="b.id" class="broadcast-card animate-in">
              <div class="card-status" :class="b.status">
                {{ $t(`admin.broadcasts.status.${b.status}`) }}
              </div>
              <div class="card-content">
                <div v-if="b.media_url" class="card-thumbnail mb-3">
                  <video v-if="isMediaVideo(b.media_url)" :src="b.media_url" muted loop onmouseover="this.play()"
                    onmouseout="this.pause()"></video>
                  <img v-else :src="b.media_url" alt="" />
                </div>
                <p class="broadcast-msg">{{ b.message_text }}</p>
                <div class="broadcast-meta">
                  <span class="meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    {{ formatDate(b.created_at) }}
                  </span>
                  <span class="meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    {{ b.sent_count }}/{{ b.total_count }}
                  </span>
                </div>
              </div>
              <div class="card-footer">
                <button v-if="b.status === 'draft'" @click="sendBroadcast(b.id)" class="send-now-btn"
                  :disabled="sendingIds.has(b.id)">
                  <span v-if="sendingIds.has(b.id)" class="spinner mr-2"></span>
                  {{ sendingIds.has(b.id) ? $t('common.sending') : $t('admin.broadcasts.sendNow') }}
                </button>
                <button @click="deleteBroadcast(b.id)" class="delete-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>
          </TransitionGroup>
        </div>
      </div>
      <div v-else class="empty-state glass-card">
        <div class="empty-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M22 2L11 13"></path>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </div>
        <h3>{{ $t('admin.broadcasts.noBroadcasts') }}</h3>
        <p>{{ $t('admin.broadcasts.startGrowing') }}</p>
        <button @click="openCreateModal" class="add-btn mt-4">{{ $t('admin.broadcasts.createFirst') }}</button>
      </div>

      <!-- Create Modal -->
      <Transition name="modal">
        <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
          <div class="modal-content glass-modal">
            <div class="modal-header">
              <h2>{{ $t('admin.broadcasts.createNew') }}</h2>
              <button @click="showModal = false" class="close-modal-btn">&times;</button>
            </div>
            <div class="modal-body">
              <!-- Telegram Preview -->
              <div class="telegram-preview-wrapper mb-6">
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">{{
                  $t('admin.broadcasts.telegramPreview') }}</label>
                <div class="tg-preview">
                  <div class="tg-bubble" :class="{ 'is-loading': uploading }">
                    <div v-if="form.media_url || uploading" class="tg-media">
                      <div v-if="uploading" class="media-skeleton">
                        <div class="skeleton-shimmer"></div>
                        <span class="upload-progress-text">Zaxiralanyapti...</span>
                      </div>
                      <template v-else-if="form.media_url">
                        <video v-if="isMediaVideo(form.media_url)" :src="form.media_url" autoplay loop muted
                          class="preview-video"></video>
                        <img v-else :src="form.media_url" alt="Media" />
                        <button @click="form.media_url = ''" class="remove-media-btn" title="O'chirish">&times;</button>
                      </template>
                    </div>
                    <div class="tg-text">
                      {{ form.message_text || $t('admin.broadcasts.messagePlaceholder') }}
                    </div>
                    <div v-if="form.button_text" class="tg-button">
                      {{ form.button_text }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-grid">
                <div class="form-group full-width">
                  <label>{{ $t('admin.broadcasts.message') }}</label>
                  <textarea v-model="form.message_text" rows="4"
                    :placeholder="$t('admin.broadcasts.messagePlaceholder')"></textarea>
                </div>

                <div class="form-group full-width">
                  <label>{{ $t('admin.broadcasts.media') }} (URL)</label>
                  <div class="image-input-group">
                    <input v-model="form.media_url" type="text" placeholder="https://..." />
                    <label class="upload-btn" :class="{ 'is-loading': uploading }">
                      <span v-if="uploading" class="spinner dark"></span>
                      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                      </svg>
                      <input type="file" hidden @change="handleFileUpload" :disabled="uploading" />
                    </label>
                  </div>
                </div>

                <div class="form-group">
                  <label>{{ $t('admin.broadcasts.buttonText') }}</label>
                  <input v-model="form.button_text" type="text"
                    :placeholder="$t('admin.broadcasts.btnTextPlaceholder')" />
                </div>
                <div class="form-group">
                  <label>{{ $t('admin.broadcasts.buttonUrl') }}</label>
                  <input v-model="form.button_url" type="text" placeholder="https://..." />
                </div>

                <div class="form-group full-width">
                  <label>{{ $t('admin.broadcasts.audience') }}</label>
                  <div class="audience-selector">
                    <div class="audience-option" :class="{ active: form.audience_type === 'all' }"
                      @click="form.audience_type = 'all'">
                      <span class="option-title">{{ $t('admin.broadcasts.audienceAll') }}</span>
                    </div>
                    <div class="audience-option" :class="{ active: form.audience_type === 'recent' }"
                      @click="form.audience_type = 'recent'">
                      <span class="option-title">{{ $t('admin.broadcasts.audienceRecent') }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="limit-note mt-4">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
                <span>{{ $t('admin.broadcasts.limitNote') }}</span>
              </div>
            </div>
            <div class="modal-footer">
              <button @click="showModal = false" class="cancel-btn">{{ $t('common.cancel') }}</button>
              <button @click="saveBroadcast" class="save-btn" :disabled="saving">
                <span v-if="saving" class="spinner"></span>
                {{ saving ? $t('common.saving') : $t('admin.broadcasts.createNew') }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </main>
  </div>
</template>

<script setup>
const { t } = useI18n()
definePageMeta({
  middleware: ['auth', 'shop-owner'],
  layout: false
})

const route = useRoute()
const slug = route.params.slug
const { token } = useAuth()
const config = useRuntimeConfig()
const toast = useToast()
const localePath = useLocalePath()

const sidebarOpen = ref(false)
const showModal = ref(false)
const saving = ref(false)
const uploading = ref(false)
const sendingIds = ref(new Set())

const isMediaVideo = (url) => {
  if (!url) return false
  const ext = url.split('.').pop().toLowerCase()
  return ['mp4', 'webm', 'ogg', 'mov', 'avi'].includes(ext)
}

const form = ref({
  message_text: '',
  media_url: '',
  button_text: '',
  button_url: '',
  audience_type: 'all',
  scheduled_at: null
})

// Fetch broadcasts
const { data: broadcasts, refresh } = useFetch(`${config.public.apiBase}/shop/${slug}/admin/broadcasts`, {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const totalSent = computed(() => {
  if (!broadcasts.value) return 0
  return broadcasts.value.reduce((acc, b) => acc + (b.sent_count || 0), 0)
})

const openCreateModal = () => {
  form.value = {
    message_text: '',
    media_url: '',
    button_text: '',
    button_url: '',
    audience_type: 'all'
  }
  showModal.value = true
}

const handleFileUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  uploading.value = true
  try {
    const res = await $fetch(`${config.public.apiBase}/upload`, {
      method: 'POST',
      body: formData,
      headers: { Authorization: `Bearer ${token.value}` }
    })
    form.value.media_url = res.url
    toast.success('Media uploaded')
  } catch (err) {
    toast.error('Upload failed')
  } finally {
    uploading.value = false
  }
}

const saveBroadcast = async () => {
  if (!form.value.message_text) {
    toast.error('Message text is required')
    return
  }

  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/shop/${slug}/admin/broadcasts`, {
      method: 'POST',
      body: form.value,
      headers: { Authorization: `Bearer ${token.value}` }
    })
    toast.success('Broadcast created as draft')
    showModal.value = false
    refresh()
  } catch (err) {
    toast.error(err.data?.detail || 'Error creating broadcast')
  } finally {
    saving.value = false
  }
}

const sendBroadcast = async (id) => {
  if (sendingIds.value.has(id)) return

  sendingIds.value.add(id)
  try {
    // Update local status immediately to hide button
    const broadcast = broadcasts.value?.find(b => b.id === id)
    if (broadcast) {
      broadcast.status = 'pending'
    }

    await $fetch(`${config.public.apiBase}/shop/${slug}/admin/broadcasts/${id}/send`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` }
    })

    toast.success('Broadcast started')
    refresh()

    // Poll for updates
    const poll = setInterval(async () => {
      await refresh()
      const current = broadcasts.value?.find(x => x.id === id)
      if (current && (current.status === 'completed' || current.status === 'failed')) {
        clearInterval(poll)
      }
    }, 5000)
  } catch (err) {
    // Revert status if failed
    const broadcast = broadcasts.value?.find(b => b.id === id)
    if (broadcast) {
      broadcast.status = 'draft'
    }
    toast.error(err.data?.detail || 'Error sending broadcast')
  } finally {
    sendingIds.value.delete(id)
  }
}

const deleteBroadcast = async (id) => {
  if (!confirm('Are you sure you want to delete this broadcast?')) return
  try {
    await $fetch(`${config.public.apiBase}/shop/${slug}/admin/broadcasts/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    toast.success('Deleted')
    refresh()
  } catch (err) {
    toast.error('Error deleting')
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
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
  padding: 40px;
  min-height: 100vh;
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }

  .admin-main {
    margin-left: 0;
    padding: 24px 16px;
    padding-top: 80px;
  }
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 8px;
  line-height: 1.1;
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.75rem;
  }
}

.page-subtitle {
  color: #6B7280;
  font-size: 1.05rem;
  font-weight: 500;
}

.glass-card {
  background: white;
  border: 1px solid #F3F4F6;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  padding: 28px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.sent {
  background: #EEF2FF;
  color: #3b82f6;
}

.stat-icon.campaigns {
  background: #F5F3FF;
  color: #a855f7;
}

.stat-label {
  font-size: 0.95rem;
  color: #6B7280;
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
}

.add-btn {
  background: #111;
  color: white;
  padding: 14px 28px;
  border-radius: 16px;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.2);
}

.add-btn:hover {
  background: #000;
  transform: scale(1.02);
}

.mobile-fab {
  display: none;
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 60px;
  height: 60px;
  border-radius: 30px;
  background: #111;
  color: white;
  border: none;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  z-index: 900;
  transition: all 0.2s;
}

@media (max-width: 1024px) {
  .mobile-hidden {
    display: none;
  }

  .mobile-fab {
    display: flex;
  }
}

.section-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 20px;
}

/* Broadcast Cards */
.broadcasts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

@media (max-width: 640px) {
  .broadcasts-grid {
    grid-template-columns: 1fr;
  }
}

.broadcast-card {
  background: white;
  border: 1px solid #F3F4F6;
  border-radius: 24px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.broadcast-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.card-status {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 6px 12px;
  border-radius: 100px;
  align-self: flex-start;
}

.card-status.draft {
  background: #F3F4F6;
  color: #4B5563;
}

.card-status.pending {
  background: #FEF3C7;
  color: #92400E;
}

.card-status.sending {
  background: #DBEAFE;
  color: #1E40AF;
}

.card-status.completed {
  background: #D1FAE5;
  color: #065F46;
}

.card-status.failed {
  background: #FEE2E2;
  color: #991B1B;
}

.broadcast-msg {
  font-size: 1rem;
  color: #374151;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.broadcast-meta {
  display: flex;
  gap: 16px;
  font-size: 0.85rem;
  color: #6B7280;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #E5E7EB;
  padding-top: 16px;
  margin-top: 4px;
}

.send-now-btn {
  background: #2563EB;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.send-now-btn:hover {
  background: #1D4ED8;
  transform: translateY(-1px);
}

.delete-btn {
  background: #FEE2E2;
  color: #DC2626;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: #FEE2E2;
  transform: scale(1.1);
}

.empty-state {
  text-align: center;
  padding: 80px 40px;
}

.empty-icon {
  display: inline-flex;
  padding: 24px;
  background: #F3F4F6;
  border-radius: 24px;
  color: #9CA3AF;
  margin-bottom: 24px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.glass-modal {
  background: white;
  border: 1px solid #F3F4F6;
  border-radius: 32px;
  width: 100%;
  max-width: 650px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalScale 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 640px) {
  .glass-modal {
    max-height: 95vh;
    border-radius: 24px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #F3F4F6;
  flex-shrink: 0;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 900;
  color: #111;
}

@media (max-width: 640px) {
  .modal-header {
    padding: 20px 24px;
  }
}

.close-modal-btn {
  width: 40px;
  height: 40px;
  background: #F3F4F6;
  border: none;
  border-radius: 14px;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6B7280;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-modal-btn:hover {
  background: #111;
  color: white;
}

.close-modal-btn:hover {
  background: #E5E7EB;
  color: #111;
}

.modal-body {
  padding: 32px;
}

/* Telegram Preview */
.telegram-preview-wrapper label {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.tg-preview {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
}

.tg-bubble {
  background: white;
  border-radius: 16px 16px 16px 4px;
  padding: 12px;
  max-width: 280px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tg-media {
  position: relative;
  margin-bottom: 12px;
}

.tg-media img,
.tg-media .preview-video {
  width: 100%;
  border-radius: 12px;
  display: block;
}

.preview-video {
  background: #000;
  max-height: 300px;
  object-fit: contain;
}

.remove-media-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  backdrop-filter: blur(4px);
  transition: all 0.2s;
}

.remove-media-btn:hover {
  background: rgba(255, 0, 0, 0.7);
  transform: scale(1.1);
}

.media-skeleton {
  width: 100%;
  aspect-ratio: 16/9;
  background: #f0f2f5;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.skeleton-shimmer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }

  100% {
    transform: translateX(100%);
  }
}

.upload-progress-text {
  position: relative;
  z-index: 1;
  font-size: 0.8rem;
  color: #8e949a;
  font-weight: 600;
}

.tg-text {
  font-size: 0.95rem;
  color: #111;
  white-space: pre-wrap;
  line-height: 1.4;
}

.tg-button {
  background: #3b82f6;
  color: white;
  text-align: center;
  padding: 10px;
  border-radius: 10px;
  margin-top: 10px;
  font-size: 0.9rem;
  font-weight: 600;
}

/* Form Styles */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 8px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 12px 14px;
  color: #111;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #3b82f6;
  outline: none;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.image-input-group {
  display: flex;
  gap: 10px;
}

.upload-btn {
  background: #F3F4F6;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #6B7280;
}

.upload-btn:hover {
  background: #E5E7EB;
  color: #111;
}

.audience-selector {
  display: flex;
  gap: 12px;
}

.audience-option {
  flex: 1;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.audience-option:hover {
  border-color: #D1D5DB;
  background: #F3F4F6;
}

.audience-option.active {
  background: #EEF2FF;
  border-color: #3b82f6;
}

.option-title {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.audience-option.active .option-title {
  color: #3b82f6;
}

.limit-note {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.85rem;
  color: #92400E;
  background: #FEF3C7;
  padding: 14px 16px;
  border-radius: 12px;
  line-height: 1.5;
  border-left: 4px solid #F59E0B;
}

.limit-note svg {
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-footer {
  margin-top: 0;
  padding: 24px 32px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  background: #F3F4F6;
  color: #374151;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #E5E7EB;
}

.save-btn {
  background: #111;
  color: white;
  padding: 12px 28px;
  border-radius: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-btn:hover:not(:disabled) {
  background: #000;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner.dark {
  border-color: rgba(0, 0, 0, 0.1);
  border-top-color: #111;
}

.upload-btn.is-loading {
  pointer-events: none;
  background: #E5E7EB;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* List Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.list-move {
  transition: transform 0.5s ease;
}

.animate-in {
  animation: slideUp 0.5s ease-out forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-thumbnail {
  width: 100%;
  height: 120px;
  border-radius: 12px;
  overflow: hidden;
  background: #F3F4F6;
  position: relative;
}

.card-thumbnail img,
.card-thumbnail video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.mb-8 {
  margin-bottom: 2rem;
}

.mt-4 {
  margin-top: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.empty- p {
  color: #6B7280;
  font-size: 1rem;
}
</style>
