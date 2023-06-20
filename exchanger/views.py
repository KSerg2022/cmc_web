from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Exchanger, ExPortfolio
from .forms import ExPortfolioForm


@login_required
def exchangers(request):
    exchangers_list = Exchanger.objects.all().filter(is_active=True)
    user_exchangers = ExPortfolio.objects.all().filter(owner=request.user.id)
    print('1---', user_exchangers)
    return render(request, 'exchanger/exchangers.html', {'exchangers': exchangers_list,
                                                         'user_exchangers': user_exchangers}
                  )


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
        else:
            messages.error(request, 'Error created your portfolio')
    user_exchangers = ExPortfolio.objects.all().filter(owner=request.user.id)
    return render(request, 'exchanger/add_portfolio.html', {'exchanger': exchanger,
                                                            'user_exchangers': user_exchangers,
                                                            'form': form})

@login_required
def detail(request, slug):
    return render(request, 'exchanger/detail.html')
