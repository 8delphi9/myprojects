from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        # create_user(self, validate_data)
        # email = validate_data['email']
        # password = validate_data['password1']
        # nickname = validate_data['nickname']

        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        if not password:
            raise ValueError('비밀번호는 필수 항목입니다.')
        if not nickname:
            raise ValueError('닉네임은 필수 항목 입니다.')

        user = self.model(
            email=UserManager.normalize_email(email),
            nickname=nickname,
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, nickname, **extra_fields):

        user = self.model(
            email=email,
            nickname=nickname,
        )
        user.set_password(password)
        user.full_clean()

        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


# User Model
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField('이메일', unique=True, max_length=100)
    nickname = models.CharField('닉네임', max_length=100, unique=True)

    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'nickname'
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'users'




