from django.urls import path

from . import views

app_name = 'exchanger'

urlpatterns = [
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('detail/<int:id>/<str:exchenger>/<slug:slug>/', views.detail, name='detail'),
    path('create_portfolio/<int:exchanger_id>/', views.create_portfolio, name='create_portfolio'),
    path('change_portfolio/<int:exchanger_id>/', views.change_portfolio, name='change_portfolio'),
    path('delete_portfolio/<int:exchanger_id>/', views.delete_portfolio, name='delete_portfolio'),
    path('data/<int:exchanger_id>/', views.get_exchanger_data, name='get_exchanger_data'),
    path('all-data/<int:user_id>/', views.get_all_data, name='get_all_data'),
    path('all_data_pdf/<int:user_id>/', views.get_all_data_pdf, name='get_all_data_pdf'),
    path('exchanger_data_pdf/<int:exchanger_id>/', views.get_exchanger_data_pdf, name='get_exchanger_data_pdf'),
    path('', views.exchangers, name='exchangers'),

]