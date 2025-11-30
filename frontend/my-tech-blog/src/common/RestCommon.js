/**
 * 对后端返回的数据模版
 * @param code
 * @param msg
 * @param data
 * @returns {{msg, code, data: null}}
 * @constructor
 */
const RestCommon = (code, msg, data = null) => {
    return {
        code: code,
        msg: msg,
        data: data
    }
}

/**
 * 通过
 * @param msg
 * @param data
 * @returns {{msg, code, data: null}}
 */
export const success = (msg, data = null) => RestCommon(200, msg, data)

/**
 * 失败
 * @param msg
 * @param data
 * @returns {{msg, code, data: null}}
 */
export const fail = (msg, data = null) => RestCommon(400, msg, data)

/**
 * 错误
 * @param msg
 * @param data
 * @returns {{msg, code, data: null}}
 */
export const error = (msg, data = null) => RestCommon(500, msg, data)
