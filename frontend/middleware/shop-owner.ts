export default defineNuxtRouteMiddleware(async (to, from) => {
    const { token, user, fetchUser } = useAuth()

    // If no token, redirect to login
    if (!token.value) {
        return navigateTo('/login')
    }

    // If user not loaded yet, try to fetch
    if (!user.value) {
        try {
            await fetchUser()
        } catch (e) {
            console.error('[Shop Owner Middleware] Ошибка загрузки пользователя:', e)
            token.value = null
            return navigateTo('/login')
        }
    }

    // Get shop slug from route params (to.params instead of useRoute())
    const shopSlug = to.params.slug

    if (!shopSlug) {
        return navigateTo('/profile')
    }

    try {
        // Get shop info
        const shop = await $fetch(`${useRuntimeConfig().public.apiBase}/platform/shops/${shopSlug}`, {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })

        // Check if user is platform admin or shop owner
        const currentUser = user.value as any
        const currentShop = shop as any

        if (currentUser && (currentUser.role === 'platform_admin' || currentShop.owner_id === currentUser.id)) {
            // Subscription check for shop owners
            if (currentUser.role !== 'platform_admin') {
                const isExpired = currentShop.subscription_status === 'expired' ||
                    (currentShop.subscription_expires_at && new Date(currentShop.subscription_expires_at) < new Date())

                const isInactive = !currentShop.is_active
                const subscriptionPath = `/shop/${shopSlug}/admin/settings/subscription`

                if ((isExpired || isInactive) && to.path !== subscriptionPath) {
                    console.warn('[Shop Owner Middleware] Shop expired/inactive, redirecting to subscription page')
                    return navigateTo(subscriptionPath)
                }
            }
            return // Allow access
        }

        // User is not authorized
        return navigateTo('/profile')
    } catch (e) {
        // Shop not found or error
        console.error('[Shop Owner Middleware] Ошибка при проверке магазина:', e)
        return navigateTo('/profile')
    }
})

