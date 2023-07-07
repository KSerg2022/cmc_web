import os
import time
import unittest

from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.html import escape
from django.contrib.auth.models import User

from blockchain.fixtures.handlers.load_blockchains_to_db import dump_to_db_blockchain

from blockchain.views import (create_blockchain_portfolio,
                              change_blockchain_portfolio, delete_blockchain_portfolio, get_blockchain_data)
from blockchain.models import Blockchain, Portfolio
from django.utils import timezone


class CreateBlockchainPortfolio(TestCase):

    def setUp(self) -> None:
        dump_to_db_blockchain()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:create_blockchain_portfolio', args='1')
        return self.client.get(url)

    def test_url_to_page_create_blockchain_portfolio(self):
        found = resolve(f'/blockchain/create_portfolio/{2}/')
        self.assertEqual(found.func, create_blockchain_portfolio)

    def test_create_blockchain_portfolio_if_user_is_not_authenticated(self):
        url = reverse('blockchain:create_blockchain_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_create_blockchain_portfolio_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')

    def test_create_blockchain_portfolio_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')

    def test_create_blockchain_portfolio_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:create_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'wallet': 'wallet',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertRedirects(response, reverse('exchanger:exchangers'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertContains(self.client.get(reverse('exchanger:exchangers')),
                            escape('Portfolio created successfully'),
                            status_code=200, html=False)

        portfolio = Portfolio.objects.first()
        self.assertEqual(portfolio.api_key, 'api_key', portfolio)

    def test_create_blockchain_portfolio_with_empty_api_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:create_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': '',
                                          'wallet': 'wallet',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')
        self.assertContains(response, escape('Error created your portfolio'))

        portfolio = Portfolio.objects.first()
        self.assertIsNone(portfolio)

    def test_create_blockchain_portfolio_with_empty_wallet_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:create_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'wallet': '',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')
        self.assertContains(response, escape('Error created your portfolio'))

        portfolio = Portfolio.objects.first()
        self.assertIsNone(portfolio)

    def test_create_blockchain_portfolio_with_not_correct_format_currencies_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:create_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'wallet': '',
                                          'comments': '',
                                          'currencies': 'zasfaaf'}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')
        self.assertContains(response, escape('Error created your portfolio'))
        self.assertContains(response, escape('Enter a valid JSON.'))

        portfolio = Portfolio.objects.first()
        self.assertIsNone(portfolio)


class ChangeBlockchainPortfolio(TestCase):

    def setUp(self) -> None:
        dump_to_db_blockchain()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')
        self.api_key = 'api_key'
        self.wallet = 'wallet'
        self.currencies = '{"coin": "contract"}'
        self.portfolio = Portfolio.objects.create(api_key=self.api_key,
                                                  wallet=self.wallet,
                                                  comments='',
                                                  currencies=self.currencies,
                                                  blockchain=Blockchain.objects.first(),
                                                  owner=self.user)

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:change_blockchain_portfolio', args='1')
        return self.client.get(url)

    def test_url_to_page_change_blockchain_portfolio(self):
        found = resolve(f'/blockchain/change_portfolio/{1}/')
        self.assertEqual(found.func, change_blockchain_portfolio)

    def test_change_blockchain_portfolio_if_user_is_not_authenticated(self):
        url = reverse('blockchain:change_blockchain_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_change_blockchain_portfolio_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')

    def test_change_blockchain_portfolio_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')

    def test_change_blockchain_portfolio_POST(self):
        self.assertEqual(self.portfolio.api_key, self.api_key)
        self.assertEqual(self.portfolio.wallet, self.wallet)
        self.assertEqual(self.portfolio.currencies, self.currencies)

        self.client.force_login(self.user)
        url = reverse('blockchain:change_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key new',
                                          'wallet': 'wallet new',
                                          'comments': '',
                                          'currencies': '{"coin": "contract new"}'}
                                    )

        self.assertRedirects(response, reverse('exchanger:exchangers'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertContains(self.client.get(reverse('exchanger:exchangers')),
                            escape('Portfolio changed successfully'),
                            status_code=200, html=False)

        portfolio = Portfolio.objects.first()
        self.assertEqual(portfolio.api_key, 'api_key new', portfolio)
        self.assertEqual(portfolio.wallet, 'wallet new', portfolio)
        self.assertEqual(portfolio.currencies, {"coin": "contract new"}, portfolio)

    def test_change_blockchain_portfolio_with_empty_api_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:change_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': '',
                                          'wallet': 'wallet',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')
        self.assertContains(response, escape('Error changed your portfolio'))

    def test_change_blockchain_portfolio_with_empty_wallet_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:change_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'wallet': '',
                                          'comments': '',
                                          'currencies': ''}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')
        self.assertContains(response, escape('Error changed your portfolio'))

    def test_change_blockchain_portfolio_with_not_correct_format_currencies_POST(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:change_blockchain_portfolio', args='1')
        response = self.client.post(url,
                                    data={'api_key': 'api_key',
                                          'wallet': '',
                                          'comments': '',
                                          'currencies': 'zasfaaf'}
                                    )

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/add_portfolio.html')
        self.assertContains(response, escape('Error changed your portfolio'))
        self.assertContains(response, escape('Enter a valid JSON.'))


class DeleteBlockchainPortfolio(TestCase):

    def setUp(self) -> None:
        dump_to_db_blockchain()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')
        self.api_key = 'api_key'
        self.wallet = 'wallet'
        self.currencies = '{"coin": "contract"}'
        self.portfolio = Portfolio.objects.create(api_key=self.api_key,
                                                  wallet=self.wallet,
                                                  comments='',
                                                  currencies=self.currencies,
                                                  blockchain=Blockchain.objects.first(),
                                                  owner=self.user)

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:delete_blockchain_portfolio', args='1')
        return self.client.get(url)

    def test_url_to_page_delete_blockchain_portfolio(self):
        found = resolve(f'/blockchain/delete_portfolio/{1}/')
        self.assertEqual(found.func, delete_blockchain_portfolio)

    def test_delete_blockchain_portfolio_if_user_is_not_authenticated(self):
        url = reverse('blockchain:delete_blockchain_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_delete_blockchain_portfolio_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'blockchain/delete_portfolio.html')

    def test_delete_blockchain_portfolio_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/delete_portfolio.html')

    def test_delete_blockchain_portfolio_GET_with_yes(self):
        self.assertTrue(Portfolio.objects.first())

        self.client.force_login(self.user)
        url = reverse('blockchain:delete_blockchain_portfolio', args='1')
        response = self.client.get(url + '?yes=yes')

        self.assertRedirects(response, reverse('exchanger:exchangers'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertContains(self.client.get(reverse('exchanger:exchangers')),
                            escape(f'Portfolio {self.portfolio.blockchain} deleted successfully'),
                            status_code=200, html=False)

        portfolio = Portfolio.objects.first()
        self.assertIsNone(portfolio)

    def test_delete_blockchain_portfolio_with_not_correct_id_portfolio(self):
        self.assertTrue(Portfolio.objects.first())

        self.client.force_login(self.user)
        url = reverse('blockchain:delete_blockchain_portfolio', args='2')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class GetBlockchainData(TestCase):

    def setUp(self) -> None:
        dump_to_db_blockchain()
        self.user = User.objects.create(username='user_test',
                                        password='!qa2ws3ED',
                                        email='test@gamil.com',
                                        first_name='test')
        self.api_key = os.environ.get('BSCSCAN_API_KEY')
        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8"}
        self.portfolio = Portfolio.objects.create(api_key=self.api_key,
                                                  wallet=self.wallet,
                                                  comments='',
                                                  currencies=self.currencies,
                                                  blockchain=Blockchain.objects.first(),
                                                  owner=self.user)

    def _get_response_for_page_GET(self):
        self.client.force_login(self.user)
        url = reverse('blockchain:get_blockchain_data', args='1')
        return self.client.get(url)

    def test_url_to_page_get_blockchain_data(self):
        found = resolve(f'/blockchain/data/{1}/')
        self.assertEqual(found.func, get_blockchain_data)

    def test_get_blockchain_data_if_user_is_not_authenticated(self):
        url = reverse('blockchain:delete_blockchain_portfolio', args='1')
        response = self.client.get(url)
        url_redirect = reverse('login') + '?next=' + url

        self.assertRedirects(response, url_redirect,
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_get_blockchain_data_templates(self):
        response = self._get_response_for_page_GET()

        self.assertTemplateUsed(response, 'blockchain/data_portfolio.html')

    def test_get_blockchain_data_GET(self):
        response = self._get_response_for_page_GET()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/data_portfolio.html')

    def test_dget_blockchain_data_with_not_correct_id_portfolio(self):
        self.assertTrue(Portfolio.objects.first())

        self.client.force_login(self.user)
        url = reverse('blockchain:get_blockchain_data', args='2')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_dget_blockchain_data_with_not_correct_api(self):
        self.client.force_login(self.user)
        blockchain = Blockchain.objects.last()
        portfolio_wrong_apy = Portfolio.objects.create(api_key='wrong_apy',
                                                       wallet=self.wallet,
                                                       comments='',
                                                       currencies=self.currencies,
                                                       blockchain=blockchain,
                                                       owner=self.user)

        url = reverse('blockchain:get_blockchain_data', args=f'{blockchain.id}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'blockchain/data_portfolio.html')
