from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from django.contrib.auth.models import User

from exchanger.models import Exchanger, ExPortfolio
from cmc.fixtures.handlers.load_currencies_to_db import dump_to_db_currencies
from cmc.models import Cryptocurrency


class ExchangerModelTest(TestCase):

    def setUp(self) -> None:
        self.name = 'name test'
        self.slug = 'name-test'
        self.host = 'https://www.okx.com'
        self.url = ''
        self.prefix = ''
        # self.is_active = True,
        self.logo = 'tests/account/data_for_test/black.jpg'

    def test_exchanger_default_symbol(self):
        exchange = Exchanger()
        self.assertEqual(exchange.name, '')

    def test_exchanger_print(self):
        exchange = Exchanger.objects.create(name=self.name,
                                            slug=self.slug)
        self.assertEqual(f'{self.name.capitalize()}', str(exchange), exchange)

    def test_exchanger_fields(self):
        fields = ['portfolio', 'id', 'name', 'slug', 'host', 'url', 'prefix',
                  'is_active', 'logo', 'website']
        exchange = Exchanger.objects.create()
        model_fields = [field.name for field in exchange._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)

    def test_exchanger_create_with_empty_name(self):
        with self.assertRaises(ValidationError):
            exchange = Exchanger.objects.create(name='')
            exchange.full_clean()
            exchange.save()

    def test_exchanger_create_with_wrong_host(self):
        with self.assertRaises(ValidationError):
            exchange = Exchanger.objects.create(name=self.name,
                                                host='/url/url'
                                                )
            exchange.full_clean()
            exchange.save()

    def test_exchanger_create_with_all_data(self):
        exchange = Exchanger.objects.create(name=self.name,
                                            host=self.host,
                                            url=self.url,
                                            prefix=self.prefix,
                                            logo=self.logo)
        self.assertEqual(exchange.name, self.name)
        self.assertEqual(exchange.slug, self.slug)
        self.assertEqual(exchange.host, self.host)
        self.assertEqual(exchange.url, self.url)
        self.assertEqual(exchange.prefix, self.prefix)
        self.assertTrue(exchange.is_active)
        self.assertEqual(exchange.logo, self.logo)

    def test_exchanger_is_active_False(self):
        exchange = Exchanger.objects.create(name=self.name)
        self.assertTrue(exchange.is_active)

        exchange.is_active = False
        self.assertFalse(exchange.is_active)

    def test_exchanger_create_with_invalid_format_photo(self):
        with self.assertRaises(ValidationError):
            exchange = Exchanger.objects.create(name=self.name,
                                                      logo='tests/account/data_for_test/text.txt')
            exchange.full_clean()
            exchange.save()

    def test_exchanger_ordering(self):
        exchanger1 = Exchanger.objects.create(name=self.name)
        exchanger2 = Exchanger.objects.create(name=self.name + '1')
        exchanges = Exchanger.objects.all()

        self.assertEqual([f'{self.name.capitalize()}', f'{self.name.capitalize() + "1"}'],
                         [str(q) for q in exchanges],
                         exchanges)
        self.assertNotEqual([f'{self.name.capitalize() + "1"}', f'{self.name.capitalize()}'],
                            [str(q) for q in exchanges],
                            exchanges)

    def test_exchanger_get_absolute_url(self):
        exchanger = Exchanger.objects.create(name=self.name)

        self.assertEqual(exchanger.get_absolute_url(),
                         f'/exchanger/detail/{self.slug}/',
                         exchanger)


