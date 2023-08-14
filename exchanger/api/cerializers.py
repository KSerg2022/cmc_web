
from rest_framework import serializers


from exchanger.models import Exchanger


class ExchangerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exchanger
        # fields = ['url', 'username', 'email', 'is_staff']
        fields = '__all__'
