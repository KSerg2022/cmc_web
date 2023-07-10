import pdfkit
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.cache import cache

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
    # exchanger = Exchanger.objects.get(id=exchanger_id)
    exchanger = get_object_or_404(Exchanger,
                                  id=exchanger_id)
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
    exchanger = get_object_or_404(Exchanger,
                                  id=exchanger_id)
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

    cache_user_exchanger = cache.get(f'user_{portfolio.owner.username.capitalize()}_exchanger_{portfolio.exchanger}')
    cache_user_total_sum = cache.get(f'user_{portfolio.owner.username.capitalize()}_total_sum_{portfolio.exchanger}')

    if cache_user_exchanger and cache_user_total_sum:
        response_exchanger = cache_user_exchanger
        total_sum = cache_user_total_sum
    else:
        response_exchanger, total_sum = get_data(portfolio)
        cache.set(f'user_{portfolio.owner.username.capitalize()}_exchanger_{portfolio.exchanger}',
                  response_exchanger, 60*3)
        cache.set(f'user_{portfolio.owner.username.capitalize()}_total_sum_{portfolio.exchanger}',
                  total_sum, 60*3)

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
    cache_user_portfolios_data = cache.get(f'user_{user_id}_portfolios_data')
    if cache_user_portfolios_data:
        user_portfolios_data = cache_user_portfolios_data
    else:
        user_portfolios_data = all_dada(user_id)
        cache.set(f'user_{user_id}_portfolios_data', user_portfolios_data, 60*10)

    XlsxFile(request.user).create_xlsx(user_portfolios_data)
    return render(request, 'exchanger/data_all_portfolios.html',
                  {'user_portfolios_data': user_portfolios_data})


@login_required
def detail(request, slug):
    return render(request, 'exchanger/detail.html')


@login_required
def get_all_data_pdf(request, user_id):
    """
    https://www.geeksforgeeks.org/python-convert-html-pdf/
    https://pythoncircle.com/post/470/generating-and-returning-pdf-as-response-in-django/
    """
    user = get_object_or_404(User, id=user_id)

    cache_user_portfolios_data = cache.get(f'user_{user_id}_portfolios_data')
    if cache_user_portfolios_data:
        user_portfolios_data = cache_user_portfolios_data
    else:
        user_portfolios_data = all_dada(user_id)
        cache.set(f'user_{user_id}_portfolios_data', user_portfolios_data, 60*10)

    pdf = get_pdf(user_portfolios_data)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=PDF_portfolio_User_{user.username.capitalize()}.pdf'
    return response


def get_pdf(user_portfolios_data):
    html = render_to_string('exchanger/pdf.html', {'user_portfolios_data': user_portfolios_data})
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf_settings = {
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdf = pdfkit.from_string(input=html,
                             css=settings.STATIC_ROOT / 'cmc/css/pdf.css',
                             configuration=config,
                             options=pdf_settings)
    return pdf
