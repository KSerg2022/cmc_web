import json
import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from account.models import Profile
from blockchain.api.serializers import BlockchainPortfolioSerializer
from blockchain.models import Blockchain, Portfolio
from blockchain.fixtures.handlers.load_blockchains_to_db import dump_to_db_blockchain


class BlockchainPortfolioForBotBase(TestCase):

    def setUp(self) -> None:
        self.name = 'Blockchain test'
        self.host = 'https://api.bscscan.com/api'
        self.api_key = 'api_key'
        self.blockchain1 = Blockchain.objects.create(name=self.name + '1',
                                                     host=self.host,
                                                     api_key=self.api_key)
        self.blockchain2 = Blockchain.objects.create(name=self.name + '2',
                                                     host=self.host,
                                                     api_key=self.api_key)
        self.wallet = 'wallet'
        self.owner1 = User.objects.create(username='User1',
                                          password='password1')
        self.owner2 = User.objects.create(username='User2',
                                          password='password1')
        self.admin = User.objects.create(username='User3',
                                         password='password1',
                                         is_staff=True)
        self.telegram1 = '@telegram1'
        self.telegram2 = '@telegram2'
        self.telegram3 = '@admin'
        self.profile_user1 = Profile.objects.create(owner=self.owner1,
                                                    telegram=self.telegram1)
        self.profile_user1 = Profile.objects.create(owner=self.owner2,
                                                    telegram=self.telegram2)
        self.profile_admin = Profile.objects.create(owner=self.admin,
                                                    telegram=self.telegram3)
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
                           "GMI": "0x93D8d25E3C9A847a5Da79F79ecaC89461FEcA846"}

        self.endpoint_list = 'portfolio-bot'

    def tearDown(self) -> None:
        Portfolio.objects.all().delete()
        Blockchain.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def create_portfolio(self):
        self.portfolio_1 = Portfolio.objects.create(owner=self.owner1,
                                                    blockchain=self.blockchain1,
                                                    wallet=self.wallet,
                                                    currencies=self.currencies)
        self.portfolio_2 = Portfolio.objects.create(owner=self.owner2,
                                                    blockchain=self.blockchain2,
                                                    wallet=self.wallet,
                                                    currencies=self.currencies)
        self.portfolio_3 = Portfolio.objects.create(owner=self.admin,
                                                    blockchain=self.blockchain1,
                                                    wallet=self.wallet,
                                                    currencies=self.currencies)
        self.portfolio_4 = Portfolio.objects.create(owner=self.owner1,
                                                    blockchain=self.blockchain2,
                                                    wallet=self.wallet,
                                                    currencies=self.currencies)

    def get_serializer_data(self, url, portfolio=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        if portfolio is None:
            return BlockchainPortfolioSerializer([self.portfolio_1, self.portfolio_2,
                                                  self.portfolio_3, self.portfolio_4],
                                                 many=True,
                                                 context=serializer_context).data
        return BlockchainPortfolioSerializer([*portfolio],
                                             many=True,
                                             context=serializer_context).data


class BlockchainPortfolioForBotApiTestCase(APITestCase, BlockchainPortfolioForBotBase):

    def setUp(self) -> None:
        super(BlockchainPortfolioForBotApiTestCase, self).setUp()
        self.client.force_login(user=self.owner1)

    def test_get(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list, args=(self.telegram1,))
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_1, self.portfolio_4])

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_not_owner_telegram(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list, args=('@telegram4',))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

    def test_get_ordering_blockchain(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list,  args=(self.telegram1,))
        response = self.client.get(url, data={'ordering': 'blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_1, self.portfolio_4])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_4, self.portfolio_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(0, Portfolio.objects.all().count())

        url = reverse(self.endpoint_list,  args=(self.telegram1,))
        data = {
            'owner': 1,
            'slug': '_',
            'blockchain': self.blockchain1.id,
            'wallet': self.wallet,
            'currencies': self.currencies
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code, response.data)
        self.assertEqual({'detail':  ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed')},
                         response.data)


class BlockchainDataForBot(APITestCase, TestCase):

    def setUp(self) -> None:
        dump_to_db_blockchain()
        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8"}

        self.user1 = User.objects.create_user(username='User1',
                                              password='password1')
        self.user2 = User.objects.create_user(username='User2',
                                              password='password2')
        self.admin = User.objects.create_superuser(username='Admin',
                                                   password='password2')
        self.telegram1 = '@telegram1'
        self.telegram2 = '@telegram2'
        self.telegram3 = '@admin'
        self.profile_user1 = Profile.objects.create(owner=self.user1,
                                                    telegram=self.telegram1)
        self.profile_user1 = Profile.objects.create(owner=self.user2,
                                                    telegram=self.telegram2)
        self.profile_admin = Profile.objects.create(owner=self.admin,
                                                    telegram=self.telegram3)

        self.blockchain = Blockchain.objects.get(name='BSC')
        self.portfolio1 = Portfolio.objects.create(owner=self.user1,
                                                   blockchain=self.blockchain,
                                                   wallet=self.wallet,
                                                   currencies=self.currencies)
        self.endpoint = 'blockchain-data-bot'

    def tearDown(self) -> None:
        Portfolio.objects.all().delete()
        Blockchain.objects.all().delete()
        User.objects.all().delete()

    def test_get_owner(self):
        self.client.force_login(user=self.user1)
        url = reverse(self.endpoint, args=(self.blockchain.id, self.telegram1, ))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(self.blockchain.name, list(response.data.keys())[0])
        self.assertEqual(len(self.currencies), len(list(response.data.values())[0]))

    def test_get_not_owner(self):
        self.client.force_login(user=self.user2)
        url = reverse(self.endpoint, args=(self.blockchain.id, self.telegram2, ))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='Not found.', code='not_found')}, response.data)

