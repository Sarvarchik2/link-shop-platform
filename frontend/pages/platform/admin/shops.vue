<template>
  <div class="platform-admin-page">
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
      <span class="mobile-title">{{ $t('platformAdmin.shops.title') }}</span>
      <NuxtLink to="/" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar :current-route="currentRoute" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div class="header-content">
          <div>
            <h1 class="admin-title">{{ $t('platformAdmin.shops.title') }}</h1>
            <p class="admin-subtitle">{{ $t('platformAdmin.shops.subtitle') }}</p>
          </div>
          <button @click="refresh" class="refresh-btn" :disabled="pending">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              :class="{ spinning: pending }">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span>{{ $t('platformAdmin.dashboard.refresh') }}</span>
          </button>
        </div>
      </div>

      <div class="admin-content">
        <!-- Statistics Cards -->
        <div class="stats-overview">
          <div class="stat-card">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z">
                </path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ shops?.length || 0 }}</div>
              <div class="stat-label">{{ $t('platformAdmin.shops.total') }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon active">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ activeShopsCount }}</div>
              <div class="stat-label">{{ $t('platformAdmin.shops.active') }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon trial">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 6v6l4 2"></path>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ trialShopsCount }}</div>
              <div class="stat-label">{{ $t('platformAdmin.shops.trial') }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon expired">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ expiredShopsCount }}</div>
              <div class="stat-label">{{ $t('platformAdmin.shops.expired') }}</div>
            </div>
          </div>
        </div>

        <!-- Filters and Search -->
        <div class="filters-section">
          <div class="search-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input v-model="searchQuery" type="text" :placeholder="$t('platformAdmin.shops.search')"
              class="search-input" />
          </div>

          <div class="filters-group">
            <select v-model="filterStatus" class="filter-select">
              <option value="">{{ $t('platformAdmin.shops.filterStatus') }}</option>
              <option value="trial">{{ $t('platformAdmin.shops.trial') }}</option>
              <option value="active">{{ $t('platformAdmin.shops.active') }}</option>
              <option value="expired">{{ $t('platformAdmin.shops.expired') }}</option>
              <option value="cancelled">{{ $t('platformAdmin.shops.cancelled') }}</option>
            </select>

            <select v-model="filterActive" class="filter-select">
              <option value="">{{ $t('platformAdmin.shops.filterActive') }}</option>
              <option value="true">{{ $t('platformAdmin.shops.onlyActive') }}</option>
              <option value="false">{{ $t('platformAdmin.shops.onlyInactive') }}</option>
            </select>

            <button @click="clearFilters" class="clear-filters-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              {{ $t('platformAdmin.shops.clear') }}
            </button>
          </div>
        </div>

        <!-- Error State -->
        <div v-if="error" class="error-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p class="error-message">{{ $t('platformAdmin.dashboard.error') }}: {{ error.message || 'Unknown' }}</p>
          <button @click="refresh" class="retry-btn">{{ $t('platformAdmin.dashboard.refresh') }}</button>
        </div>

        <!-- Loading State -->
        <div v-else-if="pending" class="loading-state">
          <div class="loading-spinner"></div>
          <p>{{ $t('platformAdmin.dashboard.loading') }}</p>
        </div>

        <!-- Table -->
        <div v-else class="table-container">
          <div class="table-header">
            <div class="table-info">
              <span>{{ $t('common.showing') }} {{ displayedShops.length }} {{ $t('common.of') }} {{ shops?.length || 0
              }}</span>
            </div>
            <div class="table-actions">
              <button @click="exportData" class="export-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                {{ $t('platformAdmin.shops.export') }}
              </button>
            </div>
          </div>

          <div class="shops-table-wrapper">
            <table class="shops-table">
              <thead>
                <tr>
                  <th @click="sortBy('id')" class="sortable">
                    <div class="th-content">
                      ID
                      <svg v-if="sortField === 'id'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('name')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.shops.table.name') }}
                      <svg v-if="sortField === 'name'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>Slug</th>
                  <th @click="sortBy('owner')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.shops.table.owner') }}
                      <svg v-if="sortField === 'owner'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>{{ $t('platformAdmin.shops.table.plan') }}</th>
                  <th @click="sortBy('subscription_status')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.shops.table.status') }}
                      <svg v-if="sortField === 'subscription_status'" width="12" height="12" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('expires_at')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.shops.table.expires') }}
                      <svg v-if="sortField === 'expires_at'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('created_at')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.shops.table.created') }}
                      <svg v-if="sortField === 'created_at'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th @click="sortBy('is_active')" class="sortable">
                    <div class="th-content">
                      {{ $t('platformAdmin.shops.table.isActive') }}
                      <svg v-if="sortField === 'is_active'" width="12" height="12" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" :class="{ reverse: sortOrder === 'desc' }">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </div>
                  </th>
                  <th>{{ $t('platformAdmin.shops.table.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="shop in paginatedShops" :key="shop.id" :class="{ 'expiring-soon': isExpiringSoon(shop) }">
                  <td>{{ shop.id }}</td>
                  <td>
                    <div class="shop-info">
                      <img v-if="shop.logo_url" :src="shop.logo_url" :alt="shop.name" class="shop-logo" />
                      <div class="shop-logo-placeholder" v-else>
                        {{ shop.name.charAt(0).toUpperCase() }}
                      </div>
                      <div class="shop-details">
                        <span class="shop-name">{{ shop.name }}</span>
                        <span v-if="shop.description" class="shop-description">{{ truncateText(shop.description, 40)
                        }}</span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <a :href="'/' + shop.slug" target="_blank" class="shop-slug-link" :title="shop.slug">
                      <code class="shop-slug">{{ shop.slug }}</code>
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                      </svg>
                    </a>
                  </td>
                  <td>
                    <div class="owner-info">
                      <div class="owner-name">{{ shop.owner_name || `ID: ${shop.owner_id}` }}</div>
                      <div class="owner-phone" v-if="shop.owner_phone">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2">
                          <path
                            d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                          </path>
                        </svg>
                        {{ shop.owner_phone }}
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="plan-name-cell">{{ shop.subscription_plan_name || '-' }}</span>
                  </td>
                  <td>
                    <span :class="['status-badge', getStatusClass(shop.subscription_status)]">
                      {{ getStatusText(shop.subscription_status) }}
                    </span>
                    <div v-if="shop.subscription_expires_at" class="days-remaining"
                      :class="getDaysRemainingClass(shop)">
                      {{ getDaysRemaining(shop) }}
                    </div>
                  </td>
                  <td>
                    <div class="expiry-date">
                      {{ shop.subscription_expires_at ? formatDate(shop.subscription_expires_at) : '-' }}
                    </div>
                    <div v-if="shop.subscription_expires_at" class="expiry-time">
                      {{ formatTime(shop.subscription_expires_at) }}
                    </div>
                  </td>
                  <td>
                    <div class="created-date">
                      {{ formatDate(shop.created_at) }}
                    </div>
                    <div class="created-time">
                      {{ formatTime(shop.created_at) }}
                    </div>
                  </td>
                  <td>
                    <span :class="['status-badge', shop.is_active ? 'status-active' : 'status-cancelled']">
                      {{ shop.is_active ? $t('common.yes') : $t('common.no') }}
                    </span>
                  </td>
                  <td>
                    <div class="actions">
                      <button @click="openShopDetails(shop)" class="action-btn btn-icon"
                        :title="$t('platformAdmin.shops.details')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="16" x2="12" y2="12"></line>
                          <line x1="12" y1="8" x2="12.01" y2="8"></line>
                        </svg>
                      </button>
                      <button @click="openPasswordModal('activate', shop)"
                        :class="['action-btn', shop.is_active ? 'btn-danger' : 'btn-success']"
                        :title="shop.is_active ? $t('platformAdmin.shops.deactivate') : $t('platformAdmin.shops.activate')">
                        {{ shop.is_active ? 'Faolsizlantirish' : $t('platformAdmin.shops.activate') }}
                      </button>
                      <button @click="openSubscriptionModal(shop)" class="action-btn btn-primary"
                        :title="$t('platformAdmin.shops.subscriptionManagement')">
                        {{ $t('platformAdmin.shops.subscription') }}
                      </button>
                      <button @click="openPasswordModal('delete', shop)" class="action-btn btn-danger icon-only"
                        title="Удалить магазин">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2">
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                          </path>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty State -->
            <div v-if="displayedShops.length === 0" class="empty-state">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z">
                </path>
              </svg>
              <p>{{ $t('platformAdmin.shops.notFound') }}</p>
              <p class="empty-subtitle"></p>
            </div>
          </div>

          <!-- Mobile Cards View -->
          <div class="mobile-shops-list">
            <div v-for="shop in paginatedShops" :key="shop.id" class="shop-mobile-card">
              <!-- Shop Header -->
              <div class="mobile-card-header">
                <div class="shop-info-mobile">
                  <img v-if="shop.logo_url" :src="shop.logo_url" :alt="shop.name" class="shop-logo-mobile" />
                  <div class="shop-logo-placeholder-mobile" v-else>{{ shop.name.charAt(0).toUpperCase() }}</div>
                  <div class="shop-details-mobile">
                    <h3 class="shop-name-mobile">{{ shop.name }}</h3>
                    <code class="shop-slug-mobile">{{ shop.slug }}</code>
                  </div>
                </div>
                <span :class="['status-badge-mobile', getStatusClass(shop.subscription_status)]">
                  {{ getStatusText(shop.subscription_status) }}
                </span>
              </div>

              <!-- Shop Info Grid -->
              <div class="mobile-card-info">
                <div class="info-row">
                  <span class="info-label">ID:</span>
                  <span class="info-value">{{ shop.id }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">{{ $t('platformAdmin.shops.table.owner') }}:</span>
                  <span class="info-value">{{ shop.owner_name || `ID: ${shop.owner_id}` }}</span>
                </div>
                <div class="info-row" v-if="shop.subscription_plan_name">
                  <span class="info-label">{{ $t('platformAdmin.shops.table.plan') }}:</span>
                  <span class="info-value">{{ shop.subscription_plan_name }}</span>
                </div>
                <div class="info-row" v-if="shop.subscription_expires_at">
                  <span class="info-label">{{ $t('platformAdmin.shops.table.expires') }}:</span>
                  <span class="info-value">
                    {{ formatDate(shop.subscription_expires_at) }}
                    <span :class="['days-badge-mobile', getDaysRemainingClass(shop)]">
                      {{ getDaysRemaining(shop) }}
                    </span>
                  </span>
                </div>
                <div class="info-row">
                  <span class="info-label">{{ $t('platformAdmin.shops.table.created') }}:</span>
                  <span class="info-value">{{ formatDate(shop.created_at) }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">{{ $t('platformAdmin.shops.table.isActive') }}:</span>
                  <span :class="['status-badge-small', shop.is_active ? 'status-active' : 'status-cancelled']">
                    {{ shop.is_active ? $t('common.yes') : $t('common.no') }}
                  </span>
                </div>
              </div>

              <!-- Actions -->
              <div class="mobile-card-actions">
                <button @click="openShopDetails(shop)" class="mobile-action-btn btn-details">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                  </svg>
                  {{ $t('platformAdmin.shops.details') }}
                </button>
                <button @click="toggleActive(shop)"
                  :class="['mobile-action-btn', shop.is_active ? 'btn-danger' : 'btn-success']">
                  {{ shop.is_active ? $t('platformAdmin.shops.deactivate') : $t('platformAdmin.shops.activate') }}
                </button>
                <button @click="openSubscriptionModal(shop)" class="mobile-action-btn btn-primary">
                  {{ $t('platformAdmin.shops.subscription') }}
                </button>
              </div>
            </div>

            <!-- Empty State for Mobile -->
            <div v-if="displayedShops.length === 0" class="empty-state-mobile">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z">
                </path>
              </svg>
              <p>{{ $t('platformAdmin.shops.notFound') }}</p>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination">
            <button @click="currentPage = 1" :disabled="currentPage === 1" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="11 17 6 12 11 7"></polyline>
                <polyline points="18 17 13 12 18 7"></polyline>
              </svg>
            </button>
            <button @click="currentPage--" :disabled="currentPage === 1" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>

            <div class="pagination-info">
              {{ $t('common.page') }} {{ currentPage }} {{ $t('common.of') }} {{ totalPages }}
            </div>

            <button @click="currentPage++" :disabled="currentPage === totalPages" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
            <button @click="currentPage = totalPages" :disabled="currentPage === totalPages" class="pagination-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 17 18 12 13 7"></polyline>
                <polyline points="6 17 11 12 6 7"></polyline>
              </svg>
            </button>
          </div>
        </div>

        <!-- Subscription Modal -->
        <div v-if="showModal && selectedShop" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ $t('platformAdmin.shops.subscriptionManagement') }}</h2>
              <button @click="closeModal" class="modal-close">×</button>
            </div>

            <div class="modal-shop-info">
              <h3>{{ selectedShop.name }}</h3>
              <p class="shop-slug-text">{{ selectedShop.slug }}</p>
              <div class="owner-info">
                <span class="owner-label">{{ $t('platformAdmin.shops.table.owner') }}:</span>
                <span class="owner-value">{{ selectedShop.owner_name || `ID: ${selectedShop.owner_id}` }}</span>
                <span v-if="selectedShop.owner_phone" class="owner-phone">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path
                      d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                    </path>
                  </svg>
                  {{ selectedShop.owner_phone }}
                </span>
              </div>
            </div>

            <div class="current-status-section">
              <label class="status-label">{{ $t('platformAdmin.shops.currentPlan') }}:</label>
              <div class="current-plan-name">{{ selectedShop.subscription_plan_name ||
                $t('platformAdmin.plans.card.inactive') }}</div>

              <label class="status-label">{{ $t('platformAdmin.shops.currentStatus') }}:</label>
              <span :class="['current-status-badge', getStatusClass(selectedShop.subscription_status)]">
                {{ getStatusText(selectedShop.subscription_status) }}
              </span>
              <div v-if="selectedShop.subscription_expires_at" class="expires-info">
                {{ $t('platformAdmin.shops.table.expires') }}: {{ formatDate(selectedShop.subscription_expires_at) }}
                <span class="days-warning" :class="getDaysRemainingClass(selectedShop)">
                  ({{ getDaysRemaining(selectedShop) }})
                </span>
              </div>
            </div>

            <!-- История подписок -->
            <div class="subscription-history-section" v-if="subscriptionHistory.length > 0">
              <h3>{{ $t('platformAdmin.shops.history') }}</h3>
              <div class="history-list">
                <div v-for="req in subscriptionHistory" :key="req.id" class="history-item">
                  <div class="history-main">
                    <span class="history-plan">{{ req.plan_name }}</span>
                    <span :class="['history-status', `status-${req.status}`]">{{ getRequestStatusText(req.status)
                      }}</span>
                  </div>
                  <div class="history-meta">
                    <span>{{ formatDate(req.requested_at) }}</span>
                    <span>{{ req.duration_months }} {{ $t('platformAdmin.plans.period.days').substring(0, 3) }}.</span>
                  </div>
                </div>
              </div>
            </div>

            <form @submit.prevent="updateSubscription" class="modal-form">
              <div class="form-group">
                <label>{{ $t('platformAdmin.shops.table.status') }}</label>
                <select v-model="subscriptionForm.status" class="form-input">
                  <option value="trial">{{ $t('platformAdmin.shops.trial') }}</option>
                  <option value="active">{{ $t('platformAdmin.shops.active') }}</option>
                  <option value="expired">{{ $t('platformAdmin.shops.expired') }}</option>
                  <option value="cancelled">{{ $t('platformAdmin.shops.cancelled') }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>{{ $t('platformAdmin.shops.table.expires') }}</label>
                <input v-model="subscriptionForm.expires_at" type="datetime-local" class="form-input" />
                <div class="quick-actions">
                  <button type="button" @click="setExpiry(1)" class="quick-btn">{{
                    $t('platformAdmin.shops.quickActions.month1') }}</button>
                  <button type="button" @click="setExpiry(3)" class="quick-btn">{{
                    $t('platformAdmin.shops.quickActions.month3') }}</button>
                  <button type="button" @click="setExpiry(6)" class="quick-btn">{{
                    $t('platformAdmin.shops.quickActions.month6') }}</button>
                  <button type="button" @click="setExpiry(12)" class="quick-btn">{{
                    $t('platformAdmin.shops.quickActions.year1') }}</button>
                </div>
              </div>
              <div class="modal-actions">
                <button type="button" @click="closeModal" class="btn-secondary" :disabled="isUpdating">{{
                  $t('common.cancel') }}</button>
                <button type="submit" class="btn-primary" :disabled="isUpdating" :class="{ 'opacity-50': isUpdating }">
                  {{ isUpdating ? $t('common.saving') : $t('platformAdmin.plans.card.activate') }}
                </button>
              </div>

            </form>
          </div>
        </div>

        <!-- Password Confirmation Modal -->
        <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
          <div class="modal-content small-modal" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ passwordModalTitle }}</h2>
              <button @click="closePasswordModal" class="modal-close">×</button>
            </div>
            <div class="modal-body">
              <p class="mb-4">{{ passwordModalMessage }}</p>
              <form @submit.prevent="confirmPasswordAction">
                <div class="form-group">
                  <label>{{ $t('auth.password') }}</label>
                  <input v-model="passwordInput" type="password" class="form-input" required
                    placeholder="Введите пароль администратора" autofocus />
                </div>
                <div class="modal-actions">
                  <button type="button" @click="closePasswordModal" class="btn-secondary">{{ $t('common.cancel')
                    }}</button>
                  <button type="submit" class="btn-primary" :class="{ 'btn-danger': pendingAction?.type === 'delete' }"
                    :disabled="isConfirming">
                    {{ isConfirming ? $t('common.processing') : $t('common.confirm') }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t } = useI18n()
definePageMeta({
  middleware: 'platform-admin'
})

const route = useRoute()
const router = useRouter()
const { token, logout } = useAuth()
const toast = useToast()

const sidebarOpen = ref(false)

const handleLogout = () => {
  logout()
  useToast().success(t('alerts.shop.loggedOut'))
}

const currentRoute = computed(() => {
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

const { data: shops, pending, refresh, error } = await useFetch('http://localhost:8000/platform/shops', {
  server: false,
  lazy: true,
  watch: [token],
  headers: computed(() => ({
    'Authorization': token.value ? `Bearer ${token.value}` : ''
  }))
})

// Filters and Search
const searchQuery = ref('')
const filterStatus = ref('')
const filterActive = ref('')

// Sorting
const sortField = ref('id')
const sortOrder = ref('asc')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 20

// Modal
const showModal = ref(false)
const selectedShop = ref(null)
const subscriptionHistory = ref([])
const subscriptionForm = reactive({
  status: 'trial',
  expires_at: ''
})
const isUpdating = ref(false)

// Password Modal State
const showPasswordModal = ref(false)
const passwordInput = ref('')
const pendingAction = ref(null)
const isConfirming = ref(false)

const passwordModalTitle = computed(() => {
  if (pendingAction.value?.type === 'delete') return 'Удаление магазина'
  return pendingAction.value?.shop.is_active ? 'Подтвердите деактивацию' : 'Подтвердите активацию'
})

const passwordModalMessage = computed(() => {
  if (pendingAction.value?.type === 'delete') return `Вы уверены, что хотите НАВСЕГДА удалить магазин "${pendingAction.value.shop.name}"? Это действие необратимо и удалит все товары и данные магазина.`
  return `Вы уверены, что хотите ${pendingAction.value?.shop.is_active ? 'деактивировать' : 'активировать'} магазин "${pendingAction.value?.shop.name}"?`
})

const openPasswordModal = (type, shop) => {
  pendingAction.value = { type, shop }
  passwordInput.value = ''
  showPasswordModal.value = true
}

const closePasswordModal = () => {
  showPasswordModal.value = false
  pendingAction.value = null
  passwordInput.value = ''
}

const confirmPasswordAction = async () => {
  if (!passwordInput.value) return
  isConfirming.value = true

  try {
    const { type, shop } = pendingAction.value

    if (type === 'activate') {
      await $fetch(`http://localhost:8000/platform/admin/shops/${shop.id}/activate`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token.value}` },
        body: { is_active: !shop.is_active, password: passwordInput.value }
      })
      toast.success(shop.is_active ? 'Магазин деактивирован' : 'Магазин активирован')
    } else if (type === 'delete') {
      await $fetch(`http://localhost:8000/platform/admin/shops/${shop.id}/delete`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token.value}` },
        body: { password: passwordInput.value }
      })
      toast.success('Магазин удален')
    }

    refresh()
    closePasswordModal()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка / Неверный пароль')
  } finally {
    isConfirming.value = false
  }
}


// Computed stats
const activeShopsCount = computed(() => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.is_active).length
})

const trialShopsCount = computed(() => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.subscription_status === 'trial').length
})

