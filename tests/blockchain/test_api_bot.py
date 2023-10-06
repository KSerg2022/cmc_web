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
from cmc.models import TelegramBot


class BlockchainPortfolioForBotBase(TestCase):

    def setUp(self) -> None:
        self.bot_name = 'bot_name',
        self.username = 'username',
        self.bot_token = 'bot_token',
        self.chat_id = '123456'
        self.telegram = TelegramBot.objects.create(bot_name=self.bot_name,
                                                   username=self.username,
                                                   bot_token=self.bot_token,
                                                   chat_id=self.chat_id)
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
        self.telegram1 = 'telegram1'
        self.telegram2 = 'telegram2'
        self.telegram3 = 'admin'
        self.profile_owner1 = Profile.objects.create(owner=self.owner1,
                                                    telegram=self.telegram1)
        self.profile_owner2 = Profile.objects.create(owner=self.owner2,
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

    def test_get(self):
        self.client.logout()
        self.create_portfolio()
        url = reverse(self.endpoint_list, )
        headers = {'TEL-USERNAME': self.telegram1,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                   }
        response = self.client.get(url, headers=headers)
        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_1, self.portfolio_4])

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_not_exist_telegram(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list, )
        headers = {'TEL_USERNAME': 'telegram4',
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                  }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='No such user', code='authentication_failed')}, response.data)

    def test_get_ordering_blockchain(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                  }
        response = self.client.get(url,
                                   headers=headers,
                                   data={'ordering': 'blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_1, self.portfolio_4])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url,
                                   headers=headers,
                                   data={'ordering': '-blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_4, self.portfolio_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, Portfolio.objects.all().count())
        url = reverse(self.endpoint_list, )
        data = {
            'owner': 1,
            'slug': '_',
            'blockchain': self.blockchain1.id,
            'wallet': self.wallet,
            'currencies': self.currencies
        }
        json_data = json.dumps(data)
        headers = {'TEL_USERNAME': self.telegram1,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                  }
        response = self.client.post(url,
                                    headers=headers,
                                    data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed')},
                         response.data)


class BlockchainDataForBot(APITestCase, TestCase):

    def setUp(self) -> None:
        self.bot_name = 'bot_name',
        self.username = 'username',
        self.bot_token = 'bot_token',
        self.chat_id = '123456'
        self.telegram = TelegramBot.objects.create(bot_name=self.bot_name,
                                                   username=self.username,
                                                   bot_token=self.bot_token,
                                                   chat_id=self.chat_id)
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
        self.telegram1 = 'telegram1'
        self.telegram2 = 'telegram2'
        self.telegram3 = 'admin'
        self.profile_user1 = Profile.objects.create(owner=self.user1,
                                                    telegram=self.telegram1)
        self.profile_user2 = Profile.objects.create(owner=self.user2,
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
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'USER_PORTFOLIO_ID': self.blockchain.id,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                  }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(self.blockchain.name, list(response.data.keys())[0], response.data)
        self.assertEqual(len(self.currencies), len(list(response.data.values())[0]))

    def test_get_not_exist_user(self):
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': 'telegram',
                   'USER_PORTFOLIO_ID': self.blockchain.id,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                  }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='No such user', code='authentication_failed')}, response.data)

    def test_get_owner_and_not_exist_portfolio(self):
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'USER_PORTFOLIO_ID': 25,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                  }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='Not found.', code='not_found')}, response.data)
