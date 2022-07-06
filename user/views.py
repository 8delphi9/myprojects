from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db import transaction
from django.contrib.auth import get_user_model

from user.serializers import RegisterSerializer
from user.authenticate import jwt_login


User = get_user_model()


# Create your views here.
# 로그인 뷰
class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        # serializer에서 구현하기
        email = request.data.get('email')
        password = request.data.get('password')

        if (email is None) or (password is None):
            return Response({
                "message": "email/password required"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({
                "message": "유저를 찾을 수 없습니다"
            }, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({
                "message": "wrong password"
            }, status=status.HTTP_400_BAD_REQUEST)

        response = Response(status=status.HTTP_200_OK)
        return jwt_login(response, user)
