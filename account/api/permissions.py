from rest_framework.permissions import BasePermission, SAFE_METHODS


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
