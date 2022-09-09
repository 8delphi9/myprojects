import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


User = get_user_model()


def validate_password12(password1, password2):
    """
    :param password1: 첫 번째 비밀번호
    :param password2: 두 번째 비밀번호
    :return: password1
    error :
        - password1 validate
        - password1, 2 require
        - password1 == password2
    explanation :
        - 회원가입 시 password1, password2를 입력 후 일치하는 비교
        - 영문자 대소문자, 숫자, 특수문자(리스트)만 허용
        - 영어 대소문자 필수
        - 특수문자 필수
        - 글자수 제한
    """
    validate_condition = [

        lambda s: all(
            x.islower()
            or x.isupper()
            or x.isdigit()
            or (x in ["!", "@", "#", "$", "%", "^", "&", "*", "_"])
            for x in s
        ),  ## 영문자 대소문자, 숫자, 특수문자(리스트)만 허용
        lambda s: any(x.islower() or x.isupper() for x in s),  ## 영어 대소문자 필수
        lambda s: any(
            (x in ["!", "@", "#", "$", "%", "^", "&", "*", "_"]) for x in s
        ),  ## 특수문자 필수
        lambda s: len(s) == len(s.replace(" ", "")),
        lambda s: len(s) >= 6,
        lambda s: len(s) <= 20,
    ]

    for validator in validate_condition:
        if not validator(password1):
            raise serializers.ValidationError(_("password ValidationError"))

    if not password1 or not password2:
        raise serializers.ValidationError(_("need two password fields"))
    if password1 != password2:
        raise serializers.ValidationError(_("password fields didn't match!"))

    return password1


# 유저 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    """
    explanation :
        - 유저의 정보를 조회하기 위한 시리얼라이저
        - 어드민전용
    """
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "last_login",
        ]


# 회원가입 시리얼라이저
class RegisterSerializer(serializers.Serializer):
    """
    explanation :
        - 회원가입 시리얼라이저
        - email, password1, password2, nickname의 validate 확인
    error :
         - validate_email : 이메일 입력 확인, 이메일 형식 확인, 이메일 중복 확인
         - validate_nickname : 닉네임 입력 확인, 닉네임 중복 확인
    """
    email = serializers.EmailField(max_length=100, write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100, write_only=True)

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError(_("email field not allowed empty"))
        get_email = User.objects.filter(email__iexact=email)
        if get_email.count() > 0:
            raise serializers.ValidationError(_("email is already registered"))
        return email

    def validate_nickname(self, nickname):
        if not nickname:
            raise serializers.ValidationError(_("nickname field not allowed empty"))
        get_name = User.objects.filter(nickname__iexact=nickname)
        if get_name.count() > 0:
            raise serializers.ValidationError(
                _("nickname is already registered with this e-mail address")
            )

        return nickname

    def validate(self, data):
        data["password1"] = validate_password12(data["password1"], data["password2"])
        data["email"] = self.validate_email(data["email"])
        data["nickname"] = self.validate_nickname(data["nickname"])
        return data

    def create(self, validate_data):
        user = User.objects.create_user(
            email=validate_data["email"],
            password=validate_data["password1"],
            nickname=validate_data["nickname"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    explanation :
        - 로그인 시리얼라이저
    """

    email = serializers.EmailField(max_length=100, write_only=True)
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    """
    explanation :
        - blacklist를 활용
        - token을 blacklist 테이블에 저장
    error :
        - 잘못된 토큰일 경우.
    """

    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid",)}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    explanation :
        - 어드민 권한으로 해당 유저의 정보를 조회할 수 있다.
    """

    class Meta:
        model = User
        fields = ["id", "email", "nickname", "is_admin"]


class UserUpdateDeleteSerializer(serializers.ModelSerializer):
    """
    explanation :
         - 어드민 권한으로 해당 유저의 정보를 수정 및 삭제할 수 있다.
    """

    class Meta:
        model = User
        fields = ["id", "nickname", "is_admin"]
