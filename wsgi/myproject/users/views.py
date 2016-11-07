from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import UserSerializer, GroupSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import DjangoModelPermissions
from myproject.permissions import HasGroupPermission

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # Demonstare DjangoModelPermissions
    permission_classes = (DjangoModelPermissions,)
    # required_groups = {
    #      'GET': [HasGroupPermission.ADMIN, HasGroupPermission.MODERATOR],
    #      'POST': [HasGroupPermission.ADMIN],
    # }

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # Demonstrate how to use HasGroupPermission
    permission_classes = (HasGroupPermission,)
    required_groups = {
         'GET': [HasGroupPermission.ADMIN],
         'POST': [HasGroupPermission.ADMIN],
     }
