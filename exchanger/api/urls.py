from django.urls import path, include
from rest_framework import routers


from exchanger.api.views import ExchangerViewSet, ExPortfolioViewSet
from exchanger.api.views_bot import ExchangerPortfolioForBot, ExchangerDataForBot, AllDataForBot

router = routers.DefaultRouter()
router.register(r'api/exchanger', ExchangerViewSet)
router.register(r'api/exportfolio', ExPortfolioViewSet)


from exchanger.api.views import ExchangerData, AllData

urlpatterns = [
    path('api/exchanger/data/<int:exchanger_id>/', ExchangerData.as_view(), name='exchanger-data'),
    path('api/user/data/all/', AllData.as_view(), name='all-data'),


    path('api/bot/exchanger-portfolio/', ExchangerPortfolioForBot.as_view(),
         name='exchanger-bot'),
    path('api/bot/exchanger-portfolio-data/', ExchangerDataForBot.as_view(),
         name='exchanger-data-bot'),

    path('api/bot/data-all/', AllDataForBot.as_view(),
         name='all-data-bot'),

    path('', include(router.urls)),
    ]

