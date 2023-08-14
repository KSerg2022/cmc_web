
from rest_framework import viewsets
from rest_framework import permissions

from blockchain.models import Blockchain, Portfolio
from blockchain.api.serializers import BlockchainSerializer, BlockchainPortfolioSerializer


class BlockchainViewSet(viewsets.ModelViewSet):
    queryset = Blockchain.objects.all()
    serializer_class = BlockchainSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BlockchainPortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = BlockchainPortfolioSerializer
    # permission_classes = [permissions.IsAuthenticated]
