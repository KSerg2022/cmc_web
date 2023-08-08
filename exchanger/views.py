import os

import pdfkit
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

from local_settings import path_wkhtmltopdf_win, path_wkhtmltopdf_lin
from .cache import (check_cache_user_portfolios_data,
                    check_caches_exchanger_data,
                    delete_caches_exchanger_data,
                    delete_cache_user_portfolios_data)
from .models import Exchanger, ExPortfolio
from .forms import ExPortfolioForm

from exchanger.tasks import save_portfolio_to_xlsx_file, save_all_to_xlsx_file, sending_email

from blockchain.models import Blockchain


@login_required
def exchangers(request):
    exchangers_list = Exchanger.objects.filter(is_active=True)
    blockchains_list = Blockchain.objects.filter(is_active=True)
    return render(request, 'exchanger/exchangers.html', {'exchangers': exchangers_list,
                                                         'blockchains_list': blockchains_list})


@login_required
def create_portfolio(request, exchanger_id):
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

            delete_caches_exchanger_data(portfolio)
            delete_cache_user_portfolios_data(portfolio.owner.id)

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

            delete_caches_exchanger_data(portfolio)
            delete_cache_user_portfolios_data(portfolio.owner.id)

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

        delete_caches_exchanger_data(portfolio)
        delete_cache_user_portfolios_data(portfolio.owner.id)

        return redirect('exchanger:exchangers')

    return render(request, 'exchanger/delete_portfolio.html', {'exchanger': exchanger,
                                                               'form': form})


@login_required
def get_exchanger_data(request, exchanger_id):
    portfolio = get_object_or_404(ExPortfolio,
                                  owner=request.user,
                                  exchanger=exchanger_id)
    response_exchanger, total_sum = check_caches_exchanger_data(portfolio)

    portfolio_name = portfolio.exchanger.name
    save_portfolio_to_xlsx_file.delay(request.user.id,
                                      [{portfolio_name: response_exchanger}],
                                      portfolio_name)

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
def get_exchanger_data_pdf(request, exchanger_id):
    """
    https://www.geeksforgeeks.org/python-convert-html-pdf/
    https://pythoncircle.com/post/470/generating-and-returning-pdf-as-response-in-django/
    """
    portfolio = get_object_or_404(ExPortfolio,
                                  owner=request.user,
                                  exchanger=exchanger_id)
    response_exchanger, total_sum = check_caches_exchanger_data(portfolio)

    pdf = get_exchanger_pdf(portfolio, response_exchanger, total_sum)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=PDF_{portfolio.exchanger.name}' \
                                      f'_{portfolio.owner.username.capitalize()}.pdf'
    return response


def get_exchanger_pdf(portfolio, user_portfolio_data, total_sum):
    html = render_to_string('exchanger/pdf_exchanger.html',
                            {'portfolio': portfolio,
                             'user_portfolio_data': user_portfolio_data,
                             'total_sum': total_sum})
    path_wkhtmltopdf = get_path_to_wkhtmltopdf()
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


@login_required
def get_all_data(request, user_id):
    user_portfolios_data = check_cache_user_portfolios_data(user_id)

    save_all_to_xlsx_file.delay(request.user.id, user_portfolios_data, 'ALL')

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
    user_portfolios_data = check_cache_user_portfolios_data(user_id)

    pdf = get_pdf(user_portfolios_data)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=PDF_portfolio_User_{user.username.capitalize()}.pdf'
    return response


def get_pdf(user_portfolios_data):
    html = render_to_string('exchanger/pdf.html', {'user_portfolios_data': user_portfolios_data})
    path_wkhtmltopdf = get_path_to_wkhtmltopdf()
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


def get_path_to_wkhtmltopdf():
    path_wkhtmltopdf = path_wkhtmltopdf_win
    if os.path.isfile(path_wkhtmltopdf):
        return path_wkhtmltopdf
    return path_wkhtmltopdf_lin


@login_required
def send_email(request, path_to_file=None, portfolio=None):
    if path_to_file:
        sending_email.delay(request.user.id, path_to_file)
    if portfolio:
        xlsx_dir = settings.MEDIA_URL + 'xlsx_files/' + f'{request.user.id}_{request.user.username.lower()}/'
        filename = f'{request.user.id}_{request.user.username.lower()}_{portfolio}.xlsx'
        path_to_file = xlsx_dir + filename
        sending_email.delay(request.user.id, path_to_file)
    messages.success(request, f'Portfolios were send to your email.')
    return redirect(request.META.get('HTTP_REFERER'))
