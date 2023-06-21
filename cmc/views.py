from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, HttpResponse, get_object_or_404

from django import forms

from cmc.models import Cryptocurrency
from exchanger.handlers import get_paginator

PAGINATOR_QTY = 10


def index(request):

    cryptocurrencies_list = Cryptocurrency.objects.all().order_by('id')[:154]
    cryptocurrencies, page_range = get_paginator(request, cryptocurrencies_list)
    return render(request,
                  'cmc/cmc/index.html',
                  {'cryptocurrencies': cryptocurrencies,
                   'page_range': page_range})


def detail(request, slug):
    crypto = get_object_or_404(Cryptocurrency,
                               slug=slug
                               )

    return render(request, 'cmc/cmc/detail.html',
                  {'crypto': crypto}
                  )
