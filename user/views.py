from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.serializers import (
    UserSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserDetailSerializer,
    UserUpdateSerializer
)
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated
)

User = get_user_model()


# Create your views here.

class UserAPIView(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    - Login 기능
    - User 조회 (어드민 전용)
    """

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return LoginSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods='post')
    def login(self, request):
        """
        - 로그인
        """
        user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "email": request.data.get('email'),
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(viewsets.GenericViewSet):
    """
    - 로그아웃 기능 (인증된 유저 전용)
    """
    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    @action(detail=False, methods='post')
    def logout(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailAPIView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    - 유저 디테일 (어드민 전용)
    - 유저 업데이트 (어드민 전용)
    - 업데이트 수정해야함.
    """
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        else:
            return UserUpdateSerializer

    def get_permissions(self):
        permission_classes = []
        if (self.action == 'retrieve') or (self.action == 'patch'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


