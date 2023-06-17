from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, HttpResponse, get_object_or_404

from django import forms

from cmc.models import Cryptocurrency


PAGINATOR_QTY = 10


def index(request):

    cryptocurrencies_list = Cryptocurrency.objects.all().order_by('id')[:154]
    paginator = Paginator(cryptocurrencies_list, per_page=PAGINATOR_QTY)
    page_numer = request.GET.get('page', 1)
    page_range = []
    if len(cryptocurrencies_list) > PAGINATOR_QTY:
        page_range = paginator.get_elided_page_range(number=paginator.num_pages // 2, on_each_side=3, on_ends=2)

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
    crypto = get_object_or_404(Cryptocurrency,
                               slug=slug
                               )

    return render(request, 'cmc/cmc/detail.html',
                  {'crypto': crypto}
                  )
