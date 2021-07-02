from rest_framework.permissions import BasePermission


class CoursePermissions(BasePermission):

    def has_permission(self, request, view):
        print('has_permissions')
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        print('has_object_permissions')
        return super().has_object_permission(request, view, obj)
