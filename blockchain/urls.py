from django.urls import path

from . import views

app_name = 'blockchain'

urlpatterns = [
    path('detail/<slug:slug>/', views.detail, name='detail'),
    # path('detail/<int:id>/<str:exchenger>/<slug:slug>/', views.detail, name='detail'),
    path('create_portfolio/<int:blockchain_id>/', views.create_blockchain_portfolio,
         name='create_blockchain_portfolio'),
    path('change_portfolio/<int:blockchain_id>/', views.change_blockchain_portfolio,
         name='change_blockchain_portfolio'),
    path('delete_portfolio/<int:blockchain_id>/', views.delete_blockchain_portfolio,
         name='delete_blockchain_portfolio'),
    # path('data/<int:exchanger_id>/', views.get_data, name='get_data'),
    # path('all-data/<int:user_id>/', views.get_all_data, name='get_all_data'),

]
