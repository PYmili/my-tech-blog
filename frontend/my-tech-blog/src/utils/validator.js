import bcryptjs from 'bcryptjs'
import store from "@/store/index.js";

export const isPhone = s => /^1[3-9]\d{9}$/.test(s)
export const isEmail = s => /^[\w.%+-]+@[\w.-]+\.\w{2,}$/.test(s)
export const isUsername = s => /^[A-Za-z][\w]{2,19}$/.test(s)
export const hashPassword = async (pwd) =>
    await bcryptjs.hash(pwd, await bcryptjs.genSalt(10))

export const parseJwt = (token) => {
    if (!token) return;
    try {
        const base64Url = token.split('.')[1] // JWT payload 部分
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        )
        return JSON.parse(jsonPayload)
    } catch (e) {
        console.error("Invalid JWT", e)
        return null
    }
}

export const JwtJson = () => {
    store.dispatch('auth/refreshAuthState')
    return parseJwt(store.getters["auth/token"].access) || {}
}

export const JwtPayload = () => {
    // 先刷新 状态
    store.dispatch('auth/refreshAuthState')
    return JwtJson() || {}
}
