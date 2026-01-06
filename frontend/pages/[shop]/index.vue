<template>
  <div class="shop-page">
    <AppHeader />

    <main class="container py-8">

      <div v-if="shopError || (shop && (!shop.is_active || shop.subscription_status === 'expired'))"
        class="unavailable-state py-24 text-center">
        <div class="mb-6 inline-flex p-4 rounded-full bg-red-50 text-red-500">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        </div>
        <h2 class="text-3xl font-black text-gray-900 mb-4">{{ $t('store.unavailableTitle') || 'Shop Temporarily
          Unavailable' }}</h2>
        <p class="text-gray-500 max-w-md mx-auto">{{ $t('store.unavailableDesc') || 'This shop is currently inactive or
          its subscription has expired.Please check back later.' }}</p>
        <NuxtLink to="/"
          class="mt-8 inline-block px-8 py-3 bg-black text-white rounded-full font-bold hover:bg-gray-800 transition-all">
          {{ $t('common.backToHome') || 'Explore Other Shops' }}
        </NuxtLink>
      </div>

      <template v-else>
        <div v-if="banner && Array.isArray(banner) && banner.length > 0" class="hero-section mb-8">
          <ClientOnly>
            <swiper-container v-if="banner.length > 1" :slides-per-view="1" :speed="500" :loop="true"
              :autoplay="{ delay: 5000 }" pagination="true" class="hero-swiper">
              <swiper-slide v-for="slide in banner" :key="slide.id">
                <div class="hero-card">
                  <div class="hero-content">
                    <div v-if="slide.badge_text" class="badge">{{ slide.badge_text }}</div>
                    <h1 class="hero-title"
                      v-html="(getLocalized(slide, 'title') ? getLocalized(slide, 'title').replace(/\\n/g, '<br/>') : '')">
                    </h1>
                    <p class="hero-price">{{ getLocalized(slide, 'subtitle') }}</p>
                    <NuxtLink :to="slide.button_link || `/${shopSlug}/products`" class="hero-btn">{{ getLocalized(slide,
                      'button_text') }}
                    </NuxtLink>
                  </div>
                  <div class="hero-image">
                    <img :src="slide.image_url" alt="Banner" />
                  </div>
                </div>
              </swiper-slide>
            </swiper-container>

            <!-- Single Banner Fallback -->
            <div v-else-if="banner[0]" class="hero-card">
              <div class="hero-content">
                <div v-if="banner[0].badge_text" class="badge">{{ banner[0].badge_text }}</div>
                <h1 class="hero-title"
                  v-html="(getLocalized(banner[0], 'title') ? getLocalized(banner[0], 'title').replace(/\\n/g, '<br/>') : '')">
                </h1>
                <p class="hero-price">{{ getLocalized(banner[0], 'subtitle') }}</p>
                <NuxtLink :to="banner[0].button_link || `/${shopSlug}/products`" class="hero-btn">{{
                  getLocalized(banner[0], 'button_text')
                }}</NuxtLink>
              </div>
              <div class="hero-image">
                <img :src="banner[0].image_url" alt="Banner" />
              </div>
            </div>
          </ClientOnly>
        </div>

        <!-- Brand Filters -->
        <section class="mb-8">
          <div class="section-header">
            <h2 class="section-title">{{ $t('store.brands') }}</h2>
            <NuxtLink :to="`/${shopSlug}/products`" class="view-all-btn">
              {{ $t('store.viewAll') }}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </NuxtLink>
          </div>
          <div class="brand-grid">
            <NuxtLink v-for="brand in displayedBrands" :key="brand.id" :to="`/${shopSlug}/products?brand=${brand.name}`"
              class="brand-card">
              <div class="brand-logo-wrapper">
                <img :src="brand.logo_url" :alt="brand.name" class="brand-logo-img" />
              </div>
              <span class="brand-name-text">{{ brand.name }}</span>
            </NuxtLink>
          </div>
        </section>

        <!-- Featured Products -->
        <section class="mb-8">
          <div class="section-header">
            <h2 class="section-title">{{ $t('store.recommended') }}</h2>
            <NuxtLink :to="`/${shopSlug}/products`" class="view-all-btn">
              {{ $t('store.viewAll') }}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </NuxtLink>
          </div>
          <div v-if="pending" class="text-center py-12 text-gray-400">
            <div class="loading-spinner"></div>
            <p class="mt-4">{{ $t('store.loadingProducts') }}</p>
          </div>
          <div v-else class="products-grid">
            <ProductCard v-for="product in featuredProducts" :key="product.id" :product="product"
              :shop-slug="shopSlug" />
          </div>

          <!-- View All Products Button -->
          <div class="view-all-section">
            <NuxtLink :to="`/${shopSlug}/products`" class="view-all-products-btn">
              <span>{{ $t('store.viewAllProducts') }}</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </NuxtLink>
          </div>
        </section>
      </template>
    </main>

    <!-- Shop Footer -->
    <footer v-if="shop" class="shop-footer">
      <div class="footer-container">
        <div class="footer-content">
          <!-- Shop Info -->
          <div class="footer-section">
            <div class="footer-brand">
              <img v-if="shop.logo_url" :src="shop.logo_url" :alt="shop.name" class="footer-logo" />
              <h3 class="footer-title">{{ shop.name }}</h3>
            </div>
            <!-- Removed description to avoid duplicate phone number issue -->
            <div v-if="shop.address" class="footer-contact-item address">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <span>{{ shop.address }}</span>
            </div>
          </div>

          <!-- Contacts -->
          <div class="footer-section">
            <h4 class="footer-subtitle">{{ $t('footer.contacts') }}</h4>
            <div v-if="shop.phone" class="footer-contact-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                </path>
              </svg>
              <a :href="`tel:${shop.phone}`" class="contact-link">{{ shop.phone }}</a>
            </div>
            <div v-if="shop.email" class="footer-contact-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <a :href="`mailto:${shop.email}`" class="contact-link">{{ shop.email }}</a>
            </div>
          </div>

          <!-- Social Media -->
          <div class="footer-section">
            <h4 class="footer-subtitle">{{ $t('footer.followUs') }}</h4>
            <div class="social-links">
              <a v-if="shop.telegram" :href="shop.telegram" target="_blank" rel="noopener noreferrer"
                class="social-link telegram">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.169 1.858-.896 6.728-.896 6.728s-.537 3.593-2.351 4.131c-1.815.538-3.785-1.15-4.371-1.705-.293-.278-5.185-3.266-5.185-3.266s-2.023-1.387 1.421-2.738c3.444-1.351 7.377-2.853 7.377-2.853s1.512-.956 2.895.538c1.383 1.494 2.109 3.266 2.109 3.266h.001z" />
                </svg>
                <span>Telegram</span>
              </a>
              <a v-if="shop.instagram" :href="shop.instagram" target="_blank" rel="noopener noreferrer"
                class="social-link instagram">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                  <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                </svg>
                <span>Instagram</span>
              </a>
              <a v-if="shop.facebook" :href="shop.facebook" target="_blank" rel="noopener noreferrer"
                class="social-link facebook">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
                </svg>
                <span>Facebook</span>
              </a>
              <a v-if="shop.whatsapp" :href="shop.whatsapp" target="_blank" rel="noopener noreferrer"
                class="social-link whatsapp">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                </svg>
                <span>WhatsApp</span>
              </a>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <p>&copy; {{ new Date().getFullYear() }} {{ shop.name }}. {{ $t('footer.rights') }}.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { register } from 'swiper/element/bundle'

register()

const { t, locale } = useI18n()
const route = useRoute()
const shopSlug = route.params.shop

const getLocalized = (obj, field) => {
  if (!obj) return ''
  return obj[`${field}_${locale.value}`] || obj[field]
}

// Fetch Shop Information
const { data: shop, error: shopError } = await useFetch(`${useRuntimeConfig().public.apiBase}/platform/shops/${shopSlug}`, {
  key: `shop-${shopSlug}`,
  onResponseError({ response }) {
    if (response.status === 403) {
      console.warn('[Storefront] Shop is inactive or expired')
    }
  }
})

// SEO
useHead({
  title: computed(() => shop.value?.name || 'Shop'),
})

// Fetch Banner
const { data: banner } = await useFetch(`${useRuntimeConfig().public.apiBase}/banner?shop_slug=${shopSlug}`, {
  key: `banner-${shopSlug}`
})

const { data: brands } = await useFetch(`${useRuntimeConfig().public.apiBase}/brands?shop_slug=${shopSlug}`, { server: false })
const { data: products, pending } = await useFetch(`${useRuntimeConfig().public.apiBase}/products?shop_slug=${shopSlug}`, {
  server: false
})

// Show only 4 featured products
const featuredProducts = computed(() => {
  if (!products.value) return []
  return products.value.slice(0, 4)
})

// Show only 6 brands
const displayedBrands = computed(() => {
  if (!brands.value) return []
  return brands.value.slice(0, 6)
})
</script>

<style scoped>
.shop-page {
  min-height: 100vh;
  background: #FAFAFA;
  /* Removed large padding-bottom to close the gap at the very bottom */
}

.shop-header {
  text-align: center;
  padding: 48px 20px;
  background: white;
  border-radius: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.shop-title-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.shop-main-logo {
  height: 100px;
  width: auto;
  max-width: 100%;
  object-fit: contain;
  background: white;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
}

.shop-name {
  font-size: 2.75rem;
  font-weight: 950;
  color: #111;
  margin: 0;
  letter-spacing: -1px;
}

.shop-description {
  font-size: 1.125rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.6;
  max-width: 600px;
}

.hero-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 32px;
  padding: 48px;
  color: white;
  position: relative;
  overflow: hidden;
  min-height: 400px;
  display: flex;
  align-items: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.hero-content {
  z-index: 2;
  max-width: 500px;
}

.badge {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  letter-spacing: 1px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 16px;
  letter-spacing: -1px;
}

.hero-price {
  font-size: 1.25rem;
  font-weight: 500;
  opacity: 0.9;
  margin-bottom: 32px;
}

.hero-btn {
  display: inline-block;
  background: white;
  color: #111;
  padding: 16px 40px;
  border-radius: 50px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
  text-decoration: none;
}

.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255, 255, 255, 0.3);
}

.hero-image {
  position: absolute;
  right: -50px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 50%;
  height: 120%;
  opacity: 0.3;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  letter-spacing: -0.5px;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
  text-decoration: none;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: #111;
  border-color: #111;
  color: white;
  transform: translateX(4px);
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

.brand-card {
  background: white;
  border: 2px solid #f0f0f0;
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #111;
}

.brand-card:hover {
  border-color: #111;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.brand-logo-wrapper {
  width: 80px;
  height: 80px;
  background: #f9f9f9;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.brand-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-name-text {
  font-weight: 700;
  font-size: 0.95rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.view-all-section {
  margin-top: 32px;
  text-align: center;
}

.view-all-products-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 18px 40px;
  background: #111;
  color: white;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.view-all-products-btn:hover {
  background: #000;
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .shop-header {
    padding: 24px 16px;
    border-radius: 16px;
  }

  .shop-name {
    font-size: 1.75rem;
  }

  .shop-description {
    font-size: 1rem;
  }

  .hero-card {
    padding: 32px 24px;
    min-height: 280px;
    border-radius: 24px;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .hero-price {
    font-size: 1rem;
    margin-bottom: 24px;
  }

  .hero-btn {
    padding: 14px 28px;
    font-size: 0.875rem;
  }

  .hero-image {
    opacity: 0.15;
    width: 70%;
  }

  .brand-grid {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 12px;
    padding-bottom: 12px;
    margin-right: -16px;
    /* Bleed to edge */
    padding-right: 16px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .brand-grid::-webkit-scrollbar {
    display: none;
  }

  .brand-card {
    flex: 0 0 140px;
    min-width: 140px;
    scroll-snap-align: start;
    padding: 16px;
    border-radius: 16px;
  }

  .brand-logo-wrapper {
    width: 60px;
    height: 60px;
    padding: 12px;
  }

  .brand-name-text {
    font-size: 0.8rem;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .section-header {
    margin-bottom: 16px;
  }

  .view-all-btn {
    padding: 8px 14px;
    font-size: 0.75rem;
  }

  .view-all-products-btn {
    padding: 16px 32px;
    font-size: 0.875rem;
  }
}

@media (min-width: 1024px) {
  .hero-image {
    opacity: 0.5;
  }

  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
}

/* Footer Styles */
.shop-footer {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  margin-top: 60px;
  padding: 60px 20px 40px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.footer-logo {
  height: 40px;
  width: auto;
  object-fit: contain;
  background: white;
  padding: 4px;
  border-radius: 8px;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.footer-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.footer-subtitle {
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  margin: 0 0 12px 0;
}

.footer-contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.footer-contact-item svg {
  flex-shrink: 0;
  color: rgba(255, 255, 255, 0.6);
}

.contact-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
}

.contact-link:hover {
  color: white;
  text-decoration: underline;
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.social-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(4px);
  border-color: rgba(255, 255, 255, 0.2);
}

.social-link.telegram:hover {
  background: rgba(37, 150, 190, 0.2);
  border-color: rgba(37, 150, 190, 0.4);
  color: #4FC3F7;
}

.social-link.instagram:hover {
  background: rgba(225, 48, 108, 0.2);
  border-color: rgba(225, 48, 108, 0.4);
  color: #E1306C;
}

.social-link.facebook:hover {
  background: rgba(24, 119, 242, 0.2);
  border-color: rgba(24, 119, 242, 0.4);
  color: #1877F2;
}

.social-link.whatsapp:hover {
  background: rgba(37, 211, 102, 0.2);
  border-color: rgba(37, 211, 102, 0.4);
  color: #25D366;
}

.footer-bottom {
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}

@media (min-width: 768px) {
  .footer-content {
    grid-template-columns: repeat(2, 1fr);
  }

  .shop-footer {
    padding: 80px 40px 40px;
  }
}

@media (min-width: 1024px) {
  .footer-content {
    grid-template-columns: repeat(3, 1fr);
    gap: 60px;
  }

  .social-links {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .social-link {
    flex: 1;
    min-width: 140px;
  }
}
</style>

<style scoped>
/* Swiper Styles */
.hero-swiper {
  width: 100%;
  height: 100%;
}

swiper-slide {
  height: auto;
}

/* Ensure hero card takes full height inside slide */
swiper-slide .hero-card {
  height: 100%;
  min-height: 400px;
}
</style>
