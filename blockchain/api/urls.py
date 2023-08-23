from django.urls import path, include
from rest_framework import routers


from blockchain.api.views import BlockchainViewSet, BlockchainPortfolioViewSet

router = routers.DefaultRouter()
router.register(r'api/blockchain-portfolio', BlockchainPortfolioViewSet, basename='portfolio')
router.register(r'api/blockchain', BlockchainViewSet)


from blockchain.api.views import BlockchainData

urlpatterns = [
    path('api/blockchain/data/<int:blockchain_id>/', BlockchainData.as_view(), name='blockchain-data'),
    path('', include(router.urls)),
    ]
