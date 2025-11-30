from django.forms import model_to_dict
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from anonymous_users.models import AnonymousUser


class RegisterAnonymousView(APIView):
    """注册访客视图"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        注册访客用户
        :param request: Request
        :param args: Arguments
        :param kwargs: Kwargs
        :return: Response
        """
        fingerprint = request.headers.get('X-Fingerprint', None)
        nickname = request.data.get('nickname', None)
        if not fingerprint or not nickname:
            return Response({'detail': '参数残缺！'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查访客是否存在
        try:
            AnonymousUser.objects.get(browser_fingerprint=fingerprint)
            AnonymousUser.objects.get(nickname=nickname)
            return Response({'detail': '访客已存在！'}, status=status.HTTP_400_BAD_REQUEST)
        except AnonymousUser.DoesNotExist:
            pass

        # 创建访客
        anonymous_user = AnonymousUser.objects.create(browser_fingerprint=fingerprint, nickname=nickname)
        anonymous_user.save()
        return Response({'detail': '创建成功！'}, status=status.HTTP_200_OK)


class GetAnonymousUserView(APIView):
    """获取访客信息视图"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """
        获取访客信息
        :param request: Request
        :param args: Arguments
        :param kwargs: Kwargs
        :return: Response
        """
        fingerprint = request.headers.get('X-Fingerprint', None)
        nickname = request.data.get('nickname', None)
        if not fingerprint:
            return Response({'detail': '参数残缺！'}, status=status.HTTP_400_BAD_REQUEST)

        anonymous_user = AnonymousUser.objects.filter(browser_fingerprint=fingerprint)
        if nickname is not None:
            anonymous_user = AnonymousUser.objects.filter(nickname=nickname)

        if anonymous_user.exists():
            return Response({'data': model_to_dict(anonymous_user.first())}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '访客不存在！'}, status=status.HTTP_400_BAD_REQUEST)
