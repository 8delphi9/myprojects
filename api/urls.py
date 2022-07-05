from django.urls import path
from user.views import UserCreateApi


urlpatterns = [
    path('register/', UserCreateApi.as_view()),
]