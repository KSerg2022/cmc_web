from rest_framework.permissions import BasePermission, SAFE_METHODS


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


class IsAuthenticatedBot(BasePermission):
    """
    Allows access only to authenticated users and (owner objects is current user or user is is_staff==True)
    """
    def has_permission(self, request, view):
        # print('+++++++', view.__dict__)

        # user = get_object_or_404(User, profile__telegram=view.kwargs['tel_username'])
        return bool(
            request.user and
            request.user.is_authenticated and
            # user and
            request.user.profile.telegram == view.kwargs['tel_username'])


class IsAuthenticatedAndOwnerOrIsStaff_for_user(BasePermission):
    """
    Allows access only to authenticated users and (current user or user is is_staff==True)
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and (obj == request.user or request.user.is_staff))
