import axios from 'axios'
import toast from 'react-hot-toast'

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
})

// リクエストインターセプター
instance.interceptors.request.use(
  (config) => {
    // デバッグ用ログ
    console.log('API Request:', {
      method: config.method,
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      headers: config.headers,
      hasAuth: !!config.headers?.Authorization
    })
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// レスポンスインターセプター
instance.interceptors.response.use(
  (response) => {
    console.log('API Response Success:', {
      status: response.status,
      url: response.config.url,
      data: response.data
    })
    return response
  },
  (error) => {
    console.error('API Response Error:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      config: {
        method: error.config?.method,
        url: error.config?.url,
        baseURL: error.config?.baseURL
      }
    })
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 認証エラー
          toast.error('認証エラーが発生しました。再度ログインしてください。')
          // ログインページへリダイレクト
          window.location.href = '/login'
          break
        case 403:
          toast.error('アクセス権限がありません。')
          break
        case 404:
          toast.error('リソースが見つかりません。')
          break
        case 500:
          toast.error('サーバーエラーが発生しました。')
          break
        default:
          toast.error(error.response.data.detail || 'エラーが発生しました。')
      }
    } else if (error.request) {
      toast.error('ネットワークエラーが発生しました。')
    } else {
      toast.error('エラーが発生しました。')
    }
    return Promise.reject(error)
  }
)

export default instance