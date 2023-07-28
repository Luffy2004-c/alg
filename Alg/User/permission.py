from rest_framework import permissions


class Userpermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 超级管理员可以获取每个人的信息
        if request.user.is_superuser:
            return True

        # 用户只能获取自己的信息
        return obj == request.user
