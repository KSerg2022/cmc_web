from django.contrib.auth.models import User

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions


class IsAuthenticatedAndOwner(BasePermission):
    """
    Allows access only to authenticated users and (owner objects is current user or user is is_staff==True)
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and obj.owner == request.user)


class IsAuthenticatedAndOwnerOrIsStaff(BasePermission):
    """
    Allows access only to authenticated users and (owner objects is current user or user is is_staff==True)
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and (obj.owner == request.user or request.user.is_staff))


class IsAuthenticatedAndOwnerOrIsStaff_for_user(BasePermission):
    """
    Allows access only to authenticated users and (current user or user is is_staff==True)
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and (obj == request.user or request.user.is_staff))


from cmc.models import pwd_verify


class IsAuthenticatedBot(BasePermission):
    """
    Allows access only to authenticated users and (owner objects is current user or user is is_staff==True)
    """

    def has_permission(self, request, view):
        verify = pwd_verify(request.META.get('HTTP_BOT_NAME'),
                            request.META.get('HTTP_USER_NAME'),
                            request.META.get('HTTP_CHAT_ID'),
                            )
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user.profile.telegram == request.META.get('HTTP_TEL_USERNAME') and
                    verify
                    )


class UserTelegramAuthentication(BaseAuthentication):
    def authenticate(self, request):
        tel_username = request.META.get('HTTP_TEL_USERNAME')
        if not tel_username:
            return None
        try:
            user = User.objects.get(profile__telegram=tel_username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        if user and user.is_active:
            return (user, None)
