from django.urls import path, include
from rest_framework import routers


from exchanger.api.views import ExchangerViewSet

router = routers.DefaultRouter()
router.register(r'api/exchanger', ExchangerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    ]

