from django.urls import path, include
from rest_framework import routers


from exchanger.api.views import ExchangerViewSet, ExPortfolioViewSet

router = routers.DefaultRouter()
router.register(r'api/exchanger', ExchangerViewSet)
router.register(r'api/exportfolio', ExPortfolioViewSet)


urlpatterns = [
    path('', include(router.urls)),
    ]

