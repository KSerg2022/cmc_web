from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from account.api.permissions import IsAuthenticatedAndOwnerOrIsStaff
from blockchain.models import Blockchain, Portfolio
from blockchain.api.serializers import BlockchainSerializer, BlockchainPortfolioSerializer


class BlockchainViewSet(viewsets.ModelViewSet):
    queryset = Blockchain.objects.all()
    serializer_class = BlockchainSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active']
    search_fields = ['name', 'is_active']
    ordering_fields = ['id', 'name']


class BlockchainPortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = BlockchainPortfolioSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner__username', 'blockchain__name']
    search_fields = ['owner__username', 'blockchain__name']
    ordering_fields = ['owner', 'blockchain__name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.user.is_staff:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedAndOwnerOrIsStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Portfolio.objects.all()
        else:
            if not self.request.user.id:
                return Portfolio.objects.none()
            return Portfolio.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
