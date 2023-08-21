
from django.contrib.auth.models import User
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from account.api.permissions import IsAuthenticatedAndOwnerOrIsStaff_for_account
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
    permission_classes = [IsAuthenticatedAndOwnerOrIsStaff_for_account]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__username', 'date_of_birth']
    search_fields = ['user__username', 'date_of_birth']
    ordering_fields = ['user__username', 'date_of_birth']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
