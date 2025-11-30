from typing import Dict
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

# 获取BlogUser模型
User = get_user_model()


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    """身份验证的序列化器"""

    @classmethod
    def get_token(cls, user: User) -> Token:
        """
        获取token
        :param user: User
        :return: dict
        """
        token = super().get_token(user)
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        """
        验证token
        :param attrs: Dict
        :return: Dict
        """
        # 用户名密码验证
        return super().validate(attrs)
