from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blockchain.api.cerializers import BlockchainSerializer, BlockchainPortfolioSerializer
from blockchain.api.views import BlockchainViewSet
from blockchain.models import Blockchain, Portfolio


class BlockchainBase(TestCase):
    def setUp(self) -> None:
        self.name = 'Blockchain test'
        self.slug = 'blockchain-test'
        self.host = 'https://api.bscscan.com/api'
        self.api_key = 'api_key'
        self.logo = 'tests/account/data_for_test/black.jpg'

    def tearDown(self) -> None:
        Blockchain.objects.all().delete()

    def create_blockchains(self):
        self.blockchain_1 = Blockchain.objects.create(name=self.name + '1',
                                                      slug=self.slug + '1',
                                                      host=self.host + '1',
                                                      api_key=self.api_key + '1',
                                                      logo=self.logo + '1')
        self.blockchain_2 = Blockchain.objects.create(name=self.name + '2',
                                                      slug=self.slug + '2',
                                                      host=self.host + '2',
                                                      api_key=self.api_key + '2',
                                                      logo=self.logo + '2')

    def get_serializer_data(self, url):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        return BlockchainSerializer([self.blockchain_1, self.blockchain_2], many=True,
                                    context=serializer_context).data


class BlockchainApiTestCase(APITestCase, BlockchainBase):

    def test_get(self):
        self.create_blockchains()
        url = reverse('blockchain-list')
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class BlockchainSerializerTestCase(BlockchainBase):

    def test_blockchain_serializer(self):
        self.create_blockchains()
        url = reverse('blockchain-list')
        serializer_data = self.get_serializer_data(url)
        expected_data = [
            {
                'id': self.blockchain_1.id,
                'name': 'Blockchain test1',
                'slug': 'blockchain-test1',
                'host': 'https://api.bscscan.com/api1',
                'api_key': 'api_key1',
                'is_active': True,
                'logo': 'http://testserver/media/tests/account/data_for_test/black.jpg1',
                'website': '',
                'scan_site': ''

            },
            {
                'id': self.blockchain_2.id,
                'name': 'Blockchain test2',
                'slug': 'blockchain-test2',
                'host': 'https://api.bscscan.com/api2',
                'api_key': 'api_key2',
                'is_active': True,
                'logo': 'http://testserver/media/tests/account/data_for_test/black.jpg2',
                'website': '',
                'scan_site': ''
            }
        ]

        self.assertEqual(expected_data, serializer_data)


class BlockchainPortfolioBase(TestCase):

    def setUp(self) -> None:
        self.name = 'Blockchain test'
        self.host = 'https://api.bscscan.com/api'
        self.api_key = 'api_key'
        self.blockchain = Blockchain.objects.create(name=self.name,
                                                    host=self.host,
                                                    api_key=self.api_key)
        self.wallet = 'wallet'
        self.owner = User.objects.create(username='User1',
                                         password='password1')
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
                           "GMI": "0x93D8d25E3C9A847a5Da79F79ecaC89461FEcA846"}

    def tearDown(self) -> None:
        Portfolio.objects.all().delete()
        User.objects.all().delete()

    def create_portfolio(self):
        self.portfolio_1 = Portfolio.objects.create(owner=self.owner,
                                                    blockchain=self.blockchain,
                                                    wallet=self.wallet,
                                                    currencies=self.currencies)

    def get_serializer_data(self, url):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        return BlockchainPortfolioSerializer([self.portfolio_1], many=True,
                                             context=serializer_context).data


class BlockchainPortfolioApiTestCase(APITestCase, BlockchainPortfolioBase):

    def test_get(self):
        self.create_portfolio()
        url = reverse('portfolio-list')
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class BlockchainPortfolioSerializerTestCase(BlockchainPortfolioBase):

    def test_blockchain_portfolio_serializer(self):
        self.create_portfolio()
        url = reverse('portfolio-list')
        serializer_data = self.get_serializer_data(url)
        expected_data = [
            {
                'id': self.portfolio_1.id,
                'slug':  'user1-blockchain-test',
                'wallet': self.wallet,
                'comments': '',
                'currencies': self.currencies,
                'owner': self.owner.id,
                'blockchain': self.blockchain.id
            },
        ]

        self.assertEqual(expected_data, serializer_data)

