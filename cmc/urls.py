from django.urls import path

from . import views

app_name = 'cmc'

urlpatterns = [
    path('', views.index, name='index'),

]
