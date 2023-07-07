from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django_json_widget.widgets import JSONEditorWidget

from .models import (Blockchain,
                     Portfolio,
                     )

# EMPTY_FIELD_ERROR = "You can't have an empty field - "
# VALID_ERROR = 'Enter a valid - '


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['api_key', 'wallet', 'comments', 'currencies']

        widgets = {
            'api_key': forms.TextInput(attrs={'style': 'height: 2em; width: 40em',
                                              'placeholder': "Enter a api key"}),
            'wallet': forms.TextInput(attrs={'style': 'height: 2em; width: 40em',
                                             'placeholder': "Enter a wallet"}),
            'comments': forms.Textarea(attrs={'style': 'height: 5em; width: 40em',
                                              'placeholder': "Enter a comments"}),
            'currencies': forms.Textarea(attrs={'style': 'height: 10em; width: 40em',
                                                'placeholder': '{\n"SYMBOL1": "adresse 1",\n'
                                                               '"SYMBOL2": "adresse 2",\n'
                                                               '"SYMBOL3": "adresse 3"\n}'}
                                         )
        }

        error_messages = {
            'currencies': {'invalid': 'Enter a valid JSON.'},
        }
