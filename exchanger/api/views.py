from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from account.api.permissions import IsAuthenticatedAndOwnerOrIsStaff, IsAuthenticatedAndOwner
from exchanger.models import Exchanger, ExPortfolio
from exchanger.api.serializers import ExchangerSerializer, ExPortfolioSerializer
from exchanger.cache import check_caches_exchanger_data, check_cache_user_portfolios_data


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
    permission_classes = [IsAuthenticatedAndOwnerOrIsStaff]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner__username', 'exchanger__name']
    search_fields = ['owner__username', 'exchanger__name']
    ordering_fields = ['owner', 'exchanger__name']


class ExchangerData(APIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedAndOwner]

    def get(self, request, exchanger_id, format=None):
        portfolio = get_object_or_404(ExPortfolio,
                                      owner=self.request.user.id,
                                      exchanger=exchanger_id)
        response_exchanger, total_sum = check_caches_exchanger_data(portfolio)

        return Response({portfolio.exchanger.name: [response_exchanger, total_sum]})


class AllData(APIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedAndOwner]

    def get(self, request, format=None):
        user_portfolios_data = check_cache_user_portfolios_data(self.request.user.id)

        return Response({self.request.user.username: user_portfolios_data})
