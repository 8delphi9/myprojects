import datetime
import jwt

from Payhere.settings import SECRET_KEY
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck
from django.contrib.auth import get_user_model

from user.utils import get_user_login

User = get_user_model()


class CustomJWTAuthentication(BaseAuthentication):
    """
    author : 이승민
    explanation :
         - PyJWT를 직접 커스텀
         - authenticate와 authenticate_credentials, enforce_csrf의 함수를 통해서
           유저에 대한 토큰을 생성하고 payload를 인코딩, 디코딩 작업을 함.
    """

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            prefix = authorization_header.split(' ')[0]
            if prefix.lower() != 'jwt':
                raise exceptions.AuthenticationFailed('Token is not jwt')

            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, SECRET_KEY, algorithms=['HS256']
            )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expire')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token Prefix missing')

        return self.authenticate_credentials(request, payload['user_id'])

    def authenticate_credentials(self, request, key):
        user = User.obejcts.filter(id=key).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is Inactive')

        self.enforce_csrf(request)

        return (user, None)

    def enforce_csrf(self, request):
        check = CSRFCheck()

        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed : {reason}')


def get_access_token(user):
    """
    author : 이승민
    explanation :
         - access_token의 payload에 user_id, email, is_staff 필드 값을 추가
         - 토큰 인코딩
    """
    access_token_payload = {
        'user_id': user.id,
        'email': user.email,
        'is_staff': user.is_staff,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=0,
            minutes=60
        ),
        'iat': datetime.datetime.utcnow()
    }

    access_token = jwt.encode(
        access_token_payload,
        SECRET_KEY, algorithm='HS256'
    )

    return access_token


def get_refresh_token(user):
    """
    author : 이승민
    explanation :
         - refresh_token의 payload에 user_id, email, is_staff 필드 값을 추가
         - 토큰 인코딩
    """
    refresh_token_payload = {
        'user_id': user.id,
        'email': user.email,
        'is_staff': user.is_staff,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }

    refresh_token = jwt.encode(
        refresh_token_payload,
        SECRET_KEY,
        algorithm='HS256'
    )

    return refresh_token


def jwt_login(response, user):
    """
    author : 이승민
    explanation :
        - user에 대한 로그인 요청이 오면 토큰들을 발행한다.
    """
    access_token = get_access_token(user)
    refresh_token = get_refresh_token(user)

    data = {
        'user': user,
        'access_token': access_token,
        'refresh_token': refresh_token
    }


    get_user_login(user)

    response.data = data
    return response



