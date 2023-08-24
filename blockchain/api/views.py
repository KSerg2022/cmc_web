from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from local_settings import ALL_PORTFOLIOS
from account.api.permissions import IsAuthenticatedAndOwnerOrIsStaff, IsAuthenticatedAndOwner
from blockchain.models import Blockchain, Portfolio
from blockchain.api.serializers import BlockchainSerializer, BlockchainPortfolioSerializer
from blockchain.cache import check_caches_blockchain_data
from exchanger.tasks import sending_PDF_by_email

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


class BlockchainData(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedAndOwner]

    def get(self, request, blockchain_id, format=None):
        portfolio = get_object_or_404(Portfolio,
                                      owner=self.request.user.id,
                                      blockchain=blockchain_id)

        response_blockchain, total_sum = check_caches_blockchain_data(portfolio)

        return Response({portfolio.blockchain.name: [response_blockchain, total_sum]})


class SendEmailData(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedAndOwner]

    def get(self, request, portfolio='all', format=None):
        if portfolio == 'all':
            portfolio = ALL_PORTFOLIOS
        xlsx_dir = settings.MEDIA_URL + 'xlsx_files/' + f'{request.user.id}_{request.user.username.lower()}/'
        filename = f'{request.user.id}_{request.user.username.lower()}_{portfolio}.pdf'
        path_to_file = xlsx_dir + filename


        sending_PDF_by_email.delay(user_id=self.request.user.id,
                                   path_to_file=path_to_file,
                                   portfolio=portfolio)
        messages = f'Portfolios "{portfolio.capitalize()}" were send to your email.'
        return Response({'messages': messages})
