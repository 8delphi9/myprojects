from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


def get_user_login(user: User):
    """
    author : 이승민
    request : User
    explanation :
        - 유저의 last_login 필드 값을 업데이트 해준다.
    """
    user.last_login = timezone.now()
    user.save()

    return user