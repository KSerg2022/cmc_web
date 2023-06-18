import time
import unittest

from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from cmc.utils.load_data_to_db import dump_to_db

from cmc.views import index, detail
from cmc.models import Cryptocurrency
from django.utils import timezone


class HomePageTest(TestCase):
    def test_root_url_resolves_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_cmc_index_templates(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'cmc/cmc/index.html')

    def test_cmc_index_GET(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'cmc/cmc/index.html')


class DetailTest(TestCase):
    def setUp(self) -> None:
        self.symbol = 'symbol_test'
        self.name = 'name_test'
        self.slug = 'name_test'
        dump_to_db(5)
        self.crypto = Cryptocurrency.objects.all()[0]

        # self.website = 'test@test.com',
        # self.contract = '123456789',
        # self.description = 'description',
        # self.logo = 'tests/account/data_for_test/black.jpg'

    def test_detail_url_resolves_to_page(self):
        found = resolve(f'/cmc/detail/{self.slug}/')
        self.assertEqual(found.func, detail)

    def test_cmc_detail_templates(self):
        response = self.client.get(f'/cmc/detail/{self.crypto.slug}/')
        self.assertTemplateUsed(response, 'cmc/cmc/detail.html')

    def test_cmc_detail_GET(self):
        url = reverse('cmc:crypto_detail', args=[self.crypto.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'cmc/cmc/detail.html')

    def test_cmc_detail_GET_if_not_crypto(self):
        url = reverse('cmc:crypto_detail', args=[self.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404, response)
        # self.assertTemplateUsed(response, 'cmc/cmc/detail.html')
