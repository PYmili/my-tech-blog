import os

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from blog_user.models import BlogUser
from blog_user.serializers import AuthTokenObtainPairSerializer


class AuthTokenObtainPairView(TokenObtainPairView):
    """身份验证视图"""

    # 设置序列化器
    serializer_class = AuthTokenObtainPairSerializer


class UploadUserAvatarView(APIView):
    """上传用户头像视图"""

    permission_classes = (IsAuthenticated,)

    # 头像允许的图片类型
    ALLOWED_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/webp']
    # 头像最大字节数 2MiB
    MAX_AVATAR_SIZE = 2 * 1024 * 1024

    def post(self, request):
        """
        处理 POST 上传用户头像
        :param request: Request
        :return: Response
        """
        file = request.FILES.get('avatar')
        if not file:
            return Response({'detail': '该字段是必填项。'}, status=status.HTTP_400_BAD_REQUEST)

        if file.content_type not in self.ALLOWED_CONTENT_TYPES:
            return Response({'detail': '仅支持 JPEG、PNG、WebP 格式。'}, status=status.HTTP_400_BAD_REQUEST)

        if file.size > self.MAX_AVATAR_SIZE:
            return Response({'detail': '头像大小不可超过 2MiB。'}, status=status.HTTP_400_BAD_REQUEST)

        user: BlogUser = request.user
        # 删除旧头像
        if user.avatar and user.avatar.name != 'avatar/default.jpg':
            # 如果文件在磁盘上存在则删除
            if default_storage.exists(user.avatar.name):
                default_storage.delete(user.avatar.name)
        # 存储新头像
        user.avatar = file
        user.save()
        return Response({'url': user.avatar.url}, status=status.HTTP_200_OK)


class UserInformationView(APIView):
    """用户信息视图"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取用户信息数据
        :param request: Request
        :return: Response
        """
        user: BlogUser = request.user
        fields = (
            'id', 'username', 'avatar', 'bio',
            'github_home_link', 'gender', 'birth_date', 'location',
            'profile_updated_at', 'date_joined', 'email'
        )
        data = model_to_dict(user, fields=fields)
        # avatar 返回完整 URL
        if data.get('avatar'):
            data['avatar'] = request.build_absolute_uri(user.avatar.url)
        return Response({'information': data}, status=status.HTTP_200_OK)


class UpdateUserInformationView(APIView):
    """更新用户信息视图"""

    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        更新用户信息请求
        :param request: Request
        :return: Response
        """
        user: BlogUser = request.user
        information = request.data.get('information')

        if not information:
            return Response({'detail': '需要更新的信息为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 更新信息
        allowed_keys = {'username', 'email', 'bio', 'github_home_link', 'gender', 'birth_date', 'location'}
        update_fields = []
        for key in allowed_keys:
            if key in information:
                setattr(user, key, information[key])
                update_fields.append(key)

        if update_fields:
            update_fields.append('profile_updated_at')  # 自动时间戳
            user.save(update_fields=update_fields)
            return Response({'detail': '更新成功'}, status=status.HTTP_200_OK)
        return Response({'detail': '无有效字段可更新'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """已登录用户修改自己的登录密码"""

    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        更新用户密码
        :param request: Request
        :return: Response
        """
        old_pwd = request.data.get('oldPassword')
        new_pwd = request.data.get('newPassword')

        if not (old_pwd and new_pwd):
            return Response({'detail': '旧密码与新密码均不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        if old_pwd == new_pwd:
            return Response({'detail': '旧密码与新密码不能相同！'}, status=status.HTTP_400_BAD_REQUEST)

        user: BlogUser = request.user

        # 校验旧密码
        if not user.check_password(old_pwd):
            return Response({'detail': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)

        # 合法性检查（长度、常见弱口令等）
        try:
            validate_password(new_pwd, user)
        except ValidationError:
            return Response({'detail': '密码验证失败！请检查密码合法性！'}, status=status.HTTP_400_BAD_REQUEST)

        # 设置新密码并保存
        user.set_password(new_pwd)
        user.save(update_fields=['password', 'profile_updated_at'])

        return Response({'detail': '密码已更新'}, status=status.HTTP_200_OK)
