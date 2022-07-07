from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


user = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['is_staff'] = user.is_admin

        return token


class ApiRefreshRefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    pass