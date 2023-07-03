from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


from .models import Exchanger, ExPortfolio
from .forms import ExPortfolioForm
from .utils.main.get_data import get_data
from .utils.main.get_all_data import get_all_data as all_dada
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


@login_required
def get_exchanger_data(request, exchanger_id):
    portfolio = get_object_or_404(ExPortfolio,
                                  owner=request.user,
                                  exchanger=exchanger_id)
    response_exchanger, total_sum = get_data(portfolio)

    if 'error' in response_exchanger[0]:
        return render(request, 'exchanger/data_portfolio.html', {'portfolio': portfolio,
                                                                 'data': response_exchanger,
                                                                 'total_sum': 0,
                                                                 })

    return render(request, 'exchanger/data_portfolio.html', {'portfolio': portfolio,
                                                             'data': response_exchanger,
                                                             'total_sum': total_sum,
                                                             })


@login_required
def get_all_data(request, user_id):
    user_portfolios_data = all_dada(user_id)
    XlsxFile(request.user).create_xlsx(user_portfolios_data)
    return render(request, 'exchanger/data_all_portfolios.html',
                  {'user_portfolios_data': user_portfolios_data})


@login_required
def detail(request, slug):
    return render(request, 'exchanger/detail.html')
