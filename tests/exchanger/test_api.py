import unittest
from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from exchanger.api.cerializers import ExchangerSerializer, ExPortfolioSerializer
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

    def tearDown(self) -> None:
        Exchanger.objects.all().delete()

    def create_exchangers(self):
        self.exchanger_1 = Exchanger.objects.create(name=self.name + '1',
                                                    slug=self.slug + '1',
                                                    host=self.host + '1',
                                                    url=self.url + '1',
                                                    prefix=self.prefix + '1',
                                                    logo=self.logo + '1')
        self.exchanger_2 = Exchanger.objects.create(name=self.name + '2',
                                                    slug=self.slug + '2',
                                                    host=self.host + '2',
                                                    url=self.url + '2',
                                                    prefix=self.prefix + '2',
                                                    logo=self.logo + '2')

    def get_serializer_data(self, url):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        return ExchangerSerializer([self.exchanger_1, self.exchanger_2], many=True,
                                   context=serializer_context).data


class ExchangerApiTestCase(APITestCase, ExchangerBase):

    def test_get(self):
        self.create_exchangers()
        url = reverse('exchanger-list')
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class ExchangerSerializerTestCase(ExchangerBase):

    def test_exchanger_serializer(self):
        self.create_exchangers()
        url = reverse('blockchain-list')
        serializer_data = self.get_serializer_data(url)
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
                'name': 'name test2',
                'slug': 'name-test2',
                'host': 'https://www.okx.com2',
                'url': '2',
                'prefix': '2',
                'is_active': True,
                'logo': 'http://testserver/media/tests/account/data_for_test/black.jpg2',
                'website': ''
            }
        ]

        self.assertEqual(expected_data, serializer_data)


class ExPortfolioBase(TestCase):

    def setUp(self) -> None:
        self.name = 'Exchanger_1'
        self.host = 'https://www.okx.com'
        self.exchanger = Exchanger.objects.create(name=self.name,
                                                  host=self.host)
        self.api_key = 'api_key'
        self.api_secret = 'api_secret'
        self.owner = User.objects.create(username='User1',
                                         password='password1')

    def tearDown(self) -> None:
        ExPortfolio.objects.all().delete()
        User.objects.all().delete()

    def create_portfolio(self):
        self.portfolio_1 = ExPortfolio.objects.create(exchanger=self.exchanger,
                                                      api_key=self.api_key,
                                                      api_secret=self.api_secret,
                                                      owner=self.owner)

    def get_serializer_data(self, url):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        return ExPortfolioSerializer([self.portfolio_1], many=True,
                                             context=serializer_context).data


class ExPortfolioApiTestCase(APITestCase, ExPortfolioBase):

    def test_get(self):
        self.create_portfolio()
        url = reverse('exportfolio-list')
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class ExPortfolioSerializerTestCase(ExPortfolioBase):

    def test_ex_portfolio_serializer(self):
        self.create_portfolio()
        url = reverse('exportfolio-list')
        serializer_data = self.get_serializer_data(url)
        expected_data = [
            {
                'id': self.portfolio_1.id,
                'slug':  'user1-exchanger_1',
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'password': '',
                'comments': '',
                'owner': self.owner.id,
                'exchanger': self.exchanger.id,
                'currencies': [],
            },
        ]

        self.assertEqual(expected_data, serializer_data)

