from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Exchanger, ExPortfolio

EMPTY_FIELD_ERROR = "You can't have an empty field - "
VALID_ERROR = 'Enter a valid - '


class ExPortfolioForm(forms.ModelForm):
    class Meta:
        model = ExPortfolio
        fields = ['api_key', 'api_secret', 'password', 'comments']

        widgets = {
            'api_key': forms.TextInput(attrs={'style': 'height: 2em; width: 40em',
                                              'placeholder': "Enter a api key"}),
            'api_secret': forms.TextInput(attrs={'style': 'height: 2em; width: 40em',
                                                 'placeholder': "Enter a api secret"}),
            'password': forms.TextInput(attrs={'style': 'height: 2em; width: 40em',
                                               'placeholder': "Enter a password"}),
            'comments': forms.Textarea(attrs={'style': 'height: 5em; width: 40em',
                                              'placeholder': "Enter a comments"}),

        }
