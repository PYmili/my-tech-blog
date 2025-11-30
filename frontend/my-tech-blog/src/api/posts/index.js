import request from "@/api/request/index.js";
import {fail, success} from "@/common/RestCommon.js";

export const statisticsApi = async () => {
    return await request.get('posts/statistics/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Statistics api error:', error)
            return fail(error.response.data.msg)
        })
}

export const recentApi = async () => {
    return await request.get('posts/recent/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Recent api error:', error)
            return fail(error.response.data.msg)
        })
}

export const getListApi = async (params) => {
    return await request.get('posts/list/', {params: params})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get post list api error:', error)
            return fail(error.response.data.msg)
        })
}

export const getHotApi = async () => {
    return await request.get('posts/hot/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get post hot api error:', error)
            return fail(error.response.data.msg)
        })
}

export const getDetailApi = async (id) => {
    return await request.get('posts/detail/', {params: {id: id}})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get post api error:', error)
            return fail(error.response.data.msg)
        })
}

export const addPostApi = async (data) => {
    return await request.post('posts/add/', data)
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Add post api error:', error)
            return fail(error.response.data.msg)
        })
}

export const deletePostApi = async (id) => {
    return await request.delete(`posts/delete/`, {params: {id: id}})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Delete post api error:', error)
            return fail(error.response.data.msg)
        })
}

export const updatePostApi = async (data) => {
    return await request.put(`posts/update/`, data)
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Update post api error:', error)
            return fail(error.response.data.msg)
        })
}

export const getCategoryListApi = async () => {
    return await request.get('posts/category/list/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get post category list api error:', error)
            return fail(error.response.data.msg)
        })
}

export const addCategoryApi = async (data) => {
    return await request.post('posts/category/add/', {category: data})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Add post category api error:', error)
            return fail(error.response.data.msg)
        })
}

export const deleteCategoryApi = async (name) => {
    return await request.delete('posts/category/delete/', {params: {name: name}})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Deleted post category api error:', error)
            return fail(error.response.data.msg)
        })
}

export const likePostApi = async (id) => {
    return await request.post(`posts/like/`, {id: id})
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Liked post api error:', error)
            return fail(error.response.data.msg)
        })
}

export const getTrafficStatistics = async () => {
    return await request.get('posts/traffic-statistics/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get traffic statistics api error:', error)
            return fail(error.response.data.msg)
        })
}

export const getChartDataApi = async (id) => {
    return await request.get('posts/chart-data/')
        .then(response => {
            return success(response.data.msg, response.data.data)
        })
        .catch(error => {
            console.error('Get chart data api error:', error)
            return fail(error.response.data.msg)
        })
}
