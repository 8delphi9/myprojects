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
    """
    author : 이승민
    로그인 : email, password, list (get)
    param request: QueryDict
    return: JSON (200 or 400)
    explanation :
        - list (get) : 어드민 권한으로 모든 유저를 조회할 수 있다.
        - login (post) : 입력받은 email과 password를 통해서 올바른 email과 password인지 검사하고
                         올바르다면 access, refresh 토큰을 발급한다.
                         이때 토큰에는 유저의 id와 email이랑 is_staff 필드를 payload에 같이 삽입 후 엔코딩한다.
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
        author : 이승민
        response : success (200), fail (400)
        - login (post) : 입력받은 email과 password를 통해서 올바른 email과 password인지 검사하고
                         올바르다면 access, refresh 토큰을 발급한다.
                         이때 토큰에는 유저의 id와 email이랑 is_staff 필드를 payload에 같이 삽입 후 엔코딩한다.
        """
        user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
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
    """
    author : 이승민
    로그아웃 : blacklist
    return: JSON (200 or 400)
    explanation :
        - logout (post) : access_token을 blacklist 테이블에 저장을 해서 로그아웃 처리를 한다.
    """
    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    @action(detail=False, methods='post')
    def logout(self, request):
        """
        author : 이승민
        로그아웃 : blacklist
        response : success (200), fail (400)
        explanation :
            - logout (post) : token을 blacklist 테이블에 저장을 해서 로그아웃 처리를 한다.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '로그아웃이 정상적으로 완료되었습니다.'}, status=status.HTTP_200_OK)


class UserDetailAPIView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    author : 이승민
    어드민 : detail (get), update (patch), delete (delete)
    param request: QueryDict
    return: JSON
    response :
        - success 200
        - fail 400, 404, 401, 403
    explanation :
        - detail (get) <어드민전용> : 어드민 권한으로 해당 유저를 조회할 수 있다.
        - update (patch) <어드민전용> : 어드민 권한으로 해당 유저의 정보를 수정할 수 있다.
        - delete (delete) <어드민전용> : 어드민 권한으로 해당 유저를 삭제할 수 있다.
    """
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        else:
            return UserUpdateDeleteSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        """
        author : 이승민
        어드민 : update (patch)
        param request: QueryDict
        return: JSON
        response :
            - success (200)
            - fail (400)
            - 유저가 없다면 (404)
            - 권한 이슈 (403)
            - 인증 이슈 (401)
        explanation :
            - update (patch) <어드민전용> : 어드민 권한으로 해당 유저의 정보를 수정할 수 있다.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserReadAPIView(mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    lookup_url_kwarg = 'user_id'
    permission_classes = [IsOwner]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return UserUpdateDeleteSerializer


class UserCreateApiView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

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


class GenaralUserApiView(GenericAPIView):
    permission_classes = [IsOwner]

    def get(self, request, user_id : int):
        """
        author: 정용수
        회원 상세정보 조회: user_id로 상세 정보를 조회
        :param request: Int
        :return: JSON
        """
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
        """
         author: 정용수
        회원정보 변경: user_id로 회원 정보를 찾아 email, nickname을 변경함
        :param request: Int
        :return: JSON
        """
        try:
            user = User.objects.get(id=user_id)

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

    def delete(self, request, user_id : int):
        """
         author: 정용수
        회원탈퇴: 이메일로 회원 탈퇴를 진행함
        :param request: Int
        :return: JSON
        """
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