const expiredShopsCount = computed(() => {
  if (!shops.value) return 0
  return shops.value.filter(s => s.subscription_status === 'expired').length
})

// Filtered and sorted shops
const displayedShops = computed(() => {
  if (!shops.value) return []

  let filtered = [...shops.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(shop =>
      shop.name?.toLowerCase().includes(query) ||
      shop.slug?.toLowerCase().includes(query) ||
      shop.owner_name?.toLowerCase().includes(query) ||
      shop.owner_phone?.includes(query)
    )
  }

  // Status filter
  if (filterStatus.value) {
    filtered = filtered.filter(shop => shop.subscription_status === filterStatus.value)
  }

  // Active filter
  if (filterActive.value !== '') {
    const isActive = filterActive.value === 'true'
    filtered = filtered.filter(shop => shop.is_active === isActive)
  }

  // Sorting
  filtered.sort((a, b) => {
    let aVal, bVal

    switch (sortField.value) {
      case 'id':
        aVal = a.id
        bVal = b.id
        break
      case 'name':
        aVal = a.name?.toLowerCase() || ''
        bVal = b.name?.toLowerCase() || ''
        break
      case 'owner':
        aVal = a.owner_name?.toLowerCase() || ''
        bVal = b.owner_name?.toLowerCase() || ''
        break
      case 'subscription_status':
        aVal = a.subscription_status
        bVal = b.subscription_status
        break
      case 'expires_at':
        aVal = a.subscription_expires_at ? new Date(a.subscription_expires_at).getTime() : 0
        bVal = b.subscription_expires_at ? new Date(b.subscription_expires_at).getTime() : 0
        break
      case 'created_at':
        aVal = a.created_at ? new Date(a.created_at).getTime() : 0
        bVal = b.created_at ? new Date(b.created_at).getTime() : 0
        break
      case 'is_active':
        aVal = a.is_active ? 1 : 0
        bVal = b.is_active ? 1 : 0
        break
      default:
        return 0
    }

    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })

  return filtered
})

