#Django Imports
from django.urls import path

#Local Imprts
from account.views import (
  UserRegistrationView,
  UserLoginView,
  UserProfileView,
  UserChangePasswordView,
  UserSendPasswordResetView,
  UserPasswordResetView
)

urlpatterns = [
  path('register', UserRegistrationView.as_view()),
  path('login', UserLoginView.as_view()),
  path('profile', UserProfileView.as_view()),
  path('change-password', UserChangePasswordView.as_view()),
  path('send-reset-password', UserSendPasswordResetView.as_view()),
  path('reset-password/<uuid>/<token>', UserPasswordResetView.as_view()),
]
