from django.shortcuts import render

# Create your views here.


def detail(request, slug):
    return render(request, 'exchanger/detail.html')
