from django.urls import path
from .views import RegisterView, LogoutAPIView, SetNewPasswordAPIView, LoginView, PasswordTokenCheckAPI,  \
    MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('users/', MyTokenObtainPairView.as_view(), name="logou"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    # path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('request-reset-email/', RequestPasswordResetEmail.as_view(),
    #      name="request-reset-email"),
    # path('password-reset/<uidb64>/<token>/',
    #      PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('password-reset-complete', SetNewPasswordAPIView.as_view(),
    #      name='password-reset-complete')
]
