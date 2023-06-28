from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from cmc.handlers.aggregation import get_aggregation_data
from cmc.handlers.cmc import Cmc
from .handlers import get_paginator
from .models import Exchanger, ExPortfolio
from .forms import ExPortfolioForm
from .utils.main.main_2 import main
from exchanger.utils.handlers.xlsx_file import XlsxFile

from blockchain.models import Blockchain


@login_required
def exchangers(request):
    exchangers_list = Exchanger.objects.filter(is_active=True)
    blockchains_list = Blockchain.objects.filter(is_active=True)
    return render(request, 'exchanger/exchangers.html', {'exchangers': exchangers_list,
                                                         'blockchains_list': blockchains_list})


@login_required
def create_portfolio(request, exchanger_id):
    exchanger = Exchanger.objects.get(id=exchanger_id)
    form = ExPortfolioForm()
    if request.method == 'POST':
        form = ExPortfolioForm(data=request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.owner = request.user
            portfolio.exchanger = exchanger
            portfolio.save()

            messages.success(request, 'Portfolio created successfully')
            return redirect('exchanger:exchangers')
        else:
            messages.error(request, 'Error created your portfolio')

    return render(request, 'exchanger/add_portfolio.html', {'exchanger': exchanger,
                                                            'form': form,
                                                            'button': 'Create'})


@login_required
def change_portfolio(request, exchanger_id):
    exchanger = Exchanger.objects.get(id=exchanger_id)
    portfolio = get_object_or_404(ExPortfolio,
                                  owner=request.user,
                                  exchanger=exchanger_id)

    form = ExPortfolioForm(instance=portfolio)
    if request.method == 'POST':
        form = ExPortfolioForm(data=request.POST)
        if form.is_valid():
            portfolio.api_key = form.cleaned_data.get('api_key')
            portfolio.api_secret = form.cleaned_data.get('api_secret')
            portfolio.password = form.cleaned_data.get('password')
            portfolio.comments = form.cleaned_data.get('comments')
            portfolio.save()

            messages.success(request, 'Portfolio changed successfully')
            return redirect('exchanger:exchangers')
        else:
            messages.error(request, 'Error changed your portfolio')

    return render(request, 'exchanger/add_portfolio.html', {'exchanger': exchanger,
                                                            'form': form,
                                                            'button': 'Change'})


@login_required
def delete_portfolio(request, exchanger_id):
    exchanger = Exchanger.objects.get(id=exchanger_id)
    portfolio = get_object_or_404(ExPortfolio,
                                  owner=request.user,
                                  exchanger=exchanger_id)

    form = ExPortfolioForm(instance=portfolio)
    if request.GET.get('yes') == 'yes':
        portfolio.delete()
        messages.success(request, f'Portfolio {portfolio.exchanger} deleted successfully')
        return redirect('exchanger:exchangers')

    return render(request, 'exchanger/delete_portfolio.html', {'exchanger': exchanger,
                                                               'form': form})


from exchanger.utils.ex_okx import ExOkx


@login_required
def get_data(request, exchanger_id):
    exchanger = get_object_or_404(Exchanger,
                                  id=exchanger_id)
    portfolio = get_object_or_404(ExPortfolio,
                                  owner=request.user,
                                  exchanger=exchanger_id)
    okx = ExOkx(api_key=portfolio.api_key,
                api_secret=portfolio.api_secret,
                passphrase=portfolio.password)
    data_exchanger = okx.get_account()
    symbol_list = [coin['coin'] for coin in list(data_exchanger.values())[0]]

    data_cmc = Cmc(symbol_list).get_data_from_cmc()
    data_total = get_aggregation_data(data_from_cmc=data_cmc,
                                      data_from_exchangers=[data_exchanger])
    total_sum = sum([coin['total'] for coin in list(data_total[0].values())[0]])

    data_, page_range = get_paginator(request, list(data_total[0].values())[0])
    return render(request, 'exchanger/data_portfolio.html', {'exchanger': exchanger,
                                                             'data': data_,
                                                             'total_sum': total_sum,
                                                             'page_range': page_range
                                                             })


@login_required
def get_all_data(request, user_id):
    user_portfolios_data = main(user_id)
    XlsxFile(request.user).create_xlsx(user_portfolios_data)
    return render(request, 'exchanger/data_all_portfolios.html',
                  {'user_portfolios_data': user_portfolios_data})


@login_required
def detail(request, slug):
    return render(request, 'exchanger/detail.html')
