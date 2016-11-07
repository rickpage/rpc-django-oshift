from rest_framework import permissions
from django.contrib.auth.models import Group

def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns
      `True` if the user is in that group.
    """
    return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()


class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in ANY of the listed required groups
    - unless they are have is_superuser = True.
    Set the required groups on the view as an attribute i.e.
    required_groups = { 'GET' : "Admins" }
    """
    # TODO: Manage the names / ids against the database or ensure DB is populated
    ADMIN = "Admin"
    MODERATOR = "Moderator"

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(view, 'required_groups', {})

        # TODO: Throw an error if empty group, because we migth have forgot a group assignment!

        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])

        # Return True if the user has all the required groups.
        return request.user.is_superuser or any([is_in_group(request.user, group_name) for group_name in required_groups])


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
