
from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from django.contrib.auth.models import User

from blockchain.models import Blockchain, Portfolio


class BlockchainModelTest(TestCase):

    def setUp(self) -> None:
        self.name = 'Blockchain test'
        self.slug = 'blockchain-test'
        self.host = 'https://api.bscscan.com/api'
        self.logo = 'tests/account/data_for_test/black.jpg'

    def test_blockchain_default_symbol(self):
        blockchain = Blockchain()
        self.assertEqual(blockchain.name, '')

    def test_blockchain_print(self):
        blockchain = Blockchain.objects.create(name=self.name,
                                             slug=self.slug)
        self.assertEqual(f'{self.name.capitalize()}', str(blockchain), blockchain)

    def test_blockchain_fields(self):
        fields = ['portfolio_blockchain', 'id', 'name', 'slug', 'host',
                  'is_active', 'logo', 'website', 'scan_site']
        blockchain = Blockchain.objects.create()
        model_fields = [field.name for field in blockchain._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)

    def test_blockchain_create_with_empty_name(self):
        with self.assertRaises(ValidationError):
            blockchain = Blockchain.objects.create(name='')
            blockchain.full_clean()
            blockchain.save()

    def test_blockchain_create_with_wrong_host(self):
        with self.assertRaises(ValidationError):
            blockchain = Blockchain.objects.create(name=self.name,
                                                 host='/url/url'
                                                 )
            blockchain.full_clean()
            blockchain.save()

    def test_blockchain_create_with_all_data(self):
        blockchain = Blockchain.objects.create(name=self.name,
                                             host=self.host,
                                             logo=self.logo)
        self.assertEqual(blockchain.name, self.name)
        self.assertEqual(blockchain.slug, self.slug)
        self.assertEqual(blockchain.host, self.host)
        self.assertTrue(blockchain.is_active)
        self.assertEqual(blockchain.logo, self.logo)

    def test_blockchain_is_active_False(self):
        blockchain = Blockchain.objects.create(name=self.name)
        self.assertTrue(blockchain.is_active)

        blockchain.is_active = False
        self.assertFalse(blockchain.is_active)

    def test_blockchain_create_with_invalid_format_photo(self):
        with self.assertRaises(ValidationError):
            blockchain = Blockchain.objects.create(name=self.name,
                                                       logo='tests/account/data_for_test/text.txt')
            blockchain.full_clean()
            blockchain.save()

    def test_blockchain_ordering(self):
        blockchain1 = Blockchain.objects.create(name=self.name)
        blockchain2 = Blockchain.objects.create(name=self.name + '1')
        blockchains = Blockchain.objects.all()

        self.assertEqual([f'{self.name.capitalize()}', f'{self.name.capitalize() + "1"}'],
                         [str(q) for q in blockchains],
                         blockchains)
        self.assertNotEqual([f'{self.name.capitalize() + "1"}', f'{self.name.capitalize()}'],
                            [str(q) for q in blockchains],
                            blockchains)

    def test_blockchain_get_absolute_url(self):
        blockchain = Blockchain.objects.create(name=self.name)

        self.assertEqual(blockchain.get_absolute_url(),
                         f'/blockchain/detail/{self.slug}/',
                         blockchain)


class PortfolioTest(TestCase):

    def setUp(self) -> None:
        self.name = 'Blockchain test'
        self.host = 'https://api.bscscan.com/api'
        self.blockchain = Blockchain.objects.create(name=self.name,
                                                    host=self.host)

        self.api_key = 'api_key'
        self.wallet = 'wallet'
        self.owner = User.objects.create(username='User1',
                                         password='password1')
        self.currencies = {"DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD",
                           "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
                           "GMI": "0x93D8d25E3C9A847a5Da79F79ecaC89461FEcA846"}

    def tearDown(self) -> None:
        pass

    def create_portfolio(self, currencies=None):
        return Portfolio.objects.create(owner=self.owner,
                                        blockchain=self.blockchain,
                                        api_key=self.api_key,
                                        wallet=self.wallet,
                                        currencies=currencies)

    def test_portfolio_default_symbol(self):
        portfolio = self.create_portfolio()
        self.assertEqual(portfolio.blockchain.name.capitalize(),
                         self.blockchain.name.capitalize())

    def test_portfolio_print(self):
        portfolio = self.create_portfolio()
        self.assertEqual(f'{self.owner.username} have {self.blockchain.name} portfolio',
                         str(portfolio), portfolio)

    def test_portfolio_fields(self):
        fields = ['id', 'owner', 'blockchain', 'slug', 'api_key', 'wallet',
                  'comments', 'currencies']
        portfolio = self.create_portfolio()
        model_fields = [field.name for field in portfolio._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)

    def test_portfolio_create_without_blockchain(self):
        with self.assertRaises(ObjectDoesNotExist):
            portfolio = Portfolio.objects.create(owner=self.owner,
                                                 api_key=self.api_key,
                                                 wallet=self.wallet
                                                 )

    def test_portfolio_create_with_empty_api_key(self):
        with self.assertRaises(ValidationError):
            portfolio = Portfolio.objects.create(owner=self.owner,
                                                 blockchain=self.blockchain,
                                                 api_key='',
                                                 wallet=self.wallet,
                                                 )
            portfolio.full_clean()
            portfolio.save()

    def test_portfolio_create_with_empty_api_secret(self):
        with self.assertRaises(ValidationError):
            portfolio = Portfolio.objects.create(owner=self.owner,
                                                 blockchain=self.blockchain,
                                                 api_key=self.api_key,
                                                 wallet=''
                                                 )
            portfolio.full_clean()
            portfolio.save()

    def test_portfolio_create_without_owner(self):
        with self.assertRaises(ObjectDoesNotExist):
            portfolio = Portfolio.objects.create(blockchain=self.blockchain,
                                                 api_key=self.api_key,
                                                 wallet=self.wallet
                                                 )

    def test_portfolio_add_currencies(self):
        portfolio = self.create_portfolio(currencies=self.currencies)

        self.assertEqual(portfolio.currencies, self.currencies)
        self.assertIsInstance(portfolio.currencies, dict)
