from django.urls import path

from . import views

app_name = 'cmc'

urlpatterns = [
    path('detail/<slug:slug>/', views.detail, name='crypto_detail'),

]
