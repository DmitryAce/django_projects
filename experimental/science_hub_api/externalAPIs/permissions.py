from rest_framework import permissions
from .models import ApiKey

class CanAccessArticles(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.auth, ApiKey):
            return request.auth.can_access_articles
        return False