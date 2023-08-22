
from django.contrib.auth.models import User
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser

from account.api.permissions import IsAuthenticatedAndOwnerOrIsStaff, IsAuthenticatedAndOwnerOrIsStaff_for_user
from account.models import Profile
from account.api.serializers import UserSerializer, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['username', 'is_active']
    search_fields = ['username', 'is_active']
    ordering_fields = ['username', ]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedAndOwnerOrIsStaff]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner__username', 'date_of_birth']
    search_fields = ['owner__username', 'date_of_birth']
    ordering_fields = ['owner__username', 'date_of_birth']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
