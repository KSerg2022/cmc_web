from rest_framework import serializers


from blockchain.models import Blockchain, Portfolio


class BlockchainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blockchain
        # fields = ['url', 'username', 'email', 'is_staff']
        fields = '__all__'


class BlockchainPortfolioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

