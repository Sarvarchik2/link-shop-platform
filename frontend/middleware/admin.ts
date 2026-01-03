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
            // Token invalid, clear and redirect
            token.value = null
            return navigateTo('/login')
        }
    }

    // Check if user is platform admin
    // Старая админка /admin доступна только для админа платформы
    if (!user.value || user.value.role !== 'platform_admin') {
        // Если у пользователя есть магазины, перенаправить в админку магазина
        try {
            const shops = await $fetch(useRuntimeConfig().public.apiBase + '/platform/shops/me', {
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })
            if (shops && shops.length > 0) {
                return navigateTo(`/shop/${shops[0].slug}/admin`)
            }
        } catch (e) {
            // Ignore error
        }
        return navigateTo('/profile')
    }
})
