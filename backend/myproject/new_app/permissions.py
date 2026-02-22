from rest_framework.permissions import BasePermission

class CheckRolePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role_user == 'student'

class CreateUniversityPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role_user == 'owner'