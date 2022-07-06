from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


def get_user_login(user: User):
    user.last_login = timezone.now()
    user.save()

    return user