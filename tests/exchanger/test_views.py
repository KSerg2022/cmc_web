import os
import time
import unittest

from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.html import escape
from django.contrib.auth.models import User

from exchanger.fixtures.handlers.load_exchangers_to_db import dump_to_db_exchanger

from exchanger.views import (create_portfolio,
                              change_portfolio, delete_portfolio, get_exchanger_data)
from exchanger.models import Exchanger, ExPortfolio
from django.utils import timezone


class CreatePortfolio(TestCase):

    def setUp(self) -> None:
        dump_to_db_exchanger()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:create_portfolio', args='1')
        return self.client.get(url)

    def test_url_to_page_create_portfolio(self):
        found = resolve(f'/exchanger/create_portfolio/{2}/')
        self.assertEqual(found.func, create_portfolio)

    def test_create_portfolio_if_user_is_not_authenticated(self):
        url = reverse('exchanger:create_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_create_portfolio_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')

    def test_create_portfolio_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')

    def test_create_portfolio_POST(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:create_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'api_secret': 'api_secret',
                                          'password': 'password',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertRedirects(response, reverse('exchanger:exchangers'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertContains(self.client.get(reverse('exchanger:exchangers')),
                            escape('Portfolio created successfully'),
                            status_code=200, html=False)

        portfolio = ExPortfolio.objects.first()
        self.assertEqual(portfolio.api_key, 'api_key', portfolio)

    def test_create_portfolio_with_empty_api_POST(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:create_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': '',
                                          'api_secret': 'api_secret',
                                          'password': 'password',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')
        self.assertContains(response, escape('Error created your portfolio'))

        portfolio = ExPortfolio.objects.first()
        self.assertIsNone(portfolio)

    def test_create_portfolio_with_empty_api_secret_POST(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:create_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'api_secret': '',
                                          'password': 'password',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')
        self.assertContains(response, escape('Error created your portfolio'))

        portfolio = ExPortfolio.objects.first()
        self.assertIsNone(portfolio)

    def test_create_portfolio_with_wrong_id_exchanger(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:create_portfolio', args=('20', ))
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'api_secret': 'api_secret',
                                          'password': 'password',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 404)


class ChangePortfolio(TestCase):

    def setUp(self) -> None:
        dump_to_db_exchanger()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')
        self.api_key = 'api_key'
        self.api_secret = 'api_secret'
        self.password = 'password'
        self.portfolio = ExPortfolio.objects.create(api_key=self.api_key,
                                                    api_secret=self.api_secret,
                                                    password=self.password,
                                                    comments='',
                                                    exchanger=Exchanger.objects.get(id=1),
                                                    owner=self.user)

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:change_portfolio', args=('1', ))
        return self.client.get(url)

    def test_url_to_page_change_portfolio(self):
        found = resolve('/exchanger/change_portfolio/1/')
        self.assertEqual(found.func, change_portfolio)

    def test_exchanger_portfolio_if_user_is_not_authenticated(self):
        url = reverse('exchanger:change_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_exchanger_portfolio_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')

    def test_exchanger_portfolio_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')

    def test_exchanger_portfolio_POST(self):
        self.assertEqual(self.portfolio.api_key, self.api_key)
        self.assertEqual(self.portfolio.api_secret, self.api_secret)

        self.client.force_login(self.user)
        url = reverse('exchanger:change_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key new',
                                          'api_secret': 'api_secret new',
                                          'password': 'password new',
                                          'comments': ''}
                                    )

        self.assertRedirects(response, reverse('exchanger:exchangers'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertContains(self.client.get(reverse('exchanger:exchangers')),
                            escape('Portfolio changed successfully'),
                            status_code=200, html=False)

        portfolio = ExPortfolio.objects.first()
        self.assertEqual(portfolio.api_key, 'api_key new', portfolio)
        self.assertEqual(portfolio.api_secret, 'api_secret new', portfolio)
        self.assertEqual(portfolio.password, 'password new', portfolio)

    def test_exchanger_portfolio_with_empty_api_POST(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:change_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': '',
                                          'api_secret': 'api_secret',
                                          'password': 'password',
                                          'comments': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')
        self.assertContains(response, escape('Error changed your portfolio'))

    def test_exchanger_portfolio_with_empty_api_secret_POST(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:change_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'api_secret': '',
                                          'password': 'password',
                                          'comments': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/add_portfolio.html')
        self.assertContains(response, escape('Error changed your portfolio'))


class DeletePortfolio(TestCase):

    def setUp(self) -> None:
        dump_to_db_exchanger()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')
        self.api_key = 'api_key'
        self.api_secret = 'api_secret'
        self.password = 'password'
        self.portfolio = ExPortfolio.objects.create(api_key=self.api_key,
                                                    api_secret=self.api_secret,
                                                    password=self.password,
                                                    comments='',
                                                    exchanger=Exchanger.objects.get(id=1),
                                                    owner=self.user)

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:delete_portfolio', args='1')
        return self.client.get(url)

    def test_url_to_page_delete_exchanger_portfolio(self):
        found = resolve(f'/exchanger/delete_portfolio/{1}/')
        self.assertEqual(found.func, delete_portfolio)

    def test_delete_exchanger_portfolio_if_user_is_not_authenticated(self):
        url = reverse('exchanger:delete_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_delete_exchanger_portfolio_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'exchanger/delete_portfolio.html')

    def test_delete_exchanger_portfolio_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/delete_portfolio.html')

    def test_delete_exchanger_portfolio_GET_with_yes(self):
        self.assertTrue(ExPortfolio.objects.first())

        self.client.force_login(self.user)
        url = reverse('exchanger:delete_portfolio', args='1')
        response = self.client.get(url + '?yes=yes')

        self.assertRedirects(response, reverse('exchanger:exchangers'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertContains(self.client.get(reverse('exchanger:exchangers')),
                            escape(f'Portfolio {self.portfolio.exchanger} deleted successfully'),
                            status_code=200, html=False)

        portfolio = ExPortfolio.objects.first()
        self.assertIsNone(portfolio)

    def test_delete_exchanger_portfolio_with_not_correct_id_portfolio(self):
        self.assertTrue(ExPortfolio.objects.first())

        self.client.force_login(self.user)
        url = reverse('exchanger:delete_portfolio', args='2')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class GetExchangerData(TestCase):

    def setUp(self) -> None:
        dump_to_db_exchanger()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')

        self.api_key = os.environ.get('OKX_API_KEY')
        self.api_secret = os.environ.get('OKX_API_SECRET_KEY')
        self.password = os.environ.get('OKX_PWD')
        self.portfolio = ExPortfolio.objects.create(api_key=self.api_key,
                                                    api_secret=self.api_secret,
                                                    password=self.password,
                                                    comments='',
                                                    exchanger=Exchanger.objects.get(id=1),
                                                    owner=self.user)

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('exchanger:get_exchanger_data', args='1')
        return self.client.get(url)

    def test_url_to_page_get_exchanger_data(self):
        found = resolve(f'/exchanger/data/{1}/')
        self.assertEqual(found.func, get_exchanger_data)

    def test_get_exchanger_data_if_user_is_not_authenticated(self):
        url = reverse('exchanger:get_exchanger_data', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_get_exchanger_data_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'exchanger/data_portfolio.html')

    def test_get_exchanger_data_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/data_portfolio.html')

    def test_dget_exchanger_data_with_not_correct_id_portfolio(self):
        self.assertTrue(ExPortfolio.objects.first())

        self.client.force_login(self.user)
        url = reverse('exchanger:get_exchanger_data', args='2')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_get_exchanger_data_with_not_correct_api(self):
        self.client.force_login(self.user)
        portfolio_wrong_apy = ExPortfolio.objects.create(api_key='wrong_apy',
                                                         api_secret=self.api_secret,
                                                         password='',
                                                         comments='',
                                                         exchanger=Exchanger.objects.get(id=3),
                                                         owner=self.user)

        url = reverse('exchanger:get_exchanger_data', args=('3', ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'exchanger/data_portfolio.html')
