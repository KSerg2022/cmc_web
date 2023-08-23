from django.urls import path, include
from rest_framework import routers


from exchanger.api.views import ExchangerViewSet, ExPortfolioViewSet

router = routers.DefaultRouter()
router.register(r'api/exchanger', ExchangerViewSet)
router.register(r'api/exportfolio', ExPortfolioViewSet)


from exchanger.api.views import ExchangerData, AllData

urlpatterns = [
    path('api/exchanger/data/<int:exchanger_id>/', ExchangerData.as_view(), name='exchanger-data'),
    path('api/user/data/all/', AllData.as_view(), name='all-data'),

    path('', include(router.urls)),
    ]

