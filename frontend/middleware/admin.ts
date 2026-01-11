export default defineNuxtRouteMiddleware(async (to, from) => {
    const { token, user, fetchUser } = useAuth()
    const localePath = useLocalePath()

    // If no token, redirect to login
    if (!token.value) {
        return navigateTo(localePath('/login'))
    }

    // If user not loaded yet, try to fetch
    if (!user.value) {
        try {
            await fetchUser()
        } catch (e) {
            // Token invalid, clear and redirect
            token.value = null
            return navigateTo(localePath('/login'))
        }
    }

    // Check if user is platform admin
    // Старая админка /admin доступна только для админа платформы
    const userData = user.value as any
    if (!userData || userData.role !== 'platform_admin') {
        // Если у пользователя есть магазины, перенаправить в админку магазина
        try {
            const shops = await $fetch<any[]>(useRuntimeConfig().public.apiBase + '/platform/shops/me', {
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })
            if (shops && shops.length > 0) {
                return navigateTo(localePath(`/shop/${shops[0].slug}/admin`))
            }
        } catch (e) {
            // Ignore error
        }
        return navigateTo(localePath('/profile'))
    }
})
