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
                <!-- Stats Grid -->
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
                            <div class="kpi-label">{{ $t('platformAdmin.finance.balance') }}</div>
                            <div class="kpi-value">{{ formatPrice(stats?.total_balance || 0) }}</div>
                            <div class="kpi-meta">
                                <span class="badge-beta">Beta</span>
                            </div>
                        </div>
                        <div class="kpi-icon-wrap">
                            <iconify-icon icon="lucide:wallet" />
                        </div>
                    </div>
                </div>

                <!-- Transactions Table -->
                <div class="section-card">
                    <div class="card-header">
                        <h3 class="card-title">{{ $t('platformAdmin.finance.transactions') }}</h3>
                        <div class="filters">
                            <!-- Future filters can go here -->
                        </div>
                    </div>

                    <div class="table-responsive">
                        <table class="data-table" v-if="transactions && transactions.length > 0">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>{{ $t('common.date') || 'Date' }}</th>
                                    <th>{{ $t('common.type') || 'Type' }}</th>
                                    <th>{{ $t('platformAdmin.finance.amount') || 'Amount' }}</th>
                                    <th>{{ $t('common.status') || 'Status' }}</th>
                                    <th>{{ $t('common.actions') || 'Action' }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="tx in transactions" :key="tx.id">
                                    <td class="mono">#{{ tx.id }}</td>
                                    <td class="text-sm">{{ formatDate(tx.created_at) }}</td>
                                    <td>
                                        <span class="type-badge" :class="tx.type.toLowerCase()">{{ tx.type }}</span>
                                    </td>
                                    <td :class="tx.amount > 0 ? 'pos' : 'neg'">
                                        {{ tx.amount > 0 ? '+' : '' }}{{ formatPrice(tx.amount) }}
                                    </td>
                                    <td>
                                        <span class="status-badge" :class="tx.status.toLowerCase()">{{ tx.status
                                            }}</span>
                                    </td>
                                    <td>
                                        <!-- Placeholder for details -->
                                        <button class="icon-btn"><iconify-icon icon="lucide:eye" /></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <div v-else class="empty-state">
                            <iconify-icon icon="lucide:info" />
                            <p>No transactions found</p>
                        </div>
                    </div>

                    <!-- Simple Pagination -->
                    <div class="pagination" v-if="totalTransactions > limit">
                        <button :disabled="offset === 0" @click="prevPage">Prev</button>
                        <span>{{ offset + 1 }} - {{ Math.min(offset + limit, totalTransactions) }} of {{
                            totalTransactions }}</span>
                        <button :disabled="offset + limit >= totalTransactions" @click="nextPage">Next</button>
                    </div>
                </div>
            </div>
        </main>
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

// Use internal URL for SSR, public URL for client
const apiBase = process.server ? config.apiBaseInternal : config.public.apiBase

const handleLogout = () => {
    logout()
    toast.success(t('auth.loggedOut'))
}

// Fetch Stats
const { data: stats, refresh: refreshStats } = useFetch(apiBase + '/platform/admin/wallet/stats', {
    headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

// Fetch Transactions
const { data: txData, pending, refresh: refreshTransactions } = useFetch(apiBase + '/platform/admin/wallet/transactions', {
    query: computed(() => ({ limit: limit.value, offset: offset.value })),
    headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` })),
    watch: [offset]
})

const refresh = () => {
    refreshStats()
    refreshTransactions()
}

const transactions = computed(() => txData.value?.transactions || [])
const totalTransactions = computed(() => txData.value?.total || 0)

const formatDate = (d) => new Date(d).toLocaleString(locale.value)
const prevPage = () => { if (offset.value >= limit.value) offset.value -= limit.value }
const nextPage = () => { if (offset.value + limit.value < totalTransactions.value) offset.value += limit.value }

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

.table-responsive {
    width: 100%;
    overflow-x: auto;
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
    border-bottom: 1px solid #f1f5f9;
}

.data-table td {
    padding: 16px;
    font-size: 0.9rem;
    font-weight: 600;
    border-bottom: 1px solid #f8fafc;
    color: #334155;
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
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 800;
    background: #f1f5f9;
    color: #475569;
}

.type-badge.topup {
    background: #eff6ff;
    color: #3b82f6;
}

.type-badge.payment {
    background: #fff1f2;
    color: #be123c;
}

.status-badge {
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
}

.status-badge.completed {
    background: #ecfdf5;
    color: #059669;
}

.status-badge.pending {
    background: #fffbeb;
    color: #b45309;
}

.status-badge.failed {
    background: #fef2f2;
    color: #dc2626;
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
}

.icon-btn:hover {
    background: #f1f5f9;
    color: #111;
}

.pagination {
    margin-top: 24px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 16px;
}

.pagination button {
    padding: 8px 16px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: white;
    cursor: pointer;
}

.pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@media (max-width: 1024px) {
    .dashboard-main {
        margin-left: 0;
    }

    .mobile-menu-btn {
        display: block;
    }
}
</style>
