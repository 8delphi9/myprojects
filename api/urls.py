from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import (
    UserCreateApi,
    LoginApi,
)

# 토큰
token_patterns = [
    path('', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
]


urlpatterns = [
    path('register/', UserCreateApi.as_view()),
    path('login/', LoginApi.as_view()),

    # 토큰 url
    path('token/', include(token_patterns))
]