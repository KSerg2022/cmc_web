import pdfkit
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from exchanger.cache import delete_cache_user_portfolios_data
from exchanger.views import get_path_to_wkhtmltopdf
from .cache import check_caches_blockchain_data, delete_caches_blockchain_data
from .forms import PortfolioForm
from .models import Portfolio, Blockchain
from exchanger.tasks import save_portfolio_to_xlsx_file


@login_required
def create_blockchain_portfolio(request, blockchain_id):
    blockchain = get_object_or_404(Blockchain,
                                   id=blockchain_id)
    form_portfolio = PortfolioForm()
    if request.method == 'POST':
        form_portfolio = PortfolioForm(data=request.POST)
        if form_portfolio.is_valid():
            portfolio = form_portfolio.save(commit=False)
            portfolio.owner = request.user
            portfolio.blockchain = blockchain
            portfolio.save()

            delete_caches_blockchain_data(portfolio)
            delete_cache_user_portfolios_data(portfolio.owner.id)

            messages.success(request, 'Portfolio created successfully')
            return redirect('exchanger:exchangers')
        else:
            messages.error(request, 'Error created your portfolio')

    return render(request, 'blockchain/add_portfolio.html', {'blockchain': blockchain,
                                                             'form_portfolio': form_portfolio,
                                                             'button': 'Create'})


@login_required
def change_blockchain_portfolio(request, blockchain_id):
    blockchain = get_object_or_404(Blockchain,
                                   id=blockchain_id)
    portfolio = get_object_or_404(Portfolio,
                                  owner=request.user,
                                  blockchain=blockchain_id)

    form_portfolio = PortfolioForm(instance=portfolio)
    if request.method == 'POST':
        form_portfolio = PortfolioForm(data=request.POST)
        if form_portfolio.is_valid():
            portfolio.wallet = form_portfolio.cleaned_data.get('wallet')
            portfolio.comments = form_portfolio.cleaned_data.get('comments')
            portfolio.currencies = form_portfolio.cleaned_data.get('currencies')
            portfolio.save()

            delete_caches_blockchain_data(portfolio)
            delete_cache_user_portfolios_data(portfolio.owner.id)

            messages.success(request, 'Portfolio changed successfully')
            return redirect('exchanger:exchangers')
        else:
            messages.error(request, 'Error changed your portfolio')

    return render(request, 'blockchain/add_portfolio.html', {'blockchain': blockchain,
                                                             'form_portfolio': form_portfolio,
                                                             'button': 'Change'})


@login_required
def delete_blockchain_portfolio(request, blockchain_id):
    blockchain = get_object_or_404(Blockchain,
                                   id=blockchain_id)
    portfolio = get_object_or_404(Portfolio,
                                  owner=request.user,
                                  blockchain=blockchain_id)

    form = PortfolioForm(instance=portfolio)
    if request.GET.get('yes') == 'yes':
        portfolio.delete()
        messages.success(request, f'Portfolio {portfolio.blockchain} deleted successfully')

        delete_caches_blockchain_data(portfolio)
        delete_cache_user_portfolios_data(portfolio.owner.id)

        return redirect('exchanger:exchangers')

    return render(request, 'blockchain/delete_portfolio.html', {'blockchain': blockchain,
                                                                'form': form})


@login_required
def get_blockchain_data(request, blockchain_id):
    portfolio = get_object_or_404(Portfolio,
                                  owner=request.user,
                                  blockchain=blockchain_id)

    response_blockchain, total_sum = check_caches_blockchain_data(portfolio)

    portfolio_name = portfolio.blockchain.name
    save_portfolio_to_xlsx_file.delay(request.user.id,
                                      [{portfolio_name: response_blockchain}],
                                      portfolio_name)

    if 'error' in response_blockchain[0]:
        return render(request, 'blockchain/data_portfolio.html', {'portfolio': portfolio,
                                                                  'data': response_blockchain,
                                                                  'total_sum': 0,
                                                                  })

    return render(request, 'blockchain/data_portfolio.html', {'portfolio': portfolio,
                                                              'data': response_blockchain,
                                                              'total_sum': total_sum,
                                                              })


@login_required
def detail(request, slug):
    return render(request, 'blockchain/detail.html')


@login_required
def get_blockchain_data_pdf(request, blockchain_id):
    """
    https://www.geeksforgeeks.org/python-convert-html-pdf/
    https://pythoncircle.com/post/470/generating-and-returning-pdf-as-response-in-django/
    """
    portfolio = get_object_or_404(Portfolio,
                                  owner=request.user,
                                  blockchain=blockchain_id)
    response_blockchain, total_sum = check_caches_blockchain_data(portfolio)

    pdf = get_blockchain_pdf(portfolio, response_blockchain, total_sum)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=PDF_{portfolio.blockchain.name}' \
                                      f'_{portfolio.owner.username.capitalize()}.pdf'
    return response


def get_blockchain_pdf(portfolio, user_portfolio_data, total_sum):
    html = render_to_string('blockchain/pdf_blockchain.html',
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
