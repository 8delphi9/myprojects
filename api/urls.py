from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from user.token_views import MyTokenObtainPairView, ApiRefreshRefreshTokenView
from user.views import (
    UserApiView,
    UserCreateApiView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from user.urls import (
    login,
    logout,
    users,
    user_detail
)

schema_view = get_schema_view(
    openapi.Info(
        title='Payhere',
        default_version='api',
        description='Payhere Swagger',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="test", email="test@test.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

# 토큰
token_patterns = [
    path('', MyTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
    path('balcklist/', TokenBlacklistView.as_view()),
    path('refresh/refresh_token', ApiRefreshRefreshTokenView.as_view())
]

user_patterns = [
    path('signup/', UserCreateApiView.as_view(), name='signup'),
    path('signup/UD/', UserApiView.as_view(), name='UDUser'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]

admin_patterns = [
    path('user/', users, name='user_list'),
    path('user/<int:user_id>', user_detail, name='user_detail')
]


urlpatterns = [
    # user
    path('user/', include(user_patterns)),

    # admin
    path('admin/', include(admin_patterns)),

    # 토큰 url
    path('token/', include(token_patterns)),

    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]