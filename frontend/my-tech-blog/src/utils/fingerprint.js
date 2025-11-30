import FingerprintJs from '@fingerprintjs/fingerprintjs'

export const getFingerprint = async () => {
    // 先尝试从 localStorage 获取
    const fingerprint = localStorage.getItem('my_tech_blog_fingerprint')
    if (fingerprint) return fingerprint

    // 生成指纹
    try {
        // 初始化指纹
        const fp = await FingerprintJs.load()
        // 获取指纹
        const result = await fp.get()
        // 存储指纹
        localStorage.setItem('my_tech_blog_fingerprint', result.visitorId)
        return result.visitorId
    } catch (error) {
        console.error('Get fingerprint error:', error)
    }
}
