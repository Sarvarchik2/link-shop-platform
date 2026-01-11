export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState('user', () => null)
    const localePath = useLocalePath()

    const login = async (phone: string, password: string, redirect: boolean = true) => {
        try {
            const formData = new URLSearchParams()
            formData.append('username', phone)
            formData.append('password', password)

            const data: any = await $fetch(useRuntimeConfig().public.apiBase + '/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData.toString()
            })
            token.value = data.access_token
            await fetchUser()
            useToast().success('Добро пожаловать!')

            if (redirect) {
                // Get return URL from query params or localStorage
                const route = useRoute()
                let queryReturnUrl: string | null = null

                if (Array.isArray(route.query.returnUrl)) {
                    queryReturnUrl = route.query.returnUrl[0] || null
                } else if (typeof route.query.returnUrl === 'string') {
                    queryReturnUrl = route.query.returnUrl
                }

                const returnUrl = queryReturnUrl || (process.client ? localStorage.getItem('returnUrl') : null)

                if (returnUrl) {
                    // Clear returnUrl from localStorage
                    if (process.client) {
                        localStorage.removeItem('returnUrl')
                    }
                    await navigateTo(returnUrl)
                } else {
                    await navigateTo(localePath('/'))
                }
            }
        } catch (error) {
            console.error('Login error:', error)
            throw error
        }
    }

    const register = async (phone: string, password: string, first_name: string, last_name: string) => {
        try {
            const data: any = await $fetch(useRuntimeConfig().public.apiBase + '/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone, password, first_name, last_name })
            })
            token.value = data.access_token
            await fetchUser()
            useToast().success('Аккаунт успешно создан!')

            // Get return URL from query params or localStorage
            const route = useRoute()
            let queryReturnUrl: string | null = null

            if (Array.isArray(route.query.returnUrl)) {
                queryReturnUrl = route.query.returnUrl[0] || null
            } else if (typeof route.query.returnUrl === 'string') {
                queryReturnUrl = route.query.returnUrl
            }

            const returnUrl = queryReturnUrl || (process.client ? localStorage.getItem('returnUrl') : null)

            if (returnUrl) {
                // Clear returnUrl from localStorage
                if (process.client) {
                    localStorage.removeItem('returnUrl')
                }
                await navigateTo(returnUrl)
            } else {
                await navigateTo(localePath('/'))
            }
        } catch (error) {
            console.error('Register error:', error)
            throw error
        }
    }

    const fetchUser = async () => {
        if (!token.value) return
        try {
            user.value = await $fetch(useRuntimeConfig().public.apiBase + '/users/me', {
                headers: { Authorization: `Bearer ${token.value}` }
            })
        } catch (e) {
            token.value = null
            user.value = null
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        navigateTo(localePath('/login'))
    }

    return { token, user, login, register, logout, fetchUser }
}
