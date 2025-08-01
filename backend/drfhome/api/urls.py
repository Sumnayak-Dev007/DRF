from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('auth/',obtain_auth_token),
    path('',views.api_home),
    path('demo/',views.apidemo),
]