// Paginated shops
const totalPages = computed(() => Math.ceil(displayedShops.value.length / itemsPerPage))

const paginatedShops = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return displayedShops.value.slice(start, end)
})

// Watch for filter changes and reset page
watch([searchQuery, filterStatus, filterActive], () => {
  currentPage.value = 1
})

// Functions
const clearFilters = () => {
  searchQuery.value = ''
  filterStatus.value = ''
  filterActive.value = ''
}

const sortBy = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
}

const getStatusClass = (status) => {
  const statusMap = {
    'trial': 'status-trial',
    'active': 'status-active',
    'expired': 'status-expired',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || 'status-trial'
}

const getStatusText = (status) => {
  const statusMap = {
    'trial': t('platformAdmin.shops.trial'),
    'active': t('platformAdmin.shops.active'),
    'expired': t('platformAdmin.shops.expired'),
    'cancelled': t('platformAdmin.shops.cancelled')
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

const getDaysRemaining = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return null
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  const days = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))

  if (days < 0) return t('platformAdmin.shops.status.expired') // Or just 'expired' logic
  if (days === 0) return t('platformAdmin.shops.expiresToday')
  if (days === 1) return t('platformAdmin.shops.expiresTomorrow')
  return t('platformAdmin.shops.daysLeft', { days })
}

