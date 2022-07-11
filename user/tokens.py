from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


user = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    author : 이승민
    explanation :
        - 유저에 맞는 토큰 payload에 email과 is_staff 필드 값을 추가
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["is_staff"] = user.is_admin

        return token


class ApiRefreshRefreshTokenSerializer(serializers.Serializer):
    """
    author : 이승민
    explanation :
        - refresh token 시리얼라이저
    """
    refresh = serializers.CharField()
    pass
