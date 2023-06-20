from django.test import TestCase
from django.core.exceptions import ValidationError

from cmc.models import Cryptocurrency
from django.contrib.auth import get_user_model

User = get_user_model()


class CryptocurrencyModelTest(TestCase):

    def setUp(self) -> None:
        self.symbol = 'symbol_test'
        self.name = 'name_test'
        self.slug = 'name_test'
        self.website = 'test@test.com',
        self.contract = '123456789',
        self.description = 'description',
        self.logo = 'tests/account/data_for_test/black.jpg'

    def test_cryptocurrency_default_symbol(self):
        cryptocurrency = Cryptocurrency()
        self.assertEqual(cryptocurrency.symbol, '')

    def test_cryptocurrency_print(self):
        cryptocurrency = Cryptocurrency.objects.create(symbol=self.symbol,
                                                       name=self.name,
                                                       slug=self.slug)
        self.assertEqual(f'{self.name}. {self.symbol}', str(cryptocurrency), cryptocurrency)

    def test_cryptocurrency_fields(self):
        fields = ['portfolio_currency', 'id', 'symbol', 'name', 'slug', 'website',
                  'contract', 'description', 'logo']
        cryptocurrency = Cryptocurrency.objects.create()
        model_fields = [field.name for field in cryptocurrency._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)

    def test_cryptocurrency_create_with_empty_symbol(self):
        with self.assertRaises(ValidationError):
            cryptocurrency = Cryptocurrency.objects.create(symbol='',
                                                           name=self.name,
                                                           slug=self.slug)
            cryptocurrency.full_clean()
            cryptocurrency.save()

    def test_cryptocurrency_create_with_empty_name(self):
        with self.assertRaises(ValidationError):
            cryptocurrency = Cryptocurrency.objects.create(symbol=self.symbol,
                                                           name='',
                                                           slug=self.slug)
            cryptocurrency.full_clean()
            cryptocurrency.save()

    def test_cryptocurrency_create_with_empty_slug(self):
        with self.assertRaises(ValidationError):
            cryptocurrency = Cryptocurrency.objects.create(symbol=self.symbol,
                                                           name=self.name,
                                                           slug='')
            cryptocurrency.full_clean()
            cryptocurrency.save()

    def test_cryptocurrency_create_with_all_data(self):
        cryptocurrency = Cryptocurrency.objects.create(symbol=self.symbol,
                                                       name=self.name,
                                                       slug=self.slug,
                                                       website=self.website,
                                                       contract=self.contract,
                                                       description=self.description,
                                                       logo=self.logo)
        self.assertEqual(cryptocurrency.website, self.website)
        self.assertEqual(cryptocurrency.contract, self.contract)
        self.assertEqual(cryptocurrency.description, self.description)
        self.assertEqual(cryptocurrency.logo, self.logo)

    def test_cryptocurrency_create_with_invalid_format_photo(self):
        with self.assertRaises(ValidationError):
            cryptocurrency = Cryptocurrency.objects.create(symbol=self.symbol,
                                                           name=self.name,
                                                           slug=self.slug,
                                                           logo='tests/account/data_for_test/text.txt')
            cryptocurrency.full_clean()
            cryptocurrency.save()

    def test_cryptocurrency_ordering(self):
        cryptocurrency1 = Cryptocurrency.objects.create(symbol=self.symbol,
                                                        name=self.name,
                                                        slug=self.slug)
        cryptocurrency2 = Cryptocurrency.objects.create(symbol=self.symbol + '1',
                                                        name=self.name + '1',
                                                        slug=self.slug + '1')
        cryptocurrencies = Cryptocurrency.objects.all()

        self.assertEqual([f'{self.name}. {self.symbol}', f'{self.name + "1"}. {self.symbol + "1"}'],
                         [str(q) for q in cryptocurrencies],
                         cryptocurrencies)
        self.assertNotEqual([f'{self.name + "1"}. {self.symbol + "1"}', f'{self.name}. {self.symbol}'],
                         [str(q) for q in cryptocurrencies],
                         cryptocurrencies)

    def test_cryptocurrency_get_absolute_url(self):
        cryptocurrency = Cryptocurrency.objects.create(symbol=self.symbol,
                                                       name=self.name,
                                                       slug=self.slug)
        # cryptocurrency.full_clean()
        # cryptocurrency.save()

        self.assertEqual(cryptocurrency.get_absolute_url(),
                         f'/cmc/detail/{self.slug}/',
                         cryptocurrency)
