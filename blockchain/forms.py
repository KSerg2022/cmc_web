from django import forms

from .models import Portfolio

# EMPTY_FIELD_ERROR = "You can't have an empty field - "
# VALID_ERROR = 'Enter a valid - '


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['wallet', 'comments', 'currencies']

        widgets = {
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
