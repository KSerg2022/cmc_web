from django.urls import path, include
from rest_framework import routers


from blockchain.api.views import BlockchainViewSet, BlockchainPortfolioViewSet

router = routers.DefaultRouter()
router.register(r'api/blockchain-portfolio', BlockchainPortfolioViewSet, basename='portfolio')
router.register(r'api/blockchain', BlockchainViewSet)


urlpatterns = [
    path('', include(router.urls)),
    ]
