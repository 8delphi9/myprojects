from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from user.serializers import RegisterSerializer, UserSerializer
from user.authenticate import jwt_login


User = get_user_model()


# Create your views here.
# 로그인 뷰
# 리팩토링
class LoginAPI(mixins.ListModelMixin,
               viewsets.GenericViewSet):

    # 로그인 액션
    @action(detail=False, methods='post')
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema('사용자 이메일', type=openapi.TYPE_STRING),
            'password': openapi.Schema('사용자 비밀번호', type=openapi.TYPE_STRING)
        },
        required=['email', 'password']
    ))
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if (email is None) or (password is  None):
            return Response(
                {
                    "message": "email or password required"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(
                {
                    "message": "User is Not Found"
                }, status=status.HTTP_404_NOT_FOUND
            )

        if not user.check_password(password):
            return Response(
                {
                    "message": "Wrong password"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(status=status.HTTP_200_OK)
        return jwt_login(response, user)


class UserCreateApi(APIView):
    @swagger_auto_schema(RegisterSerializer)
    def post(self, request, *args, **kwargs):
        """
        회원가입 api
        user 모델과 profile 모델이 반드시 같이 생성되어야 하기 때문에
        transaction 적용
        """
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({
                "message": "Request Body Error"
            }, status=status.HTTP_409_CONFLICT)

        user = serializer.save()

        response = Response(status=status.HTTP_200_OK)
        response = jwt_login(response=response, user=user)
        return response

