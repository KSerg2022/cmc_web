from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from exchanger.models import Exchanger, ExPortfolio
from exchanger.api.serializers import ExchangerSerializer, ExPortfolioSerializer


class ExchangerViewSet(viewsets.ModelViewSet):
    queryset = Exchanger.objects.all()
    serializer_class = ExchangerSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active']
    search_fields = ['name', 'is_active']
    ordering_fields = ['id', 'name']


class ExPortfolioViewSet(viewsets.ModelViewSet):
    queryset = ExPortfolio.objects.all()
    serializer_class = ExPortfolioSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner__username', 'exchanger__name']
    search_fields = ['owner__username', 'exchanger__name']
    ordering_fields = ['owner', 'exchanger__name']
