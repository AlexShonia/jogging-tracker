from rest_framework import permissions
from jogging_tracker.models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role == "admin"


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin" or request.user.role == "manager"
