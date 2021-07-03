from rest_framework.permissions import BasePermission


class CoursePermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST' and not request.user.is_staff:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['POST', 'PUT', 'PATCH'] and request.user.is_authenticated:
            return True
        elif request.method == 'DELETE' and (request.user.id == obj.owner.id):
            return True
        return False
