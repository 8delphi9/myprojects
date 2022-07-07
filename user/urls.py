from user.views import (
    UserDetailAPIView,
    UserAPIView,
    LogoutAPIView,
    UserReadAPIView,
)

users = UserAPIView.as_view({
    'get': 'list'
})

login = UserAPIView.as_view({
    'post': 'login'
})

logout = LogoutAPIView.as_view({
    'post': 'logout'
})

user_detail = UserDetailAPIView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

user_update = UserReadAPIView.as_view({
    'get': 'retrieve',
})