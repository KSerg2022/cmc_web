# from unittest import TestCase
import json

from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blockchain.api.serializers import BlockchainSerializer, BlockchainPortfolioSerializer
from blockchain.api.views import BlockchainViewSet
from blockchain.models import Blockchain, Portfolio


class BlockchainBase(TestCase):
    def setUp(self) -> None:
        self.name = 'Blockchain test'
        self.slug = 'blockchain-test'
        self.host = 'https://api.bscscan.com/api'
        self.api_key = 'api_key'
        self.logo = 'tests/account/data_for_test/black.jpg'

        self.endpoint_list = 'blockchain-list'
        self.endpoint_detail = 'blockchain-detail'

    def tearDown(self) -> None:
        Blockchain.objects.all().delete()

    def create_blockchains(self):
        self.blockchain_1 = Blockchain.objects.create(name=self.name + '1',
                                                      slug=self.slug + '1',
                                                      host=self.host + '1',
                                                      api_key=self.api_key + '1',
                                                      logo=self.logo + '1')
        self.blockchain_2 = Blockchain.objects.create(name=self.name + '5',
                                                      slug=self.slug + '5',
                                                      host=self.host + '5',
                                                      api_key=self.api_key + '5',
                                                      logo=self.logo + '5')
        self.blockchain_3 = Blockchain.objects.create(name=self.name + '3',
                                                      slug=self.slug + '3',
                                                      host=self.host + '3',
                                                      api_key=self.api_key + '3',
                                                      is_active=False,
                                                      logo=self.logo + '3')

    def get_serializer_data(self, url, blockchain=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_context = {'request': Request(request), }

        if blockchain is None:
            return BlockchainSerializer([self.blockchain_1, self.blockchain_2, self.blockchain_3],
                                        many=True,
                                        context=serializer_context).data
        return BlockchainSerializer([*blockchain],
                                    many=True,
                                    context=serializer_context).data


class BlockchainApiTestCase(APITestCase, BlockchainBase):

    def setUp(self) -> None:
        super(BlockchainApiTestCase, self).setUp()
        self.user_admin = User.objects.create_superuser(username='user_admin',
                                                        password='user_admin')
        self.client.force_login(user=self.user_admin)

    def tearDown(self) -> None:
        User.objects.all().delete()

    def test_get(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url,
                                                   blockchain=[self.blockchain_1, self.blockchain_3, self.blockchain_2])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': 'Blockchain test1'})

        serializer_data = self.get_serializer_data(url, blockchain=[self.blockchain_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_is_active(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'is_active': 'False'})

        serializer_data = self.get_serializer_data(url, blockchain=[self.blockchain_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_name(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'name': 'Blockchain test1'})

        serializer_data = self.get_serializer_data(url, blockchain=[self.blockchain_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_id(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'id'})

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-id'})

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(serializer_data, response.data['results'])

    def test_get_ordering_name(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'name'})

        serializer_data = self.get_serializer_data(url,
                                                   blockchain=[self.blockchain_1, self.blockchain_3, self.blockchain_2])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-name'})

        serializer_data = self.get_serializer_data(url,
                                                   blockchain=[self.blockchain_2, self.blockchain_3, self.blockchain_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, Blockchain.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            "name": "TEST",
            "slug": "_",
            "host": "https://api.test.com/api",
            "api_key": "teast_api_key",
            'is_active': True,
            "website": "https://test.org/en",
            "scan_site": "https://test.com/"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Blockchain.objects.all().count())
        self.assertEqual(1, response.data['id'])
        self.assertEqual(data['name'], response.data['name'])
        self.assertEqual(data['name'].lower(), response.data['slug'])

    def test_update(self):
        self.create_blockchains()

        self.assertEqual(3, Blockchain.objects.all().count())
        self.assertTrue(self.blockchain_1.is_active)

        url_for_update = reverse(self.endpoint_detail, args=(self.blockchain_1.id, ))
        data = {
            "name": self.name + '1',
            "slug": "_",
            "host": self.host + '1',
            "api_key": self.api_key + '1',
            'is_active': False,
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, Blockchain.objects.all().count())

        self.blockchain_1.refresh_from_db()
        self.assertFalse(self.blockchain_1.is_active)

    def test_delete(self):
        self.create_blockchains()
        self.assertEqual(3, Blockchain.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.blockchain_1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Blockchain.objects.all().count())


class BlockchainSerializerTestCase(BlockchainBase):

    def test_blockchain_serializer(self):
        self.create_blockchains()
        url = reverse(self.endpoint_list)
        serializer_data = self.get_serializer_data(url, blockchain=[self.blockchain_1, self.blockchain_2])
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
                'name': 'Blockchain test5',
                'slug': 'blockchain-test5',
                'host': 'https://api.bscscan.com/api5',
                'api_key': 'api_key5',
                'is_active': True,
                'logo': 'http://testserver/media/tests/account/data_for_test/black.jpg5',
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
        self.owner3 = User.objects.create(username='User3',
                                          password='password1')
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
                           "GMI": "0x93D8d25E3C9A847a5Da79F79ecaC89461FEcA846"}
        self.endpoint_list = 'portfolio-list'
        self.endpoint_detail = 'portfolio-detail'

    def tearDown(self) -> None:
        Portfolio.objects.all().delete()
        Blockchain.objects.all().delete()
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
        self.portfolio_3 = Portfolio.objects.create(owner=self.owner3,
                                                    blockchain=self.blockchain1,
                                                    wallet=self.wallet,
                                                    currencies=self.currencies)

    def get_serializer_data(self, url, portfolio=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        if portfolio is None:
            return BlockchainPortfolioSerializer([self.portfolio_1, self.portfolio_2, self.portfolio_3],
                                                 many=True,
                                                 context=serializer_context).data
        return BlockchainPortfolioSerializer([*portfolio],
                                             many=True,
                                             context=serializer_context).data


class BlockchainPortfolioApiTestCase(APITestCase, BlockchainPortfolioBase):

    def setUp(self) -> None:
        super(BlockchainPortfolioApiTestCase, self).setUp()
        self.client.force_login(user=self.owner1)

    # def tearDown(self) -> None:
    #     User.objects.all().delete()

    def test_get(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_1, self.portfolio_3, self.portfolio_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': '1'})

        serializer_data = self.get_serializer_data(url, portfolio=[self.portfolio_1, self.portfolio_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_blockchain(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'blockchain__name': 'Blockchain test2'})
        serializer_data = self.get_serializer_data(url, portfolio=[self.portfolio_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_owner(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'owner__username': 'User2'})
        serializer_data = self.get_serializer_data(url, portfolio=[self.portfolio_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_owner(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'owner'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-owner'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(serializer_data, response.data['results'])

    def test_get_ordering_blockchain(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_1, self.portfolio_3, self.portfolio_2])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-blockchain__name'})

        serializer_data = self.get_serializer_data(url,
                                                   portfolio=[self.portfolio_2, self.portfolio_1, self.portfolio_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, Portfolio.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            'owner': self.owner1.id,
            'slug': '_',
            'blockchain': self.blockchain1.id,
            'wallet': self.wallet,
            'currencies': self.currencies
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(1, Portfolio.objects.all().count())
        self.assertEqual(1, response.data['id'])

    def test_update(self):
        self.create_portfolio()

        self.assertEqual(3, Portfolio.objects.all().count())
        self.assertEqual(1, self.portfolio_1.id)
        self.assertEqual(3, len(self.portfolio_1.currencies))

        url_for_update = reverse(self.endpoint_detail, args=(self.portfolio_1.id, ))
        data = {
            'owner': self.owner1.id,
            'slug': '_',
            'blockchain': self.blockchain1.id,
            'wallet': self.wallet,
            'currencies': {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD"}
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, Portfolio.objects.all().count())

        self.portfolio_1.refresh_from_db()
        self.assertEqual(1, self.portfolio_1.id)
        self.assertEqual(1, len(self.portfolio_1.currencies))

    def test_delete(self):
        self.create_portfolio()
        self.assertEqual(3, Portfolio.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.portfolio_1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Portfolio.objects.all().count())



class BlockchainPortfolioSerializerTestCase(BlockchainPortfolioBase):

    def test_blockchain_portfolio_serializer(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        serializer_data = self.get_serializer_data(url, portfolio=[self.portfolio_1])
        expected_data = [
            {
                'id': self.portfolio_1.id,
                'slug': 'user1-blockchain-test1',
                'wallet': self.wallet,
                'comments': '',
                'currencies': self.currencies,
                'owner': self.owner1.id,
                'blockchain': self.blockchain1.id
            },
        ]

        self.assertEqual(expected_data, serializer_data)
