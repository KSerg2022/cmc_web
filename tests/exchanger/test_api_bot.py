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


from blockchain.fixtures.handlers.load_blockchains_to_db import dump_to_db_blockchain
from blockchain.models import Blockchain, Portfolio
from cmc.models import TelegramBot
from exchanger.api.serializers import ExchangerSerializer, ExPortfolioSerializer
from exchanger.models import Exchanger, ExPortfolio
from exchanger.fixtures.handlers.load_exchangers_to_db import dump_to_db_exchanger


class ExchangerPortfolioForBotBase(TestCase):

    def setUp(self) -> None:
        self.bot_name = 'bot_name',
        self.username = 'username',
        self.bot_token = 'bot_token',
        self.chat_id = '123456'
        self.telegram = TelegramBot.objects.create(bot_name=self.bot_name,
                                                   username=self.username,
                                                   bot_token=self.bot_token,
                                                   chat_id=self.chat_id)
        self.name = 'Exchanger_'
        self.host = 'https://www.okx.com'
        self.exchanger1 = Exchanger.objects.create(name=self.name + '1',
                                                   host=self.host)
        self.exchanger2 = Exchanger.objects.create(name=self.name + '2',
                                                   host=self.host)
        self.api_key = 'api_key'
        self.api_secret = 'api_secret'
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
        self.profile_user1 = Profile.objects.create(owner=self.owner1,
                                                    telegram=self.telegram1)
        self.profile_user2 = Profile.objects.create(owner=self.owner2,
                                                    telegram=self.telegram2)
        self.profile_admin = Profile.objects.create(owner=self.admin,
                                                    telegram=self.telegram3)

        self.endpoint_list = 'exchanger-bot'

    def tearDown(self) -> None:
        ExPortfolio.objects.all().delete()
        Exchanger.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def create_portfolio(self):
        self.portfolio_1 = ExPortfolio.objects.create(exchanger=self.exchanger1,
                                                      api_key=self.api_key,
                                                      api_secret=self.api_secret,
                                                      owner=self.owner1)
        self.portfolio_2 = ExPortfolio.objects.create(exchanger=self.exchanger2,
                                                      api_key=self.api_key,
                                                      api_secret=self.api_secret,
                                                      owner=self.owner2)
        self.portfolio_3 = ExPortfolio.objects.create(exchanger=self.exchanger1,
                                                      api_key=self.api_key,
                                                      api_secret=self.api_secret,
                                                      owner=self.admin)
        self.portfolio_4 = ExPortfolio.objects.create(exchanger=self.exchanger2,
                                                      api_key=self.api_key,
                                                      api_secret=self.api_secret,
                                                      owner=self.owner1)

    def get_serializer_data(self, url, exchanger=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_context = {'request': Request(request), }

        if exchanger is None:
            return ExPortfolioSerializer([self.portfolio_1, self.portfolio_3, self.portfolio_2],
                                         many=True,
                                         context=serializer_context).data
        return ExPortfolioSerializer([*exchanger], many=True,
                                     context=serializer_context).data


class ExchangerPortfolioForBotApiTestCase(APITestCase, ExchangerPortfolioForBotBase):

    def test_get(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                   }
        response = self.client.get(url, headers=headers)
        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.portfolio_1, self.portfolio_4])

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
                                                   exchanger=[self.portfolio_1, self.portfolio_4])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url,
                                   headers=headers,
                                   data={'ordering': '-blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.portfolio_4, self.portfolio_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, Portfolio.objects.all().count())

        data = {
            'exchanger': self.exchanger1.id,
            'slug': '_',
            'api_key': 'new_api_key',
            'api_secret': self.api_secret,
            'owner': self.owner1.id,
        }
        json_data = json.dumps(data)

        url = reverse(self.endpoint_list, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                   }
        response = self.client.post(url,
                                    headers=headers,
                                    data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code, response.data)
        self.assertEqual({'detail':  ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed')},
                         response.data)


class ExchangerDataForBot(APITestCase, TestCase):

    def setUp(self) -> None:
        self.bot_name = 'bot_name',
        self.username = 'username',
        self.bot_token = 'bot_token',
        self.chat_id = '123456'
        self.telegram = TelegramBot.objects.create(bot_name=self.bot_name,
                                                   username=self.username,
                                                   bot_token=self.bot_token,
                                                   chat_id=self.chat_id)
        dump_to_db_exchanger()
        self.api_key = os.environ.get('OKX_API_KEY')
        self.api_secret = os.environ.get('OKX_API_SECRET_KEY')
        self.password = os.environ.get('OKX_PWD')
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

        self.exchanger = Exchanger.objects.get(id=1)
        self.portfolio1 = ExPortfolio.objects.create(owner=self.user1,
                                                     exchanger=self.exchanger,
                                                     api_key=self.api_key,
                                                     api_secret=self.api_secret,
                                                     password=self.password,
                                                     )
        self.endpoint = 'exchanger-data-bot'

    def tearDown(self) -> None:
        ExPortfolio.objects.all().delete()
        Exchanger.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_get_owner(self):
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'USER_PORTFOLIO_ID': self.exchanger.id,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                   }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(self.exchanger.name, list(response.data.keys())[0])

    def test_get_not_exist_user(self):
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': 'telegram',
                   'USER_PORTFOLIO_ID': self.exchanger.id,
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


class AllDataForBotApiTestCase(APITestCase, TestCase):

    def setUp(self) -> None:
        self.bot_name = 'bot_name',
        self.username = 'username',
        self.bot_token = 'bot_token',
        self.chat_id = '123456'
        self.telegram = TelegramBot.objects.create(bot_name=self.bot_name,
                                                   username=self.username,
                                                   bot_token=self.bot_token,
                                                   chat_id=self.chat_id)
        dump_to_db_exchanger()
        dump_to_db_blockchain()
        self.wallet = os.environ.get('WALLET_ADDRESS')

        self.api_key = os.environ.get('OKX_API_KEY')
        self.api_secret = os.environ.get('OKX_API_SECRET_KEY')
        self.password = os.environ.get('OKX_PWD')
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
        self.profile_user1 = Profile.objects.create(owner=self.user2,
                                                    telegram=self.telegram2)
        self.profile_admin = Profile.objects.create(owner=self.admin,
                                                    telegram=self.telegram3)

        self.exchanger = Exchanger.objects.get(id=1)
        self.portfolio_exchanger = ExPortfolio.objects.create(owner=self.user1,
                                                              exchanger=self.exchanger,
                                                              api_key=self.api_key,
                                                              api_secret=self.api_secret,
                                                              password=self.password,
                                                              )

        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8"}
        self.blockchain = Blockchain.objects.get(name='BSC')
        self.portfolio_blockchain = Portfolio.objects.create(owner=self.user1,
                                                             blockchain=self.blockchain,
                                                             wallet=self.wallet,
                                                             currencies=self.currencies)

        self.endpoint = 'all-data-bot'

    def tearDown(self) -> None:
        ExPortfolio.objects.all().delete()
        Exchanger.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_get_owner(self):
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': self.telegram1,
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                   }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(self.user1.username, list(response.data.keys())[0])
        self.assertEqual(self.portfolio_exchanger.exchanger.name,
                         list(list(response.data.values())[0][0].keys())[0].upper())
        self.assertEqual(self.portfolio_blockchain.blockchain.name,
                         list(list(response.data.values())[0][1].keys())[0].upper())

    def test_get_not_exist_user(self):
        url = reverse(self.endpoint, )
        headers = {'TEL_USERNAME': 'telegram',
                   'BOT-NAME': self.bot_name,
                   'USER-NAME': self.username,
                   'CHAT-ID': str(self.chat_id)
                   }
        response = self.client.get(url, headers=headers)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='No such user', code='authentication_failed')}, response.data)

