<template>
    <div class="platform-admin-billing">
        <PlatformAdminSidebar :current-route="'billing'" :model-value="sidebarOpen"
            @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

        <main class="dashboard-main">
            <!-- Header -->
            <header class="top-nav">
                <div class="nav-left">
                    <button class="mobile-menu-btn" @click="sidebarOpen = true">
                        <iconify-icon icon="lucide:menu" />
                    </button>
                    <div class="page-info">
                        <h1 class="page-title">{{ $t('platformAdmin.finance.title') }}</h1>
                        <p class="page-subtitle">{{ $t('platformAdmin.finance.subtitle') }}</p>
                    </div>
                </div>

                <div class="nav-right">
                    <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
                        <iconify-icon icon="lucide:rotate-cw" />
                        <span>{{ $t('platformAdmin.dashboard.refresh') }}</span>
                    </button>
                </div>
            </header>

            <div class="dashboard-scroll">
                <!-- Enhanced Stats Grid -->
                <div class="kpi-grid">
                    <div class="kpi-card revenue-card">
                        <div class="kpi-content">
                            <div class="kpi-label">{{ $t('platformAdmin.finance.revenue') }}</div>
                            <div class="kpi-value">{{ formatPrice(stats?.total_revenue || 0) }}</div>
                            <div class="kpi-meta">
                                <iconify-icon icon="lucide:trending-up" />
                                <span>{{ $t('platformAdmin.dashboard.total') }}</span>
                            </div>
                        </div>
                        <div class="kpi-icon-wrap">
                            <iconify-icon icon="lucide:dollar-sign" />
                        </div>
                    </div>

                    <div class="kpi-card balance-card">
                        <div class="kpi-content">
                            <div class="kpi-label">Баланс платформы</div>
                            <div class="kpi-value">{{ formatPrice(stats?.total_balance || 0) }}</div>
                            <div class="kpi-meta">
                                <iconify-icon icon="lucide:wallet" />
                                <span>Все кошельки</span>
                            </div>
                        </div>
                        <div class="kpi-icon-wrap">
                            <iconify-icon icon="lucide:wallet" />
                        </div>
                    </div>

                    <div class="kpi-card transactions-card">
                        <div class="kpi-content">
                            <div class="kpi-label">Транзакции</div>
                            <div class="kpi-value">{{ stats?.total_transactions || 0 }}</div>
                            <div class="kpi-meta">
                                <iconify-icon icon="lucide:activity" />
                                <span>За все время</span>
                            </div>
                        </div>
                        <div class="kpi-icon-wrap">
                            <iconify-icon icon="lucide:activity" />
                        </div>
                    </div>

                    <div class="kpi-card topups-card">
                        <div class="kpi-content">
                            <div class="kpi-label">Пополнения</div>
                            <div class="kpi-value">{{ formatPrice(stats?.total_topups || 0) }}</div>
                            <div class="kpi-meta">
                                <iconify-icon icon="lucide:arrow-down-circle" />
                                <span>Входящие</span>
                            </div>
                        </div>
                        <div class="kpi-icon-wrap">
                            <iconify-icon icon="lucide:arrow-down-circle" />
                        </div>
                    </div>
                </div>

                <!-- Filters -->
                <div class="filters-bar">
                    <div class="filter-group">
                        <label>Тип:</label>
                        <select v-model="filterType" @change="applyFilters" class="filter-select">
                            <option value="">Все</option>
                            <option value="topup">Пополнение</option>
                            <option value="charge">Списание</option>
                            <option value="bonus">Бонус</option>
                        </select>
                    </div>

                    <div class="filter-group">
                        <label>Статус:</label>
                        <select v-model="filterStatus" @change="applyFilters" class="filter-select">
                            <option value="">Все</option>
                            <option value="completed">Завершено</option>
                            <option value="pending">В ожидании</option>
                            <option value="failed">Ошибка</option>
                        </select>
                    </div>

                    <div class="filter-group">
                        <label>Магазин:</label>
                        <input v-model="searchShop" @input="applyFilters" type="text" placeholder="ID или название..."
                            class="filter-input" />
                    </div>

                    <button @click="clearFilters" class="clear-filters-btn">
                        <iconify-icon icon="lucide:x" />
                        Сбросить
                    </button>
                </div>

                <!-- Transactions Table -->
                <div class="section-card">
                    <div class="card-header">
                        <h3 class="card-title">{{ $t('platformAdmin.finance.transactions') }}</h3>
                        <div class="header-actions">
                            <button @click="exportTransactions" class="export-btn">
                                <iconify-icon icon="lucide:download" />
                                Экспорт
                            </button>
                        </div>
                    </div>

                    <div class="table-responsive">
                        <!-- Desktop Table View -->
                        <div class="desktop-table-view">
                            <div class="table-scroll-hint" v-if="transactions && transactions.length > 0">
                                <iconify-icon icon="lucide:arrow-left-right" />
                                <span>Прокрутите для просмотра всех данных</span>
                            </div>
                            <table class="data-table" v-if="transactions && transactions.length > 0">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Дата</th>
                                        <th>Магазин</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                        <th>Сумма</th>
                                        <th>Статус</th>
                                        <th>Действия</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="tx in transactions" :key="tx.id">
                                        <td class="mono">#{{ tx.id }}</td>
                                        <td class="text-sm">{{ formatDate(tx.created_at) }}</td>
                                        <td>
                                            <div class="shop-info">
                                                <span class="shop-name">{{ tx.shop_name || 'N/A' }}</span>
                                                <span class="shop-id">ID: {{ tx.shop_id }}</span>
                                            </div>
                                        </td>
                                        <td>
                                            <span class="type-badge" :class="tx.type.toLowerCase()">
                                                <iconify-icon :icon="getTypeIcon(tx.type)" />
                                                {{ getTypeLabel(tx.type) }}
                                            </span>
                                        </td>
                                        <td class="description">{{ tx.description || '-' }}</td>
                                        <td :class="tx.amount > 0 ? 'pos' : 'neg'">
                                            <strong>{{ tx.amount > 0 ? '+' : '' }}{{ formatPrice(tx.amount) }}</strong>
                                        </td>
                                        <td>
                                            <span class="status-badge" :class="tx.status.toLowerCase()">
                                                {{ getStatusLabel(tx.status) }}
                                            </span>
                                        </td>
                                        <td>
                                            <button @click="viewDetails(tx)" class="icon-btn" title="Детали">
                                                <iconify-icon icon="lucide:eye" />
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <!-- Mobile Card View -->
                        <div class="mobile-cards-view" v-if="transactions && transactions.length > 0">
                            <div class="transaction-card" v-for="tx in transactions" :key="tx.id">
                                <div class="card-header-row">
                                    <span class="card-id">#{{ tx.id }}</span>
                                    <span class="status-badge" :class="tx.status.toLowerCase()">
                                        {{ getStatusLabel(tx.status) }}
                                    </span>
                                </div>

                                <div class="card-amount" :class="tx.amount > 0 ? 'pos' : 'neg'">
                                    {{ tx.amount > 0 ? '+' : '' }}{{ formatPrice(tx.amount) }}
                                </div>

                                <div class="card-info-row">
                                    <span class="type-badge" :class="tx.type.toLowerCase()">
                                        <iconify-icon :icon="getTypeIcon(tx.type)" />
                                        {{ getTypeLabel(tx.type) }}
                                    </span>
                                    <span class="card-date">{{ formatDate(tx.created_at) }}</span>
                                </div>

                                <div class="card-shop">
                                    <iconify-icon icon="lucide:store" />
                                    <div>
                                        <div class="shop-name">{{ tx.shop_name || 'N/A' }}</div>
                                        <div class="shop-id">ID: {{ tx.shop_id }}</div>
                                    </div>
                                </div>

                                <div class="card-description" v-if="tx.description">
                                    {{ tx.description }}
                                </div>

                                <button @click="viewDetails(tx)" class="card-details-btn">
                                    <iconify-icon icon="lucide:eye" />
                                    Подробнее
                                </button>
                            </div>
                        </div>

                        <div v-else-if="pending" class="loading-state">
                            <div class="spinner"></div>
                            <p>Загрузка...</p>
                        </div>

                        <div v-else class="empty-state">
                            <iconify-icon icon="lucide:inbox" />
                            <p>Транзакции не найдены</p>
                        </div>
                    </div>

                    <!-- Enhanced Pagination -->
                    <div class="pagination" v-if="totalTransactions > limit">
                        <button :disabled="offset === 0" @click="prevPage" class="page-btn">
                            <iconify-icon icon="lucide:chevron-left" />
                            Назад
                        </button>
                        <span class="page-info">
                            {{ offset + 1 }} - {{ Math.min(offset + limit, totalTransactions) }} из {{
                                totalTransactions }}
                        </span>
                        <button :disabled="offset + limit >= totalTransactions" @click="nextPage" class="page-btn">
                            Вперед
                            <iconify-icon icon="lucide:chevron-right" />
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Transaction Details Modal -->
        <Transition name="modal">
            <div v-if="selectedTransaction" class="modal-overlay" @click.self="selectedTransaction = null">
                <div class="modal-card">
                    <div class="modal-header">
                        <h3>Детали транзакции #{{ selectedTransaction.id }}</h3>
                        <button @click="selectedTransaction = null" class="close-btn">
                            <iconify-icon icon="lucide:x" />
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="detail-row">
                            <span class="label">Дата:</span>
                            <span class="value">{{ formatDate(selectedTransaction.created_at) }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Магазин:</span>
                            <span class="value">{{ selectedTransaction.shop_name }} (ID: {{
                                selectedTransaction.shop_id }})</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Тип:</span>
                            <span class="value">{{ getTypeLabel(selectedTransaction.type) }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Сумма:</span>
                            <span class="value" :class="selectedTransaction.amount > 0 ? 'pos' : 'neg'">
                                {{ formatPrice(selectedTransaction.amount) }}
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Статус:</span>
                            <span class="value">
                                <span class="status-badge" :class="selectedTransaction.status.toLowerCase()">
                                    {{ getStatusLabel(selectedTransaction.status) }}
                                </span>
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Описание:</span>
                            <span class="value">{{ selectedTransaction.description || '-' }}</span>
                        </div>
                        <div class="detail-row" v-if="selectedTransaction.meta_data">
                            <span class="label">Метаданные:</span>
                            <pre class="value">{{ JSON.stringify(selectedTransaction.meta_data, null, 2) }}</pre>
                        </div>
                    </div>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script setup>
const { t, locale } = useI18n()
const { formatPrice } = useCurrency()
const { token, logout } = useAuth()
const config = useRuntimeConfig()
const toast = useToast()

definePageMeta({ middleware: 'platform-admin' })

const sidebarOpen = ref(false)
const limit = ref(20)
const offset = ref(0)
const filterType = ref('')
const filterStatus = ref('')
const searchShop = ref('')
const selectedTransaction = ref(null)

const apiBase = process.server ? config.apiBaseInternal : config.public.apiBase

const handleLogout = () => {
    logout()
    toast.success(t('auth.loggedOut'))
}

// Fetch Stats
const { data: stats, refresh: refreshStats } = useFetch(apiBase + '/platform/admin/wallet/stats', {
    headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

// Fetch Transactions with filters
const { data: txData, pending, refresh: refreshTransactions } = useFetch(apiBase + '/platform/admin/wallet/transactions', {
    query: computed(() => ({
        limit: limit.value,
        offset: offset.value,
        type: filterType.value || undefined,
        status: filterStatus.value || undefined,
        shop_search: searchShop.value || undefined
    })),
    headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` })),
    watch: [offset]
})

const refresh = () => {
    refreshStats()
    refreshTransactions()
}

const transactions = computed(() => txData.value?.transactions || [])
const totalTransactions = computed(() => txData.value?.total || 0)

const formatDate = (d) => new Date(d).toLocaleString(locale.value, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
})

const prevPage = () => { if (offset.value >= limit.value) offset.value -= limit.value }
const nextPage = () => { if (offset.value + limit.value < totalTransactions.value) offset.value += limit.value }

const applyFilters = () => {
    offset.value = 0
    refreshTransactions()
}

const clearFilters = () => {
    filterType.value = ''
    filterStatus.value = ''
    searchShop.value = ''
    applyFilters()
}

const getTypeIcon = (type) => {
    const icons = {
        topup: 'lucide:arrow-down-circle',
        charge: 'lucide:arrow-up-circle',
        bonus: 'lucide:gift'
    }
    return icons[type.toLowerCase()] || 'lucide:circle'
}

const getTypeLabel = (type) => {
    const labels = {
        topup: 'Пополнение',
        charge: 'Списание',
        bonus: 'Бонус'
    }
    return labels[type.toLowerCase()] || type
}

const getStatusLabel = (status) => {
    const labels = {
        completed: 'Завершено',
        pending: 'В ожидании',
        failed: 'Ошибка'
    }
    return labels[status.toLowerCase()] || status
}

const viewDetails = (tx) => {
    selectedTransaction.value = tx
}

const exportTransactions = () => {
    toast.info('Функция экспорта в разработке')
}
</script>

<style scoped>
.platform-admin-billing {
    background: #f8fafc;
    min-height: 100vh;
    display: flex;
}

.dashboard-main {
    flex: 1;
    margin-left: 280px;
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.top-nav {
    padding: 24px 32px;
    background: #fff;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.mobile-menu-btn {
    display: none;
    width: 40px;
    height: 40px;
    border: none;
    background: #f1f5f9;
    border-radius: 12px;
    font-size: 1.5rem;
    cursor: pointer;
}

.page-title {
    font-size: 1.5rem;
    font-weight: 950;
    margin: 0;
    letter-spacing: -0.5px;
}

.page-subtitle {
    font-size: 0.875rem;
    color: #64748b;
    margin: 4px 0 0;
}

.refresh-btn {
    padding: 10px 16px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
}

.refresh-btn:hover {
    background: #f1f5f9;
}

.refresh-btn.loading iconify-icon {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.dashboard-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 32px;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 24px;
    margin-bottom: 32px;
}

.kpi-card {
    background: white;
    padding: 24px;
    border-radius: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.02);
}

.kpi-label {
    font-size: 0.8rem;
    font-weight: 800;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 1.85rem;
    font-weight: 950;
    color: #111;
}

.kpi-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    margin-top: 8px;
}

.kpi-icon-wrap {
    width: 56px;
    height: 56px;
    background: #f8fafc;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.75rem;
}

.revenue-card .kpi-icon-wrap {
    background: #ecfdf5;
    color: #10b981;
}

.balance-card .kpi-icon-wrap {
    background: #fff7ed;
    color: #ea580c;
}

.transactions-card .kpi-icon-wrap {
    background: #eff6ff;
    color: #3b82f6;
}

.topups-card .kpi-icon-wrap {
    background: #f5f3ff;
    color: #8b5cf6;
}

.filters-bar {
    background: white;
    padding: 20px 24px;
    border-radius: 16px;
    margin-bottom: 24px;
    display: flex;
    gap: 16px;
    align-items: flex-end;
    flex-wrap: wrap;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.filter-group label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
}

.filter-select,
.filter-input {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 600;
    min-width: 150px;
}

.clear-filters-btn {
    padding: 8px 16px;
    background: #fee2e2;
    color: #dc2626;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
}

.section-card {
    background: white;
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
}

.card-header {
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 900;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 12px;
}

.export-btn {
    padding: 8px 16px;
    background: #111;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
}

.table-responsive {
    width: 100%;
    overflow-x: auto;
    position: relative;
}

/* Desktop table view - visible by default */
.desktop-table-view {
    display: block;
}

/* Mobile cards view - hidden by default */
.mobile-cards-view {
    display: none;
}

.table-scroll-hint {
    display: none;
    padding: 8px 12px;
    background: #fef3c7;
    border: 1px solid #fbbf24;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #92400e;
    align-items: center;
    gap: 6px;
}

.table-scroll-hint iconify-icon {
    font-size: 1rem;
}

/* Mobile Transaction Cards */
.transaction-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.2s;
}

.transaction-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: #cbd5e1;
}

.card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.card-id {
    font-family: monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: #64748b;
}

.card-amount {
    font-size: 1.75rem;
    font-weight: 900;
    margin-bottom: 12px;
}

.card-amount.pos {
    color: #10b981;
}

.card-amount.neg {
    color: #ef4444;
}

.card-info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    gap: 8px;
}

.card-date {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 600;
}

.card-shop {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: #f8fafc;
    border-radius: 8px;
    margin-bottom: 12px;
}

.card-shop iconify-icon {
    font-size: 1.25rem;
    color: #64748b;
}

.card-shop .shop-name {
    font-size: 0.875rem;
    font-weight: 700;
    color: #111;
}

.card-shop .shop-id {
    font-size: 0.7rem;
    color: #94a3b8;
}

.card-description {
    font-size: 0.8rem;
    color: #64748b;
    padding: 8px 10px;
    background: #f1f5f9;
    border-radius: 6px;
    margin-bottom: 12px;
    line-height: 1.4;
}

.card-details-btn {
    width: 100%;
    padding: 10px;
    background: #111;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    transition: all 0.2s;
}

.card-details-btn:active {
    transform: scale(0.98);
    background: #000;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    text-align: left;
    padding: 16px;
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #94a3b8;
    font-weight: 800;
    border-bottom: 2px solid #f1f5f9;
}

.data-table td {
    padding: 16px;
    font-size: 0.9rem;
    font-weight: 600;
    border-bottom: 1px solid #f8fafc;
    color: #334155;
}

.shop-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.shop-name {
    font-weight: 700;
    color: #111;
}

.shop-id {
    font-size: 0.75rem;
    color: #94a3b8;
}

.description {
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.mono {
    font-family: monospace;
    color: #64748b;
}

.text-sm {
    font-size: 0.8rem;
    color: #64748b;
}

.pos {
    color: #10b981;
}

.neg {
    color: #ef4444;
}

.type-badge {
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 800;
    background: #f1f5f9;
    color: #475569;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.type-badge.topup {
    background: #dbeafe;
    color: #1e40af;
}

.type-badge.charge {
    background: #fee2e2;
    color: #991b1b;
}

.type-badge.bonus {
    background: #f3e8ff;
    color: #6b21a8;
}

.status-badge {
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
}

.status-badge.completed {
    background: #d1fae5;
    color: #065f46;
}

.status-badge.pending {
    background: #fef3c7;
    color: #92400e;
}

.status-badge.failed {
    background: #fee2e2;
    color: #991b1b;
}

.icon-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #64748b;
    transition: all 0.2s;
}

.icon-btn:hover {
    background: #f1f5f9;
    color: #111;
}

.loading-state,
.empty-state {
    padding: 60px 20px;
    text-align: center;
    color: #94a3b8;
}

.loading-state iconify-icon,
.empty-state iconify-icon {
    font-size: 3rem;
    margin-bottom: 12px;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #f1f5f9;
    border-top-color: #111;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
}

.pagination {
    margin-top: 24px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 16px;
}

.page-btn {
    padding: 10px 16px;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    background: white;
    cursor: pointer;
    font-weight: 700;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
    background: #f8fafc;
}

.page-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.page-info {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
}

/* Modal */
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

.modal-card {
    background: white;
    border-radius: 24px;
    padding: 32px;
    max-width: 600px;
    width: 100%;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.modal-header h3 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 900;
}

.close-btn {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}

.modal-body {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
}

.detail-row .label {
    font-weight: 700;
    color: #64748b;
    font-size: 0.875rem;
}

.detail-row .value {
    font-weight: 600;
    color: #111;
    text-align: right;
}

.detail-row pre {
    background: #f8fafc;
    padding: 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    overflow-x: auto;
}

.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

/* Tablet and below */
@media (max-width: 1024px) {
    .dashboard-main {
        margin-left: 0;
    }

    .mobile-menu-btn {
        display: block;
    }

    .dashboard-scroll {
        padding: 20px;
    }

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        padding: 20px;
    }

    .kpi-value {
        font-size: 1.5rem;
    }

    .kpi-icon-wrap {
        width: 48px;
        height: 48px;
        font-size: 1.5rem;
    }

    .section-card {
        padding: 20px;
        border-radius: 16px;
    }

    .filters-bar {
        flex-direction: column;
        align-items: stretch;
        padding: 16px;
    }

    .filter-group {
        width: 100%;
    }

    .filter-select,
    .filter-input {
        width: 100%;
        min-width: auto;
    }

    .clear-filters-btn {
        width: 100%;
        justify-content: center;
    }

    .card-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .header-actions {
        width: 100%;
    }

    .export-btn {
        width: 100%;
        justify-content: center;
    }

    /* Make table scrollable horizontally on tablet */
    .table-responsive {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    .table-scroll-hint {
        display: flex;
    }

    .data-table {
        min-width: 800px;
    }

    .pagination {
        justify-content: center;
        flex-wrap: wrap;
    }

    .modal-card {
        padding: 24px;
        margin: 20px;
    }
}

/* Mobile phones */
@media (max-width: 640px) {
    .dashboard-scroll {
        padding: 16px;
    }

    .top-nav {
        padding: 12px 16px;
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .nav-left {
        width: 100%;
    }

    .nav-right {
        width: 100%;
    }

    .refresh-btn {
        width: 100%;
        justify-content: center;
        padding: 10px 16px;
    }

    .page-title {
        font-size: 1.25rem;
    }

    .page-subtitle {
        font-size: 0.8rem;
    }

    .kpi-grid {
        grid-template-columns: 1fr;
        gap: 12px;
        margin-bottom: 20px;
    }

    .kpi-card {
        padding: 16px;
        border-radius: 16px;
    }

    .kpi-label {
        font-size: 0.7rem;
    }

    .kpi-value {
        font-size: 1.35rem;
    }

    .kpi-meta {
        font-size: 0.7rem;
    }

    .kpi-icon-wrap {
        width: 44px;
        height: 44px;
        font-size: 1.35rem;
        border-radius: 12px;
    }

    .filters-bar {
        padding: 12px;
        gap: 12px;
        border-radius: 12px;
        margin-bottom: 16px;
    }

    .filter-group label {
        font-size: 0.7rem;
    }

    .filter-select,
    .filter-input {
        padding: 10px 12px;
        font-size: 0.875rem;
    }

    .clear-filters-btn {
        padding: 10px 16px;
        font-size: 0.8rem;
    }

    .section-card {
        padding: 16px;
        border-radius: 12px;
    }

    .card-title {
        font-size: 1.1rem;
    }

    .export-btn {
        padding: 10px 16px;
        font-size: 0.8rem;
    }

    /* Switch to card view on mobile */
    .desktop-table-view {
        display: none;
    }

    .mobile-cards-view {
        display: block;
    }

    /* Mobile-optimized table (if cards are not used) */
    .data-table {
        min-width: 700px;
        font-size: 0.85rem;
    }

    .data-table th,
    .data-table td {
        padding: 12px 8px;
        font-size: 0.8rem;
    }

    .data-table th {
        font-size: 0.7rem;
    }

    .shop-name {
        font-size: 0.85rem;
    }

    .shop-id {
        font-size: 0.7rem;
    }

    .description {
        max-width: 120px;
    }

    .type-badge,
    .status-badge {
        padding: 4px 8px;
        font-size: 0.65rem;
    }

    .icon-btn {
        width: 28px;
        height: 28px;
        font-size: 0.9rem;
    }

    /* Mobile card adjustments */
    .transaction-card {
        padding: 14px;
        margin-bottom: 10px;
    }

    .card-amount {
        font-size: 1.5rem;
        margin-bottom: 10px;
    }

    .card-shop {
        padding: 8px;
        margin-bottom: 10px;
    }

    .card-details-btn {
        padding: 9px;
        font-size: 0.8rem;
    }

    .pagination {
        margin-top: 16px;
        gap: 8px;
    }

    .page-btn {
        padding: 8px 12px;
        font-size: 0.8rem;
    }

    .page-info {
        font-size: 0.8rem;
        width: 100%;
        text-align: center;
        order: -1;
        margin-bottom: 8px;
    }

    /* Mobile modal */
    .modal-overlay {
        padding: 0;
        align-items: flex-end;
    }

    .modal-card {
        max-width: 100%;
        max-height: 90vh;
        border-radius: 24px 24px 0 0;
        margin: 0;
        padding: 20px;
    }

    .modal-header {
        margin-bottom: 20px;
    }

    .modal-header h3 {
        font-size: 1.1rem;
    }

    .detail-row {
        flex-direction: column;
        gap: 4px;
        padding: 10px 0;
    }

    .detail-row .label {
        font-size: 0.75rem;
    }

    .detail-row .value {
        text-align: left;
        font-size: 0.875rem;
    }

    .detail-row pre {
        font-size: 0.7rem;
        padding: 10px;
    }

    /* Loading and empty states */
    .loading-state,
    .empty-state {
        padding: 40px 16px;
    }

    .loading-state iconify-icon,
    .empty-state iconify-icon {
        font-size: 2.5rem;
    }

    .spinner {
        width: 32px;
        height: 32px;
    }
}

/* Extra small phones */
@media (max-width: 375px) {
    .dashboard-scroll {
        padding: 12px;
    }

    .kpi-value {
        font-size: 1.2rem;
    }

    .kpi-icon-wrap {
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
    }

    .page-title {
        font-size: 1.1rem;
    }

    .data-table {
        min-width: 650px;
    }

    .modal-card {
        padding: 16px;
    }

    /* Extra small card adjustments */
    .card-amount {
        font-size: 1.35rem;
    }

    .card-shop .shop-name {
        font-size: 0.8rem;
    }

    .transaction-card {
        padding: 12px;
    }
}

/* Landscape orientation for phones */
@media (max-width: 896px) and (orientation: landscape) {
    .modal-overlay {
        align-items: center;
    }

    .modal-card {
        border-radius: 24px;
        max-height: 85vh;
    }

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
