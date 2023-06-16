from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, HttpResponse
from django import forms

from cmc.models import Cryptocurrency


PAGINATOR_QTY = 10


def index(request):
    cryptocurrencies_list = Cryptocurrency.objects.all().order_by('id')[:275]
    paginator = Paginator(cryptocurrencies_list, per_page=PAGINATOR_QTY, orphans=PAGINATOR_QTY)
    page_range = paginator.get_elided_page_range(number=10, on_each_side=3, on_ends=2)

    page_numer = request.GET.get('page', 1)

    try:
        cryptocurrencies = paginator.page(page_numer)
    except PageNotAnInteger:
        cryptocurrencies = paginator.page(1)
    except EmptyPage:
        cryptocurrencies = paginator.page(paginator.num_pages)

    return render(request,
                  'cmc/cmc/index.html',
                  {'cryptocurrencies': cryptocurrencies,
                   'page_range': page_range})


def detail(request, slug):
    return render(request, 'cmc/cmc/detail.html')

