import request from "@/api/request/index.js";
import {fail, success} from "@/common/RestCommon.js";

export const getCommentList = async (params) => {
    return await request.get('comment/list/', {params: params})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get comment list api error:', error)
            return fail(error.response.data.msg)
        })
}

export const addPostComment = async (data) => {
    return await request.post(`comment/add/`, data)
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Add post comment api error:', error)
            return fail(error.response.data.msg)
        })
}
