from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response


class IsAuthorOrSuperuserElseReadOnly(BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(request.user.is_superuser or obj.author == request.user or request.method in SAFE_METHODS)
	def has_permission(self, request, view):
		return bool(request.user.is_authenticated or request.method in SAFE_METHODS)

class IsSuperuser(BasePermission):
	def has_object_permission(self, request):
		return request.user.is_superuser
	def has_permission(self, request):
		return request.user.is_superuser