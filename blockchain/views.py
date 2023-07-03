from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


from .forms import PortfolioForm
from .models import Portfolio, Blockchain
from .utils.handlers.get_data import get_data


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
            print(form_portfolio.cleaned_data.values())
            portfolio.api_key = form_portfolio.cleaned_data.get('api_key')
            portfolio.wallet = form_portfolio.cleaned_data.get('wallet')
            portfolio.comments = form_portfolio.cleaned_data.get('comments')
            portfolio.currencies = form_portfolio.cleaned_data.get('currencies')
            portfolio.save()

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
        return redirect('exchanger:exchangers')

    return render(request, 'blockchain/delete_portfolio.html', {'blockchain': blockchain,
                                                                'form': form})


@login_required
def get_blockchain_data(request, blockchain_id):
    portfolio = get_object_or_404(Portfolio,
                                  owner=request.user,
                                  blockchain=blockchain_id)
    response_blockchain, total_sum = get_data(portfolio)

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
