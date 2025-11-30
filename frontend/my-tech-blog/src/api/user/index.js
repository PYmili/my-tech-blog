import request from "@/api/request/index.js";
import {fail, success} from "@/common/RestCommon.js";

export const getInformationApi = async () => {
    return await request.get('user/information/get/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get user information api error:', error)
            return fail(error.response.data.msg)
        })
}

export const uploadAvatarApi = async (file) => {
    const data = new FormData()
    // 后端接收字段名：avatar
    data.append('avatar', file)
    return request.post('user/upload-avatar/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    })
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Upload user avatar api error:', error)
            return fail(error.response.data.msg)
        })
}

export const updateInformationApi = async (data) => {
    return await request.put('user/information/update/', {'information': data})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Update user information api error:', error)
            return fail(error.response.data.msg)
        })
}

export const updatePasswordApi = async (data) => {
    return await request.put('user/password/update/',data)
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Update user password api error:', error)
            return fail(error.response.data.msg)
        })
}
