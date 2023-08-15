from rest_framework import serializers


from blockchain.models import Blockchain, Portfolio


# class BlockchainSerializer(serializers.HyperlinkedModelSerializer):
class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = '__all__'


class BlockchainPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

