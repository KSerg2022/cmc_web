from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndOwnerOrIsStaff(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and (obj.owner == request.user or request.user.is_staff))


class IsAuthenticatedAndOwnerOrIsStaff_for_account(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and (obj.user == request.user or request.user.is_staff))
