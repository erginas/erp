import axios, { AxiosInstance } from 'axios'

// Ortam değişkeniyle base URL tanımla
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Axios instance
export const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // gerekliyse cookie gönderimi
})

// İsteğe bağlı interceptor: istek öncesi
api.interceptors.request.use(
  config => {
    // Örneğin auth token ekle
    const token = localStorage.getItem('token')
    if (token) {
      config.headers!['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// İsteğe bağlı interceptor: cevap sonrası
api.interceptors.response.use(
  response => response,
  error => {
    // Global hata yakalama
    if (error.response?.status === 401) {
      // Oturumu kapat veya login sayfasına yönlendir
    }
    return Promise.reject(error)
  }
)