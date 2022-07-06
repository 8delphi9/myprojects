from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db import transaction
from django.contrib.auth import get_user_model

from user.serializers import RegisterSerializer, UserSerializer
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


class UserCreateApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, **kwargs):
        """
        author: 정용수
        회원가입: 이메일, 패스워드, 닉네임
        :param request: QueryDict
        :return: JSON
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "회원 가입이 완료되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "이메일 또는 패스워드 또는 닉네임 형식을 확인해주세요."
        }, status=status.HTTP_400_BAD_REQUEST)


class UserApi(APIView):
    def put(self, request):
        """
         author: 정용수
        회원정보 변경: 이메일로 회원 정보를 찾아 nickname을 변경함
        :param request: QueryDict
        :return: JSON
        """
        try:
            user = User.objects.get(email=request.data.get('email'))

            update_user_serializer = UserSerializer(user, data=request.data)

            if update_user_serializer.is_valid(raise_exception=True):
                update_user_serializer.save()

            return Response({
                "message": "회원 정보가 변경되었습니다."
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "message": "해당 하는 회원 정보가 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)