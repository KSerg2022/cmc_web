from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics

from account.api.permissions import IsAuthenticatedBot
from blockchain.models import Portfolio
from blockchain.api.serializers import BlockchainPortfolioSerializer
from blockchain.cache import check_caches_blockchain_data


class BlockchainPortfolioForBot(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = BlockchainPortfolioSerializer
    permission_classes = [IsAuthenticatedBot]
    ordering_fields = ['blockchain__name']

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, profile__telegram=kwargs['tel_username'])
        portfolio = Portfolio.objects.filter(owner=user.id)

        portfolio = BlockchainPortfolioSerializer(portfolio, many=True)

        return Response({'count': len(portfolio.data), 'results': portfolio.data})


class BlockchainDataForBot(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedBot]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, profile__telegram=kwargs['tel_username'])
        portfolio = get_object_or_404(Portfolio,
                                      owner=user.id,
                                      blockchain=kwargs['blockchain_id'])

        response_blockchain, total_sum = check_caches_blockchain_data(portfolio)

        return Response({portfolio.blockchain.name: [response_blockchain, total_sum]})

