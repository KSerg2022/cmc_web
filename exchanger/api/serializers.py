
from rest_framework import serializers


from exchanger.models import Exchanger, ExPortfolio


class ExchangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchanger
        fields = '__all__'


class ExPortfolioSerializer(serializers.ModelSerializer):
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ExPortfolio
        fields = '__all__'
