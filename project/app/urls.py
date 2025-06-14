from django.urls import path
from rest_framework import routers
from .users import views
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .users.views import CustomTokenObtainPairView

router = routers.DefaultRouter()

router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]