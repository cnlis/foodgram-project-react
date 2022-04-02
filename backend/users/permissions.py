from rest_framework import permissions


class AllowNoOne(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
