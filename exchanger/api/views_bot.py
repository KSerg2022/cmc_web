from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response


from account.api.permissions import IsAuthenticatedBot, UserTelegramAuthentication
from exchanger.models import ExPortfolio
from exchanger.api.serializers import ExPortfolioSerializer
from exchanger.cache import check_caches_exchanger_data, check_cache_user_portfolios_data


class ExchangerPortfolioForBot(generics.ListAPIView):
    queryset = ExPortfolio.objects.all()
    serializer_class = ExPortfolioSerializer
    authentication_classes = [UserTelegramAuthentication]
    permission_classes = [IsAuthenticatedBot]
    ordering_fields = ['exchanger__name']

    def get(self, request, *args, **kwargs):
        """headers = {'TEL_USERNAME': tel_username}"""
        user = get_object_or_404(User, profile__telegram=request.META.get('HTTP_TEL_USERNAME'))
        portfolio = ExPortfolio.objects.filter(owner=user.id)
        portfolio = ExPortfolioSerializer(portfolio, many=True)

        return Response({'count': len(portfolio.data), 'results': portfolio.data})


class ExchangerDataForBot(generics.ListAPIView):
    queryset = ExPortfolio.objects.all()
    authentication_classes = [UserTelegramAuthentication]
    permission_classes = [IsAuthenticatedBot]

    def get(self, request, *args, **kwargs):
        """headers = {'TEL_USERNAME': tel_username},
                       'USER_PORTFOLIO_ID': user_portfolio_id}"""
        user = get_object_or_404(User, profile__telegram=request.META.get('HTTP_TEL_USERNAME'))
        portfolio = get_object_or_404(ExPortfolio,
                                      owner=user.id,
                                      exchanger=request.META.get('HTTP_USER_PORTFOLIO_ID'))

        response_blockchain, total_sum = check_caches_exchanger_data(portfolio)

        return Response({portfolio.exchanger.name: [response_blockchain, total_sum]})


class AllDataForBot(generics.ListAPIView):
    authentication_classes = [UserTelegramAuthentication]
    permission_classes = [IsAuthenticatedBot]

    def get(self, request, *args, **kwargs):
        """headers = {'TEL_USERNAME': tel_username}"""
        user = get_object_or_404(User, profile__telegram=request.META.get('HTTP_TEL_USERNAME'))
        if user:
            user_portfolios_data = check_cache_user_portfolios_data(user.id)
            return Response({self.request.user.username: user_portfolios_data})

        return HttpResponseForbidden()
