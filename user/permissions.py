from rest_framework.permissions import BasePermission


class IsRecordUserOrUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.id == obj.id:
                return True
            return False
        else:
            return False