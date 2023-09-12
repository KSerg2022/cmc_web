from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics

from account.api.permissions import IsAuthenticatedBot, UserTelegramAuthentication
from blockchain.models import Portfolio
from blockchain.api.serializers import BlockchainPortfolioSerializer
from blockchain.cache import check_caches_blockchain_data


class BlockchainPortfolioForBot(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = BlockchainPortfolioSerializer
    authentication_classes = [UserTelegramAuthentication]
    permission_classes = [IsAuthenticatedBot]
    ordering_fields = ['blockchain__name']

    def get(self, request, *args, **kwargs):
        """headers = {'TEL_USERNAME': tel_username}"""
        user = get_object_or_404(User, profile__telegram=request.META.get('HTTP_TEL_USERNAME'))
        portfolio = Portfolio.objects.filter(owner=user.id)
        portfolio = BlockchainPortfolioSerializer(portfolio, many=True)

        return Response({'count': len(portfolio.data), 'results': portfolio.data})


class BlockchainDataForBot(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    authentication_classes = [UserTelegramAuthentication]
    permission_classes = [IsAuthenticatedBot]

    def get(self, request, *args, **kwargs):
        """headers = {'TEL_USERNAME': tel_username},
                       'USER_PORTFOLIO_ID': user_portfolio_id}"""
        user = get_object_or_404(User, profile__telegram=request.META.get('HTTP_TEL_USERNAME'))
        portfolio = get_object_or_404(Portfolio,
                                      owner=user.id,
                                      blockchain=request.META.get('HTTP_USER_PORTFOLIO_ID'))
        response_blockchain, total_sum = check_caches_blockchain_data(portfolio)

        return Response({portfolio.blockchain.name: [response_blockchain, total_sum]})

