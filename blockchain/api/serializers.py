from rest_framework import serializers

from blockchain.models import Blockchain, Portfolio


class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = '__all__'


class BlockchainPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
        # fields = ['owner', 'blockchain', 'slug', 'wallet', 'comments', 'currencies']


# class BlockchainSerializer__(serializers.ModelSerializer):
#     class Meta:
#         model = Blockchain
#         fields = ['id', 'name']
#
#
# class UserSerializer__(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']
#
#
# class BlockchainPortfolioSerializer(serializers.ModelSerializer):
#     blockchain = BlockchainSerializer__(read_only=True)
#     owner = UserSerializer__(read_only=True)
#
#     class Meta:
#         model = Portfolio
#         fields = '__all__'

