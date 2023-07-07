from django.test import TestCase
from django.utils.html import escape

from exchanger.forms import ExPortfolioForm


class ExPortfolioFormTest(TestCase):

    def test_form_fields_is(self):
        form = ExPortfolioForm()
        fields = ('api_key', 'api_secret', 'password', 'comments',)
        for field in fields:
            self.assertIn(field, form.fields)

    def test_form_render_text_input(self):
        form = ExPortfolioForm()
        self.assertIn('placeholder="Enter a api key"', form.as_table())
        self.assertIn('placeholder="Enter a api secret"', form.as_table())
        placeholder = escape("Now only for 'OKX'. Enter a password")
        self.assertIn(f'placeholder="{placeholder}"', form.as_table())
        self.assertIn(f'placeholder="Enter a comments"', form.as_table())

    def test_form_validation_for_blank_api_key(self):
        form = ExPortfolioForm(data={'api_key': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['api_key'], ['This field is required.'])

    def test_form_validation_for_blank_api_secret(self):
        form = ExPortfolioForm(data={'api_key': 'api_key',
                                     'api_secret': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['api_secret'], ['This field is required.'])
