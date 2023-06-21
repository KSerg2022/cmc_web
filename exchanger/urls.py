from django.urls import path

from . import views

app_name = 'exchanger'

urlpatterns = [
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('detail/<int:id>/<str:exchenger>/<slug:slug>/', views.detail, name='detail'),
    path('create_portfolio/<str:exchanger_id>/', views.create_portfolio, name='create_portfolio'),
    path('change_portfolio/<str:exchanger_id>/', views.change_portfolio, name='change_portfolio'),
    path('delete_portfolio/<str:exchanger_id>/', views.delete_portfolio, name='delete_portfolio'),
    path('data/<int:exchanger_id>/', views.get_data, name='get_data'),
    path('', views.exchangers, name='exchangers'),

]