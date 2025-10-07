from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from common.logging.view_part_logging.baseapiview import BaseTokenObtainPairView
from .views import UserRegistrationView

app_name = "user"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("token/login/", BaseTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
