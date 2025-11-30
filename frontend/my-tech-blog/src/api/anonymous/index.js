import request from "@/api/request/index.js";
import {fail, success} from "@/common/RestCommon.js";

export const getAnonymousUser = async (nickname) => {
    return await request.get('anonymous/get/', { params: { nickname: nickname } })
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error("Get anonymous user error: ", error)
            return fail(error.response.data.msg)
        })
}

export const registerAnonymousUser = async (nickname) => {
    return await request.post('anonymous/register/', {nickname: nickname})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error("Register anonymous user error: ", error)
            return fail(error.response.data.msg)
        })
}
