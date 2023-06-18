from django.urls import path

from . import views

app_name = 'exchanger'

urlpatterns = [
    path('detail/<slug:slug>/', views.detail, name='detail'),

]