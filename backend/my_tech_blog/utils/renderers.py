from rest_framework.renderers import JSONRenderer


class ApiRenderer(JSONRenderer):
    """
    统一封装 DRF 原生返回格式
    code=0  表示成功，非 0 为业务自定义错误码
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 取出状态码
        response = renderer_context['response']
        status_code = response.status_code

        # 判断当前是否异常（DRF 会把异常放在 data.detail）
        if 200 <= status_code < 300:
            code, msg = 200, 'ok'
            payload = data
        else:
            # 非 2xx 都当错误
            code = status_code
            msg = data.pop('detail', 'error') if isinstance(data, dict) else 'error'
            payload = data

        # 返回统一格式
        return super().render(
            {'code': code, 'msg': msg, 'data': payload},
            accepted_media_type,
            renderer_context
        )
