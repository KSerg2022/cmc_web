from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Profile

EMPTY_FIELD_ERROR = "You can't have an empty field - "
VALID_ERROR = 'Enter a valid - '


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'style': 'height: 20em; width: 65em',
                                               'placeholder': "Enter a user name"}),
            'password': forms.TextInput(attrs={'placeholder': "Enter a user password"}),
        }

        error_messages = {
            'username': {'required': EMPTY_FIELD_ERROR + '"username"'},
            'password': {'required': EMPTY_FIELD_ERROR + '"password"'},
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'style': 'height: 2em; width: 20em',
                                                                 'placeholder': "Enter a password"}),
                               validators=[validate_password],
                               error_messages={'required': EMPTY_FIELD_ERROR + '"password"',
                                               'invalid': VALID_ERROR + '"password"'
                                               # 'short': VALID_ERROR + '"password"'
                                               # 'unique': '',

                               },
                               )
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'style': 'height: 2em; width: 20em',
                                                                  'placeholder': "Repeat a password"}),
                                validators=[validate_password],
                                error_messages={'required': EMPTY_FIELD_ERROR + '"password"',
                                                'invalid': VALID_ERROR + '"password"'},
                                )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'style': 'height: 2em; width: 20em',
                                               'placeholder': "Enter a user name"}),
            'first_name': forms.TextInput(attrs={'style': 'height: 2em; width: 20em',
                                                 'placeholder': "Enter a last name"}),
            'email': forms.EmailInput(attrs={'style': 'height: 2em; width: 20em',
                                             'placeholder': "Enter a email"}),
        }

        error_messages = {
            'username': {'required': EMPTY_FIELD_ERROR + '"username"'},
            'email': {'required': EMPTY_FIELD_ERROR + '"email"',
                      'invalid': VALID_ERROR + '"email"'},
            'password': {'required': EMPTY_FIELD_ERROR + '"password"'},

        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'height: 2em; width: 20em',
                                                 'placeholder': "Enter a first name"}),
            'last_name': forms.TextInput(attrs={'style': 'height: 2em; width: 20em',
                                                'placeholder': "Enter a last name"}),
            'email': forms.EmailInput(attrs={'style': 'height: 2em; width: 20em',
                                             'placeholder': "Enter a email"}),
        }

        error_messages = {
            'email': {'required': EMPTY_FIELD_ERROR + '"email"',
                      'invalid': VALID_ERROR + '"email"'},
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'placeholder': "Enter a date of birth"}),
            'photo': forms.FileInput(attrs={'placeholder': "Choose a user photo"}),
        }
