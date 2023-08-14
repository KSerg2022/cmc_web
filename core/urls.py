"""
URL configuration for cmc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cmc.views import index
from exchanger.views import send_XLSX_by_email, send_PDF_by_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),

    path('exchanger/', include('exchanger.urls', namespace='exchanger')),
    path('blockchain/', include('blockchain.urls', namespace='blockchain')),

    path('cmc/', include('cmc.urls', namespace='cmc')),

    path('send_XLSX_by_email/<str:portfolio>/', send_XLSX_by_email, name='send_XLSX_by_email'),
    path('send_XLSX_by_email/<path:path_to_file>/', send_XLSX_by_email, name='send_XLSX_by_email'),
    path('send_PDF_by_email/<int:user_id>/', send_PDF_by_email, name='send_PDF_by_email'),
    path('send_PDF_by_email/<int:user_id>/<str:portfolio>/', send_PDF_by_email, name='send_PDF_by_email'),

    path('', index, name='index'),
]

from account.api.urls import urlpatterns as users_urlpatterns
from blockchain.api.urls import urlpatterns as blockchain_urlpatterns
from exchanger.api.urls import urlpatterns as exchanger_urlpatterns

urlpatterns += [*users_urlpatterns, *blockchain_urlpatterns, *exchanger_urlpatterns]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
