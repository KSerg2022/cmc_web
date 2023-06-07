from django.shortcuts import render, HttpResponse
from django import forms


class NameForm(forms.Form):
    name = forms.CharField(max_length=255)


def index(request):
    form = NameForm()
    return render(request, 'cmc/cmc/index.html', {'form': form})
