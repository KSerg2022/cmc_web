from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from blockchain.models import Blockchain, Portfolio
from blockchain.api.serializers import BlockchainSerializer, BlockchainPortfolioSerializer


class BlockchainViewSet(viewsets.ModelViewSet):
    queryset = Blockchain.objects.all()
    serializer_class = BlockchainSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active']
    search_fields = ['name', 'is_active']
    ordering_fields = ['id', 'name']


class BlockchainPortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = BlockchainPortfolioSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner__username', 'blockchain__name']
    search_fields = ['owner__username', 'blockchain__name']
    ordering_fields = ['owner', 'blockchain__name']
