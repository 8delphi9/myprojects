from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    author : 이승미
    explanation :
         - 퍼미션 커스텀
         - 사용자 본인이 작성한 가계부 또는 유저의 정보의 접근 권한을 갖도록 구현함.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.id == obj.id:
                return True
            return False
        else:
            return False