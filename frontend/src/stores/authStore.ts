import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from '@/lib/axios'

interface User {
  id: number
  email: string
  username: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })
        const { access_token } = response.data

        // ユーザー情報を取得
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        const userResponse = await axios.get('/users/me')

        set({
          token: access_token,
          user: userResponse.data,
          isAuthenticated: true,
        })
      },

      register: async (email: string, username: string, password: string) => {
        await axios.post('/auth/register', {
          email,
          username,
          password,
        }, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
      },

      logout: () => {
        delete axios.defaults.headers.common['Authorization']
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      checkAuth: () => {
        const { token } = get()
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          set({ isAuthenticated: true })
        }
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)