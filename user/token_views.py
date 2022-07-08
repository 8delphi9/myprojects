from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user.tokens import MyTokenObtainPairSerializer, ApiRefreshRefreshTokenSerializer


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """
    author : 이승민
    explanation :
         - token 커스텀한 것을 적용
    """
    serializer_class = MyTokenObtainPairSerializer


class ApiRefreshRefreshTokenView(GenericAPIView):
    """
    author : 이승민
    explanation :
         - token 커스텀
         - 토큰 payload 필수데이터에 추가적인 필드 값을 삽입
         - 만료된 refresh token은 자동으로 blacklist에 저장.
    """
    permission_classes = ()  # 중요, 이렇게 해야 접근이 가능합니다.
    authentication_classes = ()  # 중요, 이렇게 해야 접근이 가능합니다.

    serializer_class = ApiRefreshRefreshTokenSerializer

    # 리프레시 토큰 자체를 다시 발급
    def post(self, request: HttpRequest):
        serializer: ApiRefreshRefreshTokenSerializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        refresh: str = serializer.validated_data['refresh']

        try:
            refresh_token: RefreshToken = RefreshToken(refresh)
        except TokenError:
            raise InvalidToken(TokenError)

        user: User = get_object_or_404(User, id=refresh_token['user_id'])
        new_refresh_token = MyTokenObtainPairSerializer.get_token(user)
        new_access_token = new_refresh_token.access_token
        refresh_token.blacklist()

        return Response({
            'refresh': str(new_refresh_token),
            'access': str(new_access_token),
        })