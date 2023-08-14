from rest_framework import viewsets
from rest_framework import permissions

from exchanger.models import Exchanger, ExPortfolio
from exchanger.api.cerializers import ExchangerSerializer, ExPortfolioSerializer


class ExchangerViewSet(viewsets.ModelViewSet):
    queryset = Exchanger.objects.all()
    serializer_class = ExchangerSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ExPortfolioViewSet(viewsets.ModelViewSet):
    queryset = ExPortfolio.objects.all()
    serializer_class = ExPortfolioSerializer
    # permission_classes = [permissions.IsAuthenticated]
