from django.shortcuts import render, HttpResponse
from django import forms


def index(request):

    return render(request, 'cmc/cmc/index.html')


def detail(request, slug):
    pass

