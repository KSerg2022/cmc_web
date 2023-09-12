from django.urls import path, include
from rest_framework import routers


from blockchain.api.views import BlockchainData
from blockchain.api.views import BlockchainViewSet, BlockchainPortfolioViewSet, SendEmailData
from blockchain.api.views_bot import BlockchainDataForBot, BlockchainPortfolioForBot

router = routers.DefaultRouter()
router.register(r'api/blockchain-portfolio', BlockchainPortfolioViewSet, basename='portfolio')
router.register(r'api/blockchain', BlockchainViewSet)


urlpatterns = [
    path('api/blockchain/data/<int:blockchain_id>/', BlockchainData.as_view(),
         name='blockchain-data'),
    path('api/send-email/data/<str:portfolio>/', SendEmailData.as_view(),
         name='send-email-data'),


    path('api/bot/blockchain-portfolio/', BlockchainPortfolioForBot.as_view(),
         name='portfolio-bot'),
    path('api/bot/blockchain-portfolio-data/', BlockchainDataForBot.as_view(),
         name='blockchain-data-bot'),

    path('', include(router.urls)),
    ]
