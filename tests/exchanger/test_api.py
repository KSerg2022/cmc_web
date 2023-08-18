import json
import unittest
from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from exchanger.api.serializers import ExchangerSerializer, ExPortfolioSerializer
from exchanger.api.views import ExPortfolioViewSet
from exchanger.models import Exchanger, ExPortfolio


class ExchangerBase(TestCase):
    def setUp(self) -> None:
        self.name = 'name test'
        self.slug = 'name-test'
        self.host = 'https://www.okx.com'
        self.url = ''
        self.prefix = ''
        self.logo = 'tests/account/data_for_test/black.jpg'

        self.endpoint_list = 'exchanger-list'
        self.endpoint_detail = 'exchanger-detail'
        
    def tearDown(self) -> None:
        Exchanger.objects.all().delete()

    def create_exchangers(self):
        self.exchanger_1 = Exchanger.objects.create(name=self.name + '1',
                                                    slug=self.slug + '1',
                                                    host=self.host + '1',
                                                    url=self.url + '1',
                                                    prefix=self.prefix + '1',
                                                    logo=self.logo + '1')
        self.exchanger_2 = Exchanger.objects.create(name=self.name + '5',
                                                    slug=self.slug + '5',
                                                    host=self.host + '5',
                                                    url=self.url + '5',
                                                    prefix=self.prefix + '5',
                                                    logo=self.logo + '5')
        self.exchanger_3 = Exchanger.objects.create(name=self.name + '2',
                                                    slug=self.slug + '2',
                                                    host=self.host + '2',
                                                    url=self.url + '2',
                                                    prefix=self.prefix + '2',
                                                    is_active=False,
                                                    logo=self.logo + '2')

    def get_serializer_data(self, url, exchanger=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_context = {'request': Request(request), }
        if exchanger is None:
            return ExchangerSerializer([self.exchanger_1, self.exchanger_2, self.exchanger_3],
                                       many=True,
                                       context=serializer_context).data
        return ExchangerSerializer([*exchanger], many=True,
                                   context=serializer_context).data


class ExchangerApiTestCase(APITestCase, ExchangerBase):

    def setUp(self) -> None:
        super(ExchangerApiTestCase, self).setUp()
        self.user_admin = User.objects.create_superuser(username='user_admin',
                                                        password='user_admin')
        self.client.force_login(user=self.user_admin)

    def tearDown(self) -> None:
        User.objects.all().delete()

    def test_get(self):
        self.create_exchangers()
        url = reverse(self.endpoint_list)
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.exchanger_1, self.exchanger_3, self.exchanger_2])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search(self):
        self.create_exchangers()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': 'name test1'})

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.exchanger_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_is_active(self):
        self.create_exchangers()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'is_active': 'False'})

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.exchanger_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_name(self):
        self.create_exchangers()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'name': 'name test5'})
        serializer_data = self.get_serializer_data(url, exchanger=[self.exchanger_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_id(self):
        self.create_exchangers()
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
        self.create_exchangers()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'name'})

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.exchanger_1, self.exchanger_3, self.exchanger_2])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-name'})

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.exchanger_2, self.exchanger_3, self.exchanger_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, Exchanger.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            "name": "TEST",
            "slug": "_",
            "host": "https://test.com/api",
            "url": "",
            "prefix": "",
            'is_active': True,
            "website": "https://test.org/en",
        }

        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Exchanger.objects.all().count())
        self.assertEqual(1, response.data['id'])
        self.assertEqual(data['name'], response.data['name'])
        self.assertEqual(data['name'].lower(), response.data['slug'])

    def test_update(self):
        self.create_exchangers()

        self.assertEqual(3, Exchanger.objects.all().count())
        self.assertTrue(self.exchanger_1.is_active)

        url_for_update = reverse(self.endpoint_detail, args=(self.exchanger_1.id, ))
        data = {
            "name": self.name + '1',
            "slug": "_",
            "host": self.host,
            'url': self.url + '1',
            'prefix': self.prefix + '1',
            'is_active': False,
        }

        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(3, Exchanger.objects.all().count())

        self.exchanger_1.refresh_from_db()
        self.assertFalse(self.exchanger_1.is_active)

    def test_delete(self):
        self.create_exchangers()
        self.assertEqual(3, Exchanger.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.exchanger_1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Exchanger.objects.all().count())


