from rest_framework.permissions import IsAuthenticated, BasePermission
from authe.models import MainUser


class IsOwner(IsAuthenticated):
    message = 'You must be the owner.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class BlockPermission(BasePermission):
    message = 'You must be the owner of the project.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action is not 'list':
            return request.user == obj.project.creator


class TaskPermission(BasePermission):
    message = 'You must be the owner of the project or task.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action in ['list', 'create']:
            return True
        if view.action not in ['list', 'create']:
            return request.user in [obj.block.project.creator, obj.creator]


class TaskInsidePermission(BasePermission):
    message = 'You must be the owner of the project or task or comment/document.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action is 'list':
            return True
        if view.action is not 'list':
            return request.user in [obj.task.creator, obj.task.block.project.creator, obj.creator]
