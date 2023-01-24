from rest_framework import permissions


class IsAuthorOrAdminOrPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.post.owner:
            return True
        return request.user == obj.owner
