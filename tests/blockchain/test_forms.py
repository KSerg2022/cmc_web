from django.test import TestCase
from django.utils.html import escape

from blockchain.forms import PortfolioForm


class PortfolioFormTest(TestCase):

    def test_form_fields_is(self):
        form = PortfolioForm()
        fields = ('api_key', 'wallet', 'comments', 'currencies',)
        for field in fields:
            self.assertIn(field, form.fields)

    def test_form_render_text_input(self):
        form = PortfolioForm()
        self.assertIn('placeholder="Enter a api key"', form.as_table())
        self.assertIn('placeholder="Enter a wallet"', form.as_table())
        self.assertIn('placeholder="Enter a comments"', form.as_table())

        placeholder = escape('{\n"SYMBOL1": "adresse 1",\n'
                             '"SYMBOL2": "adresse 2",\n'
                             '"SYMBOL3": "adresse 3"\n}')
        self.assertIn(f'placeholder="{placeholder}"', form.as_table())

    def test_form_validation_for_blank_api_key(self):
        form = PortfolioForm(data={'api_key': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['api_key'], ['This field is required.'])

    def test_form_validation_for_blank_wallet(self):
        form = PortfolioForm(data={'api_key': 'api_key',
                                   'wallet': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['wallet'], ['This field is required.'])

    def test_form_validation_for_blank_currencies_json(self):
        form = PortfolioForm(data={'api_key': 'api_key',
                                   'wallet': 'wallet',
                                   'currencies': 'currencies'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['currencies'], ['Enter a valid JSON.'])
