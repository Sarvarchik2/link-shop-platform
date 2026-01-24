export default defineNuxtPlugin(async (nuxtApp) => {
    const { token, user, fetchUser } = useAuth()

    // If we have a token but no user, fetch the user
    if (token.value && !user.value) {
        try {
            await fetchUser()
        } catch (e) {
            console.error('Initial auth fetch failed:', e)
            token.value = null
            user.value = null
        }
    }
})
