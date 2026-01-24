<template>
    <div class="wallet-page-inner">
        <div class="page-header">
            <div class="header-content">
                <div class="header-text">
                    <h1 class="page-title">{{ $t('wallet.title') }}</h1>
                    <p class="page-subtitle">{{ $t('wallet.balance') }}</p>
                </div>
                <button class="btn btn-primary top-up-btn" @click="showTopUpModal = true">
                    <iconify-icon icon="lucide:plus" width="20"></iconify-icon>
                    <span>{{ $t('wallet.topUp') }}</span>
                </button>
            </div>
        </div>

        <div class="admin-content">
            <!-- Balance Card - Premium Design -->
            <div class="balance-card">
                <div class="balance-glass-overlay"></div>
                <div class="balance-content">
                    <div class="balance-main">
                        <div class="balance-label-group">
                            <span class="balance-label">{{ $t('wallet.balance') }}</span>
                            <div class="balance-status-tag">{{ $t('wallet.status.live') }}</div>
                        </div>
                        <div class="balance-amount">{{ formatPrice(balance) }}</div>
                    </div>
                    <div class="wallet-icon-large">
                        <iconify-icon icon="lucide:wallet" no-size></iconify-icon>
                    </div>
                </div>
                <div class="balance-footer">
                    <div class="store-id">{{ $t('wallet.shopId') }}: {{ shopSlug }}</div>
                    <div class="currency-badge">UZS</div>
                </div>
            </div>

            <!-- Transactions Section -->
            <div class="section-container">
                <div class="section-header">
                    <h2 class="section-title">{{ $t('wallet.transactionHistory') }}</h2>
                </div>

                <div v-if="loading" class="loading-state">
                    <div class="loader-spinner"></div>
                    <span>{{ $t('common.loading') }}</span>
                </div>

                <div v-else-if="!transactions || transactions.length === 0" class="empty-state">
                    <div class="empty-illustration">
                        <iconify-icon icon="lucide:history" width="64"></iconify-icon>
                    </div>
                    <p>{{ $t('wallet.noTransactions') }}</p>
                </div>

                <div v-else class="transactions-list-wrapper">
                    <!-- Desktop Table -->
                    <div class="table-responsive desktop-only">
                        <table class="premium-table">
                            <thead>
                                <tr>
                                    <th>{{ $t('wallet.table.date') }}</th>
                                    <th>{{ $t('wallet.table.type') }}</th>
                                    <th>{{ $t('wallet.table.description') }}</th>
                                    <th>{{ $t('wallet.table.amount') }}</th>
                                    <th>{{ $t('wallet.table.status') }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="transaction in transactions" :key="transaction.id">
                                    <td class="td-date">{{ formatDate(transaction.created_at) }}</td>
                                    <td>
                                        <span :class="`type-badge type-${transaction.type.toLowerCase()}`">
                                            <span class="dot"></span>
                                            {{ $t(`wallet.type.${transaction.type.toLowerCase()}`) }}
                                        </span>
                                    </td>
                                    <td class="td-desc">{{ transaction.description }}</td>
                                    <td class="td-amount" :class="transaction.amount < 0 ? 'neg' : 'pos'">
                                        {{ transaction.amount < 0 ? '-' : '+' }}{{
                                            formatPrice(Math.abs(transaction.amount)) }} </td>
                                    <td>
                                        <span :class="`status-pill status-${transaction.status.toLowerCase()}`">
                                            {{ $t(`wallet.status.${transaction.status.toLowerCase()}`) }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Mobile Cards -->
                    <div class="mobile-only mobile-transactions">
                        <div v-for="transaction in transactions" :key="transaction.id" class="m-transaction-card">
                            <div class="m-row-top">
                                <div class="m-type">
                                    <span :class="`type-badge type-${transaction.type.toLowerCase()}`">
                                        <span class="dot"></span>
                                        {{ $t(`wallet.type.${transaction.type.toLowerCase()}`) }}
                                    </span>
                                </div>
                                <div class="m-amount" :class="transaction.amount < 0 ? 'neg' : 'pos'">
                                    {{ transaction.amount < 0 ? '-' : '+' }}{{ formatPrice(Math.abs(transaction.amount))
                                        }} </div>
                                </div>
                                <div class="m-desc">{{ transaction.description }}</div>
                                <div class="m-row-bottom">
                                    <span class="m-date">{{ formatDate(transaction.created_at) }}</span>
                                    <span :class="`status-pill status-${transaction.status.toLowerCase()}`">
                                        {{ $t(`wallet.status.${transaction.status.toLowerCase()}`) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Top Up Modal -->
            <Transition name="modal-fade">
                <div v-if="showTopUpModal" class="modal-overlay" @click.self="showTopUpModal = false">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3>{{ $t('wallet.topUpBalance') }}</h3>
                            <button class="modal-close" @click="showTopUpModal = false">
                                <iconify-icon icon="lucide:x" width="24"></iconify-icon>
                            </button>
                        </div>

                        <div class="modal-body">
                            <div class="warning-box">
                                <iconify-icon icon="lucide:info" width="20"></iconify-icon>
                                <span>{{ $t('wallet.testModeWarning') }}</span>
                            </div>

                            <div class="field-group">
                                <label>{{ $t('wallet.enterAmount') }}</label>
                                <div class="amount-field">
                                    <input v-model.number="topUpAmount" type="number" placeholder="0" class="big-input"
                                        min="1000" step="5000" />
                                    <span class="field-currency">{{ $t('currency') }}</span>
                                </div>
                            </div>

                            <div class="quick-grid">
                                <button v-for="amount in [50000, 100000, 500000, 1000000]" :key="amount"
                                    @click="topUpAmount = amount" class="quick-btn"
                                    :class="{ selected: topUpAmount === amount }">
                                    +{{ formatShortPrice(amount) }}
                                </button>
                            </div>
                        </div>

                        <div class="modal-footer">
                            <button @click="showTopUpModal = false" class="btn btn-secondary">{{ $t('common.cancel')
                            }}</button>
                            <button @click="handleTopUp" class="btn btn-primary"
                                :disabled="loadingTopUp || !topUpAmount || topUpAmount < 1000">
                                <span v-if="loadingTopUp" class="spinner-small"></span>
                                <span v-else>{{ $t('wallet.topUpAction') }}</span>
                            </button>
                        </div>
                    </div>
                </div>
            </Transition>
        </div>
</template>

<script setup>
definePageMeta({
    middleware: ['auth', 'shop-owner'],
    layout: 'shop-admin'
})

const route = useRoute()
const shopSlug = route.params.slug
const { token } = useAuth()
const config = useRuntimeConfig()
const { formatPrice } = useCurrency()

const balance = ref(0)
const transactions = ref([])
const loading = ref(false)
const loadingTopUp = ref(false)
const showTopUpModal = ref(false)
const topUpAmount = ref(100000)

const formatDate = (dateString) => {
    if (!dateString) return ''
    return new Date(dateString).toLocaleString('ru-RU', {
        day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
    })
}

const formatShortPrice = (val) => {
    if (val >= 1000000) return (val / 1000000) + 'млн'
    if (val >= 1000) return (val / 1000) + 'к'
    return val
}

const fetchBalance = async () => {
    try {
        const data = await $fetch(`${config.public.apiBase}/wallet/balance`, {
            params: { shop_slug: shopSlug },
            headers: { Authorization: `Bearer ${token.value}` }
        })
        balance.value = data.balance
    } catch (error) { }
}

const fetchTransactions = async () => {
    loading.value = true
    try {
        const data = await $fetch(`${config.public.apiBase}/wallet/transactions`, {
            params: { shop_slug: shopSlug },
            headers: { Authorization: `Bearer ${token.value}` }
        })
        transactions.value = data.transactions
    } catch (error) { } finally {
        loading.value = false
    }
}

const handleTopUp = async () => {
    if (!topUpAmount.value || topUpAmount.value < 1000) return
    loadingTopUp.value = true
    try {
        const data = await $fetch(`${config.public.apiBase}/wallet/topup`, {
            method: 'POST', params: { shop_slug: shopSlug },
            body: { amount: topUpAmount.value },
            headers: { Authorization: `Bearer ${token.value}` }
        })
        balance.value = data.new_balance
        showTopUpModal.value = false
        await fetchTransactions()
        useToast().success(useI18n().t('wallet.topUpSuccess'))
    } catch (error) {
        useToast().error(useI18n().t('wallet.topUpError'))
    } finally {
        loadingTopUp.value = false
    }
}

onMounted(() => {
    fetchBalance()
    fetchTransactions()
})
</script>

<style scoped>
.wallet-page-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.page-header {
    margin-bottom: 32px;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 24px;
}

.page-title {
    font-size: 2.5rem;
    font-weight: 900;
    color: #111;
    margin: 0;
    letter-spacing: -0.04em;
}

.page-subtitle {
    color: #6B7280;
    margin: 4px 0 0 0;
    font-size: 1rem;
}

/* Balance Card */
.balance-card {
    position: relative;
    background: #111;
    border-radius: 32px;
    padding: 48px;
    color: white;
    overflow: hidden;
    margin-bottom: 48px;
    box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.25);
    transition: transform 0.3s;
}

.balance-glass-overlay {
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, transparent 70%);
    border-radius: 50%;
}

.balance-content {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 2;
}

.balance-label-group {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.balance-label {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(255, 255, 255, 0.5);
}

.balance-status-tag {
    background: rgba(34, 197, 94, 0.2);
    color: #4ADE80;
    padding: 4px 10px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 800;
}

.balance-amount {
    font-size: 4rem;
    font-weight: 950;
    letter-spacing: -0.05em;
    line-height: 1;
}

.wallet-icon-large {
    font-size: 100px;
    opacity: 0.1;
    transform: rotate(-15deg);
}

.balance-footer {
    position: relative;
    z-index: 2;
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 24px;
}

.store-id {
    font-family: monospace;
    color: rgba(255, 255, 255, 0.3);
    font-size: 0.8rem;
}

.currency-badge {
    font-weight: 800;
    color: rgba(255, 255, 255, 0.6);
}

/* Section List */
.section-container {
    background: white;
    border-radius: 24px;
    border: 1.5px solid #E5E7EB;
    padding: 32px;
}

.section-header {
    margin-bottom: 24px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 900;
    color: #111;
    letter-spacing: -0.02em;
}

/* Table Styles */
.premium-table {
    width: 100%;
    border-collapse: collapse;
}

.premium-table th {
    text-align: left;
    padding: 16px 12px;
    font-size: 0.75rem;
    font-weight: 800;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #F3F4F6;
}

.premium-table td {
    padding: 18px 12px;
    border-bottom: 1px solid #FAFAFA;
    font-size: 0.9rem;
}

.td-date {
    color: #6B7280;
    font-family: tabular-nums;
}

.td-desc {
    font-weight: 600;
    color: #111;
}

.td-amount {
    font-weight: 800;
    text-align: right;
    white-space: nowrap;
    font-size: 1rem;
}

.td-amount.pos {
    color: #10B981;
}

.td-amount.neg {
    color: #EF4444;
}

.type-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 800;
}

.type-badge .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

.type-topup {
    background: #ECFDF5;
    color: #065F46;
}

.type-topup .dot {
    background: #10B981;
}

.type-payment {
    background: #FFF1F2;
    color: #991B1B;
}

.type-payment .dot {
    background: #F43F5E;
}

.status-pill {
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 700;
    background: #F3F4F6;
    color: #4B5563;
    text-transform: uppercase;
}

.status-completed {
    background: #DCFCE7;
    color: #15803D;
}

/* Mobile Only Classes */
.mobile-only {
    display: none;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .balance-amount {
        font-size: 3rem;
    }

    .balance-card {
        padding: 32px;
    }

    .subscription-premium-page {
        padding: 20px;
    }
}

@media (max-width: 768px) {
    .desktop-only {
        display: none;
    }

    .mobile-only {
        display: block;
    }

    .header-content {
        flex-direction: column;
        align-items: stretch;
        gap: 16px;
    }

    .top-up-btn {
        width: 100%;
        justify-content: center;
    }

    .balance-card {
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 32px;
    }

    .balance-amount {
        font-size: 2.25rem;
    }

    .wallet-icon-large {
        font-size: 60px;
    }

    .balance-footer {
        margin-top: 24px;
        padding-top: 16px;
    }

    .section-container {
        padding: 20px;
        border-radius: 20px;
    }

    /* Mobile Transaction Cards */
    .m-transaction-card {
        padding: 16px 0;
        border-bottom: 1px solid #F3F4F6;
    }

    .m-transaction-card:last-child {
        border-bottom: none;
    }

    .m-row-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .m-amount {
        font-weight: 800;
        font-size: 1.1rem;
    }

    .m-desc {
        font-weight: 600;
        font-size: 0.95rem;
        color: #111;
        margin-bottom: 8px;
    }

    .m-row-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .m-date {
        font-size: 0.8rem;
        color: #9CA3AF;
    }
}

/* Modal Helper */
.spinner-small {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: rotate 0.8s linear infinite;
}

@keyframes rotate {
    to {
        transform: rotate(360deg);
    }
}

/* Warning Box */
.warning-box {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    background: #FEF3C7;
    border: 1.5px solid #FCD34D;
    border-radius: 12px;
    margin-bottom: 24px;
    color: #92400E;
    font-size: 0.9rem;
    font-weight: 600;
}

.warning-box iconify-icon {
    flex-shrink: 0;
    color: #F59E0B;
}

.btn {
    height: 54px;
    padding: 0 24px;
    border-radius: 16px;
    font-weight: 800;
    border: none;
    cursor: pointer;
    transition: 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

.btn-primary {
    background: #111;
    color: white;
}

.btn-secondary {
    background: #F3F4F6;
    color: #111;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px rgba(0, 0, 0, 0.2);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content {
    background: white;
    width: 100%;
    max-width: 480px;
    border-radius: 32px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    animation: modalSlideUp 0.3s ease-out;
}

@keyframes modalSlideUp {
    from {
        transform: translateY(20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.modal-header {
    padding: 24px 32px;
    border-bottom: 1px solid #F3F4F6;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 800;
    color: #111;
}

.modal-close {
    background: none;
    border: none;
    color: #9CA3AF;
    cursor: pointer;
    padding: 4px;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-close:hover {
    color: #111;
    transform: rotate(90deg);
}

.modal-body {
    padding: 32px;
}

.field-group {
    margin-bottom: 24px;
}

.field-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 700;
    color: #4B5563;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.amount-field {
    position: relative;
    display: flex;
    align-items: center;
}

.big-input {
    width: 100%;
    height: 72px;
    background: #F9FAFB;
    border: 2px solid #F3F4F6;
    border-radius: 20px;
    padding: 0 80px 0 24px;
    font-size: 1.75rem;
    font-weight: 800;
    color: #111;
    transition: 0.2s;
    outline: none;
}

.big-input:focus {
    background: white;
    border-color: #111;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

.field-currency {
    position: absolute;
    right: 24px;
    font-weight: 800;
    color: #9CA3AF;
    font-size: 0.9rem;
}

.quick-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.quick-btn {
    height: 48px;
    background: white;
    border: 1.5px solid #E5E7EB;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #374151;
    cursor: pointer;
    transition: 0.2s;
}

.quick-btn:hover {
    border-color: #111;
    background: #F9FAFB;
}

.quick-btn.selected {
    background: #111;
    border-color: #111;
    color: white;
}

.modal-footer {
    padding: 24px 32px;
    background: #F9FAFB;
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 12px;
}

.modal-footer .btn {
    width: 100%;
    justify-content: center;
}

/* Animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
    transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
    opacity: 0;
}

@media (max-width: 480px) {
    .modal-content {
        border-radius: 24px;
    }

    .modal-body {
        padding: 24px;
    }

    .big-input {
        font-size: 1.5rem;
        height: 64px;
    }

    .quick-grid {
        grid-template-columns: 1fr 1fr;
    }

    .modal-footer {
        grid-template-columns: 1fr;
        padding: 24px;
    }
}
</style>
