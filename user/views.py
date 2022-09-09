from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.permissions import IsOwner
from user.tokens import MyTokenObtainPairSerializer
from user.utils import get_user_login
from user.serializers import (
    UserSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserDetailSerializer,
    UserUpdateDeleteSerializer,
    RegisterSerializer,
)
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)

User = get_user_model()


# Create your views here.
class UserLoginAPIView(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    def get_queryset(self):
        if self.action == "list":
            return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        elif self.request.method == "POST":
            return LoginSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods="post")
    def login(self, request):

        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            get_user_login(user)
            res = Response(
                {
                    'email': request.data.get('email'),
                    'message': f'로그인 되었습니다. 반갑습니다 {user.nickname}님!',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response({'message': '잘못된 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    @action(detail=False, methods="post")
    def logout(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '로그아웃이 정상적으로 완료되었습니다.'}, status=status.HTTP_200_OK)


class UserDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):


    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserDetailSerializer
        else:
            return UserUpdateDeleteSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "retrieve":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        return self.update(request, *args, **kwargs)


class UserCreateApiView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "회원 가입이 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response(
            {"message": "이메일 또는 패스워드 또는 닉네임 형식을 확인해주세요."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GenaralUserApiView(GenericAPIView):
    permission_classes = [IsOwner]

    def get(self, request, user_id : int):

        try:
            user = User.objects.get(id=user_id)

            return Response({
                "message": "회원 조회가 완료되었습니다.",
                "회원 상세 정보": UserDetailSerializer(user).data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "message": "해당 하는 회원 정보가 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id : int):

        try:
            user = User.objects.get(id=user_id)

            update_user_serializer = UserSerializer(user, data=request.data)

            if update_user_serializer.is_valid(raise_exception=True):
                update_user_serializer.save()

            return Response({"message": "회원 정보가 변경되었습니다."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"message": "해당 하는 회원 정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, user_id : int):

        try:
            user = User.objects.get(id=user_id)
            user.delete()

            return Response({
                "message": "회원 탈퇴가 완료되었습니다."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": f"{e}"
            }, status=status.HTTP_400_BAD_REQUEST)

