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
        if (user.value.role === 'platform_admin' || shop.owner_id === user.value.id) {
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

