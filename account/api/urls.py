from django.urls import path, include
from rest_framework import routers


from account.api.views import UserViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/user/profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    ]
