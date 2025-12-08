export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState('user', () => null)

    const login = async (phone: string, password: string, redirect: boolean = true) => {
        try {
            const formData = new URLSearchParams()
            formData.append('username', phone)
            formData.append('password', password)

            const data: any = await $fetch('http://localhost:8000/token', {
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
                await navigateTo('/')
            }
        } catch (error) {
            console.error('Login error:', error)
            throw error
        }
    }

    const register = async (phone: string, password: string, first_name: string, last_name: string) => {
        try {
            const data: any = await $fetch('http://localhost:8000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone, password, first_name, last_name })
            })
            token.value = data.access_token
            await fetchUser()
            useToast().success('Аккаунт успешно создан!')
            await navigateTo('/')
        } catch (error) {
            console.error('Register error:', error)
            throw error
        }
    }

    const fetchUser = async () => {
        if (!token.value) return
        try {
            user.value = await $fetch('http://localhost:8000/users/me', {
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
        navigateTo('/login')
    }

    return { token, user, login, register, logout, fetchUser }
}
