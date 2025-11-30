import request from "@/api/request/index.js";
import {fail, success} from "@/common/RestCommon.js";
import axios from "axios";

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

export const loginApi = async (data) => {
    return await service.post("/login/", data)
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error("login error: ", error)
            return fail(error.response.data.msg)
        })
}

export const tokenVerifyApi = async (token) => {
    return await request.post("/token/verify/", {
        token: token,
    })
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Token verify api error:', error)
            return fail(error.response.data.msg)
        })
}
