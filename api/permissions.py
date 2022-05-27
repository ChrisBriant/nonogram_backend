# permissions.py

from rest_framework import permissions
from .models import ApiKey


class ValidApiKey(permissions.BasePermission):

    def has_permission(self, request, view):
        key = request.META.get('HTTP_AUTHORIZATION')
        if key:
            #Lookup the key
            try:
                ApiKey.objects.get(key=key)
            except Exception as e:
                print(e)
                return False
            return True
        return False

