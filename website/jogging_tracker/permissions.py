from rest_framework import permissions
from .models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or User.objects.filter(role="admin").exists()


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            User.objects.filter(role="manager").exists()
            or User.objects.filter(role="admin").exists()
        )