class ExchangerSerializerTestCase(ExchangerBase):

    def test_exchanger_serializer(self):
        self.create_exchangers()
        url = reverse(self.endpoint_list)
        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.exchanger_1, self.exchanger_2])
        expected_data = [
            {
                'id': self.exchanger_1.id,
                'name': 'name test1',
                'slug': 'name-test1',
                'host': 'https://www.okx.com1',
                'url': '1',
                'prefix': '1',
                'is_active': True,
                'logo': 'http://testserver/media/tests/account/data_for_test/black.jpg1',
                'website': ''
            },
            {
                'id': self.exchanger_2.id,
                'name': 'name test5',
                'slug': 'name-test5',
                'host': 'https://www.okx.com5',
                'url': '5',
                'prefix': '5',
                'is_active': True,
                'logo': 'http://testserver/media/tests/account/data_for_test/black.jpg5',
                'website': ''
            }
        ]

        self.assertEqual(expected_data, serializer_data)


class ExPortfolioBase(TestCase):

    def setUp(self) -> None:
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
        self.owner3 = User.objects.create(username='User3',
                                          password='password1')

        self.endpoint_list = 'exportfolio-list'
        self.endpoint_detail = 'exportfolio-detail'

    def tearDown(self) -> None:
        ExPortfolio.objects.all().delete()
        Exchanger.objects.all().delete()
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
                                                      owner=self.owner3)

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


class ExPortfolioApiTestCase(APITestCase, ExPortfolioBase):

    def setUp(self) -> None:
        super(ExPortfolioApiTestCase, self).setUp()
        self.client.force_login(user=self.owner1)

    def test_get(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': 'User2'})
        serializer_data = self.get_serializer_data(url, exchanger=[self.portfolio_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'search': 'Exchanger_1'})
        serializer_data = self.get_serializer_data(url, exchanger=[self.portfolio_1, self.portfolio_3])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_exchanger(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'exchanger__name': 'Exchanger_2'})
        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.portfolio_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_owner(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'owner__username': 'User2'})
        serializer_data = self.get_serializer_data(url, exchanger=[self.portfolio_2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_owner(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'owner'})
        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.portfolio_1, self.portfolio_2, self.portfolio_3])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-owner'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(serializer_data, response.data['results'])

    def test_get_ordering_exchanger(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'exchanger__name'})

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-exchanger__name'})

        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.portfolio_2, self.portfolio_1, self.portfolio_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, ExPortfolio.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            'exchanger': self.exchanger1.id,
            'slug': '_',
            'api_key': 'new_api_key',
            'api_secret': self.api_secret,
            'owner': self.owner1.id,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(1, ExPortfolio.objects.all().count())
        self.assertEqual(1, response.data['id'])

    def test_update(self):
        self.create_portfolio()

        self.assertEqual(3, ExPortfolio.objects.all().count())
        self.assertEqual(1, self.portfolio_1.id)
        self.assertEqual(self.api_key, self.portfolio_1.api_key)

        url_for_update = reverse(self.endpoint_detail, args=(self.portfolio_1.id, ))
        data = {
            'exchanger': self.exchanger1.id,
            'slug': '_',
            'api_key': 'new_api_key',
            'api_secret': self.api_secret,
            'owner': self.owner1.id,
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, ExPortfolio.objects.all().count())

        self.portfolio_1.refresh_from_db()
        self.assertEqual(1, self.portfolio_1.id)
        self.assertEqual('new_api_key', self.portfolio_1.api_key)

    def test_delete(self):
        self.create_portfolio()
        self.assertEqual(3, ExPortfolio.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.portfolio_1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, ExPortfolio.objects.all().count())


class ExPortfolioSerializerTestCase(ExPortfolioBase):

    def test_ex_portfolio_serializer(self):
        self.create_portfolio()
        url = reverse(self.endpoint_list)
        serializer_data = self.get_serializer_data(url,
                                                   exchanger=[self.portfolio_1])
        expected_data = [
            {
                'id': self.portfolio_1.id,
                'slug': 'user1-exchanger_1',
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'password': '',
                'comments': '',
                'owner': self.owner1.id,
                'exchanger': self.exchanger1.id,
                'currencies': [],
            },
        ]

        self.assertEqual(expected_data, serializer_data)
