import axios from 'axios'
import store from "@/store/index.js";
import {ElMessage} from "element-plus";
import {getFingerprint} from "@/utils/fingerprint.js";

// 创建 axios 实例
const service = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_URL,
    // 请求超时时间
    timeout: 10000,
    // 设置内容类型
    headers: { 'Content-Type': 'application/json' },
    // 跨域携带cookie
    withCredentials: true
})

/* ===== 请求拦截：统一带 Authorization ===== */
service.interceptors.request.use( async (config) => {
    await store.dispatch('auth/refreshAuthState')
    // 在发送请求之前添加 JWT Token
    const token = store.getters['auth/token'].access
    if (token) config.headers.Authorization = `Bearer ${token}`
    // 添加浏览器指纹
    const fingerprint = await getFingerprint()
    if (fingerprint) config.headers['X-Fingerprint'] = fingerprint
    return config
})

/* ===== 响应拦截：自动刷 token ===== */
let isRefreshing = false // 正在刷新标志
let failedQueue = [] // 暂存因 401 挂起的请求

/**
 * 刷新 access token
 * @returns {Promise<*>}
 */
const refreshToken = async () => {
    await store.dispatch('auth/refreshAuthState')
    const refresh = store.getters['auth/token'].refresh
    if (!refresh) return Promise.reject(new Error('无 refresh token'))
    // 使用原始 axios 实例发送刷新请求，避免拦截器嵌套
    return await axios.post(
        `${import.meta.env.VITE_APP_BASE_URL}/token/refresh/`,
        { refresh },
        { // 确保刷新请求不被当前的拦截器影响
            baseURL: '',
            withCredentials: false
        }
    ).then(response => {
        // 后端返回新的access token
        store.dispatch('auth/updateToken', {
            access: response.data.data.access,
            refresh: refresh
        })
        return response.data.data.access
    }).catch(async error => {
        console.error('refresh token error:', error)
        // refresh过期
        if (error.status === 401
            && error.response.data.msg === 'Token is expired') {
            ElMessage.error('登录状态生效，请重新登录。')
            await store.dispatch('auth/clearAuth')
            location.replace('/login')
        }
        return null;
    })
}

/**
 * 处理挂起队列
 * @param error
 * @param token
 */
const processQueue = (error, token = null) => {
    failedQueue.forEach(p => {
        if (error) p.reject(error)
        else p.resolve(token)
    })
    failedQueue = []
}

/* 白名单，遇到这些地址 401 直接退出，不再刷新 */
const NO_RETRY = ['/api/token/refresh/', '/api/token/verify/']

service.interceptors.response.use(
    response => response, // 2xx 直接过
    async error => {
        const originalRequest = error.config
        // 只处理 401 且不是刷新接口本身
        if (error.response?.status === 401 && !NO_RETRY.some(u => originalRequest.url.includes(u))) {
            // 如果已在刷新，把当前请求先挂起
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({
                        resolve: (token) => {
                            // 修改原始请求的 token
                            originalRequest.headers.Authorization = `Bearer ${token}`;
                            // 使用原始 axios 实例重新发送，避免再次进入拦截器逻辑
                            resolve(axios(originalRequest));
                        },
                        reject
                    })
                })
            }

            // 没有正在刷新
            isRefreshing = true
            try {
                const newAccess = await refreshToken()

                if (newAccess) {
                    processQueue(null, newAccess)
                    originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                    return axios(originalRequest);
                } else {
                    console.error('[Response Interceptor] Token refresh returned null, treating as failure.');
                    throw new Error('Token refresh failed or returned null');
                }
            } catch (refreshErr) {
                processQueue(refreshErr, null)
                return Promise.reject(refreshErr)
            } finally {
                isRefreshing = false
            }
        }
        return Promise.reject(error)
    }
)

export default service
