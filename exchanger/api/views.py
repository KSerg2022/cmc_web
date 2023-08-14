from rest_framework import viewsets
from rest_framework import permissions

from exchanger.models import Exchanger
from exchanger.api.cerializers import ExchangerSerializer


class ExchangerViewSet(viewsets.ModelViewSet):
    queryset = Exchanger.objects.all()
    serializer_class = ExchangerSerializer
    # permission_classes = [permissions.IsAuthenticated]
