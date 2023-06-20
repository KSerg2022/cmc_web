from django.urls import path

from . import views

app_name = 'exchanger'

urlpatterns = [
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('detail/<int:id>/<str:exchenger>/<slug:slug>/', views.detail, name='detail'),
    path('create_portfolio/<str:exchanger_id>/', views.create_portfolio, name='create_portfolio'),
    path('', views.exchangers, name='exchangers'),

]