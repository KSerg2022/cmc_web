from django.urls import path, include
from rest_framework import routers


from blockchain.api.views import BlockchainViewSet, BlockchainPortfolioViewSet

router = routers.DefaultRouter()
router.register(r'api/blockchain', BlockchainViewSet)
router.register(r'api/blockchain-portfolio', BlockchainPortfolioViewSet)


urlpatterns = [
    path('', include(router.urls)),
    ]
