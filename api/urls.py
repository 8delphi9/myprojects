from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from user.views import (
    LoginAPI, UserCreateApi
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

login = LoginAPI.as_view({
    'post': 'login'
})


schema_view = get_schema_view(
    openapi.Info(
        title='Swagger Payhere',
        default_version='api',
        description='LabQ API',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="test", email="test@test.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)



# 토큰
token_patterns = [
    path('', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
]

user_patterns = [
    path('login/', login),
    path('register/', UserCreateApi.as_view())
]


urlpatterns = [
    # user
    path('user/', include(user_patterns)),

    # 토큰 url
    path('token/', include(token_patterns)),

    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]