const getDaysRemainingClass = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return ''
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  const days = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))

  if (days <= 0) return 'days-expired'
  if (days <= 3) return 'days-critical'
  if (days <= 7) return 'days-warning'
  return 'days-normal'
}

const isExpiringSoon = (shop) => {
  if (!shop.subscription_expires_at || shop.subscription_status !== 'active') return false
  const now = new Date()
  const expiresAt = new Date(shop.subscription_expires_at)
  const days = Math.ceil((expiresAt - now) / (1000 * 60 * 60 * 24))
  return days > 0 && days <= 7
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const openShopDetails = (shop) => {
  router.push(`/platform/admin/shops/${shop.id}`)
}

const exportData = () => {
  const csv = [
    ['ID', 'Название', 'Slug', 'Владелец', 'Телефон', 'Статус подписки', 'Истекает', 'Активен', 'Дата создания'],
    ...displayedShops.value.map(shop => [
      shop.id,
      shop.name,
      shop.slug,
      shop.owner_name || '',
      shop.owner_phone || '',
      getStatusText(shop.subscription_status),
      shop.subscription_expires_at ? formatDate(shop.subscription_expires_at) : '',
      shop.is_active ? 'Да' : 'Нет',
      formatDate(shop.created_at)
    ])
  ].map(row => row.join(',')).join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `shops-${new Date().toISOString().split('T')[0]}.csv`
  link.click()
  toast.success(t('alerts.shop.exported'))
}

const getRequestStatusText = (status) => {
  const map = {
    pending: 'Ожидает',
    approved: 'Одобрен',
    rejected: 'Отклонен'
  }
  return map[status] || status
}

const openSubscriptionModal = async (shop) => {
  selectedShop.value = shop
  subscriptionForm.status = shop.subscription_status
  subscriptionForm.expires_at = shop.subscription_expires_at ? new Date(shop.subscription_expires_at).toISOString().slice(0, 16) : ''

  // Fetch history
  try {
    const { data } = await useFetch(`http://localhost:8000/platform/admin/subscription-requests`, {
      query: { shop_id: shop.id },
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })
    subscriptionHistory.value = data.value || []
  } catch (e) {
    console.error('Failed to fetch subscription history', e)
    subscriptionHistory.value = []
  }

  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedShop.value = null
}

const setExpiry = (months) => {
  const date = new Date()
  date.setMonth(date.getMonth() + months)
  subscriptionForm.expires_at = date.toISOString().slice(0, 16)
  if (subscriptionForm.status !== 'active') {
    subscriptionForm.status = 'active'
  }
}

const updateSubscription = async () => {
  if (!subscriptionForm.expires_at && subscriptionForm.status === 'active') {
    toast.warning(t('alerts.shop.expiryRequired'))
    return
  }

  if (isUpdating.value) return // Prevent duplicate submissions

  isUpdating.value = true
  try {
    const body = {
      subscription_status: subscriptionForm.status
    }
    if (subscriptionForm.expires_at) {
      body.expires_at = new Date(subscriptionForm.expires_at).toISOString()
    }

    await $fetch(`http://localhost:8000/platform/admin/shops/${selectedShop.value.id}/subscription`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: body
    })

    const planName = subscriptionForm.status === 'active' ? t('alerts.shop.subscriptionActivated') : t('alerts.shop.subscriptionUpdated')
    toast.success(planName)
    closeModal()
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Ошибка при обновлении подписки')
  } finally {
    isUpdating.value = false
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

@media (max-width: 640px) {
  .admin-title {
    font-size: 1.25rem !important;
    line-height: 1.2 !important;
  }

  .admin-header {
    padding: 20px !important;
  }

  .admin-content {
    padding: 16px !important;
  }
}

.admin-subtitle {
  font-size: 1rem;
  opacity: 0.85;
  font-weight: 400;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-btn svg.spinning {
  animation: spin 1s linear infinite;
}

.admin-content {
  padding: 32px;
}

@media (max-width: 640px) {
  .admin-content {
    padding: 16px !important;
  }
}

/* Statistics Overview */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 1280px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 640px) {
  .stats-overview {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #E5E7EB;
  transition: all 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
  flex-shrink: 0;
}

.stat-icon.active {
  background: #D1FAE5;
  color: #065F46;
}

.stat-icon.trial {
  background: #FEF3C7;
  color: #92400E;
}

.stat-icon.expired {
  background: #FEE2E2;
  color: #991B1B;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 900;
  color: #111;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

/* Filters Section */
.filters-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #E5E7EB;
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-group {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: 0;
  }

  .filter-select,
  .clear-filters-btn {
    width: 100%;
  }
}

.search-box {
  flex: 1;
  min-width: 300px;
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 12px 16px;
}

.search-box svg {
  color: #6B7280;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.875rem;
  color: #111;
  outline: none;
}

.search-input::placeholder {
  color: #9CA3AF;
}

.filters-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 10px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  background: white;
  font-size: 0.875rem;
  font-weight: 500;
  color: #111;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
}

.filter-select:hover {
  border-color: #D1D5DB;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-filters-btn:hover {
  background: #E5E7EB;
  color: #111;
}

/* Table Container */
.table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #E5E7EB;
}

.table-header {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #F9FAFB;
}

.table-info {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.table-actions {
  display: flex;
  gap: 12px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover {
  background: #F9FAFB;
  border-color: #D1D5DB;
}

.shops-table-wrapper {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.shops-table {
  width: 100%;
  min-width: 900px;
  border-collapse: collapse;
}

.shops-table thead {
  background: #F9FAFB;
}

.shops-table th {
  padding: 16px;
  text-align: left;
  font-weight: 700;
  font-size: 0.8125rem;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.th-content svg {
  transition: transform 0.2s;
}

.th-content svg.reverse {
  transform: rotate(180deg);
}

.shops-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.shops-table th.sortable:hover {
  background: #F3F4F6;
}

.shops-table td {
  padding: 16px;
  border-top: 1px solid #E5E7EB;
  font-size: 0.875rem;
}

.shops-table tbody tr {
  transition: background 0.2s;
}

.shops-table tbody tr:hover {
  background: #F9FAFB;
}

.shops-table tbody tr.expiring-soon {
  background: #FEF3C7;
}

.shop-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shop-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
}

.shop-logo-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: white;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.shop-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.shop-name {
  font-weight: 600;
  color: #111;
}

.shop-description {
  font-size: 0.75rem;
  color: #6B7280;
}

.shop-slug {
  background: #F3F4F6;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-family: 'Monaco', 'Courier New', monospace;
  color: #111;
  display: inline-block;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.owner-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.owner-name {
  font-weight: 600;
  color: #111;
}

.owner-phone {
  font-size: 0.75rem;
  color: #6B7280;
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.days-remaining {
  margin-top: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.days-normal {
  color: #6B7280;
}

.days-warning {
  color: #F59E0B;
}

.days-critical {
  color: #EF4444;
  font-weight: 700;
}

.days-expired {
  color: #991B1B;
  font-weight: 700;
}

.expiry-date,
.created-date {
  font-weight: 500;
  color: #111;
}

.expiry-time,
.created-time {
  font-size: 0.75rem;
  color: #6B7280;
  margin-top: 2px;
}

.actions {
  display: flex;
  gap: 6px;
  align-items: center;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-icon {
  background: #F3F4F6;
  color: #111;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: #E5E7EB;
}

.btn-primary {
  background: #111;
  color: white;
  padding: 10px;
  border-radius: 14px;
}

.btn-primary:hover {
  background: #000;
}

.btn-danger {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-danger:hover {
  background: #FECACA;
}

.btn-success {
  background: #D1FAE5;
  color: #065F46;
}

.btn-success:hover {
  background: #A7F3D0;
}

/* Empty State */
.empty-state {
  padding: 80px 20px;
  text-align: center;
  color: #6B7280;
}

.empty-state svg {
  margin-bottom: 16px;
  color: #9CA3AF;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 600;
  margin: 8px 0;
}

.empty-subtitle {
  font-size: 0.875rem;
  font-weight: 400;
  color: #9CA3AF;
}

/* Pagination */
.pagination {
  padding: 20px 24px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  background: #F9FAFB;
}

.pagination-btn {
  padding: 8px 12px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
}

.pagination-btn:hover:not(:disabled) {
  background: #F3F4F6;
  border-color: #D1D5DB;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
  padding: 0 16px;
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 600px;
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

.modal-shop-info {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.modal-shop-info h3 {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0 0 8px 0;
  color: #111;
}

.shop-slug-text {
  color: #6B7280;
  font-size: 0.875rem;
  margin: 0 0 12px 0;
}

.modal-shop-info .owner-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.owner-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.owner-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
}

.modal-shop-info .owner-phone {
  font-size: 0.875rem;
  color: #6B7280;
  display: flex;
  align-items: center;
  gap: 6px;
}

.current-status-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #F9FAFB;
  border-radius: 12px;
}

.status-label {
  display: block;
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 8px;
  font-weight: 500;
}

.current-status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.current-status-badge.status-trial {
  background: #FEF3C7;
  color: #92400E;
}

.current-status-badge.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.current-status-badge.status-expired {
  background: #FEE2E2;
  color: #991B1B;
}

.current-status-badge.status-cancelled {
  background: #F3F4F6;
  color: #4B5563;
}

.expires-info {
  margin-top: 8px;
  font-size: 0.875rem;
  color: #6B7280;
}

.days-warning {
  font-weight: 600;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.quick-btn {
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

.quick-btn:hover {
  background: #111;
  color: white;
  border-color: #111;
}

.form-group label {
  font-weight: 600;
  font-size: 0.875rem;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #111;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
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

.opacity-50 {
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

  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: auto;
  }
}

/* Modal Mobile Responsive */
@media (max-width: 640px) {
  .modal-content {
    width: calc(100% - 24px);
    padding: 20px 16px;
    max-height: 95vh;
    border-radius: 16px;
  }

  .modal-header {
    margin-bottom: 16px;
    padding-bottom: 16px;
  }

  .modal-title {
    font-size: 1.25rem;
  }

  .modal-shop-info {
    padding: 16px;
    margin-bottom: 16px;
  }

  .modal-shop-info h3 {
    font-size: 1.125rem;
  }

  .current-status-section {
    padding: 12px;
    margin-bottom: 16px;
  }

  .subscription-history-section {
    padding: 12px;
    margin-bottom: 16px;
  }

  .modal-form {
    gap: 16px;
  }

  .quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .quick-btn {
    width: 100%;
    text-align: center;
  }

  .modal-actions {
    flex-direction: column-reverse;
    gap: 8px;
  }

  .modal-actions button {
    width: 100%;
  }
}


@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }

  .shops-table-wrapper {
    overflow-x: scroll;
  }

  .shops-table {
    min-width: 1200px;
  }
}


.plan-name-cell {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 14px;
}

/* Subscription History */
.subscription-history-section {
  margin-top: 20px;
  border-top: 1px solid var(--border-color);
  padding-top: 15px;
}

.subscription-history-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-primary);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 150px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: var(--bg-secondary);
  border-radius: 6px;
  font-size: 14px;
}

.history-main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.history-plan {
  font-weight: 500;
  color: var(--text-primary);
}

.history-status {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: uppercase;
}

.status-pending {
  background-color: #fff7ed;
  color: #c2410c;
}

.status-approved {
  background-color: #f0fdf4;
  color: #15803d;
}

.status-rejected {
  background-color: #fef2f2;
  color: #b91c1c;
}

.history-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 12px;
  color: var(--text-secondary);
}

/* Mobile Cards Styles */
.mobile-shops-list {
  display: none;
}

.shop-mobile-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #E5E7EB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.mobile-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.shop-info-mobile {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.shop-logo-mobile {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.shop-logo-placeholder-mobile {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  color: #6B7280;
  flex-shrink: 0;
}

.shop-details-mobile {
  min-width: 0;
  flex: 1;
}

.shop-name-mobile {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shop-slug-mobile {
  font-size: 12px;
  color: #6B7280;
  background: #F3F4F6;
  padding: 2px 6px;
  border-radius: 4px;
}

.status-badge-mobile {
  flex-shrink: 0;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.mobile-card-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  padding: 12px 0;
  border-top: 1px solid #F3F4F6;
  border-bottom: 1px solid #F3F4F6;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.info-label {
  color: #6B7280;
  font-weight: 500;
}

.info-value {
  color: #111;
  font-weight: 600;
  text-align: right;
  display: flex;
  align-items: center;
  gap: 6px;
}

.days-badge-mobile {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.days-badge-mobile.days-critical {
  background: #FEE2E2;
  color: #991B1B;
}

.days-badge-mobile.days-warning {
  background: #FEF3C7;
  color: #92400E;
}

.days-badge-mobile.days-normal {
  background: #D1FAE5;
  color: #059669;
}

.status-badge-small {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.mobile-card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.mobile-action-btn {
  flex: 1;
  min-width: fit-content;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.mobile-action-btn.btn-details {
  background: #F3F4F6;
  color: #111;
}

.mobile-action-btn.btn-details:active {
  background: #E5E7EB;
}

.mobile-action-btn.btn-danger {
  background: #FEE2E2;
  color: #991B1B;
}

.mobile-action-btn.btn-danger:active {
  background: #FEF2F2;
}

.mobile-action-btn.btn-success {
  background: #D1FAE5;
  color: #059669;
}

.mobile-action-btn.btn-success:active {
  background: #ECFDF5;
}

.mobile-action-btn.btn-primary {
  background: #111;
  color: white;
}

.mobile-action-btn.btn-primary:active {
  background: #000;
}

.empty-state-mobile {
  text-align: center;
  padding: 60px 20px;
  color: #6B7280;
}

.empty-state-mobile svg {
  margin: 0 auto 16px;
  opacity: 0.3;
}

.empty-state-mobile p {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

/* Enhanced Mobile Responsive */
@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
    /* padding-left: 12px; */
    /* padding-right: 12px; */
  }

  .admin-header {
    padding: 16px 12px;
  }

  .admin-content {
    padding: 0;
  }

  .admin-title {
    font-size: 1.5rem;
  }

  .stats-overview {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .stat-card {
    padding: 16px;
  }

  .filters-section {
    padding: 12px;
    gap: 12px;
  }

  .table-header {
    padding: 12px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .shops-table-wrapper {
    display: none;
  }

  .mobile-shops-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 12px;
  }

  .pagination {
    padding: 12px;
  }
}
</style>

<style scoped>
.shop-slug-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #2563EB;
  text-decoration: none;
  transition: opacity 0.2s;
}
.shop-slug-link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.small-modal {
  max-width: 400px !important;
}

.icon-only {
  padding: 8px !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.mb-4 {
  margin-bottom: 24px;
}
</style>