class ExPortfolioTest(TestCase):

    def setUp(self) -> None:
        self.name = 'Exchanger_1'
        self.host = 'https://www.okx.com'
        self.exchanger = Exchanger.objects.create(name=self.name,
                                                  host=self.host)

        # self.exchanger = self.exchange
        self.api_key = 'api_key'
        self.api_secret = 'api_secret'
        self.owner = User.objects.create(username='User1',
                                         password='password1')
        self.currencies = None

    def tearDown(self) -> None:
        pass

    def create_portfolio(self):
        return ExPortfolio.objects.create(exchanger=self.exchanger,
                                          api_key=self.api_key,
                                          api_secret=self.api_secret,
                                          owner=self.owner)

    def test_ex_portfolio_default_symbol(self):
        portfolio = self.create_portfolio()
        self.assertEqual(portfolio.exchanger.name.capitalize(),
                         self.exchanger.name.capitalize())

    def test_ex_portfolio_print(self):
        portfolio = self.create_portfolio()
        self.assertEqual(f'{self.owner.username} have {self.exchanger.name} portfolio',
                         str(portfolio), portfolio)

    def test_ex_portfolio_fields(self):
        fields = ['id', 'owner', 'exchanger', 'slug', 'api_key', 'api_secret',
                  'password', 'comments', 'currencies']
        portfolio = self.create_portfolio()
        model_fields = [field.name for field in portfolio._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)

    def test_ex_portfolio_create_without_exchanger(self):
        with self.assertRaises(ObjectDoesNotExist):
            portfolio = ExPortfolio.objects.create(
                api_key=self.api_key,
                api_secret=self.api_secret,
                owner=self.owner)

    def test_ex_portfolio_create_with_empty_api_key(self):
        with self.assertRaises(ValidationError):
            portfolio = ExPortfolio.objects.create(exchanger=self.exchanger,
                                                   api_key='',
                                                   api_secret=self.api_secret,
                                                   owner=self.owner)

            portfolio.full_clean()
            portfolio.save()

    def test_ex_portfolio_create_with_empty_api_secret(self):
        with self.assertRaises(ValidationError):
            portfolio = ExPortfolio.objects.create(exchanger=self.exchanger,
                                                   api_key=self.api_key,
                                                   api_secret='',
                                                   owner=self.owner)
            portfolio.full_clean()
            portfolio.save()

    def test_ex_portfolio_create_without_owner(self):
        with self.assertRaises(ObjectDoesNotExist):
            portfolio = ExPortfolio.objects.create(exchanger=self.exchanger,
                                                   api_key=self.api_key,
                                                   api_secret=self.api_secret
                                                   )

    def test_ex_portfolio_add_currencies(self):
        dump_to_db_currencies(5)
        currencies = Cryptocurrency.objects.all()

        owner_1 = User.objects.create(username='User_1', password='user_1')
        portfolio_1 = ExPortfolio.objects.create(exchanger=self.exchanger,
                                                 api_key=self.api_key,
                                                 api_secret=self.api_secret,
                                                 owner=owner_1)

        portfolio_1.currencies.add(currencies[0].id)
        self.assertEqual(portfolio_1.currencies.all().first(), currencies[0],
                         portfolio_1.currencies)

        portfolio_1.currencies.add(currencies[1].id)
        self.assertIn(currencies[1], portfolio_1.currencies.all(),
                      portfolio_1.currencies)

        owner_2 = User.objects.create(username='User_2', password='user_2')
        portfolio_2 = ExPortfolio.objects.create(exchanger=self.exchanger,
                                                 api_key=self.api_key,
                                                 api_secret=self.api_secret,
                                                 owner=owner_2)

        portfolio_2.currencies.add(currencies[0].id)
        self.assertEqual(portfolio_2.currencies.all().first(), currencies[0],
                         portfolio_2.currencies)

        portfolio_2.currencies.add(currencies[3].id)
        self.assertIn(currencies[3], portfolio_2.currencies.all(),
                      portfolio_2.currencies)

        user_1_portfolio = Exchanger.objects.get(pk=1).portfolio.filter(owner=owner_1).first()
        self.assertEqual(owner_1, user_1_portfolio.owner)
        self.assertIn(currencies[0], user_1_portfolio.currencies.all())
        self.assertIn(currencies[1], user_1_portfolio.currencies.all())

        user_2_portfolio = Exchanger.objects.get(pk=1).portfolio.filter(owner=owner_2).first()
        self.assertEqual(owner_2, user_2_portfolio.owner)
        self.assertIn(currencies[0], user_2_portfolio.currencies.all())
        self.assertIn(currencies[3], user_2_portfolio.currencies.all())

        BTC = Cryptocurrency.objects.first()
        self.assertEqual(owner_1, BTC.portfolio_currency.first().owner)
        self.assertIn(owner_2, [portfolio.owner
                                   for portfolio in BTC.portfolio_currency.all()])

        owner_3 = User.objects.create(username='User_3', password='user_3')
        self.assertNotIn(owner_3, [portfolio.owner
                                   for portfolio in BTC.portfolio_currency.all()])
