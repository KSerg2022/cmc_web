from django.urls import path, include
from rest_framework import routers


from blockchain.api.views import BlockchainViewSet, BlockchainPortfolioViewSet, SendEmailData

router = routers.DefaultRouter()
router.register(r'api/blockchain-portfolio', BlockchainPortfolioViewSet, basename='portfolio')
router.register(r'api/blockchain', BlockchainViewSet)


from blockchain.api.views import BlockchainData

urlpatterns = [
    path('api/blockchain/data/<int:blockchain_id>/', BlockchainData.as_view(),
         name='blockchain-data'),
    path('api/send-email/data/<str:name>/', SendEmailData.as_view(),
         name='blockchain-data-email'),
    path('', include(router.urls)),
    ]
