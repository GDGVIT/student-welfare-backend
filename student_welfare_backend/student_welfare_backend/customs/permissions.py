from rest_framework.permissions import BasePermission


# Faculty field of User model is used to determine whether the user is a faculty or not
class IsFaculty(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_faculty

    def has_object_permission(self, request, view, obj):
        return request.user.is_faculty


# IsDSW field to see if user in DSW or not
class IsDSW(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_dsw | request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_dsw | request.user.is_superuser


# IsADSW field to see if user in ADSW or not
class IsADSW(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_adsw | request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_adsw | request.user.is_superuser