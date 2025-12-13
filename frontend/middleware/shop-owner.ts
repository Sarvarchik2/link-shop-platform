export default defineNuxtRouteMiddleware(async (to, from) => {
    console.log('[Shop Owner Middleware] Проверка доступа к:', to.path)
    
    const { token, user, fetchUser } = useAuth()

    // If no token, redirect to login
    if (!token.value) {
        console.log('[Shop Owner Middleware] Нет токена, редирект на /login')
        return navigateTo('/login')
    }

    // If user not loaded yet, try to fetch
    if (!user.value) {
        try {
            console.log('[Shop Owner Middleware] Загрузка данных пользователя...')
            await fetchUser()
            console.log('[Shop Owner Middleware] Пользователь загружен:', user.value?.role)
        } catch (e) {
            console.error('[Shop Owner Middleware] Ошибка загрузки пользователя:', e)
            token.value = null
            return navigateTo('/login')
        }
    }

    // Get shop slug from route params (to.params instead of useRoute())
    const shopSlug = to.params.slug
    console.log('[Shop Owner Middleware] Shop slug:', shopSlug)
    
    if (!shopSlug) {
        console.log('[Shop Owner Middleware] Нет shop slug, редирект на /profile')
        return navigateTo('/profile')
    }

    try {
        // Get shop info
        console.log('[Shop Owner Middleware] Загрузка информации о магазине...')
        const shop = await $fetch(`http://localhost:8000/platform/shops/${shopSlug}`, {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })
        console.log('[Shop Owner Middleware] Магазин загружен:', shop.name, 'Owner ID:', shop.owner_id, 'User ID:', user.value.id)

        // Check if user is platform admin or shop owner
        if (user.value.role === 'platform_admin' || shop.owner_id === user.value.id) {
            console.log('[Shop Owner Middleware] Доступ разрешен')
            return // Allow access
        }

        // User is not authorized
        console.log('[Shop Owner Middleware] Доступ запрещен, редирект на /profile')
        return navigateTo('/profile')
    } catch (e) {
        // Shop not found or error
        console.error('[Shop Owner Middleware] Ошибка при проверке магазина:', e)
        console.error('[Shop Owner Middleware] Детали ошибки:', {
            message: e.message,
            statusCode: e.statusCode,
            data: e.data
        })
        return navigateTo('/profile')
    }
